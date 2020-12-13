import serial
from datetime import datetime
import subprocess as s
import os

def notify(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))

notify("Ultrasonic Sensor", "Sensor has been activated")
# # Serial port parameters

#t1 = datetime.strptime(str(datetime.now()),'%a %b %d %H:%M:%S +0000 %Y')
#print(t1.minute)
recordedValue = {
    'counter': [],
    'valueRecord': [],
    'hour': [],
    'minute': []
}
recordedValue['counter'].append(1)
recordedValue['valueRecord'].append(2)
recordedValue['hour'].append(1)
recordedValue['minute'].append(2)
print(recordedValue)

"""
serial_speed = 9600
serial_port = '/dev/tty.HC-06-DevB' # bluetooth shield hc-06
#serial_port = '/dev/cu.usbmodem14101'
counter = 0
flag = True

if __name__ == '__main__':
    print("connecting to serial port ...")
    ser = serial.Serial(serial_port, serial_speed, timeout=10)
    ser.flushInput()
    recordedValue = {
        'counter': [],
        'valueRecord': [],
        'hour': [],
        'minute': []

    }
    while flag:
        print("recieving message from arduino ...")
        if (datetime.now().hour > 12):
            hour = datetime.now().hour - 12
        else:
            hour = datetime.now().hour
        min = datetime.now().minute
        data = ser.readline()
        print("Entering")
        print(data)
        #time.sleep(1/(9600 * 2))
        if (data != ""):
            print ("arduino says: ") # data
            print (data.decode())
            #recordedValue['counter'].append(counter)
            #recordedValue['valueRecord'].append(data.decode())
            #recordedValue['hour'].append(hour)
            #recordedValue['minute'].append(min)
        else:
            print ("arduino doesnt respond")
        counter = counter + 1
        #str2 = "Test_" + str(counter)
        #ser.write(str.encode(str2))
        if counter >1000:
            flag = False
    ser.close()
    print ("finish program and close connection!")

"""