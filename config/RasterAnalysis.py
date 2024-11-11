import os
class Configuration:
    
    def __init__(self):
        # a standard approach to predict tree count and segmentation for an example 1km tile with rgb bands and similar spatial resolution as the training data (20cm)
        self.input_image_dir = '/mnt/ssda/DK_TreeProject_DHI_KDS/kongernes2019/Final_tiffjpeg/'#'/home/sizhuo/Desktop/code_repository/TreeCountSegHeight-main/example_1km_tile_tif/'
        self.input_image_type = '.tif' #'.tif'#'.jp2'
        self.input_image_pref = '2019' # prefix of image file names, can be used to filter out images
        self.channel_names1 = ['red', 'green', 'blue'] # if four color bands, set to ['red', 'green', 'blue', 'infrared']
        self.channels = [0, 1, 2] # to take color bands in the correct order (match with the model)
        self.rgb2gray = 0 # set to 1 if using only grayscale image (convert rgb band to grayscale)
        self.band_switch = 0 # set to 1 if using only subset of bands or change the order of bands
        self.addndvi = 0
        # model downloadable with the google drive link
        self.trained_model_path = '/home/sizhuo/Downloads/saved_models/trees_20210620-0202_Adam_e4_redgreenblue_256_84_frames_weightmapTversky_MSE100_5weight_attUNet.h5'
        self.fillmiss = 0 # only fill in missing preds
        self.segcountpred = 1 # whether predict for segcount
        self.chmpred = 0 # whether predict for height
        self.normalize = 1 # patch norm
        self.segcount_tilenorm = 0
        self.maxnorm = 0
        self.gbnorm = 1 # DK gb norm from training data height model
        self.gbnorm_FI = 0 # FI gb norm from training data
        self.robustscale = 0 # using DK stats
        self.robustscaleFI_local = 0
        self.robustscaleFI_gb = 0
        self.localtifnorm = 0
        self.multires = 0
        self.downsave = 0 # same as upsample
        self.upsample = 0 # whether the output were upsampled or not
        self.upscale = 0
        self.rescale_values = 0
        self.saveresult = 1
        self.tasks = 2
        self.change_input_size = 0
        self.input_size = 256 # model input size
        self.input_shape = (self.input_size, self.input_size, len(self.channels))
        self.input_label_channel = [self.channels]
        self.inputBN = False
        self.output_dir = '/mnt/ssda/DK_TreeProject_DHI_KDS/kongernes2019/predictions/test1_rgb_model/'#'/home/sizhuo/Desktop/code_repository/TreeCountSegHeight-main/example_1km_tile_tif/predictions/'
        self.output_suffix = '_seg' # for segmentation
        self.chmdiff_prefix = 'diff_CHM_'
        self.output_image_type = '.tif'
        self.output_prefix = 'pred_'#+self.input_image_pref
        self.output_prefix_chm = 'pred_chm_'#+self.input_image_pref
        self.output_shapefile_type = '.shp'
        self.overwrite_analysed_files = False
        self.output_dtype='uint8'
        self.output_dtype_chm='int16'
        self.single_raster = 0
        self.aux_data = False
        self.operator = "MIX"  # for chm
        self.threshold = 0.5 # for segmentation
        self.BATCH_SIZE = 128 # Depends upon GPU memory and WIDTH and HEIGHT
        self.WIDTH=256 # crop size
        self.HEIGHT=256#
        self.STRIDE=224 #224 or 196   # STRIDE = WIDTH means no overlap, STRIDE = WIDTH/2 means 50 % overlap in prediction
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            



# Finland data (2 times coarser input resolution)
# import os
# class Configuration:
#     
#     def __init__(self):
        
        
#         self.input_image_dir = '/mnt/ssda/NFI_finland/smk_img/2019/'# raw tif images
        
#         self.input_image_type = '.tif'
#         self.input_image_pref = ''
        
#         self.channel_names1 = ['infared', 'green', 'blue']
#         self.channels = [1,2,0] # g, b, inf
#         self.band_switch = 0
#         self.rgb2gray = 0
#         # self.trained_model_path_chm = './saved_models/color2CHM/UNet/finland/trees_GBNIR2CHM_20211115-0035_Adam_Wmae_greenblueinfrared_256_19_frames_unet_attention_finetune_FIonly_heights2_Wmae1_clip10.h5'
#         self.trained_model_path = ['./saved_models/segcountdensity/Finland/trees_0903_20210620-0205_3weight_finetuneFIDK_179frames_normall.h5']
#         self.chmpred = 0
#         self.change_input_size = 0
#         self.normalize = 1 # patch norm
#         self.maxnorm = 0
#         self.gbnorm = 0 # DK gb norm from training data
#         self.gbnorm_FI = 0 # FI gb norm from training data
#         self.robustscale = 0 # using DK stats
#         self.robustscaleFI_local = 0
#         self.robustscaleFI_gb = 0
#         self.localtifnorm = 0
#         self.segcount_tilenorm = 0
#         self.multires = 0 # for CHM
#         self.downsave = 1
#         self.upsample = 1 # whether the output were upsampled to 256 or not
#         self.upscale = 2
#         self.rescale_values = 1 # since did rescaling!
#         self.saveresult = 1
#         self.tasks = 2
#         self.output_dir = '/mnt/ssda/NFI_finland/smk_img_pred_model0903/'
#         self.output_suffix = '_det_seg' # for segcount
#         self.fillmiss = 0 # only fill in missing preds
#         self.output_image_type = '.tif'
#         self.output_prefix_chm = ''
#         self.output_prefix = 'det_'
#         self.output_shapefile_type = '.shp'
#         self.overwrite_analysed_files = False
#         self.output_dtype='uint8'
#         self.single_raster = False
#         self.aux_data = False
#         self.operator = "MIX" 
        
#         # Variables related to batches and model
#         self.BATCH_SIZE = 8 # Depends upon GPU memory and WIDTH and HEIGHT (Note: Batch_size for prediction can be different then for training.
#         self.WIDTH=128 # crop size
#         self.HEIGHT=128 # 
#         self.STRIDE=102 #224 or 196   # STRIDE = WIDTH means no overlap, STRIDE = WIDTH/2 means 50 % overlap in prediction
#         if not os.path.exists(self.output_dir):
#             os.makedirs(self.output_dir)
