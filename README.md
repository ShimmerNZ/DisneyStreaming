# DisneyStreaming
 Raspi Network Bonding UI with Speedify
 
 I found the Speedify app was resource intensive especially when interface disconnected where it would consume 200% resource causing the Pi to overheat.
 I decided to build a seperate UI to control it as well as show up signal strength. Everythign else leverages the speedify back end.

 Install fresh install of Rasbian Desktop (built using Buster on a Raspi4b)
 apt-get update
 apt-get upgrade
 sudo raspi-config and enable SSH

 wget -q0- https://get.speedify.com | sudo -E bash -
 sudo nano /etc/speedify/speedify.com
 
 #ADD/ENABLE THE FOLLOWING TEXT
 ENABLE_SHARE=1
 SHARE_INTERFACE="eth0"

 #SAVE AND EXIT
 sudo service speedify-sharing reestart

 # For me i used the asus ac56 usb wifi dongle
 git clone https://github.com/zorani/USB-AC56-raspi
 run unstall.sh
git clone https://github.com/ShimmerNZ/DisneyStreaming
chmod +x update.sh
run update .sh
 update.sh needs to be moved to your home directory
 .desktop files can be moved to the /home/pi/Desktop directory

 sudo apt-get intall python3-pil

 install official raspberry pi 7"inch touchscreen"

 sudo nano /boot/cmdline.txt
 console=tty1 root=PARTUUID=f19d29ed-02 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait quiet splash plymouth.ignore-serial-consoles logo.nologo vt.global_cursor_default=0

 sudo systemctl edit --force --full my_script.service
 copy contents from checkwifi.service to this file save and exit
 systemctl enable my_script.service
 sudo systemctl start my_script.service