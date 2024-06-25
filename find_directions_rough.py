import numpy as np
import csv
import math
import copy

def calculate_dir(my_dir):
    if my_dir == 0:
        return [0,0]
    if my_dir == 1:
        return [1,0]
    if my_dir == 2:
        return [1,1]
    if my_dir == 3:
        return [0,1]
    if my_dir == 4:
        return [-1,1]
    if my_dir == 5:
        return [-1,0]
    if my_dir == 6:
        return [-1,-1]
    if my_dir == 7:
        return [0,-1]
    if my_dir == 8:
        return [1,-1]
    return [0, 0]

def get_unique_from_list(my_list):
    unique_val =  list(set(my_list))
    unique_val.sort()
    return unique_val

#
def discretization(my_coord, ranges):
    res = [find_if_category(ranges[0], my_coord[0]),
        find_if_float(ranges[1], my_coord[1]),
        find_if_float(ranges[2], my_coord[2]),
        find_if_float(ranges[3], my_coord[3]),
        find_if_float(ranges[4], my_coord[4])]
    if len(res) == 6:
        res.append(find_if_category(ranges[5], my_coord[5]))
    return res


def generate_rages_from_float(my_column, min_range=0):
    unique = get_unique_from_list(my_column)
    ranges_list = []
    ranges_list_left_right = []
    left =  float('-inf')
    if len(unique) < 3:
        ranges_list.append([left, float('inf')])
    else:
        a = 1
        val_prev = unique[0]
        while a < len(unique):
            val = unique[a]
            mid_dist = (val - val_prev) / 2
            right = val_prev + mid_dist
            if math.fabs(right - left) >= min_range:
                ranges_list.append([left, right])
                ranges_list_left_right.append([val_prev,val])
                val_prev = val
                left = right
            a = a + 1
        ranges_list.append([left, float('inf')])
    return [ranges_list, ranges_list_left_right]

def generate_rages_from_category(my_column):
    unique = get_unique_from_list(my_column)
    unique_s = []
    for u in unique:
        unique_s.append(str(u))
    return [copy.deepcopy(unique_s), copy.deepcopy(unique_s)]
    #return [copy.deepcopy(unique), copy.deepcopy(unique)]

def find_id_recurrention_float(id, id_left, id_right, column_ranges, value):
    cccc = column_ranges[id]
    if id_right == id_left:
        return id
    # w prawo
    if column_ranges[id][1] < value:
        return find_id_recurrention_float(int((id_right + id) / 2) + 1, id+1, id_right, column_ranges, value)
        #return find_id_recurrention(int((id_left + id) / 2), id_left, id - 1, column_ranges, value)
    else:
        # w lewo
        if column_ranges[id][0] > value:
            return find_id_recurrention_float(int((id_left + id) / 2), id_left, id - 1, column_ranges, value)
            #return find_id_recurrention(int((id_right + id) / 2), id + 1, id_right, column_ranges, value)
        # znalezione
        else:
            return id

def find_if_float(column_ranges, value):
    id = int(len(column_ranges) / 2)
    return find_id_recurrention_float(id, 0, len(column_ranges)-1, column_ranges, value)

def find_id_recurrention_categor(id, id_left, id_right, column, value):
    cccc = column[id]
    if id_right == id_left:
        return id
    # w prawo
    if column[id] < value:
        return find_id_recurrention_categor(int((id_right + id) / 2) + 1, id+1, id_right, column, value)
    else:
        # w lewo
        if column[id] > value:
            return find_id_recurrention_categor(int((id_left + id) / 2), id_left, id - 1, column, value)
        # znalezione
        else:
            return id

"""
def find_if_category(column_ranges, value):
    id = int(len(column_ranges) / 2)
    return find_id_recurrention_categor(id, 0, len(column_ranges)-1, column_ranges, value)
"""

def find_if_category(column_ranges, value):
    for a in range(len(column_ranges)):
        if column_ranges[a] == str(value):
            return a
    return None

def genarate_sets(my_file, eps0 = 4, eps1 = 4):
    header = []
    columns = []
    with open(my_file, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            if len(header) == 0:
                for val in row:
                    header.append(val)
                    columns.append([])
            else:
                a = 0
                for val in row:
                    columns[a].append(float(val))
                    a = a + 1

    predict = columns[header.index("t_dir")]
    ff_dir = columns[header.index("ff_dir")]
    fw_x = columns[header.index("fw_x")]
    fw_y = columns[header.index("fw_y")]
    fa_x = columns[header.index("fa_x")]
    fa_y = columns[header.index("fa_y")]

    df = [ff_dir, fw_x, fw_y, fa_x, fa_y, predict]

    #eps0 = 4 # 0
    #eps1 = 4 # 0.5
    [t_dir_r, foo] = generate_rages_from_category(predict)
    [ff_dir_r, foo] = generate_rages_from_category(ff_dir)
    [fw_x_r, foo] = generate_rages_from_float(fw_x, eps0)
    [fw_y_r, foo] = generate_rages_from_float(fw_y, eps0)
    [fa_x_r, foo] = generate_rages_from_float(fa_x, eps1)
    [fa_y_r, foo] = generate_rages_from_float(fa_y, eps1)

    rough_sets = np.zeros((len(ff_dir_r), len(fw_x_r), len(fw_y_r), len(fa_x_r), len(fa_y_r), len(t_dir_r)))

    df_sampled = np.zeros([len(ff_dir),6]).astype(int)
    #id_help = find_if_float(fw_x_r, 6.0)
    id_2 = find_if_float(fw_y_r, 0)
    for a in range(len(predict)):
        id_0 = find_if_category(ff_dir_r, ff_dir[a])
        id_1 = find_if_float(fw_x_r, fw_x[a])
        id_2 = find_if_float(fw_y_r, fw_y[a])
        id_3 = find_if_float(fa_x_r, fa_x[a])
        id_4 = find_if_float(fa_y_r, fa_y[a])
        id_5 = find_if_category(t_dir_r, predict[a])

        rough_sets[id_0, id_1, id_2, id_3, id_4, id_5] += 1
        df_sampled[a, 0] = id_0
        df_sampled[a, 1] = id_1
        df_sampled[a, 2] = id_2
        df_sampled[a, 3] = id_3
        df_sampled[a, 4] = id_4
        df_sampled[a, 5] = id_5

    colnames = ['ff_dir','fw_x','fw_y','fa_x','fa_y','predict']
    columns_to_take = [[0,1,2,3,4,5],
     [0,1,2,5],[0,3,4,5],[1,2,3,4,5],
     [0,5],[1,2,5],[3,4,5],
     [5]]
    columns_to_sum = [(), (3,4), (1,2), (0),
                      (1,2,3,4),(0,3,4),(0,1,2),
                      (0,1,2,3,4)]


    all_rough_sets = [rough_sets]
    for a in range(1,len(columns_to_sum)):
        sum_help = np.sum(rough_sets, axis=columns_to_sum[a])
        all_rough_sets.append(sum_help)


    ranges = [ff_dir_r,fw_x_r, fw_y_r,fa_x_r,fa_y_r,t_dir_r]

    return [all_rough_sets, columns_to_take, t_dir_r, df, df_sampled, ranges]

def find_directions(my_coord, all_rough_sets, columns_to_take, t_dir_r):
    all_values_help = []
    directions_help = []
    #print(my_coord)
    for a in range(len(all_rough_sets)):
        rs = all_rough_sets[a]
        ctt = columns_to_take[a]
        t = ()
        for b in range(len(ctt) - 1):
            t = t + (my_coord[ctt[b]],)

        none_found = False
        for b in range(len(t)):
            if t[b] is None:
                none_found = True

        if not none_found:
            values_help = []
            for c in range(len(t_dir_r)):
                t2 = t + (c,)
                values_help.append(rs[t2])

            all_values_help.append(values_help)
            ind = np.argsort(-np.array(values_help))
            dir_help = []
            sum_help = 0
            for b in range(len(values_help)):
                if values_help[ind[b]] > 0:
                    dir_help.append([t_dir_r[ind[b]], values_help[ind[b]]])
                    sum_help += values_help[ind[b]]
            if len(dir_help) > 0:
                for b in range(len(dir_help)):
                    div_help = dir_help[b][1] / sum_help
                    dir_help[b].append(div_help)
                directions_help.append(dir_help)
    return directions_help
