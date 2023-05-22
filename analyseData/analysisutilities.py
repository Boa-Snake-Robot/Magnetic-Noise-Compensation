import pandas as pd

def drop_outliers_IQR(df: pd.DataFrame, sensititvity = 1.5) -> pd.DataFrame:

   q1=df.quantile(0.25)

   q3=df.quantile(0.75)

   IQR=q3-q1

   not_outliers = df[~((df<(q1-sensititvity*IQR)) | (df>(q3+sensititvity*IQR)))]

   return not_outliers


def displayStatistics(df: pd.DataFrame, save = False, filename = None):
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

