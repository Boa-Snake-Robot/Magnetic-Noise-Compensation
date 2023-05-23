# Magnetic-Noise-Compensation-Master
Repository dedicated to Mari Linnerud's Masters thesis work. 

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
3. Fit a data set to a sine

### plotting
Module with functions to streamline data plots used during analysis.

### simulation
Still in work.
Contain modules to simulate the IMU noise and servo motor disturbance.

## Main files
The main files used during analysis is the following
- ARMA.ipynb: used to analyse initial magentometer noise
- analyseIMUvsServo.ipynb: used to analyse the effects the EM-field disturbance from the servo motor has on the IMU measurements
- estimateServoMagneticField.ipynb: used to model the generated EM field from the servo motor by fitting the datapoints to a sine
- magDisturbanceBrainstorming.py: In work. Used to brainstorm different counteractive methods of the EM disturbance from the servo motor