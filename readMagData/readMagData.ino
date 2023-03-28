#include "displayData.h"
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <TimeLib.h>


//todo:
/*Implement absolute value position and set zero angle to rom cmd */

Adafruit_BNO055 bno = Adafruit_BNO055(55, 0x28);
const int sampleRate = 100; //100Hz is BNO055 sample rate


const int testTime = 60;

const int numSamples = sampleRate*testTime;
const int bufferLen = numSamples;

/*Assign buffers*/
imu::Vector<3> magBuffer[bufferLen];
double imuTimestamps[bufferLen];

void printData(){
  Serial.println();
  Serial.println("Sending magBuffer [X,Y,Z]:");
  for(int i = 1; i < bufferLen; i++){
    imu::Vector<3> mag = magBuffer[i];
    Serial.print(mag.x());
    Serial.print(", ");
    Serial.print(mag.y());
    Serial.print(", ");
    Serial.print(mag.z());
    Serial.println();

  }

  Serial.println();
  Serial.println("Sending imuTimestamps:");
  for(int i = 0; i < bufferLen; i++){
    Serial.print(imuTimestamps[i], 4);
    Serial.print(", ");
  }
  Serial.println();
  
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
  displaySensorStatus(bno);

  /* Optional: Display current calibration status */
  displayCalStatus(bno);

  bno.setExtCrystalUse(true);

  Serial.println("Setup complete");

}

void loop(void)
{
    unsigned long start = millis();
    unsigned long last_sample = start;
    unsigned long start_time = last_sample;
    unsigned long last_round = start + 3000; 
    Serial.print("Bufferlen");
    Serial.println("Test start");
    
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
    

    /*PRINT DATA TO SERIAL MONITOR*/
    Serial.print("Test took ");
    Serial.print(millis() - start_time);
    Serial.println(" ms");
    
    printData();
  
}

    
