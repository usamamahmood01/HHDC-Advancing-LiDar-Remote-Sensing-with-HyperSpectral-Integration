# this file is used to display the lidar data in 3D.

import laspy
import numpy as np
import pyvista as pv
from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

import os


def plot3D(file):
    laz_data_file_classified=os.path.join(file)
    laz_data_file_classified=laspy.read(laz_data_file_classified)
    points = np.vstack([laz_data_file_classified.x, laz_data_file_classified.y, laz_data_file_classified.z]).T

    print("Length of total points", len(points))

    print("Dimensions: ", laz_data_file_classified.point_format.dimension_names)

    print("max z", np.max(points[:,2]))
    print("min z", np.min(points[:,2]))

    print("max x", np.max(points[:,0]))
    print("min x", np.min(points[:,0]))

    print("max y", np.max(points[:,1]))
    print("min y", np.min(points[:,1]))


    cloud = pv.PolyData(points)

    normalized_depth = (points[:, 2] - np.min(points[:, 2])) / (np.max(points[:, 2]) - np.min(points[:, 2]))

    colormap = cm.get_cmap("viridis")

    colors = colormap(normalized_depth)

    cloud.point_data["colors"] = colors

    plotter = pv.Plotter()

    plotter.background_color = "white"


    plotter.add_mesh(cloud, scalars="colors", point_size=2)
    

    plotter.show()

file1 = "368000_4306000.laz"

file = "Cylinder/cylinder_1_9.laz"

plot3D(file1)


def plot_z_axis(file):
    laz_data_file_classified = os.path.join(file)
    laz_data_file_classified = laspy.read(laz_data_file_classified)

    points = np.vstack([laz_data_file_classified.x, laz_data_file_classified.y, laz_data_file_classified.z]).T

    z_values = points[:, 2]

    plt.figure(figsize=(8, 6))
    cmap = cm.get_cmap('viridis')
    norm = Normalize(vmin=np.min(z_values), vmax=np.max(z_values))
    sc = plt.scatter(points[:, 0], points[:, 2], s=1, c=z_values, cmap=cmap, norm=norm)
    
    cbar = plt.colorbar(sc, label='Z-axis Value')
    
    plt.xlabel('X')
    plt.ylabel('Z')
    plt.grid(True)
    
    plt.show()

plot_z_axis(file)


def plot_height_distribution(file):
    laz_data_file_classified = os.path.join(file)
    laz_data_file_classified = laspy.read(laz_data_file_classified)

    points = np.vstack([laz_data_file_classified.x, laz_data_file_classified.y, laz_data_file_classified.z]).T

    z_values = points[:, 2]

    n, bins = np.histogram(z_values, bins=100)
    bin_centers = (bins[:-1] + bins[1:]) / 2

    plt.figure(figsize=(8, 6))
    plt.plot(bin_centers, n, color='red', label='Height Distribution')
    plt.xlabel('Height (m)')
    plt.ylabel('Normalized Cumulative')
    plt.title('Height Distribution and Cumulative Distribution')

    cum_dist = np.cumsum(n) / np.sum(n)

    ax2 = plt.gca().twinx()
    ax2.plot(bin_centers, cum_dist, color='blue', label='Cumulative Distribution')
    ax2.set_ylabel('Cumulative Probability', color='blue')

    percentiles = [0, 25, 50, 75, 99]
    percentile_values = np.percentile(z_values, percentiles)

    for p, v in zip(percentiles, percentile_values):
        ax2.annotate(f'{p}th: {v:.2f}', xy=(v, cum_dist[np.searchsorted(bin_centers, v)]),
                            xytext=(5, 0), textcoords='offset points', color='blue')
        ax2.axvline(x=v, color='green', linestyle='--', linewidth=1)
    
        

    plt.show()



plot_height_distribution(file)




