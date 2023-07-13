import pandas as pd
import numpy as np
from numpy import random
from analyseData import loadData as ld
from analyseData import analysisutilities as au
from filtering import servoMagNoise 
from filtering import filtering as filter
import matplotlib.pyplot as plt

plt.rcParams["figure.figsize"] = [16, 8.0]
plt.rcParams["figure.autolayout"] = True
plt.rcParams['font.size'] = 14
plt.rcParams['svg.fonttype'] = 'none'



df_IMU = ld.laodTestData("Data/projectThesisTest1/newCurrentMeas/woLoad/pureIMUdata2023-05-16 09%3A22%3A14.928527.csv").dropna()

df_servo = ld.laodTestData("Data/projectThesisTest1/newCurrentMeas/woLoad/servoData2023-05-16 09%3A22%3A14.928527.csv").dropna()
df_servo_load = ld.laodTestData("Data/projectThesisTest1/newCurrentMeas/wLoad/servoData2023-05-16 08%3A46%3A23.906719.csv").dropna()
df_IMU_load = ld.laodTestData("Data/projectThesisTest1/newCurrentMeas/wLoad/pureIMUdata2023-05-16 08%3A46%3A23.906719.csv").dropna()

mag_earth = {'X': df_IMU['magX'].mean(), 'Y': df_IMU['magY'].mean(), 'Z': df_IMU['magZ'].mean()}
mag_earth_load = {'X': df_IMU_load['magX'].mean(), 'Y': df_IMU_load['magY'].mean(), 'Z': df_IMU_load['magZ'].mean()}
ServoMagDisturbance = servoMagNoise.servoMagNoise.estimate_from_dataset(mag_earth, df_servo)
ServoMagDisturbance.print_sine_params()

# Filter and plot magnetometer measurements
df_est_earth = filter.feedforward_servo_noise(ServoMagDisturbance, df_servo)
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
    
plt.rcParams["figure.figsize"] = [10, 6.0]
plt.rcParams["figure.autolayout"] = True
plt.rcParams['font.size'] = 18
plt.rcParams['svg.fonttype'] = 'none'

df_est = ServoMagDisturbance.get_disturbance_as_timeseries(df_servo)
df_true = df_servo[['time', 'servoPos', 'servoVel', 'servoCur', 'magX', 'magY', 'magZ']].copy()
df_true['magX'] = df_true['magX']  - mag_earth['X']
df_true['magY'] = df_true['magY']  - mag_earth['Y']
df_true['magZ'] = df_true['magZ']  - mag_earth['Z']

df_error, df_std, df_rmse = filter.calc_residuals(df_true, df_est)

fig, ax = plt.subplots(2,2)
ax[0][0].plot(df_error['time'], df_error['magX'].tolist(), color = "b")
ax[0][1].plot(df_error['time'], df_error['magY'].tolist(), color = "g")
ax[1][0].plot(df_servo['time'], df_servo['magX'].tolist(), color = "r")
ax[1][1].plot(df_servo['time'], df_servo['magY'].tolist(), color = "m")

ax[1][0].set_xlabel('time [s]')
ax[1][1].set_xlabel('time [s]')
ax[0][0].set_ylabel(r'$\mu$T')
ax[1][0].set_ylabel(r'$\mu$T')
#ax[2].set_ylabel(r'$\mu$T')

fig.legend([r'$x$-axis model residual', r'$y$-axis model residual', r'$x$-axis magnetic cross-talk',r'$y$-axis magnetic cross-talk'])

plt.savefig("figuresAndResults/filterservofield/eddy.svg", format='svg')

plt.show()