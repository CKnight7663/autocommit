import numpy as np
import matplotlib.pyplot as plt

#Physical Constants
k = 1.38 * (10**(-23))      #J K^-1
c = 3 * (10**(8))           #m s^-1
h = 6.63 * (10**(-34))      #J s

#Programme Constants
freq_lim_lower = 10**11 
freq_lim_upper = 10**15
freq_lim_upper_2 = .3 * 10**15
temp_min = 2000
temp_max = 6000
user_input_freq = eval(input('Enter test frequency: '))
user_input_temp = eval(input('Enter test temperature: '))


#Functions Definitions
def Ray_J_U(nu_freq, Temp):
    #This is the formal for Intesity from Rayleigh-Jeans 
    U = (8 * np.pi * (nu_freq**2) * k * Temp) / (c**3)
    return U


def Plank_U(nu_freq,Temp):
    #This is the formula for Intesity using Planks adhusted method to account high frequecy
    U = (8 * np.pi * h * (nu_freq**3)) / ((c**3) * np.e**((h*nu_freq)/(k * Temp)) - 1)
    return U


#Function Calls

#print(Ray_J_U(user_input_freq, user_input_temp))


#Array Building - We want to build arrays for freq in the range given, and an empy array for the Intensity U, for both Plank and Ray J formulas
ray_plot_freq = np.linspace(freq_lim_lower, freq_lim_upper_2, 100)
ray_plot_U = np.zeros(100)

plank_plot_freq = np.linspace(freq_lim_lower, freq_lim_upper, 100)

temp_range = np.linspace(temp_min, temp_max, 3)
plank_U_peak = np.zeros(len(temp_range))
plank_freq_peak = np.zeros(len(temp_range))
wavelen_peak = np.zeros(len(temp_range))

area_under_curve_array = np.zeros(len(temp_range))





#Function Runs
for i in range(100):
    ray_plot_U[i] = Ray_J_U(ray_plot_freq[i], 2000)             #Running the Ray J formula for the frequency range given

#Here we want to create three plots for Plank, sitting at diffent Temperatures




for i in range(len(temp_range)):
    plank_plot_U = np.zeros(100)                                #Resets Array each run
    for j in range(100):
        plank_plot_U[j] = Plank_U(plank_plot_freq[j], temp_range[i])        #Runs our Plank formula for each frequency given at the current temperature 
        if plank_plot_U[j] > plank_plot_U[j-1]:
            plank_U_peak[i] = plank_plot_U[j]
    for l in range(100):
        if plank_plot_U[l] >= plank_U_peak[i]:
            plank_U_peak[i] = plank_plot_U[l]
            plank_freq_peak[i] = plank_plot_freq[l]
    
    plt.plot(plank_plot_freq, plank_plot_U)                     #Plots this temp graph, and runs to the next.
    plt.plot(plank_freq_peak[i], plank_U_peak[i], 'ro')
    wavelen_peak[i] = c / plank_freq_peak[i]
    



    Area_Under_Curve = 0
    for j in range(1, 100):
        df = plank_plot_freq[j] - plank_plot_freq[j-1]
        dA = plank_plot_U[j] * df
        Area_Under_Curve += dA
    area_under_curve_array[i] = Area_Under_Curve


for i in range (len(temp_range)):
    print('For wavelength peak {0:.4}m the constant is {1:.4}'.format(wavelen_peak[i], wavelen_peak[i] * temp_range[i]))

for i in range(len(temp_range)):
    sigma = area_under_curve_array[i] / (temp_range[i]**4)

    print('Area under {0:.4} K curve is {1:.4}, and ratio is {2:.4}'.format(temp_range[i], area_under_curve_array[i], sigma)) 



print(plank_freq_peak, plank_U_peak)
for i in range(100):
    ray_plot_U[i] = Ray_J_U(ray_plot_freq[i], 2000)             #Running the Ray J formula for the frequency range given





plt.plot(ray_plot_freq, ray_plot_U, ':')
plt.xlabel('Frequency: Hz^-1')
plt.plot()

plt.ylabel('Intensity U: W m^-2')
plt.title('Rayleigh-Jeans Law vs Planks Law')
#plt.yscale('log')
#plt.xscale('log')
plt.show()

