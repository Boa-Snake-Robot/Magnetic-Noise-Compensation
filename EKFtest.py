from filtering.EKF import KalmanFilter2D
from filtering import noise
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
# Sensor measurements
#accelerometer = np.array([0.1, 0.2, 9.8])  # Accelerometer measurement in m/s^2
#gyroscope = np.array([0.01])  # Gyroscope measurement in rad/s
#magnetometer = np.array([0.2, 0.3, 0.4])  # Magnetometer measurement in microtesla

# Python script to test how the filtering of the motor field helps/works

# Load IMU data and servo data
#df_servo = ld.laodTestData("Data/movingTest/ov2/servoData2023-05-27 16%3A54%3A12.760871.csv").dropna()
#df_servo = ld.laodTestData("Data/nybevegelse/servoDataBevegelse.csv").dropna()

file_avstand = "Data/movingMavtsnad/servoData2023-06-13 11%3A36%3A05.838836.csv"
df_servo = ld.laodTestData(file_avstand).dropna()

# plot timeseries of mag against estimated euler by BNO-55
fig, axs = plt.subplots(2,1)
df_servo[['time', 'magX', 'magY', 'magZ']].set_index('time').plot(ax=axs[0])

df_servo[['time', 'eulerX', 'euleY', 'eulerZ']].set_index('time').plot(ax=axs[1])



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
servoNoise = noise.servoMagNoise(A, w, phi, B)

df_est_mag = filter.filter_servo_noise(servoNoise, df_servo)

a = 4.66
#heading = np.array([])
df_est_mag.dropna()
time = df_est_mag['time'].to_numpy()
magX = df_est_mag['magX'].to_numpy()
magY = df_est_mag['magY'].to_numpy()
gyroscope = - df_servo['gyrZ'].to_numpy() # heading rate has opposite positive direction than gyroscope measurements



q = np.diag([math.radians(.001**2), 100]) # Process noise covariance
r_heading = math.radians(3**2) # Measurement noise covariance for heading
r_heading_rate = math.radians(0.001**2)  # Measurement noise covariance for heading rate


# Create an instance of KalmanFilter2D
x0 = np.array([math.radians(-70), 0])
kf = KalmanFilter2D(q, r_heading, r_heading_rate, x0)

# Perform the filtering and estimate heading/heading rate
filtered_heading = []
filtered_heading_rate = []
measured_heading = []
dt = time[1] - time[0]
for i in range(len(magX)):
    if i != 0:
        dt = time[i] - time[i-1]
    kf.predict(dt)
    h = heading_from_mag(magX[i], magY[i], 4.66)
    if math.isnan(h):
        h = filtered_heading[i-1]
    measured_heading.append(h)
    kf.update(measured_heading[i], gyroscope[i])
    filtered_heading.append(kf.get_heading())
    filtered_heading_rate.append(kf.get_heading_rate())
    

# Convert the filtered results to numpy arrays
filtered_heading = np.array(filtered_heading)
filtered_heading_rate = np.array(filtered_heading_rate)

# Plot the true values, measured values, and filtered estimates

plt.figure(figsize=(10, 6))
plt.ylim(-180,360)
plt.plot(time, df_servo['eulerX'], label='BNO Estimated Heading')
plt.plot(time, np.degrees(measured_heading), label='Measured Heading')
plt.plot(time, np.degrees(filtered_heading), label='Filtered Heading')
plt.xlabel('Time')
plt.ylabel('Heading')
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(10, 6))
#plt.plot(time, true_heading_rate, label='True Heading Rate')
plt.plot(time, gyroscope, label='Measured Heading Rate')
plt.plot(time, filtered_heading_rate, label='Filtered Heading Rate')
plt.xlabel('Time')
plt.ylabel('Heading Rate')
plt.legend()
plt.grid(True)
plt.show()
