import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA

# Read in the CSV file containing magnetometer data
data = pd.read_csv('quicktest//magReadings.csv', header=None, names=['x', 'y', 'z'])

# Combine x, y, z data into a single time series
time_series = pd.Series(np.sqrt(data['x']**2 + data['y']**2 + data['z']**2), index=pd.to_datetime(data.index), dtype='float')

# Fit an ARMA model to the time series
#arma_model = sm.tsa.arima_model.ARMA(time_series, order=(2,2))
arma_model20 = ARIMA(time_series, order=(2, 0, 0))


# Estimate the model parameters using recursive least squares
arma20_fit = arma_model20.fit()
print(arma20_fit.params)
# Print the model summary
print(arma20_fit.summary())