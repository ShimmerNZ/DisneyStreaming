# DisneyStreaming
 Raspi Network Bonding UI with Speedify
 
 The purpose of this project was to look at a way of building a device that could leverage multiple network interfaces (specifically mobile and wifi) to create a more stable network
 for IRL streaming. The commercially available products were very expensive starting at $1k US and going up from there. The concept does require a server end component to aggregate the
 traffic and forward on. I initially looked at some options to host and do this myself but came across the speedify product which was a subscription service and all done for me. 
 For clarity I am not affiliated with Speedify in any way shape or form. After some initial testing to verifify throughput which was one of my concerns... like is this service going
 to be throttled to heck? The results were pleasing and was getting upwards of 300mbps up/down over a wifi connected device to a non dedicated speedify server. 
 This was way more than enough for IRL streaming so continued to progress. This project was purpose built for a Disney streamer but could be easily customisable for any other purpose
 UI is built in Python3 using Tkinter. I originally started with a pihat touch screen but dropped it for 2 reasons:
 * UI/Resolution was too small, and limited room to display much, this was also going to be a problem with initial setup to display wifi captive portal screens
 * Capacitive touch screen sucked
 I found the Speedify app was resource intensive especially when interface disconnected where it would consume 200% resource causing the Pi to overheat.
 I decided to build a seperate UI to control it as well as show up signal strength. Everythign else leverages the speedify back end.

 Note: As of 18th Oct 2020 this has not yet been tested in the wild to determine if this is going to work as expected.

 Parts List
 ===========
 * Raspberry Pi4b - 2GB is fine
 * SD card
 * Official Raspberry pi 7 inch touchscreen
 * Neego Raspi 4 Screen case for Raspi Monitor Touchscren Display 7" - https://www.amazon.com/gp/product/B081VT2CPW/
 * Power supply - The official 3a power supply worked fine. I've also run it off battery pack just use a decent USB c cable with heavy gauge wire for power. 21awg worked for me

 To attach the dongles I created a custom back plate which I 3d printed. The STL files for that are included in the repo also.


Install fresh install of 32bit Raspberry pi Desktop OS with Desktop (built using Buster on a Raspi4b) - I used the Raspberry Pi Imager software to do this
https://www.raspberrypi.org/downloads/
or for just the iso image
https://www.raspberrypi.org/downloads/raspberry-pi-os/

#Power up Device, setup wifi and update it
 Setup location/password/wifi through desktop UI wizard
 sudo raspi-config and enable SSH
 #if manually updating then
 sudo apt-get update
 sudo apt-get upgrade
 restart


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

# Install software keyboard

# Change launch to single click

# Change file manager to not prompt when USB device is connected.