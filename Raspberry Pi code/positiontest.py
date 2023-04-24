# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import datetime
import csv
import board
import adafruit_bno055

FILENAME = "Test.csv"

i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = adafruit_bno055.BNO055_I2C(i2c)



with open(FILENAME, mode = 'w', newline='') as file:
    file.write("time, mag, acc, gyro, euler, linacc, gravity s_pos, s_vel, s_cur\n")

while True:
    t = datetime.datetime.timestamp(datetime.datetime.now())*1000
    sensorValues = [t,  sensor.magnetic, sensor.acceleration, sensor.gyro, sensor.euler, sensor.linear_acceleration, sensor.gravity]
    with open(FILENAME, 'a', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(sensorValues)

    time.sleep(.3)
