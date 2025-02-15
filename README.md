# Step-by-Step Guide for Building A Tree Database 

A follow-up tutorial for the [published tree counting/segmentation framework](https://github.com/sizhuoli/TreeCountSegHeight 'link to the original repository'). The same data license applies to this repository.



![Figure 1](figures/fig1.png)

Figure 1. From remote sensing data to a tree database. Color indicates tree height (low to high = blue to red)


## General Usage

### Production-ready mode

* Data and models are [ready](https://drive.google.com/file/d/1ZNibrh6pa4-cjXLawua6L96fOKS3uwbn/view?usp=sharing)
* All hyperparameters are properly tuned
* Configure file paths
* Follow steps 0 -> 1 -> 3

### Fine-tuning mode

* Data and models are [ready](https://drive.google.com/file/d/1ZNibrh6pa4-cjXLawua6L96fOKS3uwbn/view?usp=sharing)
* Configure file paths
* Follow steps 0 -> 1 -> 2 -> 3


## Step 0. Setup environment
Depending on your GPU driver, you may try the following environment.yml files to set up the conda environment:

1. To set up the same environment:
```
conda env create -f environment_trees_updated.yml
```

2. If the above does not work, try the following to set up the basic environment and install the missing packages manually:


```
conda env create -f environment_trees_updated_basic.yml
```



#### Activate the environment

```
conda activate tf2151full
```

## Step 1. Deep learning prediction


```
python main4_large_scale_inference_transfer_other_data.py
```

* Set configs in /config/RasterAnalysis.py
* See example results in /test_example/
* Optional: re-sample images to match the trained resolution (20 cm)
    ```
    bash prep1_downsample_img.sh
    ```
* Optional: process canopy height maps
    ```
    python prep2_processCHM.py
    ```
* Optional: create overview of all images
    ```
    bash prep3_convert_tif_shp.sh
    ```
* Optional: create vrt for visualizing all predictions
    ```
    bash post1_create_vrt_demo_results.sh /path/to/dir prediction
    ```
* Optional: clean segmentation predictions
    ```
    python post5_segmentation_mask.py
    ```


## Step 2. Grid-search for optimal hyperparameters

P.S. hyperparameters in postprocessing steps, not for deep learning prediction

### Step 2.1 Clip images for grid search

    python post3_evaluation_clip_images.py

### Step 2.2 Run grid search

    python post4_evaluation_grid_search.py

## Step 3. Extract tree points

    python post2_heatmap2points.py

* Use optimal hyperparameters from grid search
* Set configs in file
  * Hardware configurations: set "maxworkers" based on CPU cores



