from gpiozero import Button
from picamera import PiCamera
from signal import pause
import time

redPin = 3
pushbutton = 4

camera = PiCamera()
def take_picture_with_button():
    image_path = '/home/pi/Desktop/SHEDIO-copy/RaspberryPI/a_%s.jpg' % int(round(time.time() * 1000)) #change the path of where you want the photo to be saved
    camera.capture(image_path)
    print('pi took a photo')


button = Button(pushbutton)
button.when_pressed = take_picture_with_button #when the button/ touch sensor is activated, the picture will be taken and saved into the folder selected

pause()


