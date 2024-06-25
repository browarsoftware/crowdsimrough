import numpy as np
import numpy_indexed as npi

def calculate_lower_border(unique_rows, direction_1):
    #kierunek
    #direction_1 = 8
    last_column = unique_rows.shape[1] - 1
    #wszystkie unikalne do tego kierunku
    mask = (unique_rows[:, last_column] == direction_1)
    ur_ = np.copy(unique_rows[mask, :])
    # wywalamy identyfikator klasy
    ur_ = np.delete(ur_, last_column, 1)

    lower_arr = np.copy(ur_)
    border = []
    for direction_2 in range(9):
        if direction_1 != direction_2:
            #usuwamy czesc wspolna - lower approximation
            # if the output should consist of unique values and there is no need to preserve ordering
            mask2 = (unique_rows[:, last_column] == direction_2)
            ur_2 = np.copy(unique_rows[mask2, :])
            if ur_2.shape[0] > 0:
                # wywalamy identyfikator klasy
                ur_2 = np.delete(ur_2, last_column, 1)
                #lower_arr = ur_[~npi.in_(ur_, ur_2)]
                #bierzemy czesc wspolna - border
                inter = npi.intersection(ur_, ur_2)
                border.append(inter)

    #lower_arr = np.unique(lower_arr, axis=0)
    border_arr = np.zeros([0,last_column]).astype(int)
    a = 0
    while a < len(border):
        border_arr = np.concatenate((border_arr, border[a]))
        a = a + 1
    border_arr = np.unique(border_arr, axis=0)

    if border_arr.shape[0] > 0:
        lower_arr = ur_[~npi.in_(ur_, border_arr)]

    return (lower_arr, border_arr)


def calculate_raw_set_metrics(df_sampled):
    accuracy_of_approximation = []
    upper_count = []
    lower_count = []
    border_count = []
    unique_rows = np.unique(df_sampled, axis=0)

    #unique_rows_no_class = np.delete(unique_rows, 5, 1)
    #unique_rows = np.delete(unique_rows, 1, 1)
    #unique_rows = np.delete(unique_rows, 2, 1)
    class_column = unique_rows.shape[1]-1



    #unique_rows = np.delete(df_sampled_copy, 3, 1)
    all_res = []
    for dir in range(8):
        [lower_arr, border_arr] = calculate_lower_border(unique_rows, dir)
        #musimy dodać tyle wystąpień takiego elementu, ile ich faktycznie jest
        lower_arr_exp = np.zeros([0,lower_arr.shape[1]]).astype(int)
        for a in range(lower_arr.shape[0]):
            rrr = lower_arr[a,:]
            count = np.sum(np.all(rrr == df_sampled[:,0:class_column], axis=1)) - 1
            if count > 0:
                rrr = np.expand_dims(rrr, axis=0)
                for bb in range(count):
                    lower_arr_exp = np.concatenate((lower_arr_exp, rrr))

        border_arr_exp = np.zeros([0,border_arr.shape[1]]).astype(int)
        for a in range(border_arr.shape[0]):
            rrr = border_arr[a,:]
            count = np.sum(np.all(rrr == df_sampled[:,0:class_column], axis=1)) - 1
            if count > 0:
                rrr = np.expand_dims(rrr, axis=0)
                for bb in range(count):
                    border_arr_exp = np.concatenate((border_arr_exp, rrr))

        lower_arr = np.concatenate((lower_arr, lower_arr_exp))
        border_arr = np.concatenate((border_arr, border_arr_exp))
        all_res.append([lower_arr, border_arr])

        #print((lower_arr.shape[0] + border_arr.shape[0]))
        #print("accuracy_of_approximation,dir=" + str(dir) + "=" + str(lower_arr.shape[0] / (lower_arr.shape[0] + border_arr.shape[0])))

        upper_count.append(lower_arr.shape[0] + border_arr.shape[0])
        lower_count.append(lower_arr.shape[0])
        border_count.append(border_arr.shape[0])
        accuracy_of_approximation.append(lower_arr.shape[0] / (lower_arr.shape[0] + border_arr.shape[0]))


    #pozytywny obszar rodziny zbiorów
    lower_arr_fam = np.zeros([0,unique_rows.shape[1]-1])
    border_arr_fam = np.zeros([0,unique_rows.shape[1]-1])
    for dir in range(len(all_res)):
        [lower_arr, border_arr] = all_res[dir]
        if lower_arr.shape[0] > 0:
            lower_arr_fam = np.concatenate((lower_arr_fam, lower_arr))
        if border_arr.shape[0] > 0:
            border_arr_fam = np.concatenate((border_arr_fam, border_arr))

    dependency_C_D = lower_arr_fam.shape[0] / df_sampled.shape[0]
    return [accuracy_of_approximation, upper_count, lower_count, border_count, dependency_C_D]

def calculate_raws_sets_metrics(all_rough_sets, columns_to_take, df_sampled):
    metrics = []
    for subset_to_take in range(len(all_rough_sets)):
        ctt = columns_to_take[subset_to_take]
        columns_count = df_sampled.shape[1]
        df_sampled_copy = np.copy(df_sampled)
        index_mod = 0
        for a in range(columns_count):
            if a not in ctt:
                df_sampled_copy = np.delete(df_sampled_copy, a - index_mod, 1)
                index_mod += 1

        if df_sampled_copy.shape[1] > 1:
            [accuracy_of_approximation, upper_count, lower_count, border_count, dependency_C_D] = calculate_raw_set_metrics(df_sampled_copy)
            metrics.append([accuracy_of_approximation, upper_count, lower_count, border_count, dependency_C_D])
    return metrics

def sort_me_helper(metrics, all_rough_sets, columns_to_take):
    dependenies = []
    for a in range(len(metrics)):
        [accuracy_of_approximation, upper_count, lower_count, border_count, dependency_C_D] = metrics[a]
        dependenies.append(dependency_C_D)
        #print(dependency_C_D)

    ind = np.argsort(dependenies)
    ind = ind.tolist()
    ind.reverse()
    #dodajemy ostatni raw set, który jest oparty na częstotliwości
    ind.append(len(ind))
    #all_rough_sets = [0,1,2,3,4,5,6,7]
    all_rough_sets_sorted = []
    for id in ind:
        all_rough_sets_sorted.append(all_rough_sets[id])

    columns_to_take_sorted = []
    for id in ind:
        columns_to_take_sorted.append(columns_to_take[id])
    return [all_rough_sets_sorted, columns_to_take_sorted]


