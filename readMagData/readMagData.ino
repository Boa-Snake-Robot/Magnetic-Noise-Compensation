#include "displayData.h"
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <TimeLib.h>


//todo:
/*Implement absolute value position and set zero angle to rom cmd */

Adafruit_BNO055 bno = Adafruit_BNO055(55, 0x28);
const int sampleRate = 100; //100Hz is BNO055 sample rate


const int testTime = 30;

const int numSamples = sampleRate*testTime;
const int bufferLen = numSamples;

/*Assign buffers*/
imu::Vector<3> magBuffer[bufferLen];
double imuTimestamps[bufferLen];
unsigned long start = millis();

void printData(){
  Serial.println();
  //Serial.println("Sending magData [X,Y,Z, time]:");
  for(int i = 1; i < bufferLen; i++){
    imu::Vector<3> mag = magBuffer[i];
    Serial.print(mag.x());
    Serial.print(", ");
    Serial.print(mag.y());
    Serial.print(", ");
    Serial.print(mag.z());
    Serial.print(", ");
    Serial.print(imuTimestamps[i], 4);
    Serial.println();

  }

  
  
}

void setup(void)
{
  Serial.begin(9600);
  while (!Serial);
  Serial.println("Testing Servo and IMU"); 

  /* Initialise the sensor */
  if(!bno.begin())
  {
    Serial.print("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
    while(1);
  }
  
  /* Display some basic information on this sensor */
  displaySensorDetails(bno);

  /* Optional: Display current status */
  //displaySensorStatus(bno);

  /* Optional: Display current calibration status */
  //displayCalStatus(bno);

  bno.setExtCrystalUse(true);
  String isCal = "n";
  while(isCal != "y"){
    displaySensorStatus(bno);
    displayCalStatus(bno);
    Serial.println("Is calibrated?(y/n):");
    while (Serial.available() == 0) {}     //wait for data available
    isCal = Serial.readString();  //read until timeout
    isCal.trim();                        // remove any \r \n whitespace at the end of the String
  }

  Serial.println("Setup complete");
  start = millis();

}

void loop(void)
{     
  unsigned long start_loop = millis();
  unsigned long last_sample = start_loop;
  unsigned long start_time = last_sample;
  unsigned long last_round = start_loop + 3000; 
  //Serial.print("Bufferlen");
  //Serial.println("Test start");
  int i = 0;
  while (i < bufferLen){
    
    /* Sample data */
    unsigned long newTime = millis();
    unsigned long diff = newTime - last_sample;

    if(diff > (1000/sampleRate)){
      magBuffer[i] = bno.getVector(Adafruit_BNO055::VECTOR_MAGNETOMETER);
      last_sample = millis();
      imuTimestamps[i] = (double)(last_sample - start)/1000;
      i++;
      }        
    }
  
  printData();
  
  
}

    
