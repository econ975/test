import time
from matplotlib import pyplot as plt
# from scipy.fftpack import fft,ifft
import math
import cv2
from metavision_core.event_io.raw_reader import initiate_device
from metavision_core.event_io.raw_reader import RawReader
from scipy.optimize import curve_fit
import statistics
import pandas as pd
import numpy as np

df=pd.DataFrame()
df = pd.read_csv("C:\\Users\\eee\\Downloads\\2023_06_30 (1)\\2023_06_30\\goodparticle(2)_txt\\spectrum_2 2023 June 30 15_49_08.csv", header=None)
# df = pd.read_csv("C:\\Users\\eee\\Downloads\\2023_06_30 (1)\\2023_06_30\\spectrum_txt\\spectrum_2 2023 June 30 10_57_55.csv", header=None)
# df = pd.read_csv("C:\\Users\\eee\\Downloads\\2023_06_30 (1)\\2023_06_30\\spectrum_txt\\spectrum_2 2023 June 30 12_29_01.csv", header=None)

# print(df)
array = df[4].to_numpy()
# print(array)
b=[]
#
for i in range(1024):
    b.append(631.565+i*(135.317/1023))

# for i in range(1024):
#     b.append(671.752+i*(136.071/1023))

plt.plot(b,array, 'b-')
plt.xlabel("Wavelength (nm)", fontsize = 22, weight='bold')
plt.ylabel("Intensity (a.u.)", fontsize = 22, weight='bold')
plt.tick_params(labelsize=18)
plt.show()

# a=np.array(array[0:][4])
# print(a)

