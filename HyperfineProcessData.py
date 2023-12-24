import csv
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np

def lorentz(E, I0, E0, gamma0, I1, E1, gamma1,I2,E2,gamma2, b, c):
    return (I0 * ((gamma0 ** 2) / (((E - E0) ** 2) + gamma0 ** 2)) + I1 * ((gamma1 ** 2) / (((E - E1) ** 2) + gamma1 ** 2)) + I2 * ((gamma2 ** 2) / (((E - E2) ** 2) + gamma2 ** 2)) + b * E + c)

freq=[]
Intensity=[]

for line in open("C:\\Users\\eee\\Desktop\\Yuxi Programs\\ODMR_Yuxi_MagneticField.txt"):
# for line in open("C:\\Users\\eee\\Desktop\\cwodmr\\Hyperfine\\6(8dBm).txt"):
# for line in open("C:\\Users\\eee\\Desktop\\cwodmr\\Hyperfine\\1.txt"):
    listWords = line.split("\t")
    freq.append(round(float(listWords[0]),5))
    Intensity.append(float(listWords[1]))

print(freq)
print(Intensity)

# popt, pcov = curve_fit(lorentz, freq, Intensity, maxfev=50000, p0=[(max(Intensity) - min(Intensity)), 2.87461544, 0.0005, (max(Intensity) - min(Intensity)), 2.87678544, 0.0005,(max(Intensity) - min(Intensity)), 2.87896544, 0.0005, 1, max(Intensity)])
# # popt,pcov = curve_fit(lorentz,xdata,ydata,maxfev=5000, p0=[(max(ydata)-min(ydata)),2870,5,1,max(ydata)])
#
# print(popt)
# print("Splitting: " + str(1000*(popt[4]-popt[1])))
# print("Splitting: " + str(1000*(popt[7]-popt[4])))

# xfit = np.arange(2.8725, 2.8825, 0.0001)
# plt.plot(xfit, lorentz(xfit, *popt), 'g-', label='Lorentz',linewidth=5)

# plt.plot(freq, Intensity, 'bo', label='Data',markersize='1')
plt.plot(freq, Intensity, 'bo', label='Data')
plt.legend()
plt.xlabel('Microwave Frequency (MHz)', fontsize=24)
plt.ylabel('Intensity', fontsize=24)
plt.show()

# reader = csv.reader(open("C:\\Users\\eee\\Desktop\\cwodmr\\Hyperfine\\6(8dBm)(200steps_20averages).txt"), delimiter=" ")
#
# print(reader)

# try:
#     reader = csv.DictReader(f)
#     for row in reader:
#         print(row)
# finally:
#     f.close()