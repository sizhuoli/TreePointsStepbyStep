import numpy as np
import rasterio
import matplotlib.pyplot as plt
from scipy import ndimage as ndi
from skimage.feature import peak_local_max
import ipdb
import geopandas as gpd
from shapely.geometry import Point


def heat2map(heatmap, chm, elevation, image, output, min_dis = 2, thres_abs = 0.001, alpha = 0.2, height_window = 5, low_vege = 3, ndvi_tree = 0.2, scan_window = 10):
    with rasterio.open(heatmap) as src1:
        heat = src1.read(1)
        # filter out ground/buildings using ndvi mask
        with rasterio.open(image) as src:
            # calculate ndvi from 4 band image, nir is band 4, red is band 1
            img = src.read()
            denominator = img[3].astype(float) + img[0].astype(float)
            # ipdb.set_trace()
            ndvi = np.where(denominator == 0, -1,
                            (img[3].astype(float) - img[0].astype(float)) / denominator)
            # filter out ground or buildings
            assert ndvi.shape == heat.shape
            heat[ndvi < 0] = 0 # only filter out very low ndvi
            thress = max(heat.max() * alpha, thres_abs)
            coords = peak_local_max(heat, min_distance=min_dis, threshold_abs=thress)

            with rasterio.open(chm) as src2:
                height = src2.read(1)
                height = ndi.zoom(height, (heat.shape[0]/height.shape[0], heat.shape[1]/height.shape[1]))

                with rasterio.open(elevation) as src3:
                    elev = src3.read(1)
                    elev = ndi.zoom(elev, (heat.shape[0]/elev.shape[0], heat.shape[1]/elev.shape[1]))
                    point_height = []
                    point_elev = []
                    scanned_area = np.zeros_like(height)
                    if len(coords) != 0:
                        for c in coords:
                            x, y = c
                            point_height.append(height[max(0, x-height_window):min(height.shape[0], x+height_window), max(0, y-height_window):min(height.shape[1], y+height_window)].max())
                            point_elev.append(elev[max(0, x-height_window):min(elev.shape[0], x+height_window), max(0, y-height_window):min(elev.shape[1], y+height_window)].max())
                            # a binary mask to record scanned area on the height map, window to deal with the shift between optical and lidar and should cover the entire tree
                            scanned_area[max(0, x-scan_window):min(height.shape[0], x+scan_window), max(0, y-scan_window):min(height.shape[1], y+scan_window)] = 1

                    # detect peaks from height also
                    thres_h = height.copy()
                    thres_h[thres_h < low_vege] = 0 # filter out low vegetation
                    thres_h[scanned_area == 1] = 0
                    thres_h[ndvi < ndvi_tree] = 0
                    # ipdb.set_trace()
                    coords2 = peak_local_max(thres_h, min_distance=8, threshold_abs=low_vege, num_peaks=20000)
                    if len(coords2) != 0:
                        for c in coords2:
                            x, y = c
                            point_height.append(height[max(0, x-height_window):min(height.shape[0], x+height_window), max(0, y-height_window):min(height.shape[1], y+height_window)].max())
                            point_elev.append(elev[max(0, x-height_window):min(elev.shape[0], x+height_window), max(0, y-height_window):min(elev.shape[1], y+height_window)].max())


                point_height = np.array(point_height)
                point_elev = np.array(point_elev)
                # save to file
                transform = src1.transform
                crs = src1.crs
                # merge coords
                coords = np.concatenate([coords, coords2])
                if len(coords) != 0:
                    geo_points = [Point(transform * (y, x)) for x, y in coords]
                    gdf = gpd.GeoDataFrame(geometry=geo_points, crs=crs)
                    gdf['TreeHeight'] = point_height
                    gdf['TreeElevation'] = point_elev
                    # remove points with height < 1 m
                    gdf = gdf[gdf['TreeHeight'] >= 1]
                    gdf.to_file(output, driver='GPKG')
                else:
                    gdf = gpd.GeoDataFrame(geometry=[], crs=crs)
                    gdf.to_file(output, driver='GPKG')
    del heat, height, elev, coords, point_height, point_elev, geo_points, gdf
    return


def main(args):
    # process whole dir
    import os
    import glob
    from tqdm import tqdm
    heatmaps = glob.glob(args.heatmap_dir + '1km*density.tif')
    print(f'Found {len(heatmaps)} heatmaps (tree density maps) to process')
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    chm_missing = []
    elevation_missing = []
    processing_error = []
    for heat in tqdm(heatmaps):
        locate = heat.split('/')[-1].split('_')[1] + '_' + heat.split('/')[-1].split('_')[2]
        try:
            chm = glob.glob(args.chm_dir + f'**/*{locate}*.tif', recursive=True)[0]
        except:
            chm_missing.append(locate)
            print(f'No chm found for {locate}')
            continue
        try:
            elevation = glob.glob(args.elevation_dir + f'**/*{locate}*.tif', recursive=True)[0]
        except:
            elevation_missing.append(locate)
            print(f'No elevation found for {locate}')
            continue
        # try:
        ipdb.set_trace()
        image = glob.glob(args.image_dir + f'*{locate}*.tif', recursive=True)[0]
        output = os.path.join(args.output_dir, f'1km_{locate}_treeCenters.gpkg')
        heat2map(heat, chm, elevation, image, output, min_dis=args.min_dis, thres_abs=args.thres_abs, alpha = args.alpha, height_window=args.height_window, low_vege=args.low_vege, ndvi_tree=args.ndvi_tree, scan_window=args.scan_window)
        # except:
        #     processing_error.append(locate)
        #     print(f'Error processing {locate}')


    return chm_missing, elevation_missing, processing_error


def merge_all(out_dir):
    from subprocess import call
    call(['ogrmerge.py', '-f', 'GPKG', '-single', '-o', out_dir + 'merged_centers.gpkg', out_dir + '1km*.gpkg', '-src_layer_field_content', '{DS_BASENAME}'])
    return


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Convert heatmap (tree density map) to tree center points')
    # parser.add_argument('--heatmap_dir', default='/mnt/ssdc/Denmark/DK_treeProject_DHI_KDS/predictions/test2_st64_3models_solved_nan/', type=str, help='directory to heatmaps')
    parser.add_argument('--heatmap_dir', default='/mnt/ssdc/Denmark/DK_treeProject_DHI_KDS/kongernes/predictions/final_3models_std64/', type=str, help='directory to heatmaps')
    parser.add_argument('--chm_dir', default='/mnt/ssdc/Denmark/DK_treeProject_DHI_KDS/elevation/DHM/', type=str, help='directory to chm')
    parser.add_argument('--elevation_dir', default='/mnt/ssdc/Denmark/DK_treeProject_DHI_KDS/elevation/DTM/', type=str, help='directory to elevation')
    # parser.add_argument('--image_dir', default='/mnt/ssdc/Denmark/DK_treeProject_DHI_KDS/thy/images/RGBNIR_downsampled/', type=str, help='directory to RGBNIR images')
    parser.add_argument('--image_dir', default='/mnt/ssda/DK_TreeProject_DHI_KDS/kongernes2019/AOI_images/', type=str, help='directory to RGBNIR images')
    # parser.add_argument('--output_dir', default='/mnt/ssdc/Denmark/DK_treeProject_DHI_KDS/predictions/test2_st64_3models_solved_nan/tree_centers_final_scanw10_heatmapNDVI_check/', type=str, help='directory to save tree center points')
    parser.add_argument('--output_dir', default='/mnt/ssdc/Denmark/DK_treeProject_DHI_KDS/kongernes/predictions/final_3models_std64/tree_centers_final_scanw10_heatmapNDVI_check/', type=str, help='directory to save tree center points')
    parser.add_argument('--min_dis', default=2, type=int, help='minimum distance between tree centers, in pixels')
    parser.add_argument('--thres_abs', default=0.001, type=float, help='empirical threshold for kernel peak')
    parser.add_argument('--alpha', default=0.2, type=float, help='threshold for kernel peak')
    parser.add_argument('--height_window', default=5, type=int, help='window size to search for tree height and elevation, in pixels')
    parser.add_argument('--scan_window', default=10, type=int, help='window size to scan the area on height map to cover entire tree if already detected by heatmap, in pixels')
    parser.add_argument('--low_vege', default=3, type=int, help='threshold for low vegetation')
    parser.add_argument('--ndvi_tree', default=0.2, type=float, help='threshold for tree detection using NDVI')

    args = parser.parse_args()
    out_work, out_missing_chm, out_missing_elevation = main(args)
    merge_all(args.output_dir)
    print('All processing done. :D')
    print('Missing chm for: ', out_missing_chm)
    print('Missing elevation for: ', out_missing_elevation)
    print('Processing error for: ', out_work)
    print('total failed: ', len(out_missing_chm) + len(out_missing_elevation) + len(out_work))



