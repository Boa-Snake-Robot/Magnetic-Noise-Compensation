from filtering.KF import KalmanFilter2D
from filtering import servoMagNoise
from filtering import filtering as filter
from analyseData import loadData as ld
from matplotlib import pyplot as plt
import numpy as np
import math



def heading_from_mag(magX, magY, a):
    return np.arctan2(magY,magX) + math.radians(a)
    xi1 = np.arctan(magY/magX)
    if magX < 0:
        return np.pi + xi1 + math.radians(a)
    elif magX > 0 and magY < 0:
        return 2* np.pi + xi1 + math.radians(a)
    elif magX == 0 and magY > 0:
        return np.pi/2 + math.radians(a)
    elif magX == 0 and magY < 0:
        return 3*np.pi / 2 + math.radians(a)
    else:
        return xi1


# Load IMU data and servo data
df_servo = ld.laodTestData("Data/nybevegelse/servoDataBevegelse.csv").dropna()
df_imu = ld.laodTestData("Data/nybevegelse/pureIMUDataBevegelse.csv")
norm = np.sqrt((df_imu['magX'].mean())**2 + (df_imu['magY'].mean())**2)
print("Norm = ", norm)

# use previous estimate of motor field (load A, w, phi, B dircectly into servoMagNoise object)
# Servo model
#A = [90.313, 91.468, 5.836]
#w = [1, 1, 1]
#phi = [39.124, 6.150, 4.121]
#B = [88.860, -12.472, -5.779]
A = [76.1, 67.3, 16.15]
w = [1, 1, 1]
phi = [32.92, 6.16, 14.47]
B = [75.73, -8.53, 13.27]
servoNoise = servoMagNoise.servoMagNoise(A, w, phi, B)

df_est_mag = filter.feedforward_servo_noise(servoNoise, df_servo)
gyroscope = - df_servo['gyrZ'].to_numpy() # heading rate has opposite positive direction than gyroscope measurements
#df_est_mag = df_imu.copy()
#gyroscope = - df_imu['gyrZ'].to_numpy() # heading rate has opposite positive direction than gyroscope measurements


a = 4.66
df_est_mag.dropna()
time = df_est_mag['time'].to_numpy()
magX = df_est_mag['magX'].to_numpy()
magY = df_est_mag['magY'].to_numpy()


#good tuning with rejection:
# q = .[1**2, 100], r_heading = 1**2, r_rate = .001**2

# Create an instance of KalmanFilter2D
x0 = np.array([math.radians(0), 0])

# Without MDR overcompensate
q = np.diag([math.radians(.001**2), 10*2]) # Process noise covariance
r_heading = math.radians(1**2) # Measurement noise covariance for heading
r_heading_rate = math.radians(.001**2)  # Measurement noise covariance for heading rate
kf = KalmanFilter2D(q, r_heading, r_heading_rate, x0, norm, MDR_on=False)

# Without MDR
q = np.diag([math.radians(.1**2), 10*2]) # Process noise covariance
r_heading = math.radians(1**2) # Measurement noise covariance for heading
r_heading_rate = math.radians(.001**2)  # Measurement noise covariance for heading rate
kf_good = KalmanFilter2D(q, r_heading, r_heading_rate, x0, norm, MDR_on=False)

# With MDR
q = np.diag([math.radians(.1**2), 10*2]) # Process noise covariance
r_heading = math.radians(.1**2) # Measurement noise covariance for heading
r_heading_rate = math.radians(.001**2)  # Measurement noise covariance for heading rate
kf_mdr = KalmanFilter2D(q, r_heading, r_heading_rate, x0, norm)

# Perform the filtering and estimate heading/heading rate
filtered_heading = []
filtered_heading_good = []
filtered_heading_mdr = []

measured_heading = []
dt = time[1] - time[0]
for i in range(len(magX)):
    if i != 0:
        dt = time[i] - time[i-1]
    kf.predict(dt)
    kf_good.predict(dt)
    kf_mdr.predict(dt)

    h = heading_from_mag(magX[i], magY[i], 4.66)
    if math.isnan(h):
        h = measured_heading[i-1]
    measured_heading.append(h)
    kf.update(magX[i], magY[i], gyroscope[i], dt)
    kf_good.update(magX[i], magY[i], gyroscope[i], dt)
    kf_mdr.update(magX[i], magY[i], gyroscope[i], dt)

    filtered_heading.append(kf.get_heading())
    filtered_heading_good.append(kf_good.get_heading())
    filtered_heading_mdr.append(kf_mdr.get_heading())

    

# Convert the filtered results to numpy arrays
filtered_heading = np.array(filtered_heading)
filtered_heading_good = np.array(filtered_heading_good)
filtered_heading_mdr = np.array(filtered_heading_mdr)


# Plot the true values, measured values, and filtered estimates
plt.rcParams['font.size'] = 20
plt.rcParams["legend.loc"] = 'upper right'
plt.rcParams['svg.fonttype'] = 'none'
plt.figure(figsize=(10, 6))
plt.ylim(-180,360)
plt.plot(time, df_servo['eulerX'], label='BNO Estimate', color = '#0000ffff', linestyle='dashed')
#plt.plot(time, df_imu['eulerX'], label='BNO Estimate', color = '#0000ffff', linestyle='dashed')
plt.plot(time, np.degrees(measured_heading), label='Pseudo measurement', color = 'tab:orange')
plt.plot(time, np.degrees(filtered_heading), label='KF tuning 1', color = '#0000ffff')
plt.plot(time, np.degrees(filtered_heading_good), label='KF tuning 2', color = '#007d00ff', linestyle='dashed')
plt.plot(time, np.degrees(filtered_heading_mdr), label='KF with MDR', color = '#007d00ff')
#plt.xlim(0,12)
plt.xlabel('Time [s]')
plt.ylabel(r'Heading [$\degree$]')
plt.legend()
plt.grid(True)
plt.tight_layout()
#plt.savefig('figuresAndResults/headingestimate_stationary.svg', format = 'svg')
plt.show()
