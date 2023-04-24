
#!/usr/bin/env python
# -*- coding: utf-8 -*-

#*******************************************************************************
# Copyright 2017 ROBOTIS CO., LTD.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#*******************************************************************************


#*******************************************************************************
#***********************     Read and Write Example      ***********************
#  Required Environment to run this example :
#    - Protocol 2.0 supported DYNAMIXEL(X, P, PRO/PRO(A), MX 2.0 series)
#    - DYNAMIXEL Starter Set (U2D2, U2D2 PHB, 12V SMPS)
#  How to use the example :
#    - Select the DYNAMIXEL in use at the MY_DXL in the example code. 
#    - Build and Run from proper architecture subdirectory.
#    - For ARM based SBCs such as Raspberry Pi, use linux_sbc subdirectory to build and run.
#    - https://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_sdk/overview/

#  Author: Ryu Woon Jung (Leon)
#  Maintainer : Zerom, Will Son
# *******************************************************************************

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
SAMPLINGRATE = 20 #Hz

'''Setup servo communication'''

#********* DYNAMIXEL Model definition *********
MY_DXL = 'X_SERIES'       
FILENAME = 'servoposition%s.csv' % datetime.datetime.now()


# Control table address
if MY_DXL == 'X_SERIES':
    ADDR_OPERATING_MODE         = 11
    ADDR_VEL_LIMIT              = 44
    ADDR_TORQUE_ENABLE          = 64
    ADDR_LED                    = 65

    ADDR_GOAL_VEL               = 104
    ADDR_GOAL_POSITION          = 116

    ADDR_PRESENT_CURRENT        = 126
    ADDR_PRESENT_VEL            = 128
    ADDR_PRESENT_POSITION       = 132

    ADDR_VELOCITY_TRAJECTORY    = 136
    ADDR_PRESENT_INPUT_VOLTAGE  = 144

    DXL_MINIMUM_POSITION_VALUE  = 0         # Refer to the Minimum Position Limit of product eManual
    DXL_MAXIMUM_POSITION_VALUE  = 4095      # Refer to the Maximum Position Limit of product eManual
    DXL_VELOCITY_LIMIT          = 230       # Default velocit limit
    BAUDRATE                    = 57600
    LED_ON                      = 1
    LED_OFF                     = 0

# DYNAMIXEL Protocol Version (1.0 / 2.0)
# https://emanual.robotis.com/docs/en/dxl/protocol2/
PROTOCOL_VERSION            = 2.0

# Factory default ID of all DYNAMIXEL is 1
DXL_ID                      = 1

DEVICENAME                  = '/dev/ttyUSB0'

TORQUE_ENABLE               = 1     # Value for enabling the torque
TORQUE_DISABLE              = 0     # Value for disabling the torque
DXL_MOVING_STATUS_THRESHOLD = 20    # Dynamixel moving status threshold
POS_MODE                    = 3
VEL_MODE                    = 1

pos_index = 0
dxl_goal_position = np.linspace(DXL_MINIMUM_POSITION_VALUE, DXL_MAXIMUM_POSITION_VALUE, 6, dtype=int) 

# Initialize PortHandler instance
# Set the port path
# Get methods and members of PortHandlerLinux or PortHandlerWindows
portHandler = PortHandler(DEVICENAME)

# Initialize PacketHandler instance
# Set the protocol version
# Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
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

#Create new file with correct headers
with open(FILENAME, mode = 'w', newline='') as file:
    file.write("time, mag, acc, gyro, euler, linacc, gravity s_pos, s_vel, s_cur\n")

# Set correct mode and enable torque
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_OPERATING_MODE, POS_MODE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        print("Dynamixel has been successfully connected, and mode was set to position mode")
        packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_LED, LED_ON)

while 1:
    print("Press any key to continue (or press ESC to quit!)")
    if getch() == chr(0x1b):
        break
    
    print(dxl_goal_position[pos_index])
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_GOAL_POSITION, dxl_goal_position[pos_index])


    while 1:
        # Read present position, velocity, current
        dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DXL_ID, ADDR_PRESENT_POSITION)
        dxl_present_velocity, dxl_comm_result, dxl_error = packetHandler.read1ByteTxRx(portHandler, DXL_ID, ADDR_PRESENT_VEL)
        dxl_present_current, dxl_comm_result, dxl_error = packetHandler.read1ByteTxRx(portHandler, DXL_ID, ADDR_PRESENT_CURRENT)

        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))

        #Header defined above: [time, mag, acc, gyro, euler, linacc, gravity s_pos, s_vel, s_cur]
        t = datetime.datetime.timestamp(datetime.datetime.now())*1000
        sensorValues = [t,  sensor.magnetic, sensor.acceleration, sensor.gyro, sensor.euler, sensor.linear_acceleration, sensor.gravity, dxl_present_position, dxl_present_velocity, dxl_present_current]

        with open(FILENAME, 'a', newline='') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(sensorValues)

        print("[ID:%03d] GoalPos:%03d  PresPos:%03d" % (DXL_ID, dxl_goal_position[pos_index], dxl_present_position))
        
        if not abs(dxl_goal_position[pos_index] - dxl_present_position) > DXL_MOVING_STATUS_THRESHOLD:
            break

        time.sleep(1/SAMPLINGRATE) 

    # Change goal position/ velocity
    pos_index = pos_index + 1
    if pos_index >= len(dxl_goal_position):
        pos_index = 0

    



# Disable Dynamixel Torque
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))

packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_LED, LED_OFF)
# Close port
portHandler.closePort()
