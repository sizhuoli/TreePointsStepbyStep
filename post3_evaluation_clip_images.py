
# /home/sizhuo/Desktop/code_repository/CNN_AGB/

import os, subprocess
import time
import warnings
from datetime import timedelta
import numpy as np
from tqdm import tqdm

import rasterio
from osgeo import gdal
import geopandas as gpd
from shapely.geometry import box
import sys
# sys.path.append("/home/sizhuo/Desktop/code_repository/CNN_AGB/core")
from core2.data_clipping_util import raster_copy
import ipdb
gdal.SetConfigOption('CPL_LOG', '/dev/null')
warnings.filterwarnings('ignore')  # Disable warnings




def process(image_dir, output_dir_img, areas_fp, pref = '', ftype = '.tif'):
    start = time.time()
    if not os.path.exists(output_dir_img):
        os.makedirs(output_dir_img)


    print("Reading polygons shapefile")
    areas = gpd.read_file(areas_fp)

    print(areas.head())


    print("Assigning areas to input images..  ")
    # Get all input image paths
    image_paths = []

    for root, dirs, files in os.walk(image_dir):

        for file in files:
            if file.endswith(ftype) and file.startswith(pref) and 'merged' not in file:

                image_paths.append(os.path.join(root, file))

    # ipdb.set_trace()
    images_with_areas = []
    for im in tqdm(image_paths):
        # Get image bounds
        with rasterio.open(im) as raster:
            im_bounds = box(*raster.bounds)

        # Get training areas that are in this image
        areas_in_image = np.where(areas.envelope.intersects(im_bounds))[0]
        aim = [str(int(x)) for x in list(areas_in_image)]

        from itertools import zip_longest
        al2 = [''.join(x) for x in map('_'.join, zip_longest(*[aim],fillvalue=''))]
        if len(areas_in_image) > 0:
            # images_with_areas.append((im, [int(x) for x in list(areas_in_image)]))
            images_with_areas.append((im, ([int(x) for x in list(areas_in_image)], al2)))

    print(f"Done. Found {len(image_paths)} tiles of which {len(images_with_areas)} contain rectangles.")

    # ipdb.set_trace()
    # for aerial images, for CHM see below
    # For each input image, get all training areas in the image

    for im_path, area_ids in tqdm(images_with_areas, "Processing images with areas", position=1):
        for l in tqdm(range(len(area_ids[0])), f"Extracting areas for {os.path.basename(im_path)}", position=0):

            area_id = area_ids[0][l]
            al = area_ids[1][l]
            # ipdb.set_trace()
            name = os.path.basename(im_path)
            name = name.split('.')[0]

            output_fp = os.path.join(output_dir_img, f"img_{al}_{name}.tif")
            extract_ds = raster_copy(output_fp, im_path, mode="translate", bounds=areas.bounds.iloc[area_id], compress=False)


    if len(areas) > len(os.listdir(output_dir_img)):
        print(f"WARNING: Training images not found for {len(areas) - len(os.listdir(output_dir_img))} areas!")

    print(f"Image extraction completed in {str(timedelta(seconds=time.time() - start)).split('.')[0]}. \n")


    return images_with_areas






# image_dir = '/mnt/ssdc/Denmark/DK_treeProject_DHI_KDS/thy/images/RGBNIR_downsampled/'
# image_dir = "/mnt/ssda/DK_TreeProject_DHI_KDS/kongernes2019/AOI_images/"
# image_dir = '/mnt/ssdc/Denmark/DK_treeProject_DHI_KDS/predictions/test2_st64_3models_solved_nan/'
# image_dir = '/mnt/ssdc/Denmark/DK_treeProject_DHI_KDS/kongernes/predictions/final_3models_std64/'
image_dir = '/mnt/ssdc/Denmark/DK_treeProject_DHI_KDS/elevation/DHM/'
output_dir_img = "/mnt/ssdc/Denmark/DK_treeProject_DHI_KDS/vis_results/clipped_chms/"
areas_fp = '/mnt/ssdc/Denmark/DK_treeProject_DHI_KDS/vis_results/C_group.shp'

images_with_areas = process(image_dir, output_dir_img, areas_fp, pref = 'DHM', ftype = '.tif')


