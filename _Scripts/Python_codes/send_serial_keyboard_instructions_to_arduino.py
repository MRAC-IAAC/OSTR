import serial
import time

ser = serial.Serial("COM4",9600)

def drawing():
    request = input("send something...\n")
    answer = str(request) + '\n'
    entradaSerial = answer
    ser.write(entradaSerial.encode())
    print(entradaSerial)
    if answer == 'Q\n':
        exit()

while True:
    drawing()








