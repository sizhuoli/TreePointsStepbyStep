import os
from subprocess import call
import glob
import tqdm

rgb_dir = "/mnt/ssdc/Denmark/DK_treeProject_DHI_KDS/thy/images/RGB/"
nir_dir = "/mnt/ssdc/Denmark/DK_treeProject_DHI_KDS/thy/images/NIR/"
output_dir = "/mnt/ssdc/Denmark/DK_treeProject_DHI_KDS/thy/images/RGBNIR/"


rgb_files = glob.glob(rgb_dir + "1km*.tif")

for rgb_file in tqdm.tqdm(rgb_files):
    nir_path = rgb_file.replace(rgb_dir, nir_dir)
    output_path = rgb_file.replace(rgb_dir, output_dir)

    # Run gdal_merge.py command
    call(["gdal_merge.py", "-separate", "-o", output_path, rgb_file, nir_path])
    # print(f"Merged: {output_path}")
