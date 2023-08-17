# this file is used to plot the HH slices.

import h5py
import numpy as np
import matplotlib.pyplot as plt

"""
types of data in the .h5 file:
                            ultimateTruth
                            downsampled_data
"""
file_path = "366000_4306000.h5"
with h5py.File(file_path, 'r') as file:
    print(list(file.keys()))
    HH = file['downsampled_data'][:]

print("shape of output: ", HH.shape)


cake = HH[:, 9, :]

def normalize(cake):
    for i in range(cake.shape[1]):
        if np.max(cake[:, i]) != 0:
            cake[:, i] = cake[:, i] / (np.max(cake[:, i]))
    return cake

normi = normalize(cake)
normi_max = np.max(normi)
cake_max = np.max(cake)

print("shape of normi", normi.shape)
print("max of normi", normi_max)
print("max of cake", cake_max)

normi_landscape = np.flip(normi, axis=0) 
plt.imshow(normi_landscape, cmap='gray_r')  
plt.title('HH, slice 10')
plt.show()