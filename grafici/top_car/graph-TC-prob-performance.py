
from matplotlib import pyplot as plt
import numpy as np

p = np.arange(0.05, 1.01, 0.05)

N_CARS_LUX = 790
N_CARS_NY = 600
N_CARS_COL = 436



# LUXEMBURG - 1000
recv_lux = np.array([0.71, 5.12, 10.58, 13.84, 15.93, 19.3, 30.15, 36.66, 40.79, 42.38, 52.51, 53.83, 57.2, 68.13, 72.48, 70.73, 82.7, 86.76, 93.63, 99]) / 100
relay_lux = np.array([0.26, 4.065, 12.5, 21.9, 31.56, 45.84, 83.23, 115.83, 144.85, 167.77, 229.29, 254.4, 293.18, 377.255, 428.59, 446.59, 555.0225, 616.9, 702.75, 760.125]) / N_CARS_LUX
fig, ax = plt.subplots()
p1 = ax.plot(p, recv_lux)
p2 = ax.plot(p, relay_lux)
p3 = ax.plot(p, recv_lux-relay_lux)
ax.legend((p1[0],p2[0],p3[0]), ['Receivers', 'Relay', 'Difference'])
plt.xticks(np.arange(0, 1.1, 0.1))
plt.yticks(np.arange(0, 1.1, 0.1))
plt.title("Luxembourg, probabilistic alg")
plt.show()
plt.close()

# -->  optimal at circa P=75%




# NEW YORK - 5003
recv_ny = np.array([0.65, 3.9, 8.9, 17.99, 25.96, 28.46, 33.86, 42.18, 43.04, 49.82, 55.34, 54.66, 61.91, 70.65, 70.94, 78.95, 79.96, 84.72, 92.49, 99]) / 100
relay_ny = np.array([0.18, 2.5, 7.8, 21.86, 39.37, 51.0975, 71.16, 100.79, 116.4475, 148.9, 183.1025, 197, 241.28, 296.07, 319.75, 379.25, 407.46, 457.23, 526.91, 581.945]) / N_CARS_NY
fig, ax = plt.subplots()
p1 = ax.plot(p, recv_ny)
p2 = ax.plot(p, relay_ny)
p3 = ax.plot(p, recv_ny-relay_ny)
ax.legend((p1[0],p2[0],p3[0]), ['Receivers', 'Relay', 'Difference'])
plt.xticks(np.arange(0, 1.1, 0.1))
plt.yticks(np.arange(0, 1.1, 0.1))
plt.title("New York, probabilistic alg")
plt.show()
plt.close()

# -->  optimal at circa P=70%


# COLOGNE - 1000
recv_col = np.array([0.48,0.97,1.71,2.14,4.11,5.42,7.23,8.50,12.98,15.69,22.44,28.98,31.16,40.27,47.53,53.66,62.74,71.87,84.38,99.19]) / 100
relay_col = np.array([0.115,0.445,1.1325,1.8,4.49,7.07,10.8775,15.01,25.375,34.3675,53.605,75.94,88.6725,123.05,155.6275,187.0325,232.6225,281.735,349.585,415.035]) / N_CARS_COL
fig, ax = plt.subplots()
p1 = ax.plot(p, recv_col)
p2 = ax.plot(p, relay_col)
p3 = ax.plot(p, recv_col-relay_col)
ax.legend((p1[0],p2[0],p3[0]), ['Receivers', 'Relay', 'Difference'])
plt.xticks(np.arange(0, 1.1, 0.1))
plt.yticks(np.arange(0, 1.1, 0.1))
plt.title("Cologne, probabilistic alg")
plt.show()
plt.close()

# -->  optimal at circa P=75%




