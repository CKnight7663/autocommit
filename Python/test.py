import numpy as np 
import matplotlib.pyplot as plt

a = np.linspace(1, 100, 100)
b = a**2

def fun(*args):
    print(y)
y=5
fun(y)
print(a)
plt.plot(a,b)
plt.show()


def Energy_finder(n):
    
    change = 1   
    difference = 1
    y_a = 0
    current_max = 0.5
    while abs(difference) > 1E-8:
        current_max = current_max/10
        while abs(difference) > current_max:
            change += current_max*(np.sign(difference))
            x_val, y_val, h = Runge_Kutta(E_initial_guess*(change)*1E18, ODE_f_x, ODE_g_x, 1, half_width_box, 1, 0, 100)
            
            
            difference = y_val[-1]
            y_a = y_val[-1]