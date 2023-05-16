#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import utilities as u
import datetime
import numpy as np
import time
import datetime
import csv
import board
import adafruit_bno055

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

from dynamixel_sdk import * # Uses Dynamixel SDK library

'''-----------------------------------------------------------'''
SAMPLINGRATE = 100 #Hz

#********* DYNAMIXEL Model definition *********     
# Control table address
ADDR_OPERATING_MODE         = 11
ADDR_VEL_LIMIT              = 44
ADDR_TORQUE_ENABLE          = 64
ADDR_LED                    = 65

ADDR_GOAL_VEL               = 104
ADDR_PROFILE_ACCELERATION   = 108
ADDR_PROFILE_VELOCITY       = 112
ADDR_GOAL_POSITION          = 116

ADDR_PRESENT_CURRENT        = 126
ADDR_PRESENT_VEL            = 128
ADDR_PRESENT_POSITION       = 132

ADDR_VELOCITY_TRAJECTORY    = 136
ADDR_PRESENT_INPUT_VOLTAGE  = 144

# DYNAMIXEL Protocol Version (1.0 / 2.0)
# https://emanual.robotis.com/docs/en/dxl/protocol2/
PROTOCOL_VERSION            = 2.0

# Factory default ID of all DYNAMIXEL is 1
DXL_ID                      = 1
DEVICENAME                  = '/dev/ttyUSB0'

# Dynamixel values
DXL_MINIMUM_POSITION_VALUE  = 0         # Refer to the Minimum Position Limit of product eManual
DXL_MAXIMUM_POSITION_VALUE  = 4095      # Refer to the Maximum Position Limit of product eManual
DXL_VELOCITY_LIMIT          = 230       # Default velocit limit
BAUDRATE                    = 57600     # dynamixel baudrate
LED_ON                      = 1         
LED_OFF                     = 0
TORQUE_ENABLE               = 1         # Value for enabling the torque
TORQUE_DISABLE              = 0         # Value for disabling the torque
DXL_MOVING_STATUS_THRESHOLD = 20        # Dynamixel moving status threshold
POS_MODE                    = 3       
VEL_MODE                    = 1
PROFILE_ACC                 = 5         # Lowest acceleration possible

def setupServo(packetHandler: PacketHandler, mode = POS_MODE, profile_acc = 0, profile_velocity = 0):
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_OPERATING_MODE, mode)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_PROFILE_ACCELERATION, profile_acc)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        else:
            print('successfully set profile acceleration\n')
            if mode == POS_MODE:
                dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_PROFILE_VELOCITY, profile_velocity)
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
                elif dxl_error != 0:
                    print("%s" % packetHandler.getRxPacketError(dxl_error))
                else:
                    print('successfully set profile velocity\n')
            dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%s" % packetHandler.getRxPacketError(dxl_error))
            else:
                print("Dynamixel has been successfully connected, and mode was set to velocity mode")
                packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_LED, LED_ON)
    return

def readServoData(packetHandler: PacketHandler, portHandler: PortHandler, ID, COMMAND_ADDR):
    if COMMAND_ADDR == ADDR_PRESENT_CURRENT:
        dxl_reply, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, ID, COMMAND_ADDR)
    else:
        dxl_reply, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, ID, COMMAND_ADDR)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    return dxl_reply

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
    print("Sampling pure IMU measurements for 2 minutes")
    
    #Create new file with correct headers
    with open(filename, mode = 'w', newline='') as file:
        file.write("time,magX,magY,magZ,accX,accY,accZ,gyrX,gyrY,gyrZ,eulerX,eulerY,eulerZ,linX,linY,linZ,gravX,gravY,gravZ\n")

    start = datetime.datetime.timestamp(datetime.datetime.now())
    while(datetime.datetime.timestamp(datetime.datetime.now()) - start < 120): #run test for 2 minutes
        t = datetime.datetime.timestamp(datetime.datetime.now())
        sensorValues = [t,  
                        sensor.magnetic[0],             sensor.magnetic[1],             sensor.magnetic[2],
                        sensor.acceleration[0],         sensor.acceleration[1],         sensor.acceleration[2],
                        sensor.gyro[0],                 sensor.gyro[1],                 sensor.gyro[2],
                        sensor.euler[0],                sensor.euler[1],                sensor.euler[2], 
                        sensor.linear_acceleration[0],  sensor.linear_acceleration[1],  sensor.linear_acceleration[2],
                        sensor.gravity[0],              sensor.gravity[1],              sensor.gravity[2]]
        
        with open(filename, 'a', newline='') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(sensorValues)

        time.sleep(1/SAMPLINGRATE) 

    print("Successfully sampled IMU measurements.")
    return

def servoTest(sensor, packetHandler: PacketHandler, portHandler: PortHandler, filename):
    print("Starting servo test with increased veolicity")
    
    ''''servo move from max pos to min pos with different velocities. '''
    # Set correct mode, profile acceleration and enable torque
    setupServo(packetHandler, mode = POS_MODE, profile_acc = PROFILE_ACC, profile_velocity = 25)

    dxl_goal_velocity = np.linspace(25 , DXL_VELOCITY_LIMIT - 50, 5, dtype=int)
    dxl_goal_pos = [DXL_MINIMUM_POSITION_VALUE, DXL_MAXIMUM_POSITION_VALUE]

    #Create new file with correct headers
    with open(filename, mode = 'w', newline='') as file:
        file.write("time,magX,magY,magZ,accX,accY,accZ,gyrX,gyrY,gyrZ,eulerX,euleY,eulerZ,linX,linY,linZ,gravX,gravY,gravZ,servoPos,servoVel,servoCur\n")


    for velocity in dxl_goal_velocity:
        print("[ID:%03d] GoalVelocity:%03d " % (DXL_ID, velocity))
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_PROFILE_VELOCITY, velocity)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        else:
            print('successfully set profile velocity\n')
            for pos in dxl_goal_pos:
                dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_GOAL_POSITION, pos)
                while 1:
                    # Read present position, velocity and current
                    dxl_present_position = readServoData(packetHandler, portHandler, DXL_ID, ADDR_PRESENT_POSITION)
                    dxl_present_velocity = readServoData(packetHandler, portHandler, DXL_ID, ADDR_PRESENT_VEL)
                    dxl_present_current = readServoData(packetHandler, portHandler, DXL_ID, ADDR_PRESENT_CURRENT)
                    
                    data = [dxl_present_position, dxl_present_velocity, dxl_present_current]

                    #Header defined above: [time, magX, magY, magZ, accX, accY, accZ, gyrX, gyrY, gyrZ, eulerX, euleY, eulerZ, linX, linY, linZ, gravX, gravY, gravX, servoPos, servoVel, servoCur]
                    t = datetime.datetime.timestamp(datetime.datetime.now())
                    sensorValues = [t,  
                                    sensor.magnetic[0],             sensor.magnetic[1],             sensor.magnetic[2],
                                    sensor.acceleration[0],         sensor.acceleration[1],         sensor.acceleration[2],
                                    sensor.gyro[0],                 sensor.gyro[1],                 sensor.gyro[2],
                                    sensor.euler[0],                sensor.euler[1],                sensor.euler[2], 
                                    sensor.linear_acceleration[0],  sensor.linear_acceleration[1],  sensor.linear_acceleration[2],
                                    sensor.gravity[0],              sensor.gravity[1],              sensor.gravity[2], 
                                    dxl_present_position,           dxl_present_velocity,           dxl_present_current]

                    with open(filename, 'a', newline='') as file:
                        writer = csv.writer(file, delimiter=',')
                        writer.writerow(sensorValues)

                    if not abs(pos - dxl_present_position) > DXL_MOVING_STATUS_THRESHOLD:
                        break

                    time.sleep(1/SAMPLINGRATE) 
    print("Successfully finished servoTest. Disabling dynamixel torque ...")
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        print("Torque disabled")

def test(sensor, packetHandler: PacketHandler, portHandler: PortHandler):
    calibrateIMU(sensor)
    date = datetime.datetime.now()
    imufilename = 'pureIMUdata%s.csv' % date
    imufilename2 = 'pureIMUdat2a%s.csv' % date
    servoFilename = 'servoData%s.csv' % date
    samplePureIMU(sensor, imufilename)
    servoTest(sensor, packetHandler, portHandler, servoFilename)
    samplePureIMU(sensor, imufilename2)

portHandler = PortHandler(DEVICENAME)
packetHandler = PacketHandler(PROTOCOL_VERSION)

# Open port
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    print("Press any key to terminate...")
    getch()
    quit()


# Set port baudrate
if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    print("Press any key to terminate...")
    getch()
    quit()

'''Setup BNO055 I2C communication'''
i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = adafruit_bno055.BNO055_I2C(i2c)

#run test
test(sensor, packetHandler, portHandler)

   
# Disable Dynamixel Torque
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))

packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_LED, LED_OFF)
# Close port
portHandler.closePort()
