import os
import glob
from tqdm import tqdm
# dsm
dsm_path = '/mnt/ssdc/Denmark/DK_treeProject_DHI_KDS/elevation/DSM/'
dtm_path = '/mnt/ssdc/Denmark/DK_treeProject_DHI_KDS/elevation/DTM/'

# calculate chm
chm_save_path = '/mnt/ssdc/Denmark/DK_treeProject_DHI_KDS/elevation/DHM/'

# search for all dsm and dtm
dsm_files = glob.glob(dsm_path + '**/*.tif', recursive=True)
print('number of dsm files: ', len(dsm_files))

# dtm_files = glob.glob(dtm_path + '**/*.tif', recursive=True)
# print('number of dtm files: ', len(dtm_files))

missing_dtm = []
for dsmf in tqdm(dsm_files):
    dtmf = dsmf.replace('DSM', 'DTM')
    if not os.path.exists(dtmf):
        print('missing dtm: ', dtmf)
        missing_dtm.append(dsmf)
        continue
    # calculate chm
    chm_save = dsmf.replace('DSM', 'DHM')
    if not os.path.exists(chm_save):
        os.makedirs(os.path.dirname(chm_save), exist_ok=True)
    os.system(f'gdal_calc.py -A {dsmf} -B {dtmf} --outfile={chm_save} --calc="A-B"')
    print('chm saved to: ', chm_save)

print('processing done')
# check number  of chm files
chm_files = glob.glob(chm_save_path + '**/*.tif', recursive=True)
print('number of chm files: ', len(chm_files))