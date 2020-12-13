import serial
from datetime import datetime
import csv
#import notify2
import os

# # Serial port parameters
def notify(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))
serial_speed = 9600
serial_port = '/dev/tty.HC-06-DevB' # bluetooth shield hc-06
#serial_port = '/dev/cu.usbmodem14101'
counter = 1
lastNofic = 0
flag  = True
fileLoc = 'resources/recordedValues'
if __name__ == '__main__':
    recordingNum = input("Please enter recording number: ")
    fileLoc = fileLoc + str(recordingNum) + ".csv"
    csvFile = open(fileLoc,'w')
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow(['Data Number', 'Hour', 'Minute','Seconds', 'Data Value'])
    print("connecting to serial port ...")
    ser = serial.Serial(serial_port, serial_speed, timeout=10)
    str2 = "Test_" + str(counter)
    ser.flushInput()
    recordedValue = {
        'counter': [],
        'valueRecord': [],
        'hour': [],
        'minute': [],
        'second': []
    }
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
        if (data != ""):
            #print ("arduino says: ") # data
            currRecordedValue = data.decode().rstrip()
            recordedValue['counter'].append(counter)
            recordedValue['valueRecord'].append(currRecordedValue)
            recordedValue['hour'].append(hour)
            recordedValue['minute'].append(min)
            recordedValue['second'].append(secs)
            if (float(currRecordedValue) < 100 and counter - lastNofic > 20):
                notfStr = "Sensor has been activated: " + str(currRecordedValue) + " cms"
                lastNofic = counter
                #notify("Ultrasonic Sensor", notfStr)
            if min/10 == 0:
                min = str(0) + str(min)
            print('Recorded at: ' + str(hour) + ":" + str(min))
            print (currRecordedValue)
            #print([counter, hour, min, recordedValue])
            csvWriter.writerow([counter, hour, min,secs, currRecordedValue])

        else:
            print ("arduino doesnt respond")
        counter = counter + 1
        str2 = "Test_" + str(counter)
        ser.write(str.encode(str2))
        #if counter >100:
        #    flag = False
    ser.close()
    csvFile.close()
