# ORDER OF RUN: #9
# Generate table that presents the dependency of attributes D from a set of attributes C
import pickle
from rough_sets_metrics import calculate_raws_sets_metrics

for gap_size in [90, 100, 120, 140, 160, 180, 200]:
    for eps in [0.5, 0.75]:
        file = open("../data/rough_setb" + str(gap_size) + "_" + str(eps) + "_" + str(eps) + ".rs", 'rb')
        data = pickle.load(file)
        [all_rough_sets, columns_to_take, t_dir_r, df, df_sampled, ranges] = data
        file.close()
        metrics = calculate_raws_sets_metrics(all_rough_sets, columns_to_take, df_sampled)
        str_help = str(gap_size) + ", $\epsilon=" + str(eps) + "$"
        for a in range(len(metrics)):
            mm = metrics[a]
            str_help += "& " + str(round(mm[4], 3))
        print(str_help)
