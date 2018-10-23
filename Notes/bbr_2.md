# BBR 2 dev plan

Goal: put a second version of bbr in the same kernel

Process:
1. Look at original patch for bbr

    This should indicate all the files that need to be changed



2. Copy bbr code in

3. Change all bbr references to bbr 2

4. compile kernel with both instances


## Files changed for bbr 1.0

> Main commit: https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=0f8782ea14974ce992618b55f0c041ef43ed0b78

1. /include/uapi/linux/inet_diag.h

    make a struct for bbr info (note: probably can share with bbr 2.0)

2. /net/ipv4/Kconfig

    Add a config for TCP_CONG_BBR

    (Note: the DEFAULT_TCP_CONG seems changed as well)

3. /net/ipv4/Makefile b/net/ipv4/Makefile

    Add .o file

4. /net/ipv4/tcp_bbr.c 

    main code

    Seems the ".name" option is important for registering a new tcp type


## files changed for bbr 2.0

1. inet: not changed
2. Kconfig (checking in progress. net-next is stored on glomma)
3. Makefile: just add the new file
4. tcp_bbr: need to rename instances to 2.0 as needed

# Moving to new kernel

git clone https://github.com/raspberrypi/linux rpi-full-source-19
git checkout rpi-4.19.y

- Missing: 
    - sk_pacing_rate
        - net/ipv4/tcp_output.c X
        - net/ipv4/tcp_input.c X
        - net/sched/sch_fq.c X
        - net/core/filter.c X
        - net/core/sock.c X
        - include/net/sock.h X
    - tcp_clock_cache / tcp_wstamp_ns
        - net/ipv4/tcp_timer.c X 
        - net/ipv4/tcp_output.c X
        - include/linux/tcp.h X
        - net/ipv4/tcp_bbr.c X
    - is_ack_delayed
        - net/ipv4/tcp_input.c X 
        - net/ipv4/tcp_bbr.c
        - include/net/tcp.h X
    - .min_tso_segs vs .tso_segs_goal (UNUSED)

- NOTE: we are just going to want to add these individual features. Doing all the changes in next/net is too hard

Idea: Copy the net-next files over to the 4.19 branch. Do the same bbr 2.0 stuff in there as well

Commit 1: copy over the required files. See if it builds

## Docker image updates
- apt install flex bison libssl-dev
