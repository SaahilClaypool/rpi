# Raspberry Pi Setup

## Images

pi@rpi0 raspberry 0 

ssh: only works from windows (for local ssh. Should work fine once on network)

sharing internet: https://raspberrypi.stackexchange.com/questions/11684/how-can-i-connect-my-pi-directly-to-my-pc-and-share-the-internet-connection 

## Testing

### Wifi: 

client (rpi): iperf3 -s 
server (win): iperf3.exe -c rpi0.local

results: ~


### IO

## BBR

https://www.techrepublic.com/article/how-to-enable-tcp-bbr-to-improve-network-speed-on-linux/

- Add to `/etc/systctl.conf`

    ```
    net.core.default_qdisc=fq
    net.ipv4.tcp_congestion_control=bbr
    ```
- run `sudo sysctl -p` to reload

- run `sysctl net.ipv4.tcp_congestion_control` to check

    output should be: `net.ipv4.tcp_congestion_control = bbr`

### Updated bbr source: 

https://github.com/google/bbr/blob/master/README

plan: make a git commit adding updated bbr with bbr2.0 as the name? 

### Moving to kernel 4.19

./bbr_2.md

## Configuring the Kernel 

https://www.raspberrypi.org/documentation/linux/kernel/configuring.md

### Docker

Images setup: see docker file

build: `docker build . -t linux_build`

command: `docker run -v /c/Users/saahi/gitProjects/mqp/linux:/linux -v /c/Users/saahi/gitProjects/mqp/raspberry/dist:/dist -it linux_build`

#### On Glomma

Should be able to run from `~/raspberry`
```
docker run --rm \
    -v /home/saahil/raspberry/linux:/linux \
    -v /home/saahil/raspberry/out:/out \
    -e _UID=`id -u` \
    -e _GID=`id -g` \
    -it saahil/rpi_build sh /root/build_cmd.sh
```

### Clone linux source *from glomma*

git clone git+ssh://saahil@glomma.cs.wpi.edu/~/raspberry/linux

git clone git+ssh://saahil@glomma.cs.wpi.edu/~/raspberry/rpi-full-source-19


Note: cannot push to glomma while it has checked out the current branch. 
So, must check out different branch before pushing.



## Windows

### Case sensitive 

Note: issues on windows based on case sensitive files. 
See https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/fsutil-file 
https://blogs.msdn.microsoft.com/commandline/2018/06/14/improved-per-directory-case-sensitivity-support-in-wsl/ 

## Copying new image to ssd

1. sftp / rsync the output directory from glomma to local
2. start up vm (windows can't write to ext4 drive)
    - this is currently set up by sharing all usb drives to linux guest vagrant machine
    - log in with `vagrant up` and `vagrant sh`

    - the drive should should up under `/dev/sdc/`
    - mount the usb drive: 
        - can check for the usb device with lsusb or sudo fdisk -l

        Vagrant
        ```sh
        mkdir mnt/fat32
        mkdir mnt/ext4
        sudo mount /dev/sdc1 /mnt/fat32
        sudo mount /dev/sdc2 /mnt/ext4
        ```

    - copy the files over
        ```sh
        sudo cp -rf /vagrant/image/fat32/* /mnt/fat32/
        sudo cp -rf /vagrant/image/ext4/* /mnt/ext4
        ```
    - unmount the usb and unplug: 
        ```sh
        sudo umount /mnt/fat32
        sudo umount /mnt/ext4
        ```
### Git 

Because symlinks are enabled, need to use bash for git provider. See https://github.com/andy-5/wslgit

### Fix windows stupid folder delete

rd \\.\c:\Users\saahi\gitProjects\mqp\linux /S /Q 

