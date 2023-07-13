#Example code to fit the experimental data to a sine curve and evaluate the model

from utils import loadData as ld
from filtering import servoMagNoise 
from filtering import filtering as filter
from filtering import curvefitting as cf
import matplotlib.pyplot as plt


plt.rcParams["figure.figsize"] = [16, 8.0]
plt.rcParams["figure.autolayout"] = True
plt.rcParams['font.size'] = 14
plt.rcParams['svg.fonttype'] = 'none'

df_servo = ld.laodTestData("exampleData/servoDataStille.csv").dropna()
df_IMU = ld.laodTestData("exampleData/pureIMUDataStille.csv").dropna()

mag_earth = {'X': df_IMU['magX'].mean(), 'Y': df_IMU['magY'].mean(), 'Z': df_IMU['magZ'].mean()}
ServoMagDisturbance = servoMagNoise.servoMagNoise.estimate_from_dataset(mag_earth, df_servo)
ServoMagDisturbance.print_sine_params()

#remove earth's contribution to the magnetic field to plot the sinefit
df_mag_servo = df_servo.copy()
df_mag_servo['magX'] = df_mag_servo['magX']  - df_IMU['magX'].mean() 
df_mag_servo['magY'] = df_mag_servo['magY']  - df_IMU['magY'].mean() 
df_mag_servo['magZ'] = df_mag_servo['magZ']  - df_IMU['magZ'].mean() 
cf.plot_magsinefit(df_mag_servo, ServoMagDisturbance.get_params(), savefig=False)


# Filter and plot magnetometer measurements
df_est_earth = filter.feedforward_servo_noise(ServoMagDisturbance, df_servo)
df_earth_residuals = df_est_earth.copy()
df_earth_residuals['magX'] = df_earth_residuals['magX'] - mag_earth['X']
df_earth_residuals['magY'] = df_earth_residuals['magY'] - mag_earth['Y']
df_earth_residuals['magZ'] = df_earth_residuals['magZ'] - mag_earth['Z']


plt.rcParams["figure.figsize"] = [12, 4.0]
plt.rcParams["figure.autolayout"] = True
plt.rcParams['font.size'] = 18
filter.evaluate_model(ServoMagDisturbance, df_servo, mag_earth, "on training data")
plt.show()