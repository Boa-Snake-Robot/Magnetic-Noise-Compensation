from filtering import servoMagNoise
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd


def feedforward_servo_noise(disturbance: servoMagNoise.servoMagNoise, df_noisy_readings: pd.DataFrame):
    """Corrects the magnetic field measurements using feed forward
            Args:
                disturbance: servoMagNoise.servoMagNoises class containing the model of the magnetic cross-talk

                df_noisy_readings: dataframe with noisy measurements. Assumes the collumns ['time', 'magX', 'magY', 'magZ', 'servoPos', 'servoVel', 'servoCur']
            
            Returns:
                Dataframe with corrected measurements
        """
    temp = {'magX': [], 'magY': [], 'magZ': []}
    for pos in df_noisy_readings['servoPos']:
        temp['magX'] = np.append(temp['magX'], disturbance.get_mag_disturbance(pos)[0])
        temp['magY'] = np.append(temp['magY'], disturbance.get_mag_disturbance(pos)[1])
        temp['magZ'] = np.append(temp['magZ'], disturbance.get_mag_disturbance(pos)[2])
        

    est_corrected_X = (df_noisy_readings['magX'].copy() - temp['magX'].copy())
    est_corrected_Y = (df_noisy_readings['magY'].copy() - temp['magY'].copy())
    est_corrected_Z = (df_noisy_readings['magZ'].copy() - temp['magZ'].copy())


    df_est_corrected = pd.DataFrame()
    df_est_corrected['time'] = df_noisy_readings['time'].tolist()
    df_est_corrected['servoPos'] = df_noisy_readings['servoPos'].copy()
    df_est_corrected['servoVel'] = df_noisy_readings['servoVel'].copy()
    df_est_corrected['servoCur'] = df_noisy_readings['servoCur'].copy()
    df_est_corrected['magX'] = est_corrected_X
    df_est_corrected['magY'] = est_corrected_Y
    df_est_corrected['magZ'] = est_corrected_Z

    return df_est_corrected

# Help functions (Directly relevant to this work)

def calc_residuals(df_truth: pd.DataFrame, df_estimate: pd.DataFrame, index = 'servoPos', columns = ['magX', 'magY', 'magZ']) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """ Calculates the residuals and performance indeces of the estimated model
        Args:
            df_truth: Dataframe containing the real values of the feature
            df_estimate: Datafram containing the estimated values
            index: The column in the estimate used as index. index is used to make sure both dataframes has the same rows
            columns: The columns containing the estimates and thruth values in the dataframes. Assumed columns is the same in df_truth and df_estimate
        Returns:
            residuals as DataFrame in columns = columns
            std ad DataFrame in columns = columns
            RMSE as DatFrame in columns = columns
    """
    #ensure the same 
    df_truth = df_truth.copy()
    df_estimate = df_estimate.copy()
    df_truth = df_truth[df_truth[index].isin(df_estimate[index])].dropna()
    df_estimate = df_estimate[df_estimate[index].isin(df_truth[index])].dropna()
    res = df_estimate.copy()
    res[columns] = df_truth[columns] - df_estimate[columns]

    std = np.std(res)  
    mse  = np.square(np.subtract(df_truth[columns], df_estimate[columns])).mean()
    rmse = np.sqrt(mse)  

    return res, std, rmse

def evaluate_model(Model: servoMagNoise.servoMagNoise, df_samples: pd.DataFrame, df_offset: pd.DataFrame, identifier, plot = True):
    df_est = Model.get_disturbance_as_timeseries(df_samples)
    # Calculate measured magnetic field from the motor from the samples
    df_true = df_samples[['time', 'servoPos', 'servoVel', 'servoCur', 'magX', 'magY', 'magZ']].copy()
    df_true['magX'] = df_true['magX']  - df_offset['X']
    df_true['magY'] = df_true['magY']  - df_offset['Y']
    df_true['magZ'] = df_true['magZ']  - df_offset['Z']

    df_res, df_std, df_rmse = calc_residuals(df_true, df_est)
    print("On " + identifier + ":")
    print("Std:")
    print(df_std[['magX', 'magY', 'magZ']])
    print("rmse:")
    print(df_rmse[['magX', 'magY', 'magZ']])
    if plot:
        plot_residuals(df_res, "Estimation error " + identifier)

def plot_error_and_estimates(df_estimate, df_error, df_IMU, title):
    plt.rcParams["figure.figsize"] = [12.50, 6.0]
    plt.rcParams["figure.autolayout"] = True
    plt.rcParams['font.size'] = 14
    for element in ['time', 'servoPos', 'servoVel', 'servoCur']:
        fig, ax = plt.subplots(2,2)
        fig.suptitle(title)
        df_error = df_error.sort_values(element)
        df_estimate = df_estimate.sort_values(element)
        ax[0][0].scatter(df_error[element], df_error['magX'], s = 5)
        ax[0][0].scatter(df_error[element], df_error['magY'], s = 5)
        ax[0][0].scatter(df_error[element], df_error['magZ'], s = 5)
        ax[0][0].legend(['error X', 'error Y', 'error Z'])
        ax[0][0].set_xlabel(element)

        ax[0][1].axhline(y = df_IMU['magX'].mean(), color = 'r')
        ax[0][1].scatter(df_estimate[element], df_estimate['magX'], s = 5)
        ax[0][1].legend(['truth along X axis', 'estimate'])
        ax[0][1].set_xlabel(element)

        ax[1][0].axhline(y = df_IMU['magY'].mean(), color = 'r')
        ax[1][0].scatter(df_estimate[element], df_estimate['magY'], s = 5)
        ax[1][0].legend(['truth along Y axis', 'estimate'])
        ax[1][0].set_xlabel(element)


        ax[1][1].axhline(y = df_IMU['magZ'].mean(), color = 'r')
        ax[1][1].scatter(df_estimate[element], df_estimate['magZ'], s = 5)
        ax[1][1].legend(['truth along Z axis', 'estimate'])
        ax[1][1].set_xlabel(element)

def plot_residuals(df_error, title):
    fig, ax = plt.subplots(1,2)
    fig.suptitle(title)
    ax[0].scatter(df_error['time'], df_error['magX'].tolist(), s = 5)
    ax[0].scatter(df_error['time'], df_error['magY'].tolist(), s = 5)
    ax[0].scatter(df_error['time'], df_error['magZ'].tolist(), s = 5)
    #ax[0].legend(['error X', 'error Y', 'error Z'])
    ax[0].set_xlabel('time [s]')
    ax[0].set_ylabel(r'$\mu$T')

    #ax[0][1].scatter(df_error['servoPos'], df_error['magX'].tolist(), s = 5)
    #ax[0][1].scatter(df_error['servoPos'], df_error['magY'].tolist(), s = 5)
    #ax[0][1].scatter(df_error['servoPos'], df_error['magZ'].tolist(), s = 5)
    #ax[0][1].legend(['error X', 'error Y', 'error Z'])
    #ax[0][1].set_xlabel('Servo position [degrees]')
    #ax[0][1].set_ylabel(r'Estimation error [$\mu$T]')

    ax[1].scatter(df_error['servoVel'], df_error['magX'].tolist(), s = 5)
    ax[1].scatter(df_error['servoVel'], df_error['magY'].tolist(), s = 5)
    ax[1].scatter(df_error['servoVel'], df_error['magZ'].tolist(), s = 5)
    #ax[1].legend(['error X', 'error Y', 'error Z'])
    ax[1].set_xlabel('Servo shaft velocity [rpm]')
    #ax[1].set_ylabel(r'$\mu$T')
    fig.legend(['error X', 'error Y', 'error Z'])


    #ax[1][1].scatter(df_error['servoCur'], df_error['magX'].tolist(), s = 5)
    #ax[1][1].scatter(df_error['servoCur'], df_error['magY'].tolist(), s = 5)
    #ax[1][1].scatter(df_error['servoCur'], df_error['magZ'].tolist(), s = 5)
    #ax[1][1].legend(['error X', 'error Y', 'error Z'])
    #ax[1][1].set_xlabel('servo current [mA]')
    #ax[1][1].set_ylabel(r'Estimation error [$\mu$T]')
    plt.savefig("figuresAndResults/filterservofield/" + title.replace(" ", "") + ".svg", format='svg')
    plt.savefig("figuresAndResults/filterservofield/" + title.replace(" ", "") + ".png", format='png')

def plot_servo_motor_field(B_servo, B_est_servo, title, savefig = False, directory = None):
    for element in ['time', 'servoPos', 'servoVel', 'servoCur']:
        fig, ax = plt.subplots(3,1)
        ax[0].scatter(B_servo[element], B_servo['magX'])
        ax[0].scatter(B_est_servo[element], B_est_servo['magX'], s = 5)
        ax[0].legend(['truth along X axis', 'estimate'])
        #ax[0].set_xlabel(element)
        ax[0].set_ylabel(r'Motor field [$\mu$T] ')

        ax[1].scatter(B_servo[element], B_servo['magY'])
        ax[1].scatter(B_est_servo[element], B_est_servo['magY'], s = 5)
        ax[1].legend(['truth along Y axis', 'estimate'])
        #ax[1].set_xlabel(element)
        ax[1].set_ylabel(r'Motor field [$\mu$T] ')


        ax[2].scatter(B_servo[element], B_servo['magZ'])
        ax[2].scatter(B_est_servo[element], B_est_servo['magZ'], s = 5)
        ax[2].legend(['truth along Z axis', 'estimate'])
        ax[2].set_xlabel(element)
        ax[2].set_ylabel(r'Motor field [$\mu$T] ')
        fig.suptitle(title)
        if savefig:
            plt.savefig(directory + "//servoEstimate" + element + ".svg", format = 'svg')
            plt.savefig(directory + "//servoEstimate" + element + ".png", format = 'png')
