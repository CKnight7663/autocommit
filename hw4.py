import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as scig

ODE_tst = lambda x, y, z, **kwargs: (7*y**2) * x**3 
ODE_h_x = lambda x, y, z, **kwargs: (-26.2 * (kwargs.get('e') - kwargs.get('v')) * y)


#Constants


Vmax = 10**6                            #'Infinite' potential
half_width_box = 0.5 * (10**-9)         #half width of 1nm box
E_initial_guess = 1E19/26.2               #Initial guess for E
eta = 10**-15
step_size = eta**(.5) 


def V(x, a):
    if abs(x) <= a:
        return 0
    return Vmax




ODE_f_x = lambda x, y, z, **kwargs: z
ODE_h_x = lambda x, y, z, **kwargs: (-26.2 * (kwargs.get('e') - 0) * y)
ODE_g_x = lambda x, y, z, **kwargs: (-26.2 * (kwargs.get('e') - kwargs.get('v')) * y)

def Runge_Kutta(E, f, g, H, interval, n, both, N, *args):
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

    if h > 0 and both:    
        x_pos, y_pos = x_ary, y_ary
        H = -1
        x_neg, y_neg = Runge_Kutta(E, f, g, H, interval, n, both, N, x_pos, y_pos)
        x_ary = np.append(x_neg, x_pos)
        y_ary = np.append(y_neg, y_pos)
    elif h < 0:
        x_ary = np.delete(x_ary, 0)
        y_ary = np.delete(y_ary, 0)        
        x_ary = x_ary[::-1]
        y_ary = y_ary[::-1]
        return x_ary, y_ary
    

    return x_ary, y_ary, h



def Energy_finder(y, y_c, c, accuracy, guess, n):
    #y(x, b) with b some unknown constant. we know y(x=c)=y_c, so we alter b 
    #until we get y(x=c)=y_c within some degree of accuracy
    x_val, y_val, h = Runge_Kutta(guess, ODE_f_x, ODE_g_x, 1, half_width_box, n, False, 100)
    difference = abs(y_c - y_val[c])
    scatter_min, scatter_max = 0.2, 2
    
    while difference > accuracy:
        
        guess_scatter = np.linspace(scatter_min, scatter_max, 10)
        diff_guess = np.zeros(10)
        for i in range(10):
            x_val, y_val, h = Runge_Kutta(guess * guess_scatter[i], ODE_f_x, ODE_g_x, 1, half_width_box, n, False, 100)
            
            diff_guess[i] = abs(y_c - y_val[c])
        
        min_index = np.where(diff_guess == min(diff_guess))
        difference = diff_guess[min_index[0]][0]
        if min_index[0][0]==9:
            i = min_index[0][0]
            current_guess = guess * guess_scatter[i]
            scatter_min = guess_scatter[i] 
            scatter_max = guess_scatter[i] *2
        elif min_index[0][0]==0:
            i = min_index[0][0]
            current_guess = guess * guess_scatter[i]
            scatter_min = guess_scatter[i] /2
            scatter_max = guess_scatter[i] 
        else:
            i = min_index[0][0]
            current_guess = guess * guess_scatter[i]
            scatter_min = guess_scatter[i-1]
            scatter_max = guess_scatter[i+1]
        #print(min(diff_guess))
    guess = current_guess
    #print('\n\nEnergy= ', guess)    
    return guess
    
def plotter(x, y, n, Energy, y_name):
    if ((n-1) % 2) == 0:
        solution_type = 'EVEN'
        n = int((n+1)/2)
    elif ((n-1) % 2) == 1:
        solution_type = 'ODD'
        n = int(n/2)
    
    if (n%10) == 1 and n!=11:
        nth = 'st'
    elif (n%10) == 2 and (n%100)!=12:
        nth = 'nd'    
    elif (n%10) == 3 and (n%100)!=13:
        nth = 'rd'
    else:
        nth = 'th'
    
    plt.plot(x, y)
    plt.xlim(-1.2*half_width_box, 1.2*half_width_box)
    plt.ylim(1.1*min(y), 1.1*max(y))
    plt.xlabel('x')
    if y_name == 'psi':
        plt.ylabel(' \u03C8')
        plt.title('The {0}{2} {1} Soloution, with Energy = {3:.4}'.format(n, solution_type, nth, Energy))
    
    else:
        plt.ylabel(y_name)
        plt.title('The {0}{2} {1} Soloution, Probability Distribution'.format(n, solution_type, nth))
    
    plt.axvline(x=-half_width_box, c='k')
    plt.axvline(x=half_width_box, c='k')
    plt.show()


def numerical_method(y, x, dx, N):
    Y = np.zeros(N)
    y = y**2
    Area = 0
    for i in range(N-1):
        
        Area = y[i+1]*(dx)   
        Y[i] = Area
    #Y /= Y[-1] 
    j=0
    for i in Y:
        j+=i
    
    Y = Y/j
    return Y,j


    
    
def Schro_Infinite_Well(m):
    
    E_estimate = Energy_finder(Runge_Kutta, 0, -1, 1E-15, (m)*E_initial_guess, m)
    x_val, y_val, h = Runge_Kutta(E_estimate, ODE_f_x, ODE_g_x, 1, half_width_box, m, True, 100)
    return E_estimate
    
    plotter(x_val, y_val, m, E_estimate, 'psi')
    
    
    P_total_val, Area = numerical_method(y_val, x_val, h, len(y_val))
    plotter(x_val, P_total_val, m, E_estimate, 'Probability')
    return E_estimate
    
    
E_ary = []
m_ary = []
for m in range(1,5):
    E_m = Schro_Infinite_Well(m)
    E_ary.append(E_m)
    m_ary.append(m)

    
print(E_ary)    
plt.plot(m_ary, E_ary)
plt.show()
