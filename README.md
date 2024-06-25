### Source codes for paper:

# An insightful data-driven crowd simulation model based on rough sets 

Author: [Tomasz Hachaj](https://home.agh.edu.pl/~thachaj/) [Jarosław Wąs](https://home.agh.edu.pl/~jarek/)

<!--Algorithms for converting 2D to 3D are gaining importance following the hiatus brought about by the discontinuation of 3D TV production; this is due to the high availability and popularity of virtual reality systems that use stereo vision. In this paper, several depth image-based rendering (DIBR) approaches using state-of-the-art single-frame depth generation neural networks and inpaint algorithms are proposed and validated, including a novel very fast inpaint (FAST). FAST significantly exceeds the speed of currently used inpaint algorithms by reducing computational complexity, without degrading the quality of the resulting image. The role of the inpaint algorithm is to fill in missing pixels in the stereo pair estimated by DIBR. Missing estimated pixels appear at the boundaries of areas that differ significantly in their estimated distance from the observer. In addition, we propose parameterizing DIBR using a singular, easy-to-interpret adaptable parameter that can be adjusted online according to the preferences of the user who views the visualization. This single parameter governs both the camera parameters and the maximum binocular disparity. The proposed solutions are also compared with a fully automatic 2D to 3D mapping solution. The algorithm proposed in this work, which features intuitive disparity steering, the foundational deep neural network MiDaS, and the FAST inpaint algorithm, received considerable acclaim from evaluators. The mean absolute error of the proposed solution does not contain statistically significant differences from state-of-the-art approaches like Deep3D and other DIBR-based approaches using different inpaint functions. Since both the source codes and the generated videos are available for download, all experiments can be reproduced, and one can apply our algorithm to any selected video or single image to convert it.
-->
Keywords: Rough sets; Crowd simulation; Agent system; Insightful model; Social forces; Bottleneck problem

## Requirements

- numba >= 0.56, 
- numpy >= 1.23
- opencv-python >= 4.7

Tested on: 
- PC, Intel i7-9700 3GHz, 64 GB RAM, NVIDIA GeForce RTX 2060 GPU, Windows 10 OS,
- Laptop, Intel i7-11800H 2.3GHz, 32 GB RAM, NVIDIA GeForce RTX 3050 Ti Laptop GPU, Windows 11 OS.

## How to run

The program can be run with Torch backbone for networks MiDaS-S, MiDaS-H oraz MiDaS-L. Implementation is located in the folder [midas](/midas/).
- [/midas/midas_run.py](/midas/midas_run.py) is used to run live stream video (you must have a camera connected) or to process a video file (for example, in mp4 format). There are a number of options such as resolution setting, max disparity, stereo pair generation configuration for the resulting video (vertical or horizontal) and many others. Videos on which qualitative (user) studies were performed based on the pixabay collection can be downloaded from [CLICK!](https://drive.google.com/drive/folders/1xt5gVhP2kyXIWQe8xpC3nwCDejKFD0Zw?usp=sharing
)
- [/midas/midas_evaluation.py](/midas/midas_evaluation.py) evaluation of the method on KITTI dataset [CLICK!](https://www.cvlibs.net/datasets/kitti/eval_scene_flow.php?benchmark=stereo) 

The program can be run with Tensorflow/Keras backbone for networks DenseDepth (download weights from [here](https://drive.google.com/file/d/19dfvGvDfCRYaqxVKypp1fRHwK7XtSjVu/view)) and DenseDepth-Small. Implementation is located in the folder [densedepth](/densedepth/).
- [/densedepth/dense_depth_run.py](/densedepth/dense_depth_run.py) is used to run live stream video (you must have a camera connected)
- [/densedepth/dense_depth_evaluation.py](/densedepth/dense_depth_evaluation.py) evaluation of the method on KITTI dataset [CLICK!](https://www.cvlibs.net/datasets/kitti/eval_scene_flow.php?benchmark=stereo) 

The implementation that evaluate deep3d method on the KITTI and pixabay datasets can be found in the folder [deep3d](/deep3d/). In order to execute it download [Deep3D](https://github.com/HypoX64/Deep3D) and copy file [/deep3d/deep3d_evaluation.py](/deep3d/deep3d_evaluation.py) into Deep3D project folder.

In each script set the appropriate paths under which the downloaded data is locally located and output paths for the converted video!

Suggested configuration for mp4 video: DIBR + MiDaS + FAST inapint, max disparity = 75.


## Example resutls on benchmark images

Right image stereo pair is estimated from left image. Algorithm: DIBR + MiDaS + FAST inapint, max disparity = 25.

![alt text](image/mandrill.gif) ![alt text](image/pepper.gif)
![alt text](image/barbara.gif) ![alt text](image/roof.gif)
![alt text](image/lena.gif) ![alt text](image/pot.gif)

## Data source

Data downloaded from archive of experimental data from studies about pedestrian dynamics [link](https://ped.fz-juelich.de/database/doku.php)
