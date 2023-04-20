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
    ADDR_PROFILE_ACCELERATION   = 108
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
PROFILE_ACC                 = 1

vel_index = 0
dxl_goal_velocity = np.linspace(40 , DXL_VELOCITY_LIMIT - 100, 20, dtype=int)

 
last_mod = 1        #just one
present_mod = 4096  #180 degrees

# Initialize PortHandler instance
# Set the port path
# Get methods and members of PortHandlerLinux or PortHandlerWindo ws
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

# Set correct mode, profile acceleration and enable torque
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_OPERATING_MODE, VEL_MODE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_PROFILE_ACCELERATION, PROFILE_ACC)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        print('successfully set profile acceleration\n')
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        print("Dynamixel has been successfully connected, and mode was set to velocity mode")
        packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_LED, LED_ON)

while 1:
    print("Press any key to continue(or press ESC to quit!)")

    if getch() == chr(0x1b):
        break
    
    num_rounds = 0

    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_GOAL_VEL, dxl_goal_velocity[vel_index])
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        print('successfully set speed to ' + str(dxl_goal_velocity[vel_index]))
        num_rounds = 0
                

    while 1:
        # Read present position
        dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DXL_ID, ADDR_PRESENT_POSITION)
        # Read present veolicity
        dxl_present_velocity, dxl_comm_result, dxl_error = packetHandler.read1ByteTxRx(portHandler, DXL_ID, ADDR_PRESENT_VEL)
        # Read present current
        dxl_present_current, dxl_comm_result, dxl_error = packetHandler.read1ByteTxRx(portHandler, DXL_ID, ADDR_PRESENT_CURRENT)
        # Read present input voltage
        dxl_present_input_voltage, dxl_comm_result, dxl_error = packetHandler.read1ByteTxRx(portHandler, DXL_ID, ADDR_PRESENT_INPUT_VOLTAGE)
        

        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        data = [dxl_present_position, dxl_present_velocity, dxl_present_current]

        u.writeDataArrayToFile(FILENAME, data, withTimestamps = True)
        print("[ID:%03d] GoalVelocity:%03d  PresVelocity:%03d" % (DXL_ID, dxl_goal_velocity[vel_index], dxl_present_velocity))

        
        present_mod = dxl_present_position % 4096
        if (present_mod - last_mod) <= 0:
            #whenever the dynamixel has performed a full rotation
            num_rounds = num_rounds + 1
        if num_rounds > 1:
            # Change goal velocity
            vel_index = vel_index + 1
            if vel_index >= len(dxl_goal_velocity):
                dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_GOAL_VEL, 0)
                vel_index = 0
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%s" % packetHandler.getRxPacketError(dxl_error))
            else:
                print('successfully set speed to ' + str(dxl_goal_velocity[vel_index]))
                break
            dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_GOAL_VEL, dxl_goal_velocity[vel_index])
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%s" % packetHandler.getRxPacketError(dxl_error))
            else:
                print('successfully set speed to ' + str(dxl_goal_velocity[vel_index]))
                num_rounds = 0
        last_mod = present_mod


   



# Disable Dynamixel Torque
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))

packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_LED, LED_OFF)
# Close port
portHandler.closePort()
