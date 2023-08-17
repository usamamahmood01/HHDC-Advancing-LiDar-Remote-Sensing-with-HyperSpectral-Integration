import requests
from neon_aop_download_functions import *
from config import *

url = "https://raw.githubusercontent.com/NEONScience/NEON-Data-Skills/main/tutorials/Python/Lidar/intro-lidar/intro_point_clouds_py/neon_aop_download_functions.py"
response = requests.get(url)
open("neon_aop_download_functions.py", "wb").write(response.content)

print("Path of downloaded dataset:", root_path)


#   ==>> download the QA reports to the default download directory (./data)
#download_aop_files(dpID,site,year,SERC_2017_hyperprocess, match_string='.pdf',check_size=False)

# ==>> download the .shp file in the shp folder
download_aop_files(dpID,site,year,SERC_2017_shp_path,'.shp',check_size=False)
download_aop_files(dpID,site,year,SERC_2017_shp_path,'.shx',check_size=False)
print(os.listdir(SERC_2017_shp_path))

# ==>> download the .kml file in the kml folder
download_aop_files(dpID,site,year,SERC_2017_kml_path, match_string='.kml',check_size=False)

# ==>> download the .laz files in the laz folder (this may take a while)
download_aop_files(dpID,site,year,SERC_2017_laz_path,match_string='.laz')

 
# ==>> download the .h5 files in the hyper_path folder (this may take a while)
download_aop_files(dpID,site,year,SERC_2017_hyper_path,match_string='.h5', check_size=False)
