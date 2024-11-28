import os
class Configuration:
    
    def __init__(self):
        # a standard approach to predict tree count and segmentation for an example 1km tile with rgb bands and similar spatial resolution as the training data (20cm)
        self.area = 'kongernes'


        if self.area == 'thy': # rgb and nir in separate files
            self.input_image_dir = '/mnt/ssdc/Denmark/DK_treeProject_DHI_KDS/thy/images/RGBNIR_downsampled/'
            self.input_image_type = '.tif'
            self.input_image_pref = '1km'

        elif self.area == 'kongernes':
            self.input_image_dir = '/mnt/ssda/DK_TreeProject_DHI_KDS/kongernes2019/AOI_images/' #'/mnt/ssda/DK_TreeProject_DHI_KDS/kongernes2019/AOI_images/'#'/home/sizhuo/Desktop/code_repository/TreeCountSegHeight-main/example_1km_tile_tif/'
            self.input_image_type = '.tif'  # '.tif'#'.jp2'
            self.input_image_pref = '2019'  # prefix of image file names, can be used to filter out images

        else:
            raise ValueError('area not found')

        self.channel_names1 = ['red', 'green', 'blue',
                               'infrared']
        self.channels = [0, 1, 2, 3]  # to take color bands in the correct order (match with the model)
        # model downloadable with the google drive link
        self.trained_model_path = ['/home/sizhuo/Downloads/saved_models/trees_20210620-0202_Adam_e4_redgreenblue_256_84_frames_weightmapTversky_MSE100_5weight_attUNet.h5',
                                   '/home/sizhuo/Downloads/saved_models/trees_20210619-0148_Adam_e4_redgreenblueinfrared_256_84_frames_weightmapTversky_MSE100_5weight_attUNet.h5',
                                   '/home/sizhuo/Downloads/saved_models/trees_20210708-0024_Adam_e4_redgreenblueinfraredndvi_256_84_frames_weightmapTversky_MSE100_5weight_attUNet.h5']
        self.fillmiss = 0 # only fill in missing preds
        self.segcountpred = 1 # whether predict for segcount
        self.normalize = 1 # patch norm
        self.multires = 0
        self.saveresult = 1
        self.input_size = 256 # model input size
        self.inputBN = False
        self.output_dir = '/mnt/ssdc/Denmark/DK_treeProject_DHI_KDS/kongernes/predictions/final_3models_std64/' #/mnt/ssda/DK_TreeProject_DHI_KDS/kongernes2019/predictions/final1_AOI_3models_str64/'#'/home/sizhuo/Desktop/code_repository/TreeCountSegHeight-main/example_1km_tile_tif/predictions/'
        self.output_suffix = '_seg' # for segmentation
        self.output_image_type = '.tif'
        self.output_prefix = 'pred_'#+self.input_image_pref
        self.output_shapefile_type = '.shp'
        self.overwrite_analysed_files = False
        self.output_dtype='uint8'
        self.threshold = 0.5
        self.BATCH_SIZE = 112 # Depends upon GPU memory and WIDTH and HEIGHT
        self.WIDTH=256 # crop size
        self.HEIGHT=256#
        self.STRIDE=64 #224 or 196   # STRIDE = WIDTH means no overlap, STRIDE = WIDTH/2 means 50 % overlap in prediction
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            
