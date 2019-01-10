#!/usr/bin/python3
""" 
Run an trial with an increasing buffer size
Layout:
- Dynamic Buffers
    - python script
    - notes
    - Data
        - ExperimentConfigA
            - config.json
            - Trial_byte_number
                - tbf.sh: generated for each trial
"""
import os
import argparse
import csv
import matplotlib as mpl
should_show = False

min_bytes = 100000
max_bytes = 500000
steps = 40
trial_time = 300
trial_number = 1
throughput_mbit = 80
delay_ms = 10


executable = "/home/saahil/raspberry/rpi/Experiments/run.py "

tbf_string = """\
sudo tc qdisc del dev enp3s0 root
sleep 5
sudo tc qdisc add dev enp3s0 root handle 1:0 netem delay {delay}ms limit 5000
sudo tc qdisc add dev enp3s0 parent 1:1 handle 10: tbf rate {throughput}mbit buffer 1mbit limit 10000mbit
sudo tc qdisc add dev enp3s0 parent 10:1 handle 100: tbf rate {throughput}mbit burst .05mbit limit {buffer}b
sudo tc -s qdisc ls dev enp3s0
"""

# sub_folders = ["BBR", "Cubic", "BBR_vs_Cubic"]
sub_folders = ["BBR"]

def bytes_to_mbits(b):
    return b / 125000

def bytes_to_mbytes(b):
    return b / 1000000

def mbits_to_bytes(b):
    return b * 125000

def mbytes_to_bytes(b):
    return b * 1000000

def get_bytes(min_bytes=min_bytes, max_bytes=max_bytes, steps=steps):
    for bytes in [min_bytes + i * (max_bytes - min_bytes) / steps
                  for i in range(steps + 1)]:
        yield int(bytes)


def generate_sub_experiments(folders=sub_folders, remove=False):
    """
    for each given folder, make a new experiment by copying the config.json
    in that folder into a new sub_folder suffixed with the byte amount
    and a token bucket filter file with the given byte config

    yeild a bunch of experiment folders (full paths)
    """
    all_folders = []
    for folder in folders:
        experiment_folders = []
        folder = "/".join(["Data", folder])
        config = "/".join([folder, "config.json"])
        if (remove):
            remove_cmd = f"rm -rf {folder}/Trial*"
            print(remove_cmd)
            os.system(remove_cmd)

        for byte in get_bytes():
            for trial in range(trial_number):
                new_folder = "/".join([folder, f"Trial_{byte}_{trial}"])
                if (os.path.isdir(new_folder)):
                    if (remove):
                        os.system(f"rm -rf {new_folder}")
                        os.mkdir(new_folder)
                else:
                    os.mkdir(new_folder)

                os.system(f"cp {config} {new_folder}")
                tbf = tbf_string.format(buffer=byte, throughput=throughput_mbit, delay=delay_ms)
                tbf_file = "/".join([new_folder, "tbf.sh"])
                with open(tbf_file, 'w') as f:
                    print(tbf, file=f)
                experiment_folders.append(new_folder)
        all_folders.append((folder, experiment_folders))
    return all_folders



def run_sub_experiments(experiment_folders, parse=False, plot=False):
    global executable, trial_time
    for experiment_folder in experiment_folders:
        run_cmd = f"{executable} result --directory {experiment_folder} --time {trial_time} --rerun"
        if (parse):
            run_cmd = f"{executable} result --directory {experiment_folder} --time {trial_time} --parse"
        if (plot):
            run_cmd = f"{executable} result --directory {experiment_folder} --time {trial_time}"
        os.system(run_cmd)
def get_drop_rate(queue_file):
    """
    get the drop rate from the given queue file.
    """
    with open(queue_file) as csvfile:
        reader = csv.DictReader(csvfile, skipinitialspace=True)
        rows = [row for row in reader]
        startup_cutoff = int(0.50 * len(rows))
        end_cutoff = int(0.85 * len(rows))
        sent = float(rows[end_cutoff]['sent']) - float(rows[startup_cutoff]['sent'])
        drops = float(rows[end_cutoff]['drops']) - float(rows[startup_cutoff]['drops'])
        drop_rate = drops / sent
        return drop_rate * 100
def get_average_throughput(tp_file, start=.5, end=.8):
    """
    get the average throughput of the flow between start and end percent
    """
    with open (tp_file) as csvfile:
        reader = csv.DictReader(csvfile, skipinitialspace=True)
        rows = [row for row in reader]
        rows = rows[int(len(rows) * start): int(len(rows) * end)]
        total = sum(map(lambda el: int(el['throughput']), rows)) / len(rows)
    return total
def plot_experiments(folder, experiment_folders):
    """
    For each folder,
    get the drop rate (dropped / sent) at 99\% - 1\% to cut off
    the startup
    """
    queue_size  = []
    drop_rates  = []
    throughputs = {}
    rtts        = []

    for experiment_folder in experiment_folders:
        basename = os.path.basename(experiment_folder)
        _, byte, trial = basename.split("_")
        queue_file = "/".join([experiment_folder, "Results/queue_length.csv"])
        queue_size.append(int(byte))

        # Drop Rate
        drop_rate = get_drop_rate(queue_file)
        drop_rates.append(drop_rate)
        # Relative Throughput
        # Find all csv files ignoring queue length
        result_directory= "/".join([experiment_folder, "Results"])
        current_throughputs = {}
        for tp_file in os.listdir(result_directory):
            if tp_file.endswith(".csv") and tp_file != "queue_length.csv" and "tarta" in tp_file:
                protocol, machine, _ = tp_file.split("_")
                tp = (os.path.join(result_directory, tp_file))
                if not protocol in current_throughputs.keys():
                    current_throughputs[protocol] = []
                current_throughputs[protocol].append(get_average_throughput(tp))
        for protocol, tps in current_throughputs.items():
            avg = sum(tps) # / len(tps)
            if not protocol in throughputs.keys():
                throughputs[protocol] = []
            throughputs[protocol].append(avg)

    queue_size = list(map(bytes_to_mbytes, queue_size))
    plot_drop_rate(queue_size, drop_rates)
    plot_throughput(queue_size, throughputs)


def plot_drop_rate(queue_size, drop_rates):
    # plot drop rate
    plot_bdp()
    plt.plot(queue_size, drop_rates)
    plt.title(folder)
    plt.xlabel("queue size (mega bytes)")
    plt.ylabel("drop_rate (percent)")
    # plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    plt.ticklabel_format(style='sci', axis='x')
    plt.legend()
    plt.ylim(bottom=0)
    plt.xlim(left=bytes_to_mbytes(min_bytes), right=bytes_to_mbytes(max_bytes))
    plt.savefig(f"{folder}/drop_rate.svg")
    if (should_show):
        plt.show()
    print(queue_size, drop_rates)
    plt.close()

def plot_bdp():
    bdp = calc_bdp()
    bdp_1_5  = bdp * 1.5
    plt.axvline(x = bdp, label="BDP", color="orange", linestyle="--")
    plt.axvline(x = bdp_1_5, label="1.5 * BDP", color="green", linestyle="--")

def calc_bdp(min_rtt=15):
    throughput_mbyte = mbits_to_bytes(bytes_to_mbytes(throughput_mbit))
    return throughput_mbyte * min_rtt / 1000


def plot_throughput(queue_size, throughputs):
    for protocol, rates in throughputs.items():
        # rates = list(map(bytes_to_mbits, rates))
        plt.plot(queue_size, rates, label=protocol)
    # plot the total throughput
    x_data = list(map(bytes_to_mbytes, [min_bytes, max_bytes]))
    y_data = [throughput_mbit, throughput_mbit]
    plt.plot(x_data, y_data, label="Max Bandwidth")
    plot_bdp()
    plt.title(folder)
    plt.ylim(bottom=0, top=throughput_mbit + 10)
    plt.xlim(left=bytes_to_mbytes(min_bytes), right=bytes_to_mbytes(max_bytes))
    plt.legend()
    # plt.xlabel("queue size (mega bytes)")
    plt.ylabel("total throughput (mbits / second)")
    # plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    plt.ticklabel_format(style='sci', axis='x')
    plt.savefig(f"{folder}/throughput.svg")
    if (should_show):
        plt.show()
    plt.close()





if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Orchestrate a set of experiments")
    parser.add_argument("--rerun", "-r", action='store_true', default=False)
    parser.add_argument("--reparse", "-p", action='store_true', default=False)
    parser.add_argument("--replot", action='store_true', default=False)
    parser.add_argument("--show", "-s", action='store_true', default=False)
    args = parser.parse_args()
    print(args)

    if (args.show):
        should_show = True
        import matplotlib.pyplot as plt
    else:
        print("turning off interactive")
        mpl.use('Agg')
        import matplotlib.pyplot as plt
        plt.ioff()

    experiments = generate_sub_experiments(remove=args.rerun)

    if (args.rerun):
        for _folder, experiment_folders in experiments:
            run_sub_experiments(experiment_folders)
    if (args.reparse):
        for _folder, experiment_folders in experiments:
            run_sub_experiments(experiment_folders, parse=True)
    if (args.replot):
        for _folder, experiment_folders in experiments:
            run_sub_experiments(experiment_folders, plot=True)

    for folder, experiment_folders in experiments:
        print(f"\n\n{folder}")
        plot_experiments(folder, experiment_folders)
