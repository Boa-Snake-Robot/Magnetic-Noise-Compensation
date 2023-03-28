import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt

# Read in the CSV file containing magnetometer data
data = pd.read_csv('test.txt', header=None, names=['x', 'y', 'z', 't'])
#timestamps = pd.read_csv('newtest//oneSetTimestamps.csv')

# Combine x, y, z data into a single time series
x_dta = data['x']
y_dta = data['y']
z_dta = data['z']
timestamps = data['t']


# Plot the time series
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(data['t'], data['x'])
ax.plot(data['t'], data['y'])
ax.plot(data['t'], data['z'])
ax.set_xlabel('time')
ax.set_ylabel('Magnetometer Reading')
ax.set_title('Magnetometer Time Series')
plt.show()

#plot autocorrelation
fig = plt.figure(figsize=(12, 8))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(data['x'].values.squeeze(), lags=40, ax=ax1)
fig = sm.graphics.tsa.plot_acf(data['y'].values.squeeze(), lags=40, ax=ax1)
fig = sm.graphics.tsa.plot_acf(data['z'].values.squeeze(), lags=40, ax=ax1)
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(data['x'], lags=40, ax=ax2)
fig = sm.graphics.tsa.plot_pacf(data['y'], lags=40, ax=ax2)
fig = sm.graphics.tsa.plot_pacf(data['z'], lags=40, ax=ax2)
plt.show()

# Test different ARMA model orders
for p in range(3):
    for q in range(3):
        try:
            # Fit an ARMA model to the time series
            arma_model = ARIMA(data['x'], order=(p,0,q))
            arma_fit = arma_model.fit()
            
            # Print the model summary
            print(f'ARMA({p},{q}) Model Results:\n{arma_fit.summary()}\n')
            
            # Plot the model residuals
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(arma_fit.resid)
            ax.set_xlabel('Date')
            ax.set_ylabel('Residual')
            ax.set_title(f'ARMA({p},{q}) Residuals')
            plt.show()
            
        except:
            continue
