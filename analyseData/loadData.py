import pandas as pd

def _convertVel(num: int):
    bitstring = num.to_bytes(length=5, byteorder='big')
    manipulated = bitstring[-4:]
    return int.from_bytes(manipulated, byteorder='big', signed=True)

def _convertCur(num: int):
    bitstring = num.to_bytes(length=5, byteorder='big')
    manipulated = bitstring[-2:]
    return int.from_bytes(manipulated, byteorder='big', signed=True)

def laodTestData(filename, save = False) -> pd.DataFrame:
    #Loads IMU measurments from csv and removes the obvious outliers (super spikes :)
    df = pd.read_csv(filename, sep = ',', header=0, index_col=False)

    #remove obvious outliers due to measurement noise
    df['time'] = (df['time'] - df['time'].iloc[0])
    df[['magX', 'magY', 'magZ']] = df[['magX', 'magY', 'magZ']][(df[['magX', 'magY', 'magZ']] < 500) & (df[['magX', 'magY', 'magZ']] > -500)].dropna()
    df[['accX', 'accY', 'accZ']] = df[['accX', 'accY', 'accZ']][(df[['accX', 'accY', 'accZ']] < 20) & (df[['accX', 'accY', 'accZ']] > -20)].dropna()

    #remove additional measurement noise
    df['accZ'] = df['accZ'][(df['accZ'] < 20) & (df['accZ'] > 8)].dropna()

    if {'servoPos', 'servoVel', 'servoCur'}.issubset(df.columns):
        df['servoPos'] = df['servoPos'][df['servoPos'] < 5000].dropna()

        for index, val in enumerate(df['servoVel']):
            df['servoVel'].iloc[index] = _convertVel(val)

        for index, val in enumerate(df['servoCur']):
            df['servoCur'].iloc[index] = _convertCur(val)

        df['servoVel'] = df['servoVel'] * 0.229 #rpm 
        df['servoPos'] = df['servoPos'] * 0.088 #deg
        df['servoCur'] = df['servoCur'] * 2.69 #mA
    
    if save:
        df.to_csv(filename + 'Translated.csv')
        

    return df
