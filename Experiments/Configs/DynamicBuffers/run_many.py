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
            - SubTrial
                - tbf.sh: generated for each trial
"""
import os
import argparse
import csv
import matplotlib.pyplot as plt

min_bytes = 150000
max_bytes = 500000
steps = 10
trial_time = 60

executable = "/home/saahil/raspberry/rpi/Experiments/run.py "

tbf_string = """\
sudo tc qdisc del dev enp3s0 root

sudo tc qdisc add dev enp3s0 root handle 1:0 netem delay 10ms limit 1000
sudo tc qdisc add dev enp3s0 parent 1:1 handle 10: tbf rate 80mbit buffer 1mbit limit 1000mbit 
sudo tc qdisc add dev enp3s0 parent 10:1 handle 100: tbf rate 80mbit burst .05mbit limit {}b
"""

sub_folders = ["BBR_vs_Cubic"]


def get_bytes(min_bytes=min_bytes, max_bytes=max_bytes, steps=steps):
    for bytes in [min_bytes + i * (max_bytes - min_bytes) / steps
                  for i in range(steps + 1)]:
        yield int(bytes)


def generate_sub_experiments(folders=sub_folders):
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

        for byte in get_bytes():
            new_folder = "/".join([folder, f"Trial_{byte}"])
            if (not os.path.isdir(new_folder)):
                os.mkdir(new_folder)

            os.system(f"cp {config} {new_folder}")
            tbf = tbf_string.format(byte)
            tbf_file = "/".join([new_folder, "tbf.sh"])
            with open(tbf_file, 'w') as f:
                print(tbf, file=f)
            experiment_folders.append(new_folder)
        all_folders.append((folder, experiment_folders))
    return all_folders



def run_sub_experiments(experiment_folders):
    global executable, trial_time
    for experiment_folder in experiment_folders:
        run_cmd = f"{executable} result --directory {experiment_folder} --time {trial_time} --rerun"
        os.system(run_cmd)

def plot_exiperments(folder, experiment_folders):
    """
    For each folder,
    get the drop rate (dropped / sent) at 90\% - 10\% to cut off 
    the startup

    """
    queue_size = []
    drop_rates = []
    for byte, experiment_folder in zip(get_bytes(), experiment_folders):
        queue_file = "/".join([experiment_folder, "Results/queue_length.csv"])
        with open(queue_file) as csvfile:
            reader = csv.DictReader(csvfile, skipinitialspace=True)
            rows = [row for row in reader]
            startup_cutoff = int(0.1 * len(rows))
            end_cutoff = int(0.9 * len(rows))
            sent = int(rows[end_cutoff]['sent']) - int(rows[startup_cutoff]['sent'])
            drops = int(rows[end_cutoff]['drops']) - int(rows[startup_cutoff]['drops'])
            drop_rate = drops / sent
            queue_size.append(byte)
            drop_rates.append(drop_rate * 100)

    plt.plot(queue_size, drop_rates)
    plt.xlabel("queue size (bytes)")
    plt.ylabel("drop_rate (percent)")
    plt.savefig(f"{folder}/drop_rate.svg")
    print(queue_size, drop_rates)




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Orchestrate a set of experiments")
    parser.add_argument("--rerun", "-r", action='store_true', default=False)
    args = parser.parse_args()
    print(args)

    experiments = generate_sub_experiments()

    if (args.rerun):
        for _folder, experiment_folders in experiments:
            run_sub_experiments(experiment_folders)

    for folder, experiment_folders in experiments:
        plot_exiperments(folder, experiment_folders)
