import RPi.GPIO as GPIO
import time

LED=17 #check the pinout diagram



GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(LED,GPIO.OUT)

print("led is on")

GPIO.output(LED,GPIO.HIGH)
time.sleep(5)

print("led is off")

GPIO.output(LED, GPIO.LOW)