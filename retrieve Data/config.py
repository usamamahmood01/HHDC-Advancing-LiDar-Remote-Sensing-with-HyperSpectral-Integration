# liDar dpID: DP1.30003.001
# HyperSpectral dpID: DP3.30006.001

"""
Sites available:
YELL, WREF, WOOD, WLOU, UNDE, UKFS, TREE, TOOL, TEAK, TALL, SYCA, STER, STEI, SRER ,SOAP,
SJER, SERC, SCBI, RMNP, REDB, PUUM, PRIN, OSBS, ORNL, ONAQ, OAES, NOGP, NIWO, MOAB, MLBS,
MCRA, MCDI, LIRO, LENO, LAJA, KONZ, KONA, JORN, JERC, HOPB, HEAL, HARV, GUIL, GUAN, GRSM,
DSNY, DELA, DEJU, DCFS, CUPE, CPER, CLBJ, BONA, BLUE, BLAN, BART, BARR, ARIK, ABBY
"""


# this config file is used to set the path of the data,
# and the dpID and site of the data and the year of the data.
# currently, the year is set to 2017-07, and the site is set to SERC
# the dpID is set to DP3.30006.001, which is the hyperspectral data

dpID = 'DP3.30006.001'
site = 'SERC'

year='2017-07'

root_path = './data/'+site+'/'+year
SERC_2017_shp_path = root_path+'/laz/shp'
SERC_2017_kml_path = root_path+'/laz/kml'
SERC_2017_laz_path = root_path+'/laz/laz'
SERC_2017_hyper_path = root_path+'/hyperspectral/hyper'
SERC_2017_hyperprocess = root_path+'/hyperspectral/process'
