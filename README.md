# Magnetic-Noise-Compensation-Master
Repository dedicated to Mari Linnerud's Masters thesis work.
This branch contains all the code using used for the work, including plotting and brainstorming scripts. The main branch is a destilled version of this branch, containing only the algorithms relevant to the proposed heading estimation technique and curvefitting of the magnetic cross-talk. 

This repository is used to 
- help analyse the noise on the BNO-055 IMU when under disturbance from the generated electromagnetic field from the servo motors of the BOA snake robot
- model the noise
- simulate it to investigate sensor fusion methods to restore heading and magnetometer estimates during actuation of the servo motors.

## Folder structure
### experiments
The experiments folder contains the scripts used to sample data during the experiments.

### analyseData
Contains modules to 
1. Load the data from the csv files generated during the servo motor experiments
2. Utilities for analysis of the data

### plotting
Module with functions to streamline data plots used during analysis.

### filtering
Module containing the methods used to filter the magnetometer measurements to improve the heading estimates. KF.py contains the kalman filter. curvefitting.py contains the code to fit a sine to magnetometer data, servoMagNoise.py estimates the magnetic cross-talk.  filtering.py contains the code to correct the magnetometer measurements using the predictor found using servoMagNoise.py

## Main files
The main files used during analysis is the following
- ARMA.py: used to analyse initial magentometer noise
- analyseIMUvsServo.ipynb: used to analyse the effects the EM-field disturbance from the servo motor has on the IMU measurements
- estimateServoMagneticField.ipynb: used to model the generated EM field from the servo motor by fitting the datapoints to a sine
- magDisturbanceModelEvaluation.py: Used to evaluate the cross-talk model
- magDisturvanceShielding.py: Used to evaluate the effect of shielding
- KFtest.py: tests the kalman filter on IMU and servo data