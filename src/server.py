#!/usr/bin/python

import socket
import json
import keyboard
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time
import datetime
import pandas as pd
import numpy as np


#Set IP and Port of listening server
ip      = "192.168.7.1"
port    = 8080
listeningAddress = (ip, port)

dataComplete = []
time_stamp = []
#Make datagram socket using IPv4 addressing scheme and bind it 
datagramSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
datagramSocket.bind(listeningAddress)

name = input("Enter subject name: ")

#Save data in JSON with labels
def save_json(label):
    global dataComplete
    filename = '../data/'+str(name) + str(label) + "data.json" #Will save each finger in separate files, check if this can be improved
    data_to_save = {'label': label, 'data': dataComplete,'time':time_stamp}
    with open(filename, 'w') as f:
        json.dump(data_to_save, f, indent = 4)
    plotting(filename)
    print('Data saved with label:', label, "length: ", len(dataComplete))
    dataComplete.clear()
    time_stamp.clear()

#Receive new data to append
def receive_data():
    emgVal,_ = datagramSocket.recvfrom(128)
    emgVal = float(emgVal.decode())
    dataComplete.append(emgVal)
    time_stamp.append(time.time())
    
#Listen to keyboard press
def listen_keyboard():
    if keyboard.is_pressed('1'): #Thumb
        dataComplete.clear() #Clear data before saving
        while keyboard.is_pressed('1'): 
            receive_data()
        save_json('1')
    elif keyboard.is_pressed('2'): #Index
        dataComplete.clear()
        while keyboard.is_pressed('2'): 
            receive_data()
        save_json('2')
    elif keyboard.is_pressed('3'): #Middle
        dataComplete.clear()
        while keyboard.is_pressed('3'): 
            receive_data()
        save_json('3')
    elif keyboard.is_pressed('4'): #Ring
        dataComplete.clear()
        while keyboard.is_pressed('4'): 
            receive_data()
        save_json('4')
    elif keyboard.is_pressed('5'): #Little
        dataComplete.clear()
        while keyboard.is_pressed('5'): 
            receive_data()
        save_json('5')


def plotting(path):
    df = pd.read_json(path)

    label = df['label'][0]
    x = df['data']
    time = df['time']

    fig, ax = plt.subplots()
    ax.plot(time, x)
    ax.set_title(label)
    ax.set_xlabel('Time')
    ax.set_ylabel('Data')
    ax.grid()
    plt.savefig('../plots/'+path[:-4]+'png')

print("Hold number key 1-5 to record data in JSON (\'ctrl+c\' to exit)")
print("1 = Thumb, 2 = Index, 3 = Middle, 4 = Ring, 5 = Little")

while(True):
    try:
        listen_keyboard()
    except KeyboardInterrupt:
        datagramSocket.close() #Close socket
        print("Interrupt!")
        break