import pandas as pd
import matplotlib.pyplot as plt

'''Assumes csv file contains header'''
FILENAME = "servoposition2023-04-11 11:56:08.360587.csv"
FILENAME = "servoposition2023-04-11 11:59:19.372798.csv"
FILENAME = "servoposition2023-04-11 12:03:15.133447.csv"
FILENAME = "servoposition2023-04-11 12:05:08.347221.csv"
FILENAME = "servoposition2023-04-11 13:59:55.273074.csv"
FILENAME = "servoposition2023-04-11 14:06:27.370840.csv"
FILENAME = "servoposition2023-04-11 14:10:14.976037.csv"
FILENAME = "servoposition2023-04-11 14:27:54.549886.csv"
FILENAME = "servoTestitest.csv"


data_frame = pd.read_csv(FILENAME, sep = ',', header=0)
data_frame.set_index('time').plot(subplots=True)
plt.show()

    