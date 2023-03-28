#ifndef __DISP_DATA_H__
#define __DISP_DATA_H__

#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>

/* Set the delay between fresh samples */
#define BNO055_SAMPLERATE_DELAY_MS (100)
#define SETUP_TIME_MS (10000)

// Check I2C device address and correct line below (by default address is 0x29 or 0x28)
//                                   id, address

//Displays some basic information on this sensor from the unified
//sensor API sensor_t type (see Adafruit_Sensor for more information)
void displaySensorDetails(Adafruit_BNO055& bno);

//Display some basic info about the sensor status''
void displaySensorStatus(Adafruit_BNO055& bno);

//Display sensor calibration status
void displayCalStatus(Adafruit_BNO055& bno);

void displayData(Adafruit_BNO055& bno, sensors_event_t& event);

void displayRawData(Adafruit_BNO055& bno);

void displayOrientation(Adafruit_BNO055& bno, sensors_event_t& event);

String inputChoise(const String question);

#endif
