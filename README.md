### Source codes for paper:

# An insightful data-driven crowd simulation model based on rough sets 

Author: [Tomasz Hachaj](https://home.agh.edu.pl/~thachaj/) [Jarosław Wąs](https://home.agh.edu.pl/~jarek/)

<!--Algorithms for converting 2D to 3D are gaining importance following the hiatus brought about by the discontinuation of 3D TV production; this is due to the high availability and popularity of virtual reality systems that use stereo vision. In this paper, several depth image-based rendering (DIBR) approaches using state-of-the-art single-frame depth generation neural networks and inpaint algorithms are proposed and validated, including a novel very fast inpaint (FAST). FAST significantly exceeds the speed of currently used inpaint algorithms by reducing computational complexity, without degrading the quality of the resulting image. The role of the inpaint algorithm is to fill in missing pixels in the stereo pair estimated by DIBR. Missing estimated pixels appear at the boundaries of areas that differ significantly in their estimated distance from the observer. In addition, we propose parameterizing DIBR using a singular, easy-to-interpret adaptable parameter that can be adjusted online according to the preferences of the user who views the visualization. This single parameter governs both the camera parameters and the maximum binocular disparity. The proposed solutions are also compared with a fully automatic 2D to 3D mapping solution. The algorithm proposed in this work, which features intuitive disparity steering, the foundational deep neural network MiDaS, and the FAST inpaint algorithm, received considerable acclaim from evaluators. The mean absolute error of the proposed solution does not contain statistically significant differences from state-of-the-art approaches like Deep3D and other DIBR-based approaches using different inpaint functions. Since both the source codes and the generated videos are available for download, all experiments can be reproduced, and one can apply our algorithm to any selected video or single image to convert it.
-->
Keywords: Rough sets; Crowd simulation; Agent system; Insightful model; Social forces; Bottleneck problem

## Requirements

- Python 3.X
- numba >= 0.56, 
- numpy >= 1.23
- opencv-python >= 4.7
- R language >= 3.6.2 

Tested on: 
- PC, Intel i7-9700 3GHz, 64 GB RAM, NVIDIA GeForce RTX 2060 GPU, Windows 10 OS,
- Laptop, Intel i7-11800H 2.3GHz, 32 GB RAM, NVIDIA GeForce RTX 3050 Ti Laptop GPU, Windows 11 OS.

## How to run

Run scripts in following order:
1. Generate input data [data_reader_calculate_forces.py](data_reader_calculate_forces.py)
2. Further process the input data [generate_input_data.R](generate_input_data.R)
3. Generate rough sets (this will create large files) [generate_rough_sets.py](generate_rough_sets.py)
4. Social forces simulation 1,000 agents [simulation_social_forces_loop_all.py](simulation_social_forces_loop_all.py)
5. Social forces simulation, data from file [simulate_social_forces_from_file.py](simulate_social_forces_from_file.py)
6. Rough sets simulation, data from file [simulation_rough_set_from_file.py](simulation_rough_set_from_file.py)
7. Simulation rough set, 1,000 agents [simulation_rough_set_loop_all.py](simulation_rough_set_loop_all.py)
8. Generate reference data from csv [generate_reference_data.py](generate_reference_data.py)
9. Generate table that presents the dependency of attributes D from a set of attributes C [tables/Dependency_C_D_tables.py](tables/Dependency_C_D_tables.py)
10. Generate table that presents values of accuracy of approximation etc. [tables/eval_tables.py](tables/eval_tables.py)
11. Generate table that presents the results of the logarithm of cumulated crowd density comparison between actual data and results obtained by the social forces algorithm and rough set-based algorithm [tables/MSE_tables.py](tables/MSE_tables.py)

Additional scripts:
- Plot input data to screen or file [show_input_data.py](show_input_data.py)
- Plot rough set [sets_plots/plot_set_social.py](sets_plots/plot_set_social.py)
- Plot trajectories of all persons walking through a bottleneck [sets_plots/plot_example_trajectories.py](sets_plots/plot_example_trajectories.py) 
## Example result plots

Reference data

![alt text](fig/reference90/00200.png)

Trajectories of all persons walking through a bottleneck

![alt text](image/tp.png)

The logarithm of the cumulated crowd density which is defined as the total time number of iteration of simulation when a certain cell in simulation grid was occupied by an agent.

![alt text](image/rougfromfile90.0.5.png)

This figure visualizes the rough set generated from a dataset with a bottleneck width equal to 100 cm with conditional attributes C7.

![alt text](image/rs.png)


## Data source

Data downloaded from archive of experimental data from studies about pedestrian dynamics [link](https://ped.fz-juelich.de/database/doku.php)
