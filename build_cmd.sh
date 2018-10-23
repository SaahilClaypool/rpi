cd /linux
echo $_UID
echo $_GID

KERNEL=kernel7
make mrproper
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- bcm2709_defconfig -j8
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- zImage modules dtbs -j8

mkdir /build
mkdir /build/fat32
mkdir /build/fat32/overlays/
mkdir /build/ext4

make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- INSTALL_MOD_PATH=/build/ext4 modules_install -j8

# cp /build/fat32/$KERNEL.img /build/fat32/$KERNEL-backup.img
cp arch/arm/boot/zImage /build/fat32/$KERNEL.img
cp arch/arm/boot/dts/*.dtb /build/fat32/
cp arch/arm/boot/dts/overlays/*.dtb* /build/fat32/overlays/
cp arch/arm/boot/dts/overlays/README /build/fat32/overlays/

rm -rf $OUT/build
mv /build $OUT

chown -R $_UID:$_GID $OUT 
