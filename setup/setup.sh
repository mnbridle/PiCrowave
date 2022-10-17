#!/bin/bash

# Install font dependencies
sudo apt install fonts-freefont-ttf

# Install distutils
sudo apt install python3-distutils

# Get pip
wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py
source ~/.profile

# Install 2.8 inch TFT LCD screen
sudo ./system_backup.sh

if [ -f /etc/X11/xorg.conf.d/40-libinput.conf ]; then
sudo rm -rf /etc/X11/xorg.conf.d/40-libinput.conf
fi
if [ ! -d /etc/X11/xorg.conf.d ]; then
sudo mkdir -p /etc/X11/xorg.conf.d
fi
sudo cp ./usr/tft9341-overlay.dtb /boot/overlays/
sudo cp ./usr/tft9341-overlay.dtb /boot/overlays/tft9341.dtbo

source ./system_config.sh
sudo echo "hdmi_force_hotplug=1" >> ./boot/config.txt.bak
sudo echo "dtparam=i2c_arm=on" >> ./boot/config.txt.bak
sudo echo "dtparam=spi=on" >> ./boot/config.txt.bak
sudo echo "enable_uart=1" >> ./boot/config.txt.bak
sudo echo "dtoverlay=tft9341:rotate=270" >> ./boot/config.txt.bak
sudo echo "hdmi_group=2" >> ./boot/config.txt.bak
sudo echo "hdmi_mode=1" >> ./boot/config.txt.bak
sudo echo "hdmi_mode=87" >> ./boot/config.txt.bak
sudo echo "hdmi_cvt 480 360 60 6 0 0 0" >> ./boot/config.txt.bak
sudo echo "hdmi_drive=2" >> ./boot/config.txt.bak
sudo cp -rf ./boot/config.txt.bak /boot/config.txt
sudo cp -rf ./usr/99-calibration.conf-32-270  /etc/X11/xorg.conf.d/99-calibration.conf
sudo cp -rf ./usr/99-fbturbo.conf  /usr/share/X11/xorg.conf.d/99-fbturbo.conf
#if test "$root_dev" = "/dev/mmcblk0p7";then
#sudo cp ./usr/cmdline.txt-noobs /boot/cmdline.txt
#else
#sudo cp ./usr/cmdline.txt /boot/
#fi
sudo cp ./usr/inittab /etc/
#sudo cp ./boot/config-32.txt /boot/config.txt
sudo touch ./.have_installed
echo "gpio:resistance:32:270:480:360" > ./.have_installed