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



 ![Front](/images/screen.jpg)
 ![Back view](/images/backview.jpg)

 Parts List
 ===========
 * Raspberry Pi4b - 2GB is fine
 * SD card
 * Official Raspberry pi 7 inch touchscreen
 * Neego Raspi 4 Screen case for Raspi Monitor Touchscren Display 7" - https://www.amazon.com/gp/product/B081VT2CPW/
 * Power supply - The official 3a power supply worked fine. I've also run it off battery pack just use a decent USB c cable with heavy gauge wire for power. 21awg worked for me

 To attach the dongles I created a custom back plate which I 3d printed. The STL files for that are included in the repo also.


Install Process
================
Install fresh install of 32bit Raspberry pi Desktop OS with Desktop (built using Buster on a Raspi4b) - I used the Raspberry Pi Imager software to do this  
https://www.raspberrypi.org/downloads/  
or for just the iso image  
https://www.raspberrypi.org/downloads/raspberry-pi-os/  

## Power up Device, setup wifi and update it
 Setup location/password/wifi through desktop UI wizard
 ```
 sudo raspi-config and enable SSH
 ```
 ### Alternative manual method
 ```
 sudo apt-get update
 sudo apt-get upgrade
 restart
 ```

## Install Speedify  
 ```
 wget -qO- https://get.speedify.com | sudo -E bash -
 sudo apt-get install speedifyui
 sudo nano /etc/speedify/speedify.conf
 ```
 Add/Enable the following
 ```
 ENABLE_SHARE=1  
 SHARE_INTERFACE="eth0"  
 SHARE_WITHOUT_SPEEDIFY=1
 ```
 Save and Exit 
 ```
 sudo service speedify-sharing restart
 ```

## Add iPhone support & Autostart
 ```
 sudo apt install usbmuxd
 /usr/share/speedify/speedify_cli startupconnect on
 ```

## Install USB Wifi driver - only for AC56 device  
 ```
 cd /home/pi
 sudo apt-get install bc raspberrypi-kernel-headers
 sudo apt-get install dkms
 git clone -b v5.7.0 https://github.com/aircrack-ng/rtl8812au.git
 cd rtl*
 sed -i 's/CONFIG_PLATFORM_I386_PC = y/CONFIG_PLATFORM_I386_PC = n/g' Makefile
 sed -i 's/CONFIG_PLATFORM_ARM64_RPI = n/CONFIG_PLATFORM_ARM64_RPI = y/g' Makefile
 sed -i 's/^dkms build/ARCH=arm dkms build/' dkms-install.sh
 sed -i 's/^MAKE="/MAKE="ARCH=arm\ /' dkms.conf
 sudo ./dkms-install.sh
 ```

## Clone streaming repo and do the install  
 ``` 
 git clone https://github.com/ShimmerNZ/DisneyStreaming
 cd DisneyStreaming
 chmod +x update.sh
 cp /home/pi/DisneyStreaming/update.sh /home/pi/update.sh
 run update .sh
 mkdir /home/pi/logs
 mkdir /home/pi/.config/autostart
 pcmanfm --set-wallpaper /home/pi/DisneyStreaming/images/desktop.png

 sudo cp /home/pi/DisneyStreaming/images/splash.png /usr/share/plymouth/themes/pix/splash.png  
 ```
 
 
## Install software keyboard  
 ```
 sudo apt-get install matchbox-keyboard
 ``` 
## Install some Python library dependancies  
 ``` 
 sudo apt-get install python3-pil python3-pil.imagetk
 ```

## Install official raspberry pi 7"inch touchscreen"  
 ```
 sudo nano /boot/config.txt
 ```
 add the following at the bottom  
 ```
 disable_splash=1
 lcd_rotate=2
 max_usb_current=1
 ```

## modify boot process to remove the raspbery pi stuff                                                                                
 ```
 sudo nano /boot/cmdline.txt
 ```
 append the following to the end  
 ```
 quiet splash loglevel=0 logo.nologo
 ```

## AC56 Wifi fix  
 ```
 sudo systemctl edit --force --full wificheck.service 
 ```
 copy contents from wificheck.service to this file save and exit
 ``` 
 systemctl enable wificheck.service
 sudo systemctl start wificheck.service
 ```
 fix power saving
 ```
 sudo nano /etc/rc.local
 ```
 add the following before exit 0
 ```
 /sbin/iw dev wlan1 set power_save off
 ```

## File Manager changes 
 * Open File Manager --> Edit --> Preferences --> General  --> tick "Open files with single click"  
 * Open File Manager --> Edit --> Preferences --> General  --> tick "Don't ask options on launch executeabe file"  
 * Open File Manager --> Edit --> Preferences --> Volume Management  --> untick "Show availabkle options for removeable media when they are inserted"  

## Speedify UI changes
 * Set bonding mode to streaming  
 * Set Disconnect on Exit to Off  
 * Transport mode UDP  
 * Fastest Server  
