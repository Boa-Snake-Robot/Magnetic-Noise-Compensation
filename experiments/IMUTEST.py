#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import time
import datetime
import csv
import board
import adafruit_bno055

SAMPLINGRATE = 100 #Hz




def calibrateIMU(sensor):
    isCalibrated = "n"
    while(1):
        isCalibrated = input("Is the sensor calibrated? (y/n)")
        print("The calibration status is: {}".format(sensor.calibration_status))
        if isCalibrated == 'y':
            break
    print("Finished calibrating sensor")
    return

def samplePureIMU(sensor, filename):
    print("Sampling pure IMU measurements for 15 minutes")
    
    #Create new file with correct headers
    with open(filename, mode = 'w', newline='') as file:
        file.write("time,magX,magY,magZ,accX,accY,accZ,gyrX,gyrY,gyrZ\n")

    start = datetime.datetime.timestamp(datetime.datetime.now())
    while(datetime.datetime.timestamp(datetime.datetime.now()) - start < 15*60): #run test for 15 minutes
        t = datetime.datetime.timestamp(datetime.datetime.now())
        sensorValues = [t,  
                        sensor.magnetic[0],             sensor.magnetic[1],             sensor.magnetic[2],
                        sensor.acceleration[0],         sensor.acceleration[1],         sensor.acceleration[2],
                        sensor.gyro[0],                 sensor.gyro[1],                 sensor.gyro[2]]
        
        with open(filename, 'a', newline='') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(sensorValues)

        time.sleep(1/SAMPLINGRATE) 

    print("Successfully sampled IMU measurements.")
    return

def test(sensor):
    calibrateIMU(sensor)
    date = datetime.datetime.now()
    imufilename = 'IMUTESTdata%s.csv' % date
    samplePureIMU(sensor, imufilename)


'''Setup BNO055 I2C communication'''
i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = adafruit_bno055.BNO055_I2C(i2c)

#run test
test(sensor)