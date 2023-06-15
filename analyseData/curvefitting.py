import numpy as np
from matplotlib import pyplot as plt
from scipy import optimize 
import pandas as pd


def _func(x, A, w, phi, B, deg = True):
    '''Calculates A*sin(w*x - phi) + B'''
    if deg:
        x = x*np.pi/180
    return A * np.sin(w*x - phi) + B

def fit_sine(x_data, y_data):
    """Fits a dataset to a sine
        Returns:
           params: [A, w, phi, B] of y = A*sin(w*x - phi) + B
    """
    params, param_cov = optimize.curve_fit(_func, x_data, y_data)
    return params, param_cov

def _generalise_sine(x, A, w, phi, B, deg = True):
    if deg:
        x = x*np.pi/180
    return A * np.sin(w*(x-phi)) + B

def _get_generalise_sine_params(A, B, C, D):
    phi = C/B
    if B < 0:   
        B = abs(B)
        A = - A
    if A < 0:
        phi = phi - np.pi/B
        A = abs(A)
    while phi < 0:
        phi = phi + 2*np.pi/B

    params = [A, B, phi, D]
    return params

def fit_magnetometer_data(df):
    """Performs sine curve fitting on mag vs pos scatteplot, plots the fitted sine and saves sine params to file

        Args:
            df: dataframe containing servopos, magX, magY and magZ

        Returns:
           dataframe with generalised sine parameters
    """
    df = df.sort_values(by=['servoPos'])
    Directions = ['magX', 'magY', 'magZ']
    df_params = pd.DataFrame(columns=Directions)
    for direction in Directions:
        params, param_cov = fit_sine(df['servoPos'].to_numpy(), np.array(df[direction].to_numpy()))
        gen_params = _get_generalise_sine_params(params[0], params[1], params[2], params[3])
        df_params[direction] = gen_params
    return df_params

def plot_magsinefit(df, curvefit_params, savefig = False, directory = None):
    """Plots the fitted curve to the datafram

        Args:
            df: dataframe containing servopos, magX, magY and magZ
            curvefit_params: the generalised sine parameters of the sine curvefit
            savefig: specifies if the figure should be saved
            directory: if savefig=True, the figure is saved to the specified

        Returns:
           nothing
    """
    df = df.sort_values(by=['servoPos'])
    Directions = ['magX', 'magY', 'magZ']

    '''PLOT MAG VS POS AND FITTED CURVE'''
    plt.rcParams["figure.figsize"] = [12.50, 4.0]
    plt.rcParams["figure.autolayout"] = True
    plt.rcParams['font.size'] = 20
    plt.rcParams['axes.ymargin'] = .4

    for direction in Directions:
        plt.scatter(df['servoPos'], df[direction], s = 5, label = 'Data')
        params = curvefit_params[direction].to_numpy()
        plt.xlabel('Servo position [deg]')
        plt.ylabel(r'Magnetic field [$\mu T$]')
        plt.plot(df['servoPos'], _generalise_sine(np.array(df['servoPos']), params[0], params[1], params[2], params[3]), label='y =' + f'{params[0]:.2f}' + ' sin(' + f'{params[1]:.2f}' + '(x - ' + f'{params[2]:.2f}' + ')) + ' + f'{params[3]:.2f}')
        
        plt.legend()
        plt.title(direction)
        
        if savefig:
            plt.savefig(directory + '//curvefit' + direction + '.svg')
        else:
            plt.show()
        plt.close()