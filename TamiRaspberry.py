import serial
import json
import socket
import RPi.GPIO as GPIO
import time
from time import sleep


ser = serial.Serial("/dev/ttyUSB0", 9600, timeout=.1)  

sock = socket.socket()
print ('Socket created ...')

port = 23000
sock.bind(('', port))
sock.listen(5)

print ('socket is listening')
c, addr = sock.accept()
print ('got connection from ', addr)

while True:
    received_data = ser.read() #read serial port
    sleep(0.3)
    data_left = ser.inWaiting() #check for remaining byte
    received_data += ser.read(data_left)
    received_data = str(received_data).replace("b'","")
    received_data = str(received_data).replace("\\n'","")
    if received_data.startswith("$START") and received_data.endswith("$END"):
        received_data = str(received_data).replace("$START","")
        received_data = str(received_data).replace("$END","")
        
    c.send(bytes(received_data.encode("utf-8")))
    
    jsonReceived = str(c.recv(1024))
    jsonReceived = jsonReceived.replace("b'","")
    jsonReceived = jsonReceived.replace("'","")

    jsonData = json.loads(jsonReceived)
    
    print ('--Received Data Start--')
    print ('Horizantal_Left_Motor ' , jsonData['Horizantal_Left_Motor'])
    print ('Horizantal_Right_Motor ' , jsonData['Horizantal_Right_Motor'])
    print ('Vertical_Back_Motor ' , jsonData['Vertical_Back_Motor'])
    print ('Vertical_Front_Motor ' , jsonData['Vertical_Front_Motor'])
    print ('--Received Data End--')
    print ('')
 
    A = str(jsonData['Horizantal_Left_Motor'])
    B = str(jsonData['Horizantal_Right_Motor'])      
    C = str(jsonData['Vertical_Back_Motor'])
    D = str(jsonData['Vertical_Front_Motor'])
          
    motorData = str(A) + "," + str(B) + "," + str(C) + "," + str(D) + "#"
    print (motorData)
    ser.write(motorData.encode())
    sleep(0.3)