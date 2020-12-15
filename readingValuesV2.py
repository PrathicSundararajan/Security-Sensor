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
   if not os.path.exists('resources2'):
        os.mkdir('resources2')

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
total = 0
distance_wall = 1000
if __name__ == '__main__':
    csvWriter, csvFile = begWriter()
    print("connecting to serial port ...")
    ser = serial.Serial(serial_port, serial_speed, timeout=10)
    str2 = "Test_" + str(counter)
    ser.flushInput()
    recordedValue = {'counter': [], 'valueRecord': [], 'hour': [], 'minute': [], 'second': []}
    ser.write(str.encode(str2))
    while flag:
        print("recieving message from arduino ...")
        if (datetime.now().hour > 12):
            hour = datetime.now().hour - 12
        else:
            hour = datetime.now().hour
        min = datetime.now().minute
        secs = datetime.now().second
        data = ser.readline()
        #print(data)
        #time.sleep(1/(9600 * 2))
        if (data != "" and data != " "):
            currRecordedValue = data.decode().rstrip()   
            if float(currRecordedValue) == float(-1000):
                print('Entering')
                flag = False                 
            total = total + float(currRecordedValue)
            print('Curr Value', currRecordedValue, 'Counter', counter, 'lastNotific', lastNofic)
            if (float(currRecordedValue) > distance_wall and counter - lastNofic > 20):
                notfStr = "Sensor has been activated: " + str(currRecordedValue) + " cms"
                lastNofic = counter
                notify("Ultrasonic Sensor", notfStr)
            if min/10 == 0:
                min = str(0) + str(min)
            recordedValue = appending(recordedValue, counter, currRecordedValue, hour, min, secs)
            csvWriter.writerow([counter, hour, min,secs, currRecordedValue])
        else:
            print ("arduino doesnt respond")
        counter = counter + 1
        str2 = "Test_" + str(counter)
        #ser.write(str.encode(str2))
        while not flag:
            print('Entering2')
            data = ser.readline()
            currRecordedValue = data.decode().rstrip()   
            #if (data != "" and data != " " and float(currRecordedValue) != float(-1000)):
            if (data != "" and data != " "):
                print(data)
                flag = True

    ser.close()
    csvFile.close()
