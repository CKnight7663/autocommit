import numpy as np 
import matplotlib.pyplot as plt

x = np.linspace(-100, 100, 101)
y = []
for i in x:
    y.append(i**2)

print(x[5], y[5])


plt.plot(x,y)
plt.show() 