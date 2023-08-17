'''
input: scene, diameter, distanceX, distanceY
output: downsampled scene
'''


import os
import numpy as np
import h5py
from skimage import exposure
import matplotlib.pyplot as plt
from scipy import ndimage

file_id = input("Enter the cordinates of hyperspectral cube (e.g., 368000_4306000): ")

file_path = f'data/SERC/2017-07/hyperspectral/hyper/NEON_D02_SERC_DP3_{file_id}_reflectance.h5'

file = h5py.File(file_path, 'r')

hyperspectral_data = file['SERC']['Reflectance']['Reflectance_Data'][:]
diameter = int(input("Enter diameter of circle: "))
X = int(input("Enter distance between each radius across (X): "))
Y = int(input("Enter distance between each radius along (Y): "))

x, y = np.meshgrid(np.arange(-diameter/2, diameter/2), np.arange(-diameter/2, diameter/2))
circle_mask = (x**2 + y**2) <= (diameter/2)**2

original_height, original_width, spectral_bands = hyperspectral_data.shape

new_height = original_height // Y
new_width = original_width // X

downsampled_data = np.zeros((new_height, new_width, spectral_bands))

for i in range(new_height):
    for j in range(new_width):
        y_start = i * Y
        y_end = y_start + Y
        x_start = j * X
        x_end = x_start + X
        for band in range(spectral_bands):
            pixel_region = hyperspectral_data[y_start:y_end, x_start:x_end, band]
            circle_average = np.mean(pixel_region[circle_mask])
            downsampled_data[i, j, band] = circle_average

reduced_array = ndimage.gaussian_filter(downsampled_data, sigma=0.6)


if not os.path.exists("LowRes"):
    os.makedirs("LowRes")

filename = 'LowRes/reduced_array.h5'
with h5py.File(filename, 'w') as f:
    f.create_dataset('data', data=reduced_array)

print(f"Saved reduced array with shape {reduced_array.shape} to {filename}.")

####################################################################################################

"""
Display output
"""

folder_path = 'LowRes'

file_list = os.listdir(folder_path)

h5_files = [file for file in file_list if file.endswith('.h5')]
if len(h5_files) == 0:
    print("No .h5 files found in the folder.")
    exit()

file_name = h5_files[0]

file_path = os.path.join(folder_path, file_name)

file = h5py.File(file_path, 'r')

def printName(name,node):
    if isinstance(node, h5py.Dataset):
        print(name)
file.visititems(printName)

def printNodes(name,node):
    if isinstance(node, h5py.Dataset):
        print(node)
file.visititems(printNodes)

serc_refl = file['data']

refl_shape = serc_refl.shape

print("shape of file:",serc_refl.shape)

np3D = np.array(serc_refl)

b56 = serc_refl[:,:,55].astype(float)
serc_ext = [0, 100, 0, 100]

def linearStretch(percent):
    pLow, pHigh = np.percentile(b56[~np.isnan(b56)], (percent, 100 - percent))
    img_rescale = exposure.rescale_intensity(b56, in_range=(pLow, pHigh))
    plt.imshow(img_rescale, extent=serc_ext, cmap='gist_earth')
    plt.title('SERC Band 56 \n Linear ' + str(percent) + '% Contrast Stretch')
    ax = plt.gca()
    ax.ticklabel_format(useOffset=False, style='plain')
    rotatexlabels = plt.setp(ax.get_xticklabels(), rotation=90)
    plt.show()

linearStretch(25)


####################################################################################################

"""
Delete all .h5 files in the folder
"""

# Filter the list to only include .h5 files
h5_files = [file for file in file_list if file.endswith('.h5')]

# Remove each .h5 file in the folder
for file_name in h5_files:
    file_path = os.path.join(folder_path, file_name)
    os.remove(file_path)

print("All .h5 files have been deleted for sake of memory.")

