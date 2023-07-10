import pandas as pd
import numpy as np
from numpy import random
from analyseData import loadData as ld
from analyseData import curvefitting as cf
from analyseData import analysisutilities as au
from filtering import noise 
from filtering import filtering as filter
import matplotlib.pyplot as plt

plt.rcParams["figure.figsize"] = [16, 8.0]
plt.rcParams["figure.autolayout"] = True
plt.rcParams['font.size'] = 14



df_IMU = ld.laodTestData("Data/projectThesisTest1/newCurrentMeas/woLoad/pureIMUdata2023-05-16 09%3A22%3A14.928527.csv").dropna()

df_servo = ld.laodTestData("Data/projectThesisTest1/newCurrentMeas/woLoad/servoData2023-05-16 09%3A22%3A14.928527.csv").dropna()
df_servo_load = ld.laodTestData("Data/projectThesisTest1/newCurrentMeas/wLoad/servoData2023-05-16 08%3A46%3A23.906719.csv").dropna()
df_IMU_load = ld.laodTestData("Data/projectThesisTest1/newCurrentMeas/wLoad/pureIMUdata2023-05-16 08%3A46%3A23.906719.csv").dropna()

mag_earth = {'X': df_IMU['magX'].mean(), 'Y': df_IMU['magY'].mean(), 'Z': df_IMU['magZ'].mean()}
mag_earth_load = {'X': df_IMU_load['magX'].mean(), 'Y': df_IMU_load['magY'].mean(), 'Z': df_IMU_load['magZ'].mean()}
ServoMagDisturbance = noise.servoMagNoise.estimate_from_dataset(mag_earth, df_servo)
ServoMagDisturbance.print_sine_params()

# Filter and plot magnetometer measurements
df_est_earth = filter.filter_servo_noise(ServoMagDisturbance, df_servo)
df_earth_residuals = df_est_earth.copy()
df_earth_residuals['magX'] = df_earth_residuals['magX'] - mag_earth['X']
df_earth_residuals['magY'] = df_earth_residuals['magY'] - mag_earth['Y']
df_earth_residuals['magZ'] = df_earth_residuals['magZ'] - mag_earth['Z']


#plot_error_and_estimates(df_est_earth, abs(df_est_residuals), "Filtered magnetic field")
#plot_residuals(df_earth_residuals, "Estimation error of earth's magnetic field")
#plot_servo_motor_field(B_servo, B_est_servo, res)
# Plot/ evaluate servo model

plt.rcParams["figure.figsize"] = [12, 4.0]
plt.rcParams["figure.autolayout"] = True
plt.rcParams['font.size'] = 18
filter.evaluate_model(ServoMagDisturbance, df_servo, mag_earth, "on training data")
filter.evaluate_model(ServoMagDisturbance, df_servo_load, mag_earth_load, "on validation data")
plt.show()
    




#B_est_servo = B_est_servo.sort_values('servoCur')    
#B_est_servo[['servoVel', 'servoCur']].set_index('servoCur').plot()
#norm = np.array([])
#for index, row in B_est_servo.iterrows():
#    norm = np.append(norm, np.linalg.norm(row[['magX', 'magY', 'magZ']]))
#B_servo = B_servo.sort_values('time')
#B_servo[['magX', 'magY', 'magZ', 'servoCur']].set_index('servoCur').plot(subplots=True)
#plt.figure()
#plt.scatter(B_servo['servoCur'], norm)
#plt.show()

