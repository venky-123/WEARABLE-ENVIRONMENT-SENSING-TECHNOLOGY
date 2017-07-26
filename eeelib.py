from picamera import PiCamera
import RPi.GPIO as GPIO
from time import sleep
import serial
import pynmea2
import csv
import MySQLdb

#Connection to SQL server!
db = MySQLdb.connect("192.168.0.2","moderator","moderator","main_aat" )

# prepare a cursor object using cursor() method
cursor = db.cursor() #set journey_id as 'd'

#Setup here !!!

#Timestamp here !!! 
print db
format_str="""INSERT INTO root(journey_id,initial_timestamp,cluster_id,gps_tags,image_tags) VALUES ('','','','','hello');"""
sql_command=format_str.format()  #inserting time stamp into the values and updating the data base
cursor.execute(sql_command)

GPIO.setmode(GPIO.BCM)                                        
GPIO.setup(20,GPIO.OUT)
GPIO.setup(21,GPIO.OUT)
i=1
r=0
d=5
camera = PiCamera()
sql_command_1="""SELECT TOP 1 journey_id FROM root ORDER BY journey_id DESC;"""
j_id=cursor.execute(sql_command_1)
while(1):
    GPIO.output(21,GPIO.HIGH)
    GPIO.output(20,GPIO.LOW)	
    file_name='/home/pi/wear/photos/%s_%s.jpg' % (d,i)
    camera.capture(file_name)      #captures the photo and stores in the given directory  with the name as the integer 'i'
    i=i+1
    r=r+1
    #for serial communication of GPS data through USB
    #object for gps data
    #inserting into gps_seq table
    format_str="""INSERT INTO gps_seq(journey_id,loc_long,loc_lat,time_stamp,gps_tags) VALUES ({j_id},{loc_long},{loc_lat},'{time_stamp}','');"""                         #prints longitude in a particular format given below(string data type)
    sql_command_2=format_str.format(j_id=j_id,loc_long=i,loc_lat=r,timestamp=(time.time()-start))
    sql.execute(sql_command_2)
    #inserting time stamp and journey id into image_seq
    format_str="""INSERT INTO image_seq(journey_id,image_num,image,time_stamp,image_tags) VALUES ({j_id},'','',{time_stamp},'');"""
    sql_command_3=format_str.format(j_id=j_id,time_stamp=(time.time()-start))
    cursor.execute(sql_command_3)
    #inserting image ito the server 
    format_str="""INSERT INTO image-seq('image') 
    SELECT BulkColumn 
    FROM Openrowset( Bulk '{path}', Single_Blob) as img"""
    sql_command_4=format_str.format(path=file_name)  
    cursor.execute(sql_command_4)      
		
			#writer.writerow( (idlt, idln) ) #idlt = latitude; idln=longitude !!
		

#Database Connection close! 
db.close()
'''flat=float(msg.lat)                    #conversion of string data type into float
flon=float(msg.lon)                    #conversion of string data type into float
dlt=flat/100            
idlt=int(dlt) + (flat-int(dlt)*100)/60 #converting the format into a general format ( in degrees )
dln=flon/100 
idln=int(dln) + (flon-int(dln)*100)/60 #converting the format into a general format ( in degrees )'''

#
#
#
#
#    The serial port contains the following data ...
#
#
#
#	$GPGSA,A,3,17,09,28,08,26,07,15,,,,,,2.4,1.4,1.9*.6,1.7,2.0*3C
#	$GPRMC,031349.000,A,3355.3471,N,11751.7128,W,0.00,143.39,210314,,,A*76
#	$GPGGA,031350.000,3355.3471,N,11751.7128,W,1,06,1.7,112.2,M,-33.7,M,,0000*6F
#	$GPGSA,A,3,17,09,28,08,07,15,,,,,,,2.6,1.7,2.0*3C
#	$GPGSV,3,1,12,17,67,201,30,09,62,112,28,28,57,022,21,08,55,104,20*7E
#	$GPGSV,3,2,12,07,25,124,22,15,24,302,30,11,17,052,26,26,49,262,05*73
#	$GPGSV,3,3,12,30,51,112,31,57,31,122,,01,24,073,,04,05,176,*7E
#	$GPRMC,031350.000,A,3355.3471,N,11741.7128,W,0.00,143.39,210314,,,A*7E
#	$GPGGA,031351.000,3355.3471,N,11741.7128,W,1,07,1.4,112.2,M,-33.7,M,,0000*6C
#
#
#    Out of which only GPGGA format data is required 
#	
#
#
#	$GPGGA,031351.000,------>latitude (3355.3471),N,--------->longitude(11741.7128),W,1,07,1.4,112.2,M,-33.7,M,,0000*6C
#
#
#	these latitude and longitudes are in the following format
#	latitude ---->   ddmm.mmmm
#	longitude---->   dddmm.mmmm
#
#	d- degrees 
#	m- minutes
#
#
#
#
#
#
#
#
#
#
