from picamera import PiCamera
import RPi.GPIO as GPIO
from time import sleep
import serial
import pynmea2
import csv
GPIO.setmode(GPIO.BCM)
GPIO.setup(20,GPIO.OUT)
GPIO.setup(21,GPIO.OUT)
i=1
r=0
camera = PiCamera()
while(1):
        GPIO.output(21,GPIO.HIGH)
	GPIO.output(20,GPIO.LOW)
        camera.capture('/home/pi/wear/photos/%s.jpg' % i)
        i=i+1
	ofile  = open('gps_data.csv', 'a')
        writer = csv.writer(ofile)
	ser= serial.Serial('/dev/ttyUSB0',9600)
	s=ser.readline()
	if '$GPGGA' in s:
		r=r+1
		if(r>2):
			msg=pynmea2.parse(s)
			print msg.lat
        	        print msg.lon
			flat=float(msg.lat)
			flon=float(msg.lon)
			dlt=flat/100
			idlt=int(dlt) + (flat-int(dlt)*100)/60
			dln=flon/100
			idln=int(dln) + (flon-int(dln)*100)/60
			#print idlt
			#print idln
			#print msg.timestamp
			#print '\n'
			writer.writerow( (idlt, idln) )
		ofile.close()

