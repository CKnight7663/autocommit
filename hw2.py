#Task 1
import numpy as np 
import matplotlib.pyplot as plt



#Experiment Constants
a_width = .09E-3                                                        #Width of 1 slit
L_distance_x = 480E-3                                                   #Distance from slit to screen
d_distance_y = 0.4E-3                                                   #Distance between slits
b_distance_z = 1E-3                                                     #Height of slits
wavlen = 670E-9                                                         #Wavelength of light

#Experiment Ranges
z_domain_limits = 75E-4                                                 #Range on z-axis
y_domain_limits = z_domain_limits * (3/2)                               #Range on y-axis (3/2 times z as we want a 3:2 aspect ratio)
z_domain_size   = 500                                                   #Size of z-data
y_domain_size   = int(z_domain_size * (3/2))                            #Size of y-data (3/2 times z as we want a 3:2 aspect ratio)






#Functions
def alpha(theta, a):
    #Computes alpha for easier reading and implementation 
    alp = (np.pi * a / wavlen) * np.sin(theta)
    return alp


def beta(theta, d):
    #Computes alpha for easier reading and implementation
    bet = (np.pi * d / wavlen) * np.sin(theta)
    return bet


def Intensity(theta, a, d, slit_bool):
    #function to give the intensity pattern I/I_0
    if slit_bool:                                                                                               #Boolian Value tells us if we want single slit diffraction, or twin slit
        intensity_pattern = (np.sin(alpha(theta, a))/alpha(theta, a))**2 * (np.cos(beta(theta, d)))**2          #a, d variables in place to allow for different slit width and distance between, useful for task 4
    else:
        intensity_pattern = (np.sin(alpha(theta, a))/alpha(theta, a))**2        
    return (intensity_pattern) 



#Array Building
y = np.linspace(-y_domain_limits, y_domain_limits, y_domain_size)                       #Creating an array of y values from given
theta_array = np.arctan(y/L_distance_x)                                                 #and finding the corresponding theta values

intensity_twin_slit_array = Intensity(theta_array, a_width, d_distance_y, True)         #Running the Intensity function for the above theta array, for twin slit



#Plotting
plt.plot(theta_array, intensity_twin_slit_array)
plt.xlabel('Theta (rads)')
plt.ylabel('I/I_0')
plt.title('Twin Slit')
plt.grid()
plt.show()


#Task 2
intensity_single_slit_array = Intensity(theta_array, a_width, d_distance_y, False)      #Rerunning the Inensity function for a single slit

plt.plot(theta_array, intensity_twin_slit_array, label='Twin Slit')
plt.plot(theta_array, intensity_single_slit_array, label='Single Slit')
plt.legend()
plt.xlabel('Theta (rads)')
plt.ylabel('I/I_0')
plt.title('Single and Twin Slit')
plt.grid()
plt.show()
 

#Task 3
#Array Building
z = np.linspace(-z_domain_limits, z_domain_limits, z_domain_size)                       #Build a similar array for z values as done before
phi_array = np.arctan(z/L_distance_x)                                                   #and its corresponding phi angle


def intensity_2D(intensity_y, intensity_z):
    #Function to find the total intensity at a given 2-dimensional point
    intensity_total = intensity_y * intensity_z                                         #Total intensity will just be the product of the two intensitys
    return intensity_total


intensity_y = intensity_twin_slit_array
intensity_z = Intensity(phi_array, a_width, d_distance_y, True)                         #Running Intensity funcion again for the z axis
Y, Z = np.meshgrid(intensity_y, intensity_z)                                            #/////////////////////
X = intensity_2D(Y, Z)                                                                  #/////////////////////

im = plt.imshow(X, cmap=plt.cm.RdBu)                                                    #/////////////////////
plt.show()



#Task 4
intensity_z = Intensity(phi_array, b_distance_z, d_distance_y, False)
Y, Z = np.meshgrid(intensity_y, intensity_z)
X = intensity_2D(Y, Z)

im = plt.imshow(X, cmap=plt.cm.RdBl)
plt.show()