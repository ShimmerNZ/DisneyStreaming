# Monitoring App so that you can see the status of the various interfaces, connectivity status, throughput, CPU utilisation and temp
# of the Raspberry Pi
# include speed test function - speedtest-cli
# show IP address
# captive portal launch?
# enable/disable speedify

#!/usr/bin/python3
from gpiozero import CPUTemperature
from tkinter import ttk
from PIL import Image, ImageTk
import time
import tkinter as tk
import speedify
import json
import re
import os
import subprocess
import argparse
import psutil

interface ="wlan0" # this is just a sample value

#CPU Temp Section
cpu=CPUTemperature()
print(cpu.temperature)
global tx_prev
global rx_prev
(tx_prev,rx_prev)=(0,0)
#Speedify settingssudo apt-get install python3-pil python3-pil.imagetk
#state=speedify.show_state()

#stats=speedify.stats(5)
#print(stats[0][1])

#for item in stats:
#    print(item)
#stats_dict=json.dumps(stats)
#print(stats_dict['adapters'])
#print(state)
#print(stats)
#print(speedify.show_connectmethod())
#print(speedify.show_currentserver())
#print(speedify.Priority)
#print(speedify.speedtest())

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
        img=tk.PhotoImage(file='down.gif')
        img2=tk.PhotoImage(file='up.gif')
        lbl=tk.Label(self, image=img, bg='#0b0c1b')
        lbl.image = img
        lbl.grid(row=1, column=3)
        lbl=tk.Label(self, image=img2, bg='#0b0c1b')
        lbl.image = img2
        lbl.grid(row=1, column=6)

        tk.Label(self,text='DOWNLOAD ',bg='#0b0c1b',fg='#fff', font=("HCo Gotham SSm",16)).grid(row=1, column=4)
        tk.Label(self,text='Mbps', bg='#0b0c1b',fg='#9193a8', font=("HCo Gotham SSm",16)).grid(row=1, column=5, sticky='W')
        tk.Label(self,text='UPLOAD ', bg='#0b0c1b',fg='#fff', font=("HCo Gotham SSm",16)).grid(row=1, column=7)
        tk.Label(self,text='Mbps', bg='#0b0c1b',fg='#9193a8', font=("HCo Gotham SSm",16)).grid(row=1, column=8, stick='W')

        self.TXspeed = tk.StringVar()

        tk.Label(self,textvariable=self.TXspeed , bg='#0b0c1b',fg='#fff', font=("HCo Gotham SSm",40)).grid(row=2, column=6, rowspan=2, columnspan=3)
        self.RXspeed = tk.StringVar()
        tk.Label(self,textvariable=self.RXspeed , bg='#0b0c1b',fg='#fff', font=("HCo Gotham SSm",40)).grid(row=2, column=3, rowspan=2, columnspan=3)

        #Adapter Stats
        tk.Label(self,text='CONNECTION TYPE  ', bg='#0b0c1b',fg='#fff', font=("HCo Gotham SSm",10)).grid(row=7, column=4)
        tk.Label(self,text='INTERFACE NAME  ', bg='#0b0c1b',fg='#fff', font=("HCo Gotham SSm",10)).grid(row=7, column=5, columnspan=2)
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
        tk.Button(self, text="Exit", command = exit).grid(row=0, column=0, columnspan=2, rowspan=2)
        tk.Button(self, text="Connect", command= self.connect).grid(row=0, column=8, columnspan=2, rowspan=2, sticky='E')

        #Progress bar code 
        s=ttk.Style()
        s.configure("green.Vertical.TProgressbar", troughcolor="gray", background="green")
        s.configure("yellow.Vertical.TProgressbar", troughcolor="gray", background="yellow")
        s.configure("red.Vertical.TProgressbar", troughcolor="gray", background="red")
        
        progress2=ttk.Progressbar(self,orient='vertical',length=250, variable=self.CPUutil)
        progress2.grid(row=3,column=2, rowspan=13)
        progress2.config(mode='determinate')

        #slap in a logo here
        img3=Image.open('Brianlogo.png').resize((100,100))
		img=ImageTk.PhotoImage(img3)
        lbl=tk.Label(self, image=img3, bg='#0b0c1b')
        lbl.image = img3
        lbl.grid(row=22, column=0, columnspan=4, rowspan=2)

        #variable time
        self.TimerInterval = 1000
        self.TimerInterval2 = 3000
        self.TimerInterval3 = 1250
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
        
        # call Get Temp which will call itself after a delay
        self.GetTemp()
        self.GetCPU()
        self.GetState()
        self.GetAdapter()
        self.GetSpeed()
        self.GetCurrentServer()
        
    def GetTemp(self):
        ## replace this with code to read sensor
        self.TemperatureC.set(self.TempC)
        #self.TemperatureF.set(self.TempF)
        tempFile =open("/sys/class/thermal/thermal_zone0/temp")
        cpu_temp = tempFile.read()
        self.TempC = round(float(cpu_temp)/1000,1) 
        self.TempF = round(float(1.8*float(cpu_temp))/1000+32,1)
        TempCheck=int(self.TempC)
        #insert colour change on temp
        s=ttk.Style()
        s.configure("green.Vertical.TProgressbar", troughcolor="gray", background="green")
        s.configure("yellow.Vertical.TProgressbar", troughcolor="gray", background="yellow")
        s.configure("red.Vertical.TProgressbar", troughcolor="gray", background="red")
        if TempCheck <= 50:
            progress=ttk.Progressbar(self, maximum=90, orient="vertical",length=250,style="green.Vertical.TProgressbar",variable=self.TemperatureC)
        elif 75 < TempCheck <= 80:
            progress=ttk.Progressbar(self, maximum=90, orient="vertical",length=250,style="yellow.Vertical.TProgressbar",variable=self.TemperatureC)
        elif TempCheck > 80:
            progress=ttk.Progressbar(self, maximum=90, orient="vertical",length=250,style="red.Vertical.TProgressbar",variable=self.TemperatureC)
        else:
           progress=ttk.Progressbar(self, maximum=90, orient="vertical",length=250,style="green.Vertical.TProgressbar",variable=self.TemperatureC)

        progress.grid(row=3,column=1, rowspan=13)
        progress.config(mode='determinate')

        # Now repeat call
        self.after(self.TimerInterval,self.GetTemp)

    def GetCPU(self):
        self.CPUutil.set(self.CPUUtil)
        self.CPUUtil=psutil.cpu_percent(interval=None, percpu=False)
        self.CPUUtil=int(self.CPUUtil)

        self.after(self.TimerInterval3,self.GetCPU)

    def GetState(self):
        self.Connectionstate.set(self.State)
        stateraw=speedify.show_state()
        #self.State=(str(stateraw).replace('State.', ''))
        StateStr=str(stateraw).replace('State.', '')
        if StateStr == "LOGGED_IN":
            self.State="DISCONNECTED"
        else:
            self.State=(str(stateraw).replace('State.', '')) 

        # Now repeat call
        self.after(self.TimerInterval,self.GetState)

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

	# Now repeat call
        self.after(self.TimerInterval,self.GetAdapter)

    def GetCurrentServer(self):
        self.Currentserver.set(self.Server)
        servers=speedify.show_currentserver()
        self.Server=servers['friendlyName']
        self.after(self.TimerInterval2,self.GetCurrentServer)

    def connect(self):
        checkState = self.State
        checkState = str(checkState)
        if checkState!="CONNECTED":

            speedify.connect_closest()
        else:
            speedify.disconnect()

    def exit(self):
        exit()

  #  def get_bytes(t, iface='connectify0'):
  #      with open('/sys/class/net/' + iface + '/statistics/' + t + '_bytes', 'r') as f:
  #          data = f.read();
  #      return int(data)
  
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
        #time.sleep(1)
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
