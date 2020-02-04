import os
import rasterio
import rasterio.features
import rasterio.plot
import numpy as np
from data_accessor import open_sftp_connection

files = os.listdir('data/raw')

for filename in files:
    if filename[-4:]=='.tif':
        print("\n")
        print(filename)
        with rasterio.open('data/raw/' + filename) as dataset:
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

            rasterio.plot.show(dataset)
