# this file is use to extract a single cylinder from the scene.

import os
import numpy as np
import laspy


output_folder = "Cylinder" 
diameter = 100  
distanceX = 100  
distanceY = 100 
file_path = "368000_4306000.laz"


if not os.path.exists(output_folder):
    os.makedirs(output_folder)

in_file = laspy.read(file_path)

x = in_file.x
y = in_file.y
z = in_file.z

min_x = np.min(x)
max_x = np.max(x)
min_y = np.min(y)
max_y = np.max(y)

num_cylinders_x = int((max_x - min_x) / distanceX)
num_cylinders_y = int((max_y - min_y) / distanceY)

for i in range(num_cylinders_x):
    for j in range(num_cylinders_y):
        center_x = min_x + i * distanceX + diameter / 4
        center_y = min_y + j * distanceY + diameter / 2

        radius = diameter / 2
        mask = ((x - center_x) ** 2 + (y - center_y) ** 2) <= radius ** 2
        
        points_in_cylinder = in_file.points[mask]

        print(f"points_in_cylinder {i}_{j}: {points_in_cylinder.point_format.dimension_names}")

        print(f"Total points in cylinder xxx {i}_{j}: {points_in_cylinder.X}")

        print(f"Total points in cylinder  yyy {i}_{j}: {points_in_cylinder.Y}")

        print(f"Total points in cylinder zzz {i}_{j}: {points_in_cylinder.Z}")

        header = laspy.LasHeader(point_format=3, version="1.2")
        header.add_extra_dim(laspy.ExtraBytesParams(name="random", type=np.int32))
        header.scales = np.array([0.1, 0.1, 0.1])

        out_file = laspy.LasData(header)


        out_file.X = points_in_cylinder.X
        out_file.Y = points_in_cylinder.Y
        out_file.Z = points_in_cylinder.Z


        print(f"outfile header {i}_{j}: {out_file.header}")

        print(f"outfile X values {i}_{j}: {out_file.X}")

        print(f"outfile Y values {i}_{j}: {out_file.Y}")

        print(f"outfile Z values {i}_{j}: {out_file.Z}")


        out_file.write(f"{output_folder}/cylinder_{i}_{j}.laz")



