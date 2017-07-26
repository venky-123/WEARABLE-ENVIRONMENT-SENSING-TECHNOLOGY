from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.start_preview()
for i in range(20):
    sleep(0.2)
    camera.capture('/home/pi/wear/photos/%s.jpg' % i)
camera.stop_preview()

