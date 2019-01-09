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

BDP =       300000
min_bytes = 100000
max_bytes = 500000
steps = 40
trial_time = 300
trial_number = 1

executable = "/home/saahil/raspberry/rpi/Experiments/run.py "

tbf_string = """\
sudo tc qdisc del dev enp3s0 root
sleep 5
sudo tc qdisc add dev enp3s0 root handle 1:0 netem delay 10ms limit 5000
sudo tc qdisc add dev enp3s0 parent 1:1 handle 10: tbf rate 80mbit buffer 1mbit limit 10000mbit
sudo tc qdisc add dev enp3s0 parent 10:1 handle 100: tbf rate 80mbit burst .05mbit limit {}b
sudo tc -s qdisc ls dev enp3s0
"""

# sub_folders = ["BBR", "Cubic", "BBR_vs_Cubic"]
sub_folders = ["BBR"]


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
                tbf = tbf_string.format(byte)
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

def plot_exiperments(folder, experiment_folders):
    """
    For each folder,
    get the drop rate (dropped / sent) at 99\% - 1\% to cut off 
    the startup

    """
    queue_size = []
    drop_rates = []
    for experiment_folder in experiment_folders:
        basename = os.path.basename(experiment_folder)
        _, byte, trial = basename.split("_")
        queue_file = "/".join([experiment_folder, "Results/queue_length.csv"])
        with open(queue_file) as csvfile:
            reader = csv.DictReader(csvfile, skipinitialspace=True)
            rows = [row for row in reader]
            startup_cutoff = int(0.50 * len(rows))
            end_cutoff = int(0.85 * len(rows))
            sent = float(rows[end_cutoff]['sent']) - float(rows[startup_cutoff]['sent'])
            drops = float(rows[end_cutoff]['drops']) - float(rows[startup_cutoff]['drops'])
            drop_rate = drops / sent
            print(f"sent: {sent}, drops: {drops}, drop_rate: {drop_rate}")
            queue_size.append(int(byte))
            drop_rates.append(drop_rate * 100)

    for rate in zip(queue_size, drop_rates):
        print("rate is: ", rate)
    plt.scatter(queue_size, drop_rates)
    plt.title(folder)
    plt.xlabel("queue size (bytes)")
    plt.ylabel("drop_rate (percent)")
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    plt.savefig(f"{folder}/drop_rate.svg")
    if (should_show):
        plt.show()
    print(queue_size, drop_rates)
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
        plot_exiperments(folder, experiment_folders)
