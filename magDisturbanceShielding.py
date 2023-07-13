import pandas as pd
import numpy as np
from numpy import random
from analyseData import loadData as ld
from filtering import curvefitting as cf
from analyseData import analysisutilities as au
from filtering import servoMagNoise 
from filtering import filtering as filter
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
#plt.rcParams["figure.figsize"] = [16, 8.0]
#plt.rcParams["figure.autolayout"] = True
#plt.rcParams['font.size'] = 14

plt.rcParams["figure.figsize"] = [12, 10]
plt.rcParams['font.size'] = 20
plt.rcParams["legend.loc"] = 'upper right'
plt.rcParams['svg.fonttype'] = 'none'

def calc_earth_residuals(df_est_earth, mag_earth):
    df_res = df_est_earth.copy()
    df_res['magX'] = df_res['magX'] - mag_earth['X']
    df_res['magY'] = df_res['magY'] - mag_earth['Y']
    df_res['magZ'] = df_res['magZ'] - mag_earth['Z']

    return df_est_earth, df_res

# Load Experimental data

df_IMU0 = ld.laodTestData("Data/shieldingtestV2/pureIMUdata0.csv").dropna()
df_servo0 = ld.laodTestData("Data/shieldingtestV2/servoData0.csv").dropna()

df_IMU_distance = ld.laodTestData("Data/shieldingtestV2/pureIMUdataavstand.csv").dropna()
df_servo_distance = ld.laodTestData("Data/shieldingtestV2/servoDataavstand.csv").dropna()

df_IMU_distance2 = ld.laodTestData("Data/shieldingtestV2/pureIMUdataavstand2.csv").dropna()
df_servo_distance2 = ld.laodTestData("Data/shieldingtestV2/servoDataavstand2.csv").dropna()


df_IMU1 = ld.laodTestData("Data/shieldingtestV2/pureIMUdata1.csv").dropna()
df_servo1 = ld.laodTestData("Data/shieldingtestV2/servoData1.csv").dropna()

df_IMU3 = ld.laodTestData("Data/shieldingtestV2/pureIMUdata3.csv").dropna()
df_servo3 = ld.laodTestData("Data/shieldingtestV2/servoData3.csv").dropna()

df_IMU3r = ld.laodTestData("Data/shieldingtestV2/pureIMUdata3rundt.csv").dropna()
df_servo3r = ld.laodTestData("Data/shieldingtestV2/servoData3rundt.csv").dropna()

df_IMU5r = ld.laodTestData("Data/shieldingtestV2/pureIMUdata5rundt.csv").dropna()
df_servo5r = ld.laodTestData("Data/shieldingtestV2/servoData5rundt.csv").dropna()


# Plot IMU before and compare them
mag0 = pd.pivot_table(df_IMU0, index = ['time'], values= ['magX', 'magY', 'magZ'])
mag1 = pd.pivot_table(df_IMU1, index = ['time'], values= ['magX', 'magY', 'magZ'])
mag3 = pd.pivot_table(df_IMU3, index = ['time'], values= ['magX', 'magY', 'magZ'])
mag3r = pd.pivot_table(df_IMU3r, index = ['time'], values= ['magX', 'magY', 'magZ'])
mag5r = pd.pivot_table(df_IMU5r, index = ['time'], values= ['magX', 'magY', 'magZ'])

maga = pd.pivot_table(df_IMU_distance, index = ['time'], values= ['magX', 'magY', 'magZ'])
maga2 = pd.pivot_table(df_IMU_distance2, index = ['time'], values= ['magX', 'magY', 'magZ'])


fig, axs = plt.subplots(3,1)
mag0['magX'].plot(ax=axs[0])
mag1['magX'].plot(ax=axs[0])
mag3['magX'].plot(ax=axs[0])
mag3r['magX'].plot(ax=axs[0])
mag5r['magX'].plot(ax=axs[0])
axs[0].set_ylabel(r'x-axis [$\mu$T]')
axs[0].set_xlabel('')

mag0['magY'].plot(ax=axs[1])
mag1['magY'].plot(ax=axs[1])
mag3['magY'].plot(ax=axs[1])
mag3r['magY'].plot(ax=axs[1])
mag5r['magY'].plot(ax=axs[1])
axs[1].set_ylabel(r'y-axis [$\mu$T]')
axs[1].set_xlabel('')

mag0['magZ'].plot(ax=axs[2])
mag1['magZ'].plot(ax=axs[2])
mag3['magZ'].plot(ax=axs[2])
mag3r['magZ'].plot(ax=axs[2])
mag5r['magZ'].plot(ax=axs[2])
axs[2].set_ylabel(r'z-axis [$\mu$T]')
axs[2].set_xlabel('Time [s]')


fig.legend(['without shielding', '0.1 mm shielding', '0.3 mm shielding', ' 0.3 mm + around', '0.5 mm + around'])
plt.suptitle('Initially measured magnetic field')
#plt.savefig("figuresAndResults/shieldingtest/pureIMU.svg", format = 'svg')
#plt.savefig("figuresAndResults/shieldingtest/pureIMU.png", format = 'png')
plt.plot()

fig, axs = plt.subplots(3,1)
mag0['magX'].plot(ax=axs[0])
maga['magX'].plot(ax=axs[0])
maga2['magX'].plot(ax=axs[0])
mag5r['magX'].plot(ax=axs[0])
axs[0].set_ylabel(r'x-axis [$\mu$T]')
axs[0].set_xlabel('')

mag0['magY'].plot(ax=axs[1])
maga['magY'].plot(ax=axs[1])
maga2['magY'].plot(ax=axs[1])
mag5r['magY'].plot(ax=axs[1])
axs[1].set_ylabel(r'y-axis [$\mu$T]')
axs[1].set_xlabel('')

mag0['magZ'].plot(ax=axs[2])
maga['magZ'].plot(ax=axs[2])
maga2['magZ'].plot(ax=axs[2])
mag5r['magZ'].plot(ax=axs[2])
axs[2].set_ylabel(r'z-axis [$\mu$T]')
fig.legend(['normal', '10 mm distance', '20 mm distance',  '0.5 mm + around'])
plt.suptitle('Initially measured magnetic field')
#plt.savefig("figuresAndResults/shieldingtest/pureIMUDIstance.svg", format = 'svg')
#plt.savefig("figuresAndResults/shieldingtest/pureIMUDIstance.png", format = 'png')
plt.plot()


mag_earth0 = {'X': df_IMU0['magX'].mean(), 'Y': df_IMU0['magY'].mean(), 'Z': df_IMU0['magZ'].mean()}
ServoMagDisturbance0 = servoMagNoise.servoMagNoise.estimate_from_dataset(mag_earth0, df_servo0)
print(".0 mm test")
ServoMagDisturbance0.print_sine_params()

mag_eartha = {'X': df_IMU_distance['magX'].mean(), 'Y': df_IMU_distance['magY'].mean(), 'Z': df_IMU_distance['magZ'].mean()}
ServoMagDisturbancea = servoMagNoise.servoMagNoise.estimate_from_dataset(mag_eartha, df_servo_distance)
print("10 mm distance test")
ServoMagDisturbancea.print_sine_params()

mag_eartha2 = {'X': df_IMU_distance2['magX'].mean(), 'Y': df_IMU_distance2['magY'].mean(), 'Z': df_IMU_distance2['magZ'].mean()}
ServoMagDisturbancea2 = servoMagNoise.servoMagNoise.estimate_from_dataset(mag_eartha2, df_servo_distance2)
print("20 mm distance test")
ServoMagDisturbancea2.print_sine_params()


mag_earth1 = {'X': df_IMU1['magX'].mean(), 'Y': df_IMU1['magY'].mean(), 'Z': df_IMU1['magZ'].mean()}
ServoMagDisturbance1 = servoMagNoise.servoMagNoise.estimate_from_dataset(mag_earth1, df_servo1)
print(".1 mm test")
ServoMagDisturbance1.print_sine_params()


mag_earth3 = {'X': df_IMU3['magX'].mean(), 'Y': df_IMU3['magY'].mean(), 'Z': df_IMU3['magZ'].mean()}
ServoMagDisturbance3 = servoMagNoise.servoMagNoise.estimate_from_dataset(mag_earth3, df_servo3)
print(".3 mm test")
ServoMagDisturbance3.print_sine_params()


mag_earth3r = {'X': df_IMU3r['magX'].mean(), 'Y': df_IMU3r['magY'].mean(), 'Z': df_IMU3r['magZ'].mean()}
ServoMagDisturbance3r = servoMagNoise.servoMagNoise.estimate_from_dataset(mag_earth3r, df_servo3r)
print(".3 mm + around test")
ServoMagDisturbance3r.print_sine_params()

mag_earth5r = {'X': df_IMU5r['magX'].mean(), 'Y': df_IMU5r['magY'].mean(), 'Z': df_IMU5r['magZ'].mean()}
ServoMagDisturbance5r = servoMagNoise.servoMagNoise.estimate_from_dataset(mag_earth5r, df_servo5r)
print(".5 mm + around test")
ServoMagDisturbance5r.print_sine_params()

# Plot performance of servo motor estimate
B_servo0 = df_servo0.copy()
B_servo0['magX'] = B_servo0['magX'].copy() - df_IMU0['magX'].mean()
B_servo0['magY'] = B_servo0['magY'].copy() - df_IMU0['magY'].mean()
B_servo0['magZ'] = B_servo0['magZ'].copy() - df_IMU0['magZ'].mean()

B_servoa = df_servo_distance.copy()
B_servoa['magX'] = B_servoa['magX'].copy() - df_IMU_distance['magX'].mean()
B_servoa['magY'] = B_servoa['magY'].copy() - df_IMU_distance['magY'].mean()
B_servoa['magZ'] = B_servoa['magZ'].copy() - df_IMU_distance['magZ'].mean()

B_servoa2 = df_servo_distance2.copy()
B_servoa2['magX'] = B_servoa2['magX'].copy() - df_IMU_distance2['magX'].mean()
B_servoa2['magY'] = B_servoa2['magY'].copy() - df_IMU_distance2['magY'].mean()
B_servoa2['magZ'] = B_servoa2['magZ'].copy() - df_IMU_distance2['magZ'].mean()

B_servo1 = df_servo1.copy()
B_servo1['magX'] = B_servo1['magX'].copy() - df_IMU1['magX'].mean()
B_servo1['magY'] = B_servo1['magY'].copy() - df_IMU1['magY'].mean()
B_servo1['magZ'] = B_servo1['magZ'].copy() - df_IMU1['magZ'].mean()

B_servo3 = df_servo3.copy()
B_servo3['magX'] = B_servo3['magX'].copy() - df_IMU3['magX'].mean()
B_servo3['magY'] = B_servo3['magY'].copy() - df_IMU3['magY'].mean()
B_servo3['magZ'] = B_servo3['magZ'].copy() - df_IMU3['magZ'].mean()

B_servo3r = df_servo3r.copy()
B_servo3r['magX'] = B_servo3r['magX'].copy() - df_IMU3r['magX'].mean()
B_servo3r['magY'] = B_servo3r['magY'].copy() - df_IMU3r['magY'].mean()
B_servo3r['magZ'] = B_servo3r['magZ'].copy() - df_IMU3r['magZ'].mean()

B_servo5r = df_servo5r.copy()
B_servo5r['magX'] = B_servo5r['magX'].copy() - df_IMU5r['magX'].mean()
B_servo5r['magY'] = B_servo5r['magY'].copy() - df_IMU5r['magY'].mean()
B_servo5r['magZ'] = B_servo5r['magZ'].copy() - df_IMU5r['magZ'].mean()

B_est_servo0 =  ServoMagDisturbance0.get_disturbance_as_timeseries(df_servo0)
B_est_servoa =  ServoMagDisturbancea.get_disturbance_as_timeseries(df_servo_distance)
B_est_servoa2 =  ServoMagDisturbancea2.get_disturbance_as_timeseries(df_servo_distance2)
B_est_servo1 =  ServoMagDisturbance1.get_disturbance_as_timeseries(df_servo1)
B_est_servo3 =  ServoMagDisturbance3.get_disturbance_as_timeseries(df_servo3)
B_est_servo3r = ServoMagDisturbance3r.get_disturbance_as_timeseries(df_servo3r)
B_est_servo5r = ServoMagDisturbance5r.get_disturbance_as_timeseries(df_servo5r)

df_res0 , df_std0 , df_rmse0    = filter.calc_residuals(B_servo0 , B_est_servo0 )
df_resa , df_stda , df_rmsea    = filter.calc_residuals(B_servoa , B_est_servoa )
df_resa2 , df_stda2 , df_rmsea2 = filter.calc_residuals(B_servoa2 , B_est_servoa2)
df_res1 , df_std1 , df_rmse1    = filter.calc_residuals(B_servo1 , B_est_servo1 )
df_res3 , df_std3 , df_rmse3    = filter.calc_residuals(B_servo3 , B_est_servo3 )
df_res3r, df_std3r, df_rmse3r   = filter.calc_residuals(B_servo3r, B_est_servo3r)
df_res5r, df_std5r, df_rmse5r   = filter.calc_residuals(B_servo5r, B_est_servo5r)

filter.evaluate_model(ServoMagDisturbance0, df_servo0, mag_earth0, "0.0 mm shielding sheet", plot=False)
filter.evaluate_model(ServoMagDisturbance1, df_servo1, mag_earth1, "0.1 mm shielding sheet", plot=False)
filter.evaluate_model(ServoMagDisturbance3, df_servo3, mag_earth3, "0.3 mm shielding sheet", plot=False)
filter.evaluate_model(ServoMagDisturbance3r, df_servo3r, mag_earth3r, "0.3 mm shielding sheet and 0.1 mm around", plot = False)
filter.evaluate_model(ServoMagDisturbance5r, df_servo5r, mag_earth5r, "0.5 mm shielding sheet and 0.1 mm around", plot = False)
filter.evaluate_model(ServoMagDisturbancea, df_servo_distance, mag_eartha, "10 mm distance between motor and IMU", plot=False)
filter.evaluate_model(ServoMagDisturbancea2, df_servo_distance2, mag_eartha2, "20 mm distance between motor and IMU", plot=False)



fig, ax = plt.subplots(3,1)
fig.suptitle("Estimation residuals")
ax[0].scatter(df_res0['time'], df_res0['magX'].tolist(), s = 5)
#ax[0].scatter(df_res1['time'], df_res1['magX'].tolist(), s = 5)
ax[0].scatter(df_res3['time'], df_res3['magX'].tolist(), s = 5)
ax[0].scatter(df_res3r['time'], df_res3r['magX'].tolist(), s = 5)
ax[0].scatter(df_res5r['time'], df_res5r['magX'].tolist(), s = 5)
ax[0].set_ylabel(r'x-axis [$\mu$T]')


ax[1].scatter(df_res0['time'], df_res0['magY'].tolist(), s = 5)
#ax[1].scatter(df_res1['time'], df_res1['magY'].tolist(), s = 5)
ax[1].scatter(df_res3['time'], df_res3['magY'].tolist(), s = 5)
ax[1].scatter(df_res3r['time'], df_res3r['magY'].tolist(), s = 5)
ax[1].scatter(df_res5r['time'], df_res5r['magY'].tolist(), s = 5)
ax[1].set_ylabel(r'y-axis [$\mu$T]')


ax[2].scatter(df_res0['time'], df_res0['magZ'].tolist(), s = 5)
#ax[2].scatter(df_res1['time'], df_res1['magZ'].tolist(), s = 5)
ax[2].scatter(df_res3['time'], df_res3['magZ'].tolist(), s = 5)
ax[2].scatter(df_res3r['time'], df_res3r['magZ'].tolist(), s = 5)
ax[2].scatter(df_res5r['time'], df_res5r['magZ'].tolist(), s = 5)
ax[2].set_ylabel(r'z-axis [$\mu$T]')
      
ax[2].set_xlabel('time [s]')
fig.legend(['without shielding', '0.3 mm shielding', ' 0.3 mm + around', '0.5 mm + around'])
#plt.savefig("figuresAndResults/shieldingtest/MotorResiduals.svg", format = 'svg')
#plt.savefig("figuresAndResults/shieldingtest/MotorResiduals.png", format = 'png')


fig, ax = plt.subplots(3,1)
fig.suptitle("Estimation residuals")
ax[0].scatter(df_res0['time'], df_res0['magX'].tolist(), s = 5)
ax[0].scatter(df_resa['time'], df_resa['magX'].tolist(), s = 5)
ax[0].scatter(df_resa2['time'], df_resa2['magX'].tolist(), s = 5)
ax[0].set_ylabel(r'x-axis [$\mu$T]')


ax[1].scatter(df_res0['time'], df_res0['magY'].tolist(), s = 5)
ax[1].scatter(df_resa['time'], df_resa['magY'].tolist(), s = 5)
ax[1].scatter(df_resa2['time'], df_resa2['magY'].tolist(), s = 5)
ax[1].set_ylabel(r'y-axis [$\mu$T]')


ax[2].scatter(df_res0['time'], df_res0['magZ'].tolist(), s = 5)
ax[2].scatter(df_resa['time'], df_resa['magZ'].tolist(), s = 5)
ax[2].scatter(df_resa2['time'], df_resa2['magZ'].tolist(), s = 5)
ax[2].set_ylabel(r'z-axis [$\mu$T]')
      
ax[2].set_xlabel('time [s]')
fig.legend(['Normal', '10 mm distance', '20 mm distance'])
#plt.savefig("figuresAndResults/shieldingtest/MotorResidualsdistance.svg", format = 'svg')
#plt.savefig("figuresAndResults/shieldingtest/MotorResidualsdistance.png", format = 'png')




#filter.plot_servo_motor_field(B_servo1, B_est_servo1,"Estimated servo motor field with 0.1mm shielding.", savefig=True, directory="figuresAndResults//shieldingtest//shielding1")

# Plot/ evaluate servo model

#filter.evaluate_model(ServoMagDisturbance1, df_servo1, mag_earth1, "on training data with 0.1 mm shielding")

# plot earth residuals when IMU0 is defined as correct
#estimate earth's magnetic filed
#df_est_earth0 = filter.feedforward_servo_noise(ServoMagDisturbance0, df_servo0)
#df_est_earth1 = filter.feedforward_servo_noise(ServoMagDisturbance1, df_servo1)
#df_est_earth3 = filter.feedforward_servo_noise(ServoMagDisturbance3, df_servo3)
#df_est_earth3r = filter.feedforward_servo_noise(ServoMagDisturbance3r, df_servo3r)
#df_est_earth5r = filter.feedforward_servo_noise(ServoMagDisturbance5r, df_servo5r)
#filter.plot_residuals(df_earth_residuals, "Estimation error of earth's magnetic field")


#PLOT ESTIMATED FIELD EXPECT .1 MM SHIELDING SHEET

fig, axs = plt.subplots(3,1)
B_est_servo0[['servoPos', 'magX']].set_index('servoPos').plot(ax=axs[0], legend = False)
#B_est_servo3[['servoPos', 'magX']].set_index('servoPos').plot(ax=axs[0], legend = False)
#B_est_servo3r[['servoPos', 'magX']].set_index('servoPos').plot(ax=axs[0], legend = False)
B_est_servo5r[['servoPos', 'magX']].set_index('servoPos').plot(ax=axs[0], legend = False)
B_est_servoa[['servoPos', 'magX']].set_index('servoPos').plot(ax=axs[0], legend = False) 
B_est_servoa2[['servoPos', 'magX']].set_index('servoPos').plot(ax=axs[0], legend = False)
axs[0].set_ylabel(r'x-axis [$\mu$T]')
axs[0].set_xlabel('')

B_est_servo0[['servoPos', 'magY']].set_index('servoPos').plot(ax=axs[1], legend = False)
#B_est_servo3[['servoPos', 'magY']].set_index('servoPos').plot(ax=axs[1], legend = False)
#B_est_servo3r[['servoPos', 'magY']].set_index('servoPos').plot(ax=axs[1], legend = False)
B_est_servo5r[['servoPos', 'magY']].set_index('servoPos').plot(ax=axs[1], legend = False)
B_est_servoa[['servoPos', 'magY']].set_index('servoPos').plot(ax=axs[1], legend = False) 
B_est_servoa2[['servoPos', 'magY']].set_index('servoPos').plot(ax=axs[1], legend = False)
axs[1].set_ylabel(r'y-axis [$\mu$T]')
axs[1].set_xlabel('')

B_est_servo0[['servoPos', 'magZ']].set_index('servoPos').plot(ax=axs[2], legend = False)
#B_est_servo3[['servoPos', 'magZ']].set_index('servoPos').plot(ax=axs[2], legend = False)
#B_est_servo3r[['servoPos', 'magZ']].set_index('servoPos').plot(ax=axs[2], legend = False)
B_est_servo5r[['servoPos', 'magZ']].set_index('servoPos').plot(ax=axs[2], legend = False)
B_est_servoa[['servoPos', 'magZ']].set_index('servoPos').plot(ax=axs[2], legend = False) 
B_est_servoa2[['servoPos', 'magZ']].set_index('servoPos').plot(ax=axs[2], legend = False)
axs[2].set_ylabel(r'z-axis [$\mu$T]')
axs[2].set_xlabel(r'Servo shaft position [$\degree$]')

#fig.legend(['without shielding', '0.3 mm shielding', ' 0.3 mm + around', '0.5 mm + around', '10 mm distance', '20 mm distance'])
fig.legend(['without shielding', '0.5 mm + around', '10 mm distance', '20 mm distance'])

fig.suptitle("Estimated magnetic disturbance with shielding techniques")
#plt.savefig("figuresAndResults/shieldingtest/estimatedServoField.svg", format = 'svg')
#plt.savefig("figuresAndResults/shieldingtest/estimatedServoField.png", format = 'png')
#

plt.show()