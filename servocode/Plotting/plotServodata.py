import pandas as pd
import matplotlib.pyplot as plt

'''Assumes csv file contains header'''
IMUWPower = "withpower.csv"
IMUWTorque = "withTorque.csv"
IMUPos = "poscontrol.csv"
IMUVel = "velcontrol.csv"

servoPos = "servoPosTest.csv"
servoVel = "servoVelTest.csv"
FILENAME = "TestingData\\withpower.csv"

data_frame = pd.read_csv(FILENAME, sep = ', ', header=0)
data_frame.set_index('time').plot(subplots=True)
plt.show()

    