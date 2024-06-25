# ORDER OF RUN: #3
# Generate rough sets
from find_directions_rough import genarate_sets
import pickle
eps0=0.5
eps1=0.5
gap=250
for gap in [90, 100, 120, 140, 160, 180, 200]:
    for eps in [0.5, 0.75]:
        print('gap=' + str(gap) + ",eps=" + str(eps))
        eps0 = eps1 = eps
        [all_rough_sets, columns_to_take, t_dir_r, df, df_sampled, ranges] = genarate_sets('data/results_to_file_imp_no_zero_b' + str(gap) + '.txt', eps0=eps0, eps1=eps1)

        file = open('data/rough_set' + 'b' + str(gap) + "_" + str(eps0) + '_' + str(eps1) + '.rs', 'wb')
        data = [all_rough_sets, columns_to_take, t_dir_r, df, df_sampled, ranges]
        pickle.dump(data, file)
        file.close()
