#!/usr/bin/python3
# Monitoring App so that you can see the status of the various interfaces, connectivity status, throughput, CPU utilisation and temp
# of the Raspberry Pi
# include speed test function - speedtest-cli
# show IP address
# captive portal launch?
# enable/disable speedify


from gpiozero import CPUTemperature
from tkinter import ttk
from PIL import Image, ImageTk
import time
import tkinter as tk
import speedify
import urllib.request
import json
import re
import requests
import os
import subprocess
import argparse
import psutil
import urllib.request

interface ="wlan0" # this is just a sample value


#import stuff I don't want to load into github
try:
    from secrets import secrets
    print(secrets)
except ImportError:
    print('failed to read secrets file containing Youtube API key')
    raise

#CPU Temp Section
cpu=CPUTemperature()
global tx_prev
global rx_prev
(tx_prev,rx_prev)=(0,0)
#Speedify settingssudo apt-get install python3-pil python3-pil.imagetk

class PopUpConfirmQuit(tk.Toplevel):
    """A TopLevel popup that asks for confirmation that the user wants to quit.
    Upon confirmation, the App is destroyed.
    If not, the popup closes and no further action is taken
    """
    def __init__(self, master=None):
        super().__init__(master)
        tk.Label(self, text="What would you like to do?").pack()
        tk.Button(self, text='Exit App', command=self.Exit, fg='green').pack(side=tk.RIGHT, fill=tk.BOTH, padx=5, pady=5)
        tk.Button(self, text='Cancel', command=self.destroy).pack(side=tk.RIGHT, fill=tk.BOTH, padx=5, pady=5)
        tk.Button(self, text='Restart', command=self.Reboot, fg='red').pack(side=tk.RIGHT, fill=tk.BOTH, padx=5, pady=5)
        tk.Button(self, text='Shutdown', command=self.Shutdown, fg='red').pack(side=tk.RIGHT, fill=tk.BOTH, padx=5, pady=5)
    
    def Shutdown(self):
        os.system('shutdown -h now')

    def Reboot(self):
        os.system('reboot')

    def Exit(self):
        exit()
 
class Mainframe(tk.Frame):
    def __init__(self,master,*args,**kwargs):
        tk.Frame.__init__(self,master,*args,**kwargs)

        self.configure(bg='#0b0c1b')

        #CPU headins
        self.TemperatureC = tk.IntVar()
        tk.Label(self,textvariable = self.TemperatureC,bg='#0b0c1b',fg='#fff', font=("HCo Gotham SSm",10)).grid(row=18, column=1)
        TempHeading='CPU'+'\n'+'Temp'
        tk.Label(self,text=TempHeading,bg='#0b0c1b',fg='#fff', font=("HCo Gotham SSm",10) ).grid(row=2, column=1)
        tk.Label(self,text='°C',bg='#0b0c1b',fg='#fff', font=("HCo Gotham SSm",10) ).grid(row=21, column=1)

        self.CPUutil=tk.IntVar()
        tk.Label(self,textvariable = self.CPUutil,bg='#0b0c1b',fg='#fff', font=("HCo Gotham SSm",10)).grid(row=18, column=2)
        CPUHeading='CPU'+'\n'+'Util'
        tk.Label(self,text=CPUHeading,bg='#0b0c1b',fg='#fff', font=("HCo Gotham SSm",10) ).grid(row=2, column=2)
        tk.Label(self,text='%',bg='#0b0c1b',fg='#fff', font=("HCo Gotham SSm",10)).grid(row=21, column=2)


        #Server Details
        self.Currentserver = tk.StringVar()
        tk.Label(self,textvariable=self.Currentserver,bg='#0b0c1b',fg='#fff',font=("HCo Gotham SSm",14,"italic")).grid(row=4, column=3, columnspan=6)

        self.Connectionstate = tk.StringVar()

        tk.Label(self,textvariable=self.Connectionstate,bg='#0b0c1b',fg='#fff',font=("HCo Gotham SSm",14)).grid(row=5, column=3, columnspan=6)

        #download stats
        img=tk.PhotoImage(file='/home/pi/DisneyStreaming/down.gif')
        img2=tk.PhotoImage(file='/home/pi/DisneyStreaming/up.gif')
        lbl=tk.Label(self, image=img, bg='#0b0c1b')
        lbl.image = img
        lbl.grid(row=1, column=3)
        lbl=tk.Label(self, image=img2, bg='#0b0c1b')
        lbl.image = img2
        lbl.grid(row=1, column=6, sticky='E')

        tk.Label(self,text='DOWNLOAD ',bg='#0b0c1b',fg='#fff', font=("HCo Gotham SSm",16)).grid(row=1, column=4)
        tk.Label(self,text='Mbps', bg='#0b0c1b',fg='#9193a8', font=("HCo Gotham SSm",16)).grid(row=1, column=5, sticky='W')
        tk.Label(self,text='UPLOAD ', bg='#0b0c1b',fg='#fff', font=("HCo Gotham SSm",16)).grid(row=1, column=7, sticky='W')
        tk.Label(self,text='Mbps', bg='#0b0c1b',fg='#9193a8', font=("HCo Gotham SSm",16)).grid(row=1, column=7, columnspan=2)

        self.TXspeed = tk.StringVar()

        tk.Label(self,textvariable=self.TXspeed , bg='#0b0c1b',fg='#fff', font=("HCo Gotham SSm",40)).grid(row=2, column=6, rowspan=2, columnspan=3)
        self.RXspeed = tk.StringVar()
        tk.Label(self,textvariable=self.RXspeed , bg='#0b0c1b',fg='#fff', font=("HCo Gotham SSm",40)).grid(row=2, column=3, rowspan=2, columnspan=3)

        #Adapter Stats
        tk.Label(self,text='CONNECTION TYPE  ', bg='#0b0c1b',fg='#fff', font=("HCo Gotham SSm",10)).grid(row=7, column=4)
        tk.Label(self,text='INTERFACE NAME  ', bg='#0b0c1b',fg='#fff', font=("HCo Gotham SSm",10)).grid(row=7, column=5, columnspan=2, padx=50 )
        tk.Label(self,text='SIGNAL QUALITY  ', bg='#0b0c1b',fg='#fff', font=("HCo Gotham SSm",10)).grid(row=7, column=7)
        tk.Label(self,text='CONNECTION STATE  ', bg='#0b0c1b',fg='#fff', font=("HCo Gotham SSm",10)).grid(row=7, column=8)


        self.Adapterstate1 = tk.StringVar()
        tk.Label(self,textvariable=self.Adapterstate1, bg='#0b0c1b',fg='#fff', font=("HCo Gotham SSm",14)).grid(row=8, column=4, rowspan=10)
        self.Adapterstate2 = tk.StringVar()
        tk.Label(self,textvariable=self.Adapterstate2, bg='#0b0c1b',fg='#fff', font=("HCo Gotham SSm",14)).grid(row=8, column=5, rowspan=10, columnspan=2)
        self.Adapterstate3 = tk.StringVar()
        tk.Label(self,textvariable=self.Adapterstate3, bg='#0b0c1b',fg='#fff', font=("HCo Gotham SSm",14)).grid(row=8, column=8, rowspan=10)
        self.Adapterstate4= tk.StringVar()
        tk.Label(self,textvariable=self.Adapterstate4, bg='#0b0c1b',fg='#fff', font=("HCo Gotham SSm",14)).grid(row=8, column=7, rowspan=10)
     
        #Exit and Connect Buttons
        img4=Image.open('/home/pi/DisneyStreaming/exit.png').resize((40,40))
        img4=ImageTk.PhotoImage(img4)
        lbl1=tk.Button(self, image=img4, command=lambda: PopUpConfirmQuit(self), borderwidth=0, highlightthickness=0, bg='#0b0c1b')
        lbl1.image=img4
        lbl1.grid(row=0, column=0, columnspan=3, rowspan=2)

        global imgon
        global imgoff
        img5=Image.open('/home/pi/DisneyStreaming/on.png')
        imgon=ImageTk.PhotoImage(img5)
        img6=Image.open('/home/pi/DisneyStreaming/off.png')
        imgoff=ImageTk.PhotoImage(img6)
        lbl2=tk.Button(self, image=imgon, borderwidth=0, highlightthickness=0, bg='#0b0c1b')
        lbl2['command']= lambda arg=lbl2:self.connect(arg)
        lbl2.grid(row=0, column=8, columnspan=2, rowspan=2, sticky='E')

        #Progress bar code 
        s=ttk.Style()
        s.configure("green.Vertical.TProgressbar", troughcolor="gray", background="green")
        s.configure("yellow.Vertical.TProgressbar", troughcolor="gray", background="yellow")
        s.configure("red.Vertical.TProgressbar", troughcolor="gray", background="red")
        # use the above to set colour below
        progress=ttk.Progressbar(self, maximum=90, orient="vertical",length=250,style="green.Vertical.TProgressbar",variable=self.TemperatureC)
        progress.grid(row=3,column=1, rowspan=13)
        progress.config(mode='determinate')

        progress2=ttk.Progressbar(self,orient='vertical',length=250, variable=self.CPUutil)
        progress2.grid(row=3,column=2, rowspan=13)
        progress2.config(mode='determinate')

        #slap in a logo here
        img3=Image.open('/home/pi/DisneyStreaming/Brianlogo.png').resize((80,80))
        img3=ImageTk.PhotoImage(img3)
        lbl=tk.Button(self, image=img3, command=self.Special, borderwidth=0, highlightthickness=0, bg='#0b0c1b')
        lbl.image = img3
        lbl.grid(row=22, column=1, columnspan=2, rowspan=2)

        #sub count goes here
        self.Currentsubs = tk.StringVar()
        tk.Label(self,textvariable=self.Currentsubs, bg='#0b0c1b',fg='#fff', font=("HCo Gotham SSm",14)).grid(row=22, column=3, rowspan=3)
        

        #variable time
        self.TimerInterval = 700
        self.TimerInterval2 = 2000
        self.TimerInterval3 = 5000
        self.TimerInterval4 = 300000 # 5min poll for Sub count
        self.TempC = 0
        self.TempF = 0
        self.ProgressStyle = 'green.Vertical.TProgressbar'
        self.State = 'checking'
        self.Adapter1 = 'checking'
        self.Adapter2 = ''
        self.Adapter3 = ''
        self.Adapter4 = ''
        self.rxspeed = ''
        self.txspeed = ''
        self.Server = 'checking Server'
        self.CPUUtil = ''
        self.Subs='0'

        #call functions here
        self.GetTemp()
        self.GetCPU()
        self.GetState()
        self.GetAdapter()
        self.GetSpeed()
        self.GetCurrentServer()
        self.GetSubs()
        
    def GetTemp(self):
        ## replace this with code to read sensor
        self.TemperatureC.set(self.TempC)
        #self.TemperatureF.set(self.TempF)
        tempFile =open("/sys/class/thermal/thermal_zone0/temp")
        cpu_temp = tempFile.read()
        self.TempC = int(float(cpu_temp)/1000) 
        self.TempF = round(float(1.8*float(cpu_temp))/1000+32,1)
        TempCheck=int(self.TempC)
        # Now repeat call
        self.after(self.TimerInterval3,self.GetTemp)

    def GetCPU(self):
        self.CPUutil.set(self.CPUUtil)
        self.CPUUtil=psutil.cpu_percent(interval=None, percpu=False)
        self.CPUUtil=int(self.CPUUtil)

        self.after(self.TimerInterval2,self.GetCPU)

    def GetState(self):
        self.Connectionstate.set(self.State)
        stateraw=speedify.show_state()
        #self.State=(str(stateraw).replace('State.', ''))
        StateStr=str(stateraw).replace('State.', '')
        if StateStr == "LOGGED_IN":
            self.State="DISCONNECTED"
        else:
            self.State=(str(stateraw).replace('State.', '')) 
        # Logic to update the button at the top

        self.after(self.TimerInterval2,self.GetState)

    def GetAdapter(self):
        self.Adapterstate1.set(self.Adapter1)
        self.Adapterstate2.set(self.Adapter2)
        self.Adapterstate3.set(self.Adapter3)
        self.Adapterstate4.set(self.Adapter4)
        self.Adapter1=''
        self.Adapter2=''
        self.Adapter3=''
        self.Adapter4=''
        adapters=speedify.show_adapters() 

        for entry in adapters:
            if entry['state']=='connected':
                if entry['type']=='Ethernet':
                    self.Adapter1 = self.Adapter1 + 'Mobile' + '\n'
                    self.Adapter2 = self.Adapter2 + entry['adapterID'] +'\n'
                    self.Adapter3 = self.Adapter3 + entry['state']+ '\n'
                    self.Adapter4 = self.Adapter4 + 'N/A' + '\n'
                else:
                    self.Adapter1 = self.Adapter1 + entry['type'] + '\n'
                    self.Adapter2 = self.Adapter2 + entry['adapterID'] +'\n'
                    self.Adapter3 = self.Adapter3 + entry['state']+ '\n'
                    if entry['type'] =='Wi-Fi':
                        cmd = subprocess.Popen('iwconfig %s' % entry['adapterID'], shell=True, stdout=subprocess.PIPE, universal_newlines = True, bufsize=1)
                        #str=stdout.decode(encoding='UTF-8')
                        for line in cmd.stdout:
                            if 'Link Quality' in line:
                                #self.Adapter4 = self.Adapter4 + line.lstrip(' ')
                                pattern = '\d+'
                                result = re.findall(pattern, line.lstrip(' '))
                                linkpercent=(int(int(result[0])/int(result[1])*100))
                                self.Adapter4 = self.Adapter4 + (str(linkpercent) + '%\n')
                            elif 'Not-Associated' in line:
                                self.Adapter4 = self.Adapter4 + 'No signal'
                    else:
                        self.Adapter4 = self.Adapter4 + '\n'
        self.after(self.TimerInterval3,self.GetAdapter)

    def GetCurrentServer(self):
        self.Currentserver.set(self.Server)
        servers=speedify.show_currentserver()
        self.Server=servers['friendlyName']
        self.after(self.TimerInterval3,self.GetCurrentServer)

    def connect(self, arg):
        checkState = self.State
        checkState = str(checkState)
        if checkState!="CONNECTED":

            speedify.connect_closest()
            arg['image']= imgon
        else:
            speedify.disconnect()
            arg['image']= imgoff

    def Special(self):
        print('reserved for later use')

    def GetSubs(self):
        self.Currentsubs.set(self.Subs)
        CHANNEL_ID = "UCtjJTv95d8aUbRfjejXKOZA"
        DATA_SOURCE = "https://www.googleapis.com/youtube/v3/channels/?part=statistics&id="+CHANNEL_ID+"&key="+secrets['youtube_token']
        DATA_LOCATION1 = ["items", 0, "statistics", "viewCount"]
        DATA_LOCATION2 = ["items", 0, "statistics", "subscriberCount"]
        DATA_LOCATION3 = ["items", 0, "statistics", "videoCount"]
        try:
            data=urllib.request.urlopen(DATA_SOURCE).read()
            print(data)
            subs=json.loads(data)["items"][0]["statistics"]["subscriberCount"]
            views=json.loads(data)["items"][0]["statistics"]["viewCount"]
            videos=json.loads(data)["items"][0]["statistics"]["videoCount"]
            self.Subs="Subscriber Count: "+subs+ " View Count: "+views+" Video Count: "
            #self.Subs=subs
        except RuntimeError as e:
            print("Some error occured, retrying! -", e)
        self.after(self.TimerInterval4,self.GetCurrentServer)
              
  
    def GetSpeed(self):
        # throw in the connectify interface throughput stats
        #(tx_prev, rx_prev) = (0,0)
        global tx
        global rx
        if os.path.exists('/sys/class/net/connectify0/statistics/tx_bytes'):
            with open('/sys/class/net/' + 'connectify0' + '/statistics/' + 'tx' + '_bytes', 'r') as f:
                 try:
                     data = f.read();
                     tx= int(data)
                 except:
                     tx=0
                     print('exception handled gracefully')
        else:
            tx=0
        if os.path.exists('/sys/class/net/connectify0/statistics/rx_bytes'):
            with open('/sys/class/net/' + 'connectify0' + '/statistics/' + 'rx' + '_bytes', 'r') as f:
                 try:
                     data = f.read();
                     rx=int(data)
                 except:
                     rx=0
        else:
            rx=0
       # tx=self.get_bytes('tx')
       # rx=self.get_bytes('rx')
        global tx_prev
        global rx_prev
        self.TXspeed.set(self.txspeed)
        self.RXspeed.set(self.rxspeed)
        self.rxspeed=''
        self.txspeed=''
        if tx_prev > 0:
            tx_speed = ((tx - tx_prev)/100000)*0.75
            #print('TX: ',round(tx_speed,1), 'Mbps')
            self.txspeed=str(round(tx_speed,1))
        if rx_prev > 0:
            rx_speed = ((rx - rx_prev)/100000)*.75
            #print('RX: ', round(rx_speed,1), 'Mbps')
            self.rxspeed=str(round(rx_speed,1))
        tx_prev = tx
        rx_prev = rx
        self.after(self.TimerInterval,self.GetSpeed)



class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
               
        # set the title bar text
        self.title('B&A Live')
        # Make sure app window is big enough to show title 
        self.geometry('800x480')
        self['background']='#0b0c1b'
        # create and pack a Mainframe window
        Mainframe(self).pack()
        
        # now start
        self.mainloop()
                    
# create an App object
# it will run itself
App()
