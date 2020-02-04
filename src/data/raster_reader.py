import os
import rasterio
from data_accessor import open_sftp_connection

with rasterio.open('') as dataset:
    mask = dataset.dataset_mask()

    for geom, val in rasterio.features.shapes(mask, transform=dataset.transform):
        geom = rasterio.warp.transform_geom(dataset.crs, 'EPSG:4326', geom, precision=6)
        print(geom)
