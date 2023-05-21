import numpy as np
from matplotlib import pyplot as plt
from scipy import optimize 
import pandas as pd

'''Calculates A*sin(w*x - phi) + B'''
def func(x, A, w, phi, B, deg = True):
    if deg:
        x = x*np.pi/180
    return A * np.sin(w*x - phi) + B


'''returns params: [A, w, phi, B]'''
def fit_sine(x_data, y_data):
    #n, m = np.shape(x_data)
    #x_data = np.reshape(x_data, n*m)
    #n, m = np.shape(y_data)
    #y_data = np.reshape(y_data, n*m)

    #Bounds = (0, [np.inf, np.inf, 360, np.inf]) #Bounds for [A, w, phi, B]. 
    #Bounds= ([None, 0, None, None],[None, None, None, None])
    Bounds= ([None, None, None, None],[None, None, None, None])     #Only thing that works
    params, param_cov = optimize.curve_fit(func, x_data, y_data, bounds=Bounds)
    print('Params: ')
    print(params)
    return params, param_cov

def generalise_sine(x, A, B, C, D, deg = True):
    if deg:
        x = x*np.pi/180
    params = get_generalise_sine_params(A, B, C, D)
    return params[0] * np.sin(params[1]*(x-params[2])) + params[3]

def get_generalise_sine_params(A, B, C, D):
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

def plot_generalised_sine(x, params1):
    plt.figure()
    plt.plot(x, func(x, params1[0], params1[1], params1[2], params1[3]), label = "original")
    plt.plot(x, generalise_sine(x, params1[0], params1[1], params1[2], params1[3]), label = "generalized")
    plt.legend()


'''Performs sine curve fitting on mag vs pos scatteplot, plots the fitted sine and saves sine params to file'''
def fitMagnetometerData(df, saveFig = False, directory = None):

    '''PLOT MAG VS POS AND FITTED CURVE'''
    plt.rcParams["figure.figsize"] = [12.50, 6.0]
    plt.rcParams["figure.autolayout"] = True
    plt.rcParams['font.size'] = 20
    df = df.sort_values(by=['servoPos'])
    Directions = ['magX', 'magY', 'magZ']
    df_params = pd.DataFrame(columns=Directions)
    for direction in Directions:
        params, param_cov = fit_sine(df['servoPos'].to_numpy(), np.array(df[direction].to_numpy()))
        gen_params = get_generalise_sine_params(params[0], params[1], params[2], params[3])
        df_params[direction] = gen_params
        plt.scatter(df['servoPos'], df[direction], s = 5, label = 'Data')
        plt.xlabel('Servo position [deg]')
        plt.ylabel(r'Magnetic field [$\mu T$]')
        plt.plot(df['servoPos'], func(np.array(df['servoPos']), params[0], params[1], params[2], params[3]), label='y =' + f'{gen_params[0]:.2f}' + ' sin(' + f'{gen_params[1]:.2f}' + '(x - ' + f'{gen_params[2]:.2f}' + ')) + ' + f'{gen_params[3]:.2f}')
        
        plt.legend(loc='lower left')
        plt.title(direction)
        
            
        if saveFig:
            plt.savefig(directory + "//curvefit" + direction + ".eps")
        else:
            plt.show()
        plt.close()
    return df_params


