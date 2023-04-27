import pandas as pd
import matplotlib.pyplot as plt

FILENAME = "servoposition2023-04-24 14%3A24%3A43.046057.csv"
FILENAME = "servoposition2023-04-24 14%3A24%3A01.730985.csv"
FILENAME = "servoposition2023-04-25 11%3A07%3A10.462038.csv"
df = pd.read_csv(FILENAME, sep = ', ', header=0, index_col=False)
df['time'] = (df['time'] - df['time'].iloc[0])
df['servoVel'] = df['servoVel'] * 0.229
df['servoPos'] = df['servoPos'] * 0.88
mag = pd.pivot_table(df, index = ['time'], values= ['magX', 'magY', 'magZ'])
gyr = pd.pivot_table(df, index = ['time'], values= ['gyrX', 'gyrY', 'gyrZ'])
acc = pd.pivot_table(df, index = ['time'], values= ['accX', 'accY', 'accZ'])
servo = pd.pivot_table(df, index = ['time'], values= ['servoPos', 'servoVel', 'servoCur'])

mag.plot(figsize=(12, 8))
acc.plot(figsize=(12, 8))
gyr.plot(figsize=(12, 8))
servo.plot(y='servoVel', figsize=(12, 8))


df.plot(kind='scatter', x='servoPos', y='magX', color='r', figsize=(12, 2))
df.plot(kind='scatter', x='servoPos', y='magY', color='g', figsize=(12, 2))
df.plot(kind='scatter', x='servoPos', y='magZ', color='b', figsize=(12, 2))
#scatter = pd.pivot_table(df, index = 'servoPos', values = ['magX', 'magY', 'magZ'])
#scatter.plot()
plt.show()

print(mag)
print(acc)
print(gyr)
print(servo)
