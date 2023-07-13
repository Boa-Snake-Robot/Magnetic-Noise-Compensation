# Magnetic-Noise-Compensation-Master
Repository dedicated to Mari Linnerud's Masters thesis work. 

This repository is used to 
- help analyse the noise on the BNO-055 IMU when under disturbance from the generated electromagnetic field from the servo motors of the BOA snake robot
- model the noise

The code requires the csv files or dataframes with the following columns, separated by ',', and not ', ':
time, magX, magY, magZ, accX, accY, accZ, gyrX, gyrY, gyrZ

## Folder structure
### experiments
The experiments folder contains the scripts used to sample data during the experiments.

### utils
Contains utilities to load the experimental data


### filtering
Module containing the methods used to filter the magnetometer measurements to improve the heading estimates. EKF.py contains the kalman filter. servoMagNoise.py estimates the magnetic cross-talk.  filtering.py contains the code to correct the magnetometer measurements using the predictor found using servoMagNoise.py

## Main files
The main files used during analysis is the following
- estimateServoMagneticField.ipynb: used to model the generated EM field from the servo motor by fitting the datapoints to a sine
- magDisturbanceModelEvaluation.py: Used to evaluate the cross-talk model