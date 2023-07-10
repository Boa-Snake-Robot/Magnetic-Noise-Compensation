import numpy as np
import scipy
import math


class KalmanFilter2D:
    def __init__(self, q, r_heading, r_heading_rate, x0, init_mag_norm, MDR_on = True):
        self.Q = q                              # Process noise covariance
        self.R_heading = r_heading              # Measurement noise covariance for heading
        self.R_heading_rate = r_heading_rate    # Measurement noise covariance for heading rate

        self.x = x0                             # Initial state estimate
        self.P = np.zeros((2, 2))               # Initial error covariance estimate
        self.norm = init_mag_norm
        self.MDR = MDR_on

    def predict(self, dt):
        # State prediction
        F = np.array([[1., dt],
                      [0., 1]])
        self.x = np.dot(F, self.x)

        #discretize Q
        A = np.array([[1., 0],
                      [0.,0]])
        D1 = np.hstack((-A, self.Q))
        D2 = np.hstack((np.zeros((2,2)), A.T))
        D = np.vstack((D1,D2))*dt
        V = scipy.linalg.expm(D)
        V1 = V[2:, 2:] 
        V2 = V[0:2, 2:]
        Q = V1.T @ V2

        # Error covariance prediction
        self.P = np.dot(np.dot(F, self.P), F.T) + Q

    def update(self, magX, magY, gyro, dt):
        I = np.eye(2)
        heading = np.arctan2(magY,magX) + math.radians(4.66)
        norm = np.sqrt(magX**2 + magY**2)
        r_h = self.R_heading
        if not math.isnan(heading):
            if self.MDR:
                #adaptively increase R
                r_h += .01*((heading - self.get_heading())**2) #Increase based on measured heading and estimated heading
                r_h += .01*(abs(norm - self.norm)**2)
                
            # Compute the innovation or measurement residual for heading
            H_heading = np.array([[1., 0.]])
            innovation_heading = heading - np.dot(H_heading, self.x)

            # Compute the Kalman gain for heading
            S_heading = np.dot(np.dot(H_heading, self.P), H_heading.T) + r_h
            K_heading = np.dot(np.dot(self.P, H_heading.T), np.linalg.inv(S_heading))

            # Update the state estimate for heading
            self.x = self.x + np.dot(K_heading, innovation_heading)
            # Update the error covariance for heading
            self.P = np.dot((I - np.dot(K_heading, H_heading)), self.P)
            
    

        

        # Compute the innovation or measurement residual for heading rate
        H_heading_rate = np.array([[0., 1.]])
        innovation_heading_rate = gyro - np.dot(H_heading_rate, self.x)

        # Compute the Kalman gain for heading rate
        S_heading_rate = np.dot(np.dot(H_heading_rate, self.P), H_heading_rate.T) + self.R_heading_rate
        K_heading_rate = np.dot(np.dot(self.P, H_heading_rate.T), np.linalg.inv(S_heading_rate))

        # Update the state estimate for heading rate
        self.x = self.x + np.dot(K_heading_rate, innovation_heading_rate)

        # Update the error covariance for heading rate
        self.P = np.dot((I - np.dot(K_heading_rate, H_heading_rate)), self.P)

    def get_heading(self):
        return self.x[0]

    def get_heading_rate(self):
        return self.x[1]
