import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as scig
import random as rdm

#Programme constants
x_initial = 0
x_final = 1/3
Num_n = 10000


def numerical_integral(fx, xmin, xmax, n, **kwargs):
    #Uses the rectangle rule to find an estimate for the area under a curve f(x)
    interval = np.linspace(xmin, xmax, int(round(n)) + 1)
    Area = 0
    n = int(round(n))
    for i in range(1, n):
        h = fx(interval[i-1])
        Area += (interval[i] - interval[i-1]) * h
    
    return Area


def wavefunction(x):
    f_x = 2 * ((np.sin(x * np.pi)) ** 2)
    return f_x

Num_P = numerical_integral(wavefunction, x_initial, x_final, Num_n) 
print('The estimate for the Integral using the rectangle rule with {0} segments, is: {1:.4}'.format(Num_n, Num_P))

#Task 2
scipy_integral, scipy_uncertainty = scig.quad(wavefunction, x_initial, x_final)
print('Using Scipy, we get the integral to be : {0:.4}'.format(scipy_integral))




#Task 3
eta_iter = 5

def Accuracy(meas_func, expected_func, xmin, xmax, iteration_N, **kwargs):
    eta = abs(expected_func - meas_func(wavefunction, xmin, xmax, iteration_N, **kwargs)) / expected_func
    return eta

def Eta_Accuracy(function_estimate, function_actual, xmin, xmax, iterations, **kwargs):
    #
    iter_len = len(iterations)
    eta = np.zeros(iter_len)  
    for i in range(iter_len):
        eta[i] = Accuracy(function_estimate, function_actual, xmin, xmax, iterations[i], **kwargs) 
    
    if 'eta_plot' in kwargs:
        if kwargs.get('eta_plot'):
    
            plt.plot(iterations, eta)
            if 'log' in kwargs:
                if kwargs.get('log'):
                    plt.xscale('log')
            
            plt.show()
    function_order = 0
    for i in range(iter_len):
        for j in range (iter_len):
            if i < j:
                function_order += (np.log(eta[j]/eta[i]))/(np.log(iterations[i]/iterations[j])) 
                #print(function_order)
    function_order /= ((iter_len - 1) * (iter_len / 2))
    return iterations, eta, function_order




#Definging Arrays
linear = np.linspace(100, 10000, 1001)
factors_10 = np.zeros(eta_iter)
for i in range(0, eta_iter):
    factors_10[i] = 10**(i+2)
    
        
        
        
        

print(Eta_Accuracy(numerical_integral, scipy_integral, x_initial, x_final, factors_10, eta_plot=True, log=True))



#Task 4
monte_n = 10000
def monte_carlo(fx, xmin, xmax, trials, *,monte_print=False, **kwargs):
    #Estimating the integral using random number generations
    xval = np.linspace(xmin, xmax, 1000)
    yval = fx(xval)
    ymin = min(yval)
    ymax = max(yval)
    xlist= []
    ylist= []
    x2list=[]
    y2list=[]
    box_area = (ymax - ymin) * (xmax - xmin) 
    success = 0
    for i in range(int(round(trials))):
        xrdm = rdm.uniform(xmin, xmax)
        yrdm = rdm.uniform(ymin, ymax)
        
        if yrdm <= fx(xrdm):
            success += 1
            xlist.append(xrdm)
            ylist.append(yrdm)
        else:
            x2list.append(xrdm)
            y2list.append(yrdm)
  
        
    if 'func_plot' in kwargs:
        if kwargs.get('func_plot'):
            plt.plot(xval,yval)         
            plt.scatter(xlist, ylist, s=.75)
            plt.scatter(x2list, y2list,s=.75)
            plt.show()
    
        
    monte_estimate = (success/trials) * box_area
    if monte_print:
        print('Using the Monte Carlo Method with {0} trials, we have : {1:.4}'.format(trials, monte_estimate))

    return monte_estimate
        

monte_carlo(wavefunction, x_initial, x_final, monte_n, func_plot=True)        

Eta_Accuracy(monte_carlo, scipy_integral, x_initial, x_final, factors_10, monte_print=True, eta_plot=True, log=True)
Eta_Accuracy(monte_carlo, scipy_integral, x_initial, x_final, linear, eta_plot=True)

