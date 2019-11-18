import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as scig

ODE_tst = lambda x, y, z, **kwargs: (7*y**2) * x**3 
ODE_h_x = lambda x, y, z, **kwargs: (-26.2 * (kwargs.get('e') - kwargs.get('v')) * y)


#Constants


Vmax = 10**6                            #'Infinite' potential
half_width_box = 0.5 * (10**-9)         #half width of 1nm box
E_initial_guess = 1               #Initial guess for E
eta = 10**-15
step_size = eta**(.5) 


def V(x, a):
    if abs(x) <= a:
        return 0
    return Vmax




ODE_f_x = lambda x, y, z, **kwargs: z
ODE_h_x = lambda x, y, z, **kwargs: (-26.2 * (kwargs.get('e') - 0) * y)
ODE_g_x = lambda x, y, z, **kwargs: (-26.2 * (kwargs.get('e') - kwargs.get('v')) * y)

def Runge_Kutta(E, f, g, H, interval, n, N, *args):
    a = interval
    h = H * a / N
    
    if ((n-1) % 4) == 0:
        y_0 = 1
        z_0 = 0
    elif ((n-1) % 4) == 1:
        y_0 = 0
        z_0 = -1
    elif ((n-1) % 4) == 2:
        y_0 = -1
        z_0 = 0
    elif ((n-1) % 4) == 3:
        y_0 = 0
        z_0 = 1
    
    x_ary = np.zeros(N)
    y_ary = np.zeros(N)
    z_ary = np.zeros(N)
    
    x_ary[0] = 0
    y_ary[0] = y_0
    z_ary[0] = z_0/a
    
    
    k1 = lambda x, y, z: h * f(x, y, z, e=E, v=V(x, a))    
    l1 = lambda x, y, z: h * g(x, y, z, e=E, v=V(x, a))

    k2 = lambda x, y, z: h * f(x + h/2, y + k1(x, y, z)/2, z + l1(x, y, z)/2, e=E, v=V(x, a))    
    l2 = lambda x, y, z: h * g(x + h/2, y + k1(x, y, z)/2, z + l1(x, y, z)/2, e=E, v=V(x, a))

    k3 = lambda x, y, z: h * f(x + h/2, y + k2(x, y, z)/2, z + l2(x, y, z)/2, e=E, v=V(x, a))    
    l3 = lambda x, y, z: h * g(x + h/2, y + k2(x, y, z)/2, z + l2(x, y, z)/2, e=E, v=V(x, a))

    k4 = lambda x, y, z: h * f(x + h, y + k3(x, y, z), z + l3(x, y, z), e=E, v=V(x, a))    
    l4 = lambda x, y, z: h * g(x + h, y + k3(x, y, z), z + l3(x, y, z), e=E, v=V(x, a))

      
    
    for i in range(N-1):
        x_ary[i+1] = x_ary[i] + h
        y_ary[i+1] = (y_ary[i] + (k1(x_ary[i], y_ary[i], z_ary[i]) / 6) 
            + (k2(x_ary[i], y_ary[i], z_ary[i]) / 3) 
            + (k3(x_ary[i], y_ary[i], z_ary[i]) / 3)
            + (k4(x_ary[i], y_ary[i], z_ary[i]) / 6))

        z_ary[i+1] = (z_ary[i] + (l1(x_ary[i], y_ary[i], z_ary[i]) / 6) 
            + (l2(x_ary[i], y_ary[i], z_ary[i]) / 3) 
            + (l3(x_ary[i], y_ary[i], z_ary[i]) / 3)
            + (l4(x_ary[i], y_ary[i], z_ary[i]) / 6))

    if h > 0:    
        x_pos, y_pos = x_ary, y_ary
        H = -1
        x_neg, y_neg = Runge_Kutta(E, f, g, H, interval, n, N, x_pos, y_pos)
        x_ary = np.append(x_neg, x_pos)
        y_ary = np.append(y_neg, y_pos)
    elif h < 0:
        x_ary = np.delete(x_ary, 0)
        y_ary = np.delete(y_ary, 0)        
        x_ary = x_ary[::-1]
        y_ary = y_ary[::-1]
        return x_ary, y_ary
    

    return x_ary, y_ary, h



def Energy_finder(E_guess, n):

    change = 1   
    difference = 100
    diff_prev = difference
    y_a = 0
    current_max = change *0.25
    while abs(difference) > 1E-12:
        #print(current_max)
        while abs(difference) > current_max:
            x_val, y_val, h = Runge_Kutta(E_guess*(change)*1E18, ODE_f_x, ODE_g_x, 1, half_width_box, n, 100)
            difference = y_val[-1]
            if abs(difference/diff_prev) >1:
                change -= current_max*(np.sign(difference))
            else:
                change += current_max*(np.sign(difference))
            print(difference)
            diff_prev = difference
        current_max = current_max/10
        
    Energy = (E_guess*(change)*1E18)
    print('y(a) = {0:.15}\ndifference = {1:.5}\nEnergy = {2:.8}\n'.format(y_val[-1], difference, (Energy)))

    return x_val, y_val, h, difference, change, Energy

def plotter(x, y):
    plt.scatter(x, y, s=.04)
    plt.xlim(-1.2*half_width_box, 1.2*half_width_box)
    plt.ylim(1.1*min(y), 1.1*max(y))
    plt.xlabel('x')
    plt.ylabel(' \u03C8')
    plt.axvline(x=-half_width_box, c='k')
    plt.axvline(x=half_width_box, c='k')
    plt.show()

m=1
x_val, y_val, h, difference, change, E_estimate = Energy_finder(E_initial_guess, m)
x_val, y_val, h = Runge_Kutta(E_estimate, ODE_f_x, ODE_g_x, 1, half_width_box, m, 1000)
plotter(x_val, y_val)
