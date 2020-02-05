import os
import rasterio
import rasterio.features
from rasterio.plot import show
from rasterio.merge import merge
import glob
import numpy as np
from data_accessor import open_sftp_connection

def tif_summary(filename):
    with rasterio.open('data/raw/' + filename) as dataset:
        print("\n")
        print(filename)
        raster_summary(dataset)

def raster_summary(dataset):
    mask = dataset.dataset_mask()

    for geom, val in rasterio.features.shapes(mask, transform=dataset.transform):
        geom = rasterio.warp.transform_geom(dataset.crs, 'EPSG:4326', geom, precision=6)
        print(geom)

    array = dataset.read()
    stats = []

    for band in array:
        stats.append({
        'min': band.min(),
        'mean': band.mean(),
        'median': np.median(band),
        'max': band.max()})

    for thing in stats:
        print(thing)

    show(dataset)

files = os.listdir('data/raw')
tif_files = []
las_files = []

for filename in files:
    if filename[-4:]=='.tif':
        tif_files.append(filename)
    elif filename[-4]=='.las':
        las_files.append(filename)
