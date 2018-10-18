cd /linux
KERNEL=kernel7
make O=/out ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- bcm2709_defconfig
make O=/out ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- zImage modules dtbs
mkdir /mnt
mkdir /mnt/fat32
mkdir /mnt/ext4

sudo make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- INSTALL_MOD_PATH=/mnt/ext4 modules_install

# sudo cp /mnt/fat32/$KERNEL.img /mnt/fat32/$KERNEL-backup.img
cp arch/arm/boot/zImage /mnt/fat32/$KERNEL.img
cp arch/arm/boot/dts/*.dtb /mnt/fat32/
cp arch/arm/boot/dts/overlays/*.dtb* /mnt/fat32/overlays/
cp arch/arm/boot/dts/overlays/README /mnt/fat32/overlays/

mv /mnt $OUT
