import serial
import pynmea2
import csv
while(1):
	ofile  = open('gps_data.csv', 'a')
        writer = csv.writer(ofile)
	ser= serial.Serial('/dev/ttyUSB0',9600)
	s=ser.readline()
	if '$GPGGA' in s:
		msg=pynmea2.parse(s)
		flat= float(msg.lat)
		flon= float(msg.lon)
		dlt=flat/100
		idlt=int(dlt) + (flat-int(dlt)*100)/60
		dln=flon/100
		idln=int(dln) + (flon-int(dln)*100)/60
		print idlt
		print idln
		print msg.timestamp
		print '\n'
		writer.writerow( (idlt, idln) )
	ofile.close()

