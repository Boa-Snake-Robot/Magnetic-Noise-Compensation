# Magnetic-Noise-Compensation
Repository dedicated to Mari Linnerud's Masters thesis work. 

This repository contains example code for the proposed improved heading estimation technique in the Master's thesis

The code requires the csv files or dataframes from experimental data with the following columns, separated by `','`, and not `', '`:
`[time, magX, magY, magZ, accX, accY, accZ, gyrX, gyrY, gyrZ]`.

## Folder structure
### experiments
The `experiments` folder contains the scripts used to sample data during the experiments, using the Dynamixel XH540-V150R BLDC servo motor from Robotis, and the BNO-055 smart sensor IMU on a breakoutboard from Adafruit.

### utils
Utilities to load the experimental data

### filtering
Module containing the methods used to filter the magnetometer measurements to improve the heading estimates. 
- `curvefitting.py` fits a dataset to a sine curve
- `servoMagNoise.py` estimates the magnetic cross-talk.  
- `filtering.py` contains the code to correct the magnetometer measurements using the predictor found using `servoMagNoise.py` 
- `KF.py` contains the kalman filter. One can choose to remove the adaptive magnetic disturbance rejection from the Kalman filter by setting the parameter `MDR_on = False`


## Example files
The following files shows examples on how to use the filtering module. The example data used can be found in the `exampleData` folder, whcih were acquired using `servoTest.py` in the `experiments` folder. 
- `modelEvaluation.py`: model the generated EM field from the servo motor by fitting the datapoints to a sine, and evaluate the cross-talk model
- `KFtest.py`: Example of correcting the disturbed magnetometer measurements using a cross-talk model with the `servoMagNoise` class, and how to use the adaptive Kalman filter with magnetic disturbance rejection.
