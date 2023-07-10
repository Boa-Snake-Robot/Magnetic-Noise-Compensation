
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
import matplotlib.pyplot as plt


def plot_xyz_timeseries(data):
    ax = data[['time', 'magX', 'magY', 'magZ']].set_index('time').plot(subplots=True)
    ax[0].set_xlabel('')
    ax[1].set_xlabel('')
    ax[2].set_xlabel('time [s]')
    ax[0].set_ylabel(r'$\mu$ T')
    ax[1].set_ylabel(r'$\mu$ T')
    ax[2].set_ylabel(r'$\mu$ T')
    plt.legend()
    plt.show()
    #data[['time', 'gyrX', 'gyrY', 'gyrZ']].set_index('time').plot(subplots=True)
    #data[['time', 'accX', 'accY', 'accZ']].set_index('time').plot(subplots=True)
    
    data[['magX', 'magY', 'magZ']].plot.kde()
    plt.show()


def zero_mean_df(df, exlude_time = False):
    if exlude_time:
        df_xyz = df.loc[:, df.columns != 'time']
        df_xyz = df_xyz- df_xyz.mean()
        df.loc[:, df.columns != 'time'] = df_xyz
    else:
        df = df - df.mean()
    return df

def saveStatistics(filename, df):
    agg = df.agg( {
        "magX": ["min", "max", "median", "skew", "kurtosis", "mean", "std"],
        "magY": ["min", "max", "median", "skew", "kurtosis", "mean", "std"],
        "magZ": ["min", "max", "median", "skew", "kurtosis", "mean", "std"],
        
    }, skipna = True, numeric_only = True
)
    agg.to_csv(filename, sep=',')
    print(agg)
        

def drop_outliers_IQR(df: pd.DataFrame, sensititvity = 1.5) -> pd.DataFrame:

   q1=df.quantile(0.25)

   q3=df.quantile(0.75)

   IQR=q3-q1

   not_outliers = df[~((df<(q1-sensititvity*IQR)) | (df>(q3+sensititvity*IQR)))]

   return not_outliers

plt.rcParams["figure.figsize"] = [10.50, 6.0]
plt.rcParams["figure.autolayout"] = True
plt.rcParams['font.size'] = 20
plt.rcParams['axes.ymargin'] = .4
# Read in the CSV file containing magnetometer data
data = pd.read_csv("Data/ARMA/IMUTESTdata2023-06-05 09%3A00%3A57.294645.csv", sep = ',', header=0, index_col=False)
saveStatistics("IMUNoiseCharStatistics.csv", data)
data['time'] = (data['time'] - data['time'].iloc[0])
plot_xyz_timeseries(data)

#remove obvious outliers due to measurement noise
data_dropped_outliers = drop_outliers_IQR(data, sensititvity=3)
plot_xyz_timeseries(data_dropped_outliers)
saveStatistics("IMUNoiseCharStatistics.csv", data_dropped_outliers)


#plot autocorrelation
fig = plt.figure(figsize=(7, 10))
ax1 = fig.add_subplot(211)
sm.graphics.tsa.plot_acf(data['magX'].values.squeeze(), lags=5, ax=ax1, alpha = 0.05, label = 'X')
sm.graphics.tsa.plot_acf(data['magY'].values.squeeze(), lags=5, ax=ax1, alpha = 0.05, label = 'Y')
sm.graphics.tsa.plot_acf(data['magZ'].values.squeeze(), lags=5, ax=ax1, alpha = 0.05, label = 'Z')

ax2 = fig.add_subplot(212)
sm.graphics.tsa.plot_pacf(data['magX'], lags=5, ax=ax2, alpha = 0.05, label = 'X')
sm.graphics.tsa.plot_pacf(data['magY'], lags=5, ax=ax2, alpha = 0.05, label = 'Y')
sm.graphics.tsa.plot_pacf(data['magZ'], lags=5, ax=ax2, alpha = 0.05, label = 'Z')
ax2.set_xlabel('Lag')

ax1.legend(loc='upper right')
ax2.legend(loc='upper right')
plt.show()