import pandas as pd
import numpy as np
from analyseData import loadData as ld
from analyseData import curvefitting as cf
from analyseData import analysisutilities as au
from simulation import noise as noise
import matplotlib.pyplot as plt

def filter_servonoise(disturbance: noise.servoMagNoise, df_noisy_readings: pd.DataFrame):
    temp = {'X': [], 'Y': [], 'Z': []}
    for pos in servo_pos:
        temp['X'] = np.append(temp['X'], disturbance.get_mag_disturbance(pos)[0])
        temp['Y'] = np.append(temp['Y'], disturbance.get_mag_disturbance(pos)[1])
        temp['Z'] = np.append(temp['Z'], disturbance.get_mag_disturbance(pos)[2])
        

    est_mag_X = (df_noisy_readings['magX'].copy() - temp['X'].tolist())
    est_mag_Y = (df_noisy_readings['magY'].copy() - temp['Y'].tolist())
    est_mag_Z = (df_noisy_readings['magZ'].copy() - temp['Z'].tolist())


    df_est_mag = pd.DataFrame()
    df_est_mag['time'] = time.tolist()
    df_est_mag['X'] = est_mag_X
    df_est_mag['Y'] = est_mag_Y
    df_est_mag['Z'] = est_mag_Z
    return df_est_mag


def plot(df_estimate, df_error):
    plt.rcParams["figure.figsize"] = [12.50, 6.0]
    plt.rcParams["figure.autolayout"] = True
    plt.rcParams['font.size'] = 14
    fig, ax = plt.subplots(2,2)

    ax[0][0].plot(df_error['time'], df_error['X'].tolist())
    ax[0][0].plot(df_error['time'], df_error['Y'].tolist())
    ax[0][0].plot(df_error['time'], df_error['Z'].tolist())
    ax[0][0].legend(['error X', 'error Y', 'error Z'])

    ax[0][1].axhline(y = df_IMU['magX'].mean(), color = 'r')
    ax[0][1].plot(df_estimate['time'], df_estimate['X'])
    ax[0][1].legend(['truth along X axis', 'estimate'])

    ax[1][0].axhline(y = df_IMU['magY'].mean(), color = 'r')
    ax[1][0].plot(df_estimate['time'], df_estimate['Y'])
    ax[1][0].legend(['truth along Y axis', 'estimate'])


    ax[1][1].axhline(y = df_IMU['magZ'].mean(), color = 'r')
    ax[1][1].plot(df_estimate['time'], df_estimate['Z'])
    ax[1][1].legend(['truth along Z axis', 'estimate'])
    plt.show()


acc_std = [0.014, 0.015, 0.018]
gyr_std = [0.001, 0.002, 0.001]
mag_std = [0.637, 0.385, 0.613] 

df_IMU = ld.laodTestData("Data/projectThesisTest1/newCurrentMeas/woLoad/pureIMUdata2023-05-16 09%3A22%3A14.928527.csv").dropna()
df_servo = ld.laodTestData("Data/projectThesisTest1/newCurrentMeas/woLoad/servoData2023-05-16 09%3A22%3A14.928527.csv").dropna()
time = df_servo['time'].to_numpy()
servo_pos = df_servo['servoPos'].to_numpy()

mag_earth = {'X': df_IMU['magX'].mean(), 'Y': df_IMU['magY'].mean(), 'Z': df_IMU['magZ'].mean()}
Mag_disturbance = noise.servoMagNoise.estimate_from_dataset(mag_earth, df_servo)
IMU_noise = noise.IMUnoise(acc_std, gyr_std, mag_std)



df_est_mag = filter_servonoise(Mag_disturbance, df_servo)
df_est_error = df_est_mag.copy()
df_est_error['X'] = df_est_error['X'] - mag_earth['X']
df_est_error['Y'] = df_est_error['Y'] - mag_earth['Y']
df_est_error['Z'] = df_est_error['Z'] - mag_earth['Z']
plot(df_est_mag, df_est_error)