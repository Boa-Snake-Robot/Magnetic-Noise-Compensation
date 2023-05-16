import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def convertVel(num):
    bitstring = num.to_bytes(length=5, byteorder='big')
    manipulated = bitstring[-4:]
    return int.from_bytes(manipulated, byteorder='big', signed=True)

def convertCur(num):
    bitstring = num.to_bytes(length=5, byteorder='big')
    manipulated = bitstring[-2:]
    return int.from_bytes(manipulated, byteorder='big', signed=True)

def displayStatistics(df, save = False, filename = None):
    if save:
        assert(filename != None)
    agg = df.agg( {
        "magX": ["mean", "std", "skew", "kurtosis"],
        "magY": ["mean", "std", "skew", "kurtosis"],
        "magZ": ["mean", "std", "skew", "kurtosis"],
        "accX": ["mean", "std", "skew", "kurtosis"],
        "accY": ["mean", "std", "skew", "kurtosis"],
        "accZ": ["mean", "std", "skew", "kurtosis"],
        "gyrX": ["mean", "std", "skew", "kurtosis"],
        "gyrY": ["mean", "std", "skew", "kurtosis"],
        "gyrZ": ["mean", "std", "skew", "kurtosis"],
    }, skipna = True, numeric_only = True
).round(3)
    if save:
        agg.to_csv(filename, sep=',')
    print(agg.transpose())
    return

def laodTestData(filename, save = False):
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
            df['servoVel'].iloc[index] = convertVel(val)

        for index, val in enumerate(df['servoCur']):
            df['servoCur'].iloc[index] = convertCur(val)

        df['servoVel'] = df['servoVel'] * 0.229 #rpm 
        df['servoPos'] = df['servoPos'] * 0.088 #deg
        df['servoCur'] = df['servoCur'] * 2.69 #mA
    
    if save:
        df.to_csv(filename + 'Translated.csv')
    displayStatistics(df, filename=filename + "statistics-"  + ".csv", save=save )
        

    return df





#This does not work...
def removeOutliersZscore(data, threshold=3):
    """
    Remove outliers from the dataset using Z-score method.

    Parameters:
    data (DataFrame): The input dataset.
    threshold (float): The threshold for Z-score. Data points with Z-score greater than the threshold will be considered as outliers.

    Returns:
    The input dataset with outliers removed.
    """
    z_scores = np.abs((data - data.mean()) )/ data.std()
    filtered_data = data[(z_scores < threshold).all(axis=1)]
    return filtered_data


#Dette fungerer ikke helt. finn ut
def drop_outliers_IQR(df, sensititvity = 1.5):

   q1=df.quantile(0.25)

   q3=df.quantile(0.75)

   IQR=q3-q1

   not_outliers = df[~((df<(q1-sensititvity*IQR)) | (df>(q3+sensititvity*IQR)))]

   return not_outliers

def compareIMUMeasurements(df1, df2):
    #Compares a set of IMU measurements
    #Main use: see if theres a difference befor and after servo was turned on 

    mag1 = pd.pivot_table(df1, index = ['time'], values= ['magX', 'magY', 'magZ'])
    gyr1 = pd.pivot_table(df1, index = ['time'], values= ['gyrX', 'gyrY', 'gyrZ'])
    acc1 = pd.pivot_table(df1, index = ['time'], values= ['accX', 'accY', 'accZ'])

    mag2 = pd.pivot_table(df2, index = ['time'], values= ['magX', 'magY', 'magZ'])
    gyr2 = pd.pivot_table(df2, index = ['time'], values= ['gyrX', 'gyrY', 'gyrZ'])
    acc2 = pd.pivot_table(df2, index = ['time'], values= ['accX', 'accY', 'accZ'])

    fig, axs = plt.subplots(3,2, figsize=(16,9))
    mag1.plot(ax=axs[0][0])
    mag2.plot(ax=axs[0][1])
    acc1.plot(ax=axs[1][0])
    acc2.plot(ax=axs[1][1])
    gyr1.plot(ax=axs[2][0])
    gyr2.plot(ax=axs[2][1])
    plt.show()
    return

def plotServo(df, directory):

    sns.pairplot(df[['magX', 'magY', 'magZ', 'servoVel', 'servoPos', 'servoCur']], corner = True)
    plt.savefig(directory + '/magServoPairPlot.eps', format='eps')
    sns.pairplot(df[['accX', 'accY', 'accZ', 'servoVel', 'servoPos', 'servoCur']], corner = True)
    plt.savefig(directory + '/accServoPairPlot.eps', format='eps')
    sns.pairplot(df[['gyrX', 'gyrY', 'gyrZ', 'servoVel', 'servoPos', 'servoCur']], corner = True)
    plt.savefig(directory + '/gyrServoPairPlot.eps', format='eps')

    sns.pairplot(df[['linX', 'linY', 'linZ', 'servoVel', 'servoPos', 'servoCur']], corner = True)
    plt.savefig(directory + '/linServoPairPlot.eps', format='eps')
    sns.pairplot(df[['gravX', 'gravY', 'gravZ', 'servoVel', 'servoPos', 'servoCur']], corner = True)
    sns.pairplot(df[['eulerX', 'euleY', 'eulerZ', 'servoVel', 'servoPos', 'servoCur']], corner = True)

    return

def plotIMU(df1):
    #df1 = drop_outliers_IQR(df1)
    df1.set_index('time').plot(subplots=True, figsize=(12,20))

    fig, ax = plt.subplots(3, 3, figsize=(12, 20))
    sns.histplot(data=df1['gyrX'], ax=ax[0][0]).set(xlabel = 'gyrX')
    sns.histplot(data=df1['gyrY'], ax=ax[1][0]).set(xlabel = 'gyrY')
    sns.histplot(data=df1['gyrZ'], ax=ax[2][0]).set(xlabel = 'gyrZ')
    sns.histplot(data=df1['magX'], ax=ax[0][1]).set(xlabel = 'magX')
    sns.histplot(data=df1['magY'], ax=ax[1][1]).set(xlabel = 'magY')
    sns.histplot(data=df1['magZ'], ax=ax[2][1]).set(xlabel = 'magZ')
    sns.histplot(data=df1['accX'], ax=ax[0][2]).set(xlabel = 'accX')
    sns.histplot(data=df1['accY'], ax=ax[1][2]).set(xlabel = 'accY')
    sns.histplot(data=df1['accZ'], ax=ax[2][2]).set(xlabel = 'accZ')

