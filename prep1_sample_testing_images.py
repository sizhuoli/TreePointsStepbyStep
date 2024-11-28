# preprocessing step: randomly sample testing images to test model

import os
import tqdm
import glob


def load_all_files(args):
    # load all files in a directory
    files = glob.glob(args.path + '*.tif', recursive=False)
    print('number of files: ', len(files))
    return files




def sampler(files, args):
    # randomly sample n files
    import random
    random.seed(args.seed)
    random.shuffle(files)
    files = files[:args.n]
    return files

def copy_test_files(files, args):
    # copy files to a new directory
    import shutil
    if not os.path.exists(args.save_dir):
        os.mkdir(args.save_dir)
    for f in tqdm.tqdm(files):
        shutil.copy(f, args.save_dir)
    print('files copied to ', args.save_dir)
    print('number of files: ', len(files))

    return

def main(args):
    allfiles = load_all_files(args)
    testfiles = sampler(allfiles, args)
    copy_test_files(testfiles, args)
    print('done')
    return

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Randomly sample tif files')
    parser.add_argument('--path', default='/mnt/ssda/DK_TreeProject_DHI_KDS/kongernes2019/Final_tiffjpeg/', type=str, help='path to all tif files')
    parser.add_argument('--n', default=100, type=int, help='number of files to sample')
    parser.add_argument('--save_dir', default='/mnt/ssda/DK_TreeProject_DHI_KDS/kongernes2019/test_images/', type=str, help='path to save the sampled files')
    parser.add_argument('--seed', default=0, type=int, help='random seed')
    args = parser.parse_args()
    main(args)

