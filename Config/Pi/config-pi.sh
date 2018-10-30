# sudo fdisk -l;
SD1=/dev/sdf1;
SD2=/dev/sdf2;

sudo mount $SD1 /mnt/fat32;
sudo mount $SD2 /mnt/ext4;

sudo nvim /mnt/ext4/etc/hostname;
sudo nvim /mnt/ext4/etc/hosts;

sudo touch /mnt/fat32/ssh

sudo cp -rf ~/raspberry/img/build/* /mnt;

sudo umount /mnt/fat32;
sudo umount /mnt/ext4;
