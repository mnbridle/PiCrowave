#!/bin/bash
KERNEL=kernel8

echo "Mounting SD card..."
mkdir -p ~/mnt
mkdir -p ~/mnt/fat32
mkdir -p ~/mnt/ext4
sudo mount /dev/mmcblk0p1 ~/mnt/fat32
sudo mount /dev/mmcblk0p2 ~/mnt/ext4

echo "Backing up kernel"
sudo cp ~/mnt/fat32/$KERNEL.img ~/mnt/fat32/$KERNEL-$(date +%s).img

echo "Install kernel modules"
OLD_PWD=$(pwd)
cd ~/src/raspberry-pi/linux
sudo env PATH=$PATH make ARCH=arm64 INSTALL_MOD_PATH=~/mnt/ext4 modules_install
cd $OLD_PWD

echo "Copying over kernel"
sudo cp ~/src/raspberry-pi/linux/arch/arm64/boot/Image ~/mnt/fat32/$KERNEL.img
sudo cp ~/src/raspberry-pi/linux/arch/arm64/boot/dts/broadcom/*.dtb ~/mnt/fat32/
sudo cp ~/src/raspberry-pi/linux/arch/arm64/boot/dts/overlays/*.dtb* ~/mnt/fat32/overlays/
sudo cp ~/src/raspberry-pi/linux/arch/arm64/boot/dts/overlays/README ~/mnt/fat32/overlays/

echo "Unmount SD card"
sudo umount ~/mnt/fat32
sudo umount ~/mnt/ext4