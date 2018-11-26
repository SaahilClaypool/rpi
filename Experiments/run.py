#!/usr/bin/python3
import os
import argparse

CUR_DIR = os.getcwd()
TOOLS_DIR = f"{CUR_DIR}/../NetworkTools"
PARSE_PCAP = f"{TOOLS_DIR}/Parse_pcap/target/release/parse_pcap"
PLOT_PCAP = f"{TOOLS_DIR}/Parse_pcap/plot.py"

START_TRIAL = f"{CUR_DIR}/start_trial.py"



def main():
    print("run_one")
    parser = argparse.ArgumentParser(description="Orchestrate a set of experiments")
    parser.add_argument("name", help="name of ouput")
    parser.add_argument("--directory", "-d", required=True)
    parser.add_argument("--build", "-b")
    parser.add_argument("--trial", "-t")
    parser.add_argument("--granularity", "-g", default="")
    parser.add_argument("--show", "-s", default="")
    
    args = parser.parse_args()
    print(args)

    if (args.build):
        os.system(f"cd {TOOLS_DIR}/Parse_pcap; cargo build --release; cd -;" )

    if (args.trial):
        trial_cmd = f"""\
        cd {args.directory};
        mkdir Results;
        {START_TRIAL} {args.trial};
        """
        os.system(trial_cmd)
        off_cmd = f"""\
        sudo tc qdisc del dev enp3s0 root
        tc -s qdisc ls dev enp3s0
        """
        os.system(off_cmd)

    parse_cmd = f"""\
    cd {args.directory}/Results;
    rm *.csv; {PARSE_PCAP} '.*' '.' {args.granularity};
    cd -;
    """
    os.system(parse_cmd)

    plot_cmd = f"""\
    cd {args.directory}/Results;
    {PLOT_PCAP} . . {args.name}.png {args.show}
    mv {args.name}.png ..;
    cd -;
    """
    os.system(plot_cmd)



    

if __name__ == "__main__":
    main()