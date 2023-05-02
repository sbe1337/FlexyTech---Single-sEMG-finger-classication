#!/usr/bin/python3

### using multithreading 
'''
in this code the sensor data is read and saved in the memory where it is continuously updated.
the sensor thread continuosly enqueue the sensor reading at 1Khz sampling frequency, and the send thread will send the data
to the computer/laptop.
it doesn't matter how fast we recieve the data as long as we measure it at the right frequency.

If this script is kept open - beaglebone needs to be shutdown due to some overflow error!
'''
import queue
import socket 
import threading
from time import sleep,time

# Set server address and create a datagram socket
serverAddress = ("192.168.7.1", 8080)
clientSensorSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Analog input to read from file
pin = 0
file = "/sys/bus/iio/devices/iio:device0/in_voltage{}_raw".format(pin)
f = open(file, "r")

# Read sensor data from file and put in queue
def read_sensor_data():
    while(True):
        try:
            f.seek(0)
            data = f.read().strip()
            clientSensorSocket.sendto(data.encode(), serverAddress)
            sleep(0.001) #Play around with this value!
        
        except KeyboardInterrupt:
            break
        
read_sensor_data()      
        
# Send sensor data to server from queue
# def send_sensor_data():
#     while(True):
#         try:
            
#             data = data_queue.get()
#             clientSensorSocket.sendto(data.encode(), serverAddress)
#             #sleep(0.0005) #Play around with this value!
#         except KeyboardInterrupt:
#             break

        
    #dataIn,_ = clientSensorSocket.recvfrom(128)#128

      
# Create a queue to hold the sensor data
# data_queue = queue.Queue()

# # Create a thread to read the sensor data
# sensor_thread = threading.Thread(target=read_sensor_data)
# send_thread = threading.Thread(target=send_sensor_data)

# # Start the threads
# send_thread.start()
# sensor_thread.start()

# while(True):
#     try:
#         pass
#     except KeyboardInterrupt:
#         clientSensorSocket.close() #Close socket
#         print("Interrupt!")
        