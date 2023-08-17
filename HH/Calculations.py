# this file is used to calculate the DTM, DEM, and CHM from the .h5 file and plot them.

import h5py
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import median_filter

def compute_DTM_DEM_CHM(h5_file_path, DTMthreshold=0.02, DEMthreshold=0.98):
    with h5py.File(h5_file_path, 'r') as h5_file:
        hhdc = h5_file['downsampled_data'][:]

    print("shape of output: ", hhdc.shape)
    print("max of Z: ", np.max(hhdc.shape[0]))

    pdf_denominator = np.sum(hhdc, axis=0)
    pdf_denominator[pdf_denominator == 0] = 1
    pdf = np.divide(hhdc, pdf_denominator, where=(pdf_denominator != 0), out=np.zeros_like(hhdc))

    cdf = np.cumsum(pdf, axis=0)

    DTM = np.zeros((hhdc.shape[1], hhdc.shape[2]))
    for x in range(hhdc.shape[1]):
        for y in range(hhdc.shape[2]):
            dtm_height = np.argmax(cdf[:, x, y] >= DTMthreshold)
            
            DTM[x, y] = dtm_height if dtm_height >= 0 else 0

    DEM = np.zeros((hhdc.shape[1], hhdc.shape[2]))
    for x in range(hhdc.shape[1]):
        for y in range(hhdc.shape[2]):
            dem_height = np.argmax(cdf[:, x, y] >= DEMthreshold)
            DEM[x, y] = dem_height if dem_height >= 0 else 0

    DTM = median_filter(DTM, size=9)


    print("max of DEM: ", np.max(DEM))
    print("min of DEM: ", np.min(DEM))

    print("max of DTM: ", np.max(DTM))
    print("min of DTM: ", np.min(DTM))

    max_diff = np.max(DEM) - np.max(DTM)
    min_diff = np.min(DEM) - np.min(DTM)
    CHM = np.clip(DEM - DTM, min_diff, max_diff)

    print("max of CHM: ", np.max(CHM))
    print("min of CHM: ", np.min(CHM))


    plt.figure(figsize=(12, 10))
    plt.grid(False)

    plt.gca().set_facecolor('white')
    plt.subplot(131)
    plt.imshow(np.flip(DTM, axis= 0), cmap='viridis', vmin=np.min(DTM), vmax=np.max(DTM)) 
    plt.axis('off')
    plt.colorbar(shrink=0.5)
    plt.title('Digital Terrain Model (DTM)')

    plt.subplot(132)
    plt.imshow(np.flip(DEM, axis=0), cmap='viridis', vmin=np.min(DEM), vmax=np.max(DEM))
    plt.axis('off')
    plt.colorbar(shrink=0.5)
    plt.title('Digital Elevation Model (DEM)')

    plt.subplot(133)
    plt.imshow(np.flip(CHM, axis=0), cmap='viridis', vmin=np.min(CHM), vmax=np.max(CHM))
    plt.axis('off')
    plt.colorbar(shrink=0.5)
    plt.title('Canopy Height Model (CHM)')

    plt.tight_layout()
    plt.show()

h5_file_path = '366000_4306000.h5'
compute_DTM_DEM_CHM(h5_file_path)
