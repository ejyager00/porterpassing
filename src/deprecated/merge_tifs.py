import os
import rasterio
from rasterio.merge import merge

def merge_tifs(directory, new_directory=None):
    files = os.listdir(directory)
    tif_files = []
    for filename in files:
        if filename[-4:]=='.tif':
            tif_files.append(rasterio.open(directory + filename))
    mosaic, out_trans = merge(tif_files)
    out_meta = tif_files[0].meta.copy()
    out_meta.update({"driver": "GTiff",
                     "height": mosaic.shape[1],
                     "width": mosaic.shape[2],
                     "transform": out_trans,
                     "crs": "+proj=utm +zone=35 +ellps=GRS80 +units=m +no_defs "
                     })
    if new_directory==None:
        new_directory=directory
    with rasterio.open(new_directory + 'mosaic.tif', "w", **out_meta) as dest:
        dest.write(mosaic)
    for file in tif_files:
        file.close()

if __name__ == '__main__':
    merge_tifs('data/raw/', 'data/interim/')
