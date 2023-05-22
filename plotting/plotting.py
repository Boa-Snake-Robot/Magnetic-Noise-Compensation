import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def compare_IMU_measurements(df1: pd.DataFrame, df2: pd.DataFrame):
    """Compares a set of IMU measurements
        Main use: see if theres a difference before and after servo was turned on 
        
        Args:
            df1: dataframe with IMU and servo measurements
            df2: same as df1 to compare with df1
        
        return: nothing
    """
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
    axs[0][0].set_title("Before")
    axs[0][1].set_title("After")
    plt.show()
    return

def plot_servo(df: pd.DataFrame, directory):
    """ Plots the IMU and servo measurements during experiments
        Args:
            df: dataframe with IMU and servo measurements
            directory: directory to save figures

        Returns:
            Nothing

    """

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

def plot_IMU(df1):
    """ Plots the IMU measurements when servo does not actuate
        Args:
            df1: dataframe with IMU  measurements

        Returns:
            Nothing

    """
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