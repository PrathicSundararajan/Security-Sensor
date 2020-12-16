# Author: Prathic 
# Version: 2.0 
# Instructables Battery Powered Competition 
import serial
from datetime import datetime
import csv
import os

# notification system for OS
def notify(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))

# creates resources folder if it doesn't exist
def checkResource():
   if not os.path.exists('resources'):
        os.mkdir('resources')

def begWriter():
    checkResource()
    fileLoc = 'resources/recordedValues'
    recordingNum = input("Please enter recording number: ")
    fileLoc = fileLoc + str(recordingNum) + ".csv"
    csvFile = open(fileLoc,'w')
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow(['Data Number', 'Hour', 'Minute','Seconds', 'Data Value'])
    return csvWriter, csvFile

def appending(recordedValue, counter, currRecordedValue, hour, min, secs):
    recordedValue['counter'].append(counter)
    recordedValue['valueRecord'].append(currRecordedValue)
    recordedValue['hour'].append(hour)
    recordedValue['minute'].append(min)
    recordedValue['second'].append(secs)
    return recordedValue

serial_speed = 9600
serial_port = '/dev/tty.HC-06-DevB' # bluetooth shield hc-06
#serial_port = '/dev/cu.usbmodem14101'
counter = 1
lastNofic = 0
flag  = True
distance_wall = 30 #VARIABLE that determines when the sensor goes off
if __name__ == '__main__':
    csvWriter, csvFile = begWriter()
    print("connecting to serial port ...")
    x=os.system("ls /dev/tty.HC-06-DevB")
    if x!=0:
        raise ValueError('The bluetooth module is not connected')
    ser = serial.Serial(serial_port, serial_speed, timeout=10)   
    str2 = "Test_" + str(counter)
    ser.flushInput()
    recordedValue = {'counter': [], 'valueRecord': [], 'hour': [], 'minute': [], 'second': []}
    ser.write(str.encode(str2))
    data = ser.readline()  
    if counter == 1 and data != "" and data != " ":
        currRecordedValue = data.decode().rstrip()  
        if currRecordedValue == "":
            flag = False
        while not flag:
            print('Switch is off currently')
            data = ser.readline()
            currRecordedValue = data.decode().rstrip()   
            if (currRecordedValue != "" and currRecordedValue != " "):
                print('Switch is turned back on')
                flag = True
    while flag:
        if (datetime.now().hour > 12):
            hour = datetime.now().hour - 12
        else:
            hour = datetime.now().hour
        min = datetime.now().minute
        secs = datetime.now().second
        data = ser.readline()        
        if (data != "" and data != " "):
            currRecordedValue = data.decode().rstrip()  
            if currRecordedValue == "":
                flag = False
            if float(currRecordedValue) == float(-1000):
                print('Switch turned off')
                flag = False        
            if counter % 50 == 0:
                print('ID: ', counter,'Curr Value: ', currRecordedValue, 'lastNotific: ', lastNofic)
            if (float(currRecordedValue) < distance_wall and counter - lastNofic > 250 and currRecordedValue != -1000):
                notfStr = "[" + str(hour) + ":"  + str(min) + ":" + str(secs) + "] " + "Sensor Activation- " + str(currRecordedValue) + " cms"
                lastNofic = counter
                notify("Security Sensor #1", notfStr)
            if min/10 == 0:
                min = str(0) + str(min)
            recordedValue = appending(recordedValue, counter, currRecordedValue, hour, min, secs)
            csvWriter.writerow([counter, hour, min,secs, currRecordedValue])
        else:
            print ("arduino doesnt respond")
        counter = counter + 1
        str2 = "Test_" + str(counter)
        while not flag:
            print('Switch is still turned off')
            data = ser.readline()
            currRecordedValue = data.decode().rstrip()   
            if (currRecordedValue != "" and currRecordedValue != " "):
                flag = True
    ser.close()
    csvFile.close()
