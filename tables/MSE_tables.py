# ORDER OF RUN: #11
# Generate table that presents the results of the logarithm of cumulated crowd density comparison between actual data and results obtained by the social forces algorithm and rough set-based algorithm
import pickle
import numpy as np


#for gap_size in [90, 100, 120, 140, 160, 180, 200, 220, 250]:
for gap_size in [90, 100, 120, 140, 160, 180, 200]:
    density_rough = []
    file = open("../results/reference/plot_data" + str(gap_size), 'rb')
    denisty_plot_ref = pickle.load(file)
    file.close()

    file = open("../results/simulation_social_forces_from_file/plot_data" + str(gap_size), 'rb')
    denisty_plot_simulation = pickle.load(file)
    file.close()

    for eps in [0.5, 0.75]:
        file = open("../results/simulation_rough_from_file/plot_data" + str(gap_size) + "_" + str(eps) + "_" + str(eps) + ".rs", 'rb')
        denisty_plot_rough = pickle.load(file)
        file.close()
        density_rough.append(denisty_plot_rough)

    mse_S = (np.square(np.log(denisty_plot_ref) - np.log(denisty_plot_simulation))).mean()

    mse_R0 = (np.square(np.log(denisty_plot_ref) - np.log(density_rough[0]))).mean()
    mse_R1 = (np.square(np.log(denisty_plot_ref) - np.log(density_rough[1]))).mean()

    print(str(gap_size) + " & " + str(round(mse_S,3)) + " & " + str(round(mse_R0,3)) + " & " + str(round(mse_R1,3)))
