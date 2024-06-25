# ORDER OF RUN: #10
#

import pickle
import sys
sys.path.append('../')
from rough_sets_metrics import calculate_raws_sets_metrics, sort_me_helper
gap_size = 90
eps = 0.75
file = open("../data/rough_setb" + str(gap_size) + "_" + str(eps) + "_" + str(eps) + ".rs", 'rb')
data = pickle.load(file)
[all_rough_sets, columns_to_take, t_dir_r, df, df_sampled, ranges] = data
file.close()
metrics = calculate_raws_sets_metrics(all_rough_sets, columns_to_take, df_sampled)
D = ['E','SE','S','SW','W','NW','N','NE']
for c in range(len(metrics)):
    [accuracy_of_approximation, upper_count, lower_count, border_count, dependency_C_D] = metrics[c]
    for a in range(len(upper_count)):
        print("C" + str(c + 1) + " & " + D[a] + " & "
              + str(f'{round(accuracy_of_approximation[a], 4) : .4f}') + " & "
              + str(f'{round(lower_count[a] / df_sampled.shape[0], 4) : .4f}') + " & "
              + str(f'{round(border_count[a] / df_sampled.shape[0], 4) : .4f}') + " & "
              + str(f'{round(upper_count[a] / df_sampled.shape[0], 4) : .4f}\\\\')
              )
