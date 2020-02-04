import os
import rasterio
from dotenv import find_dotenv, load_dotenv
#above line is only necessary if this is not run in tandem with make_dataset.py
from data_accessor import open_sftp_connection

load_dotenv(find_dotenv())
#above line is only necessary if this is not run in tandem with make_dataset.py

with open_sftp_connection(str(os.environ.get("DIRECTORY_PATH"))) as sftp:
    directory_structure = sftp.listdir_attr()

    # Print data
    for attr in directory_structure:
        if attr.filename[-3:]=='tif':
            print("found 1")
            with rasterio.open(attr.filename) as dataset:
                mask = dataset.dataset_mask()

                for geom, val in rasterio.features.shapes(mask, transform=dataset.transform):
                    geom = rasterio.warp.transform_geom(dataset.crs, 'EPSG:4326', geom, precision=6)
                    print(geom)
