#include "displayData.h"

/**************************************************************************/
/*
    Displays some basic information on this sensor from the unified
    sensor API sensor_t type (see Adafruit_Sensor for more information)
*/
/**************************************************************************/
void displaySensorDetails(Adafruit_BNO055& bno)
{
  sensor_t sensor;
  bno.getSensor(&sensor);
  Serial.println("------------------------------------");
  Serial.print  ("Sensor:       "); Serial.println(sensor.name);
  Serial.print  ("Driver Ver:   "); Serial.println(sensor.version);
  Serial.print  ("Unique ID:    "); Serial.println(sensor.sensor_id);
  Serial.print  ("Max Value:    "); Serial.print(sensor.max_value); Serial.println(" xxx");
  Serial.print  ("Min Value:    "); Serial.print(sensor.min_value); Serial.println(" xxx");
  Serial.print  ("Resolution:   "); Serial.print(sensor.resolution); Serial.println(" xxx");
  Serial.println("------------------------------------");
  Serial.println("");
  delay(500);
}

/**************************************************************************/
/*
    Display some basic info about the sensor status
*/
/**************************************************************************/
void displaySensorStatus(Adafruit_BNO055& bno)
{
  /* Get the system status values (mostly for debugging purposes) */
  uint8_t system_status, self_test_results, system_error;
  system_status = self_test_results = system_error = 0;
  bno.getSystemStatus(&system_status, &self_test_results, &system_error);

  /* Display the results in the Serial Monitor */
  Serial.println("");
  Serial.print("System Status: 0x");
  Serial.println(system_status, HEX);
  Serial.print("Self Test:     0x");
  Serial.println(self_test_results, HEX);
  Serial.print("System Error:  0x");
  Serial.println(system_error, HEX);
  Serial.println("");
  delay(500);
}

/**************************************************************************/
/*
    Display sensor calibration status
*/
/**************************************************************************/
void displayCalStatus(Adafruit_BNO055& bno)
{
  /* Get the four calibration values (0..3) */
  /* Any sensor data reporting 0 should be ignored, */
  /* 3 means 'fully calibrated" */
  uint8_t system, gyro, accel, mag;
  system = gyro = accel = mag = 0;
  bno.getCalibration(&system, &gyro, &accel, &mag);

  /* The data should be ignored until the system calibration is > 0 */
  if (!system)
  {
    Serial.print("! ");
  }

  /* Display the individual values */
  Serial.print("Sys:");
  Serial.print(system, DEC);
  Serial.print(" G:");
  Serial.print(gyro, DEC);
  Serial.print(" A:");
  Serial.print(accel, DEC);
  Serial.print(" M:");
  Serial.print(mag, DEC);
  Serial.println();
}

void displayOrientation(Adafruit_BNO055& bno, sensors_event_t& event){
  bno.getEvent(&event);

  Serial.print("X: ");
  Serial.print(event.orientation.x, 4);
  Serial.print("\tY: ");
  Serial.print(event.orientation.y, 4);
  Serial.print("\tZ: ");
  Serial.print(event.orientation.z, 4);
  Serial.print("\t\t");
}
void displayRawData(Adafruit_BNO055& bno){
  imu::Vector<3> acc = bno.getVector(Adafruit_BNO055::VECTOR_ACCELEROMETER);
  Serial.print("Acc [X,Y,Z]: [");
  Serial.print(acc.x());
  Serial.print(", ");
  Serial.print(acc.y());
  Serial.print(", ");
  Serial.print(acc.z());
  Serial.print("]\t\t");

  imu::Vector<3> mag = bno.getVector(Adafruit_BNO055::VECTOR_MAGNETOMETER);
  Serial.print("Mag [X,Y,Z]: [");
  Serial.print(mag.x());
  Serial.print(", ");
  Serial.print(mag.y());
  Serial.print(", ");
  Serial.print(mag.z());
  Serial.print("]\t\t");

  imu::Vector<3> gyr = bno.getVector(Adafruit_BNO055::VECTOR_GYROSCOPE);
  Serial.print("Gyr [X,Y,Z]: [");
  Serial.print(gyr.x());
  Serial.print(", ");
  Serial.print(gyr.y());
  Serial.print(", ");
  Serial.print(gyr.z());
  Serial.print("]\t\t");
}

void displayData(Adafruit_BNO055& bno, sensors_event_t& event){
  displayOrientation(bno, event);
  /* Optional: Display calibration status */
  displayCalStatus(bno);

  displayRawData(bno);
  
  /* Optional: Display sensor status (debug only) */
  //displaySensorStatus();

  Serial.println("");
}


String inputChoise(const String question){
  Serial.flush();
  Serial.println(question);
  Serial.flush();
  while (Serial.available() == 0) {}     //wait for data available
  String ans = Serial.readString();  //read until timeout
  ans.trim();
  return ans;
}