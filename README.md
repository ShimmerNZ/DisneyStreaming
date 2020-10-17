# DisneyStreaming
 Raspi Network Bonding UI with Speedify
 
 I found the Speedify app was resource intensive especially when interface disconnected where it would consume 200% resource causing the Pi to overheat.
 I decided to build a seperate UI to control it as well as show up signal strength. Everythign else leverages the speedify back end.

Install fresh install of 32bit Raspberry pi Desktop OS with Desktop (built using Buster on a Raspi4b) - I used the Raspberry Pi Imager software to do this
https://www.raspberrypi.org/downloads/
or for just the iso image
https://www.raspberrypi.org/downloads/raspberry-pi-os/

#Power up Device, setup wifi and update it
 Setup location/password/wifi through desktop UI wizard
 sudo raspi-config and enable SSH
 sudo apt-get update
 sudo apt-get upgrade


#install Speedify
 wget -q0- https://get.speedify.com | sudo -E bash -
 sudo nano /etc/speedify/speedify.com
 
 #ADD/ENABLE THE FOLLOWING TEXT
 ENABLE_SHARE=1
 SHARE_INTERFACE="eth0"

 #SAVE AND EXIT
 sudo service speedify-sharing restart

# Add iPhone tether support and enable auto start for speedify
 sudo apt install usbmuxd
 /usr/share/speedify/speedify_cli startupconnect on

#install USB Wifi dongle driver - in my case the ASUS AC56 device
 git clone https://github.com/zorani/USB-AC56-raspi
 cd to reepo
 run install.sh

#Clone streaming repo and do the install
 git clone https://github.com/ShimmerNZ/DisneyStreaming
 chmod +x update.sh
 run update .sh
 
 cp /home/pi/DisneyStreaming/update.sh /home/pi/update.sh
 
#Install some Python library dependancies
 sudo apt-get intall python3-pil
 
#install official raspberry pi 7"inch touchscreen"

# modify boot process to remove the raspbery pi stuff                                                                              
 sudo nano /boot/cmdline.txt
 console=tty1 root=PARTUUID=f19d29ed-02 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait quiet splash plymouth.ignore-serial-consoles logo.nologo vt.global_cursor_default=0

# I had problems with wlan1 intermittently returning a NO CARRIER error and it would not connect again until reboot, dhcpcd service restart or wlan1 link brought down and up again. I created a simple python script that runs as as service that checks and if wrong it fixes it
 sudo systemctl edit --force --full wificheck.service
 copy contents from wificheck.service to this file save and exit
 systemctl enable wificheck.service
 sudo systemctl stabrianandamandart wificheck.service