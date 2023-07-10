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
    plt.rcParams['font.size'] = 20
    mag1 = pd.pivot_table(df1, index = ['time'], values= ['magX', 'magY', 'magZ'])
    gyr1 = pd.pivot_table(df1, index = ['time'], values= ['gyrX', 'gyrY', 'gyrZ'])
    acc1 = pd.pivot_table(df1, index = ['time'], values= ['accX', 'accY', 'accZ'])

    mag2 = pd.pivot_table(df2, index = ['time'], values= ['magX', 'magY', 'magZ'])
    gyr2 = pd.pivot_table(df2, index = ['time'], values= ['gyrX', 'gyrY', 'gyrZ'])
    acc2 = pd.pivot_table(df2, index = ['time'], values= ['accX', 'accY', 'accZ'])

    fig, axs = plt.subplots(1,2, figsize=(12,4))
    mag1.plot(ax=axs[0], legend=False)
    mag2.plot(ax=axs[1], legend= False)
    axs[0].set_title("Before")
    axs[1].set_title("After")
    axs[0].set_xlabel("Time [s]")
    axs[1].set_xlabel("Time [s]")
    axs[0].set_ylabel(r'$\mu T$')
    fig.legend([r'$x$-axis', r'$y$-axis', r'$z$-axis'])
    plt.savefig('figuresAndResults/comparison.svg', format='svg')



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
    #sns.set(font_scale=1.8)
    sns.pairplot(df[['magX', 'magY', 'magZ', 'servoVel', 'servoPos', 'servoCur']], corner = True)
    plt.savefig(directory + '/magServoPairPlot.svg', format='svg')
    sns.pairplot(df[['accX', 'accY', 'accZ', 'servoVel', 'servoPos', 'servoCur']], corner = True)
    plt.savefig(directory + '/accServoPairPlot.svg', format='svg')
    i = sns.pairplot(df[['gyrX', 'gyrY', 'gyrZ', 'servoVel', 'servoPos', 'servoCur']], corner = True)
    axs = i.axes
    axs[5,0].ticklabel_format(style='sci', scilimits=(0,0), axis='x')
    axs[5,1].ticklabel_format(style='sci', scilimits=(0,0), axis='x')
    axs[5,2].ticklabel_format(style='sci', scilimits=(0,0), axis='x')

    plt.savefig(directory + '/gyrServoPairPlot.svg', format='svg')

    plt.show()
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
    plt.show()