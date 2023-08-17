"""
input: distanceX, distanceY, diameter, file_path, downsample = False, remove_nosie = False
output: ultimateTruth, downsampled_data
"""

import numpy as np
import laspy
import h5py
from scipy import stats

def HH(distanceX, distanceY, diameter, file_path, downsample = False, remove_nosie = False):
    las = laspy.read(file_path)

    if len(las.z) != 0 and remove_nosie:
        z_lower_percentile = np.percentile(las.z, 0.1) 
        z_upper_percentile = np.percentile(las.z, 99.9)

        noise_mask = (las.z >= z_lower_percentile) & (las.z <= z_upper_percentile)
        
        filtered_points = las[noise_mask]

    x = filtered_points.x
    y = filtered_points.y
    z = filtered_points.z

    min_x = np.min(x)
    max_x = np.max(x)
    min_y = np.min(y)
    max_y = np.max(y)

    num_cylinders_x = int((max_x - min_x) / (distanceX))
    num_cylinders_y = int((max_y - min_y) / (distanceY))

    maxHeight = np.max(z)
    minHeight = np.min(z)
    num_height_bins = int((maxHeight - minHeight) * 2)

    ultimateTruth = np.empty((num_cylinders_x, num_cylinders_y, num_height_bins))

    alturasFp = np.linspace(minHeight, maxHeight ,num_height_bins+1)
    
    gausSigma  = 6.0 / (2.355)
    gaussian = stats.norm(loc=0, scale=gausSigma)

    for i in range(num_cylinders_x):
        for j in range(num_cylinders_y):

            radius = diameter / 2

            center_x = min_x + i * distanceX + radius
            center_y = min_y + j * distanceY + radius

            mask = ((x - center_x) ** 2 + (y - center_y) ** 2) <= radius ** 2
            points_in_cylinder_z = z[mask]

            if (len(points_in_cylinder_z) > 25) and downsample:
                distances = np.sqrt((x[mask] - center_x) ** 2 + (y[mask] - center_y) ** 2)
                probs = gaussian.pdf(distances)
                probs = probs / np.sum(probs)
                num_samples = np.random.randint(18, 23)
                selected_indices = np.random.choice(np.arange(len(points_in_cylinder_z)), num_samples, p=probs)
                fp = points_in_cylinder_z[selected_indices]
            else:
                fp = points_in_cylinder_z

            hist = np.histogram(fp, bins=alturasFp)[0]

            ultimateTruth[i][j] = hist

            print("Cylinder {} of {}".format(i * num_cylinders_y + j + 1, num_cylinders_x * num_cylinders_y))

    ultimateTruth = np.transpose(ultimateTruth)

    return ultimateTruth

file_id = input("Enter the cordinates of hyperspectral cube (e.g., 368000_4306000): ")
distanceX = int(input("Enter diameter of circle: "))
distanceY = int(input("Enter distance between each radius across (X): "))
diameter = int(input("Enter distance between each radius across (Y): "))


file_path = f'data/SERC/2017-07/laz/laz/NEON_D02_SERC_DP1_{file_id}_classified_point_cloud_colorized.laz'


ultimateTruth = HH(distanceX, distanceY, diameter, file_path, downsample=False, remove_nosie=True)
downsampled_data = HH(distanceX, distanceY, diameter, file_path, downsample=True, remove_nosie=True)

file_path = file_id+".h5"
with h5py.File(file_path, 'w') as file:
    file.create_dataset('ultimateTruth', data=ultimateTruth)
    file.create_dataset('downsampled_data', data=downsampled_data)
