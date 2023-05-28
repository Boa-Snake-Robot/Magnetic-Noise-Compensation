import numpy as np
from numpy import ndarray
from numpy import random
from analyseData import curvefitting as cf
import pandas as pd


class IMUnoise():
    acc_std: ndarray
    gyro_std: ndarray
    mag_std: ndarray

    def __init__(self, acc_std: ndarray, gyro_std: ndarray, mag_std: ndarray):

        self.acc_std = acc_std
        self.gyro_std = gyro_std
        self.mag_std = gyro_std
    
    def get_mag_noise(self) -> ndarray:
        return np.array[random.normal(0, self.mag_std[0]), random.normal(0, self.mag_std[1]), random.normal(0, self.mag_std[2])]
    
    def get_acc_noise(self) -> ndarray:
        return np.array[random.normal(0, self.acc_std[0]), random.normal(0, self.acc_std[1]), random.normal(0, self.acc_std[2])]
    
    def get_gyr_noise(self) -> ndarray:
        return np.array[random.normal(0, self.gyro_std[0]), random.normal(0, self.gyro_std[1]), random.normal(0, self.gyro_std[2])]


class servoMagNoise():
    A:  ndarray
    w:  ndarray
    phi:ndarray 
    B:  ndarray

    def __init__(self, A: ndarray, w: ndarray, phi: ndarray, B: ndarray):
        self.A = A
        self.w = w
        self.phi = phi
        self.B = B

    @classmethod
    def estimate_from_dataset(self, mag_earth: dict, df_servo: pd.DataFrame):
        """Estimates the generated electromagnetic field based on earths magnetic field and IMU measurements where the servo motor actuates
            Args:
                mag_earth: [muT] dictionary with entries ['X', 'Y', 'Z] of floats or integers

                df_servo: dataframe with servo motor measurements with columns ['magX', 'magY', 'magZ']
            
            Returns:
                Nothing
        """
        df_mag_servo = df_servo.copy()
        df_mag_servo['magX'] = df_mag_servo['magX']  - mag_earth['X']
        df_mag_servo['magY'] = df_mag_servo['magY']  - mag_earth['Y']
        df_mag_servo['magZ'] = df_mag_servo['magZ']  - mag_earth['Z']
        params = cf.fit_magnetometer_data(df_mag_servo)
        
        
        paramsX = params['magX'].to_numpy()
        paramsY = params['magY'].to_numpy()
        paramsZ = params['magZ'].to_numpy()
        A   = [paramsX[0], paramsY[0], paramsZ[0]]
        w   = [paramsX[1], paramsY[1], paramsZ[1]]
        phi = [paramsX[2], paramsY[2], paramsZ[2]]
        B   = [paramsX[3], paramsY[3], paramsZ[3]]

        return servoMagNoise(A, w, phi, B)
    
    def _func(self, A: float, w: float, phi: float, B: float, shaftPos: float, deg = True): 
        if deg:
            shaftPos = shaftPos*np.pi/180
        return A * np.sin(w*(shaftPos - phi)) + B
        
    def get_mag_disturbance(self, shaftPos: float, deg = True) -> ndarray:
        """Estimates and returns the electromagnetic disturbance along the X, Y and Z axis
            Args:
                shaftPos: servo motors shaft position in degrees or radians (range from 0 to 360 deg)
                deg: bool saying if the shaft position is in degrees or radians
            Returns:
                numpy array of magnetic disurbance along the axes [x value, y value, z value]
        """

        dist =  np.array([0, 0, 0])
        for i in range(0,3):
            dist[i] = self._func(self.A[i], self.w[i], self.phi[i], self.B[i], shaftPos, deg)
        return dist
       
            