# https://ped.fz-juelich.de/database/doku.php
import numpy as np

def assign_to_vector_field(all_vectors, vector_field_X, vector_field_Y, dxy, XX_YY_vectors):
    for key in all_vectors.keys():
        vvv = all_vectors[key]
        for vx in vvv:
            for a in range(len(vector_field_X)):
                if vector_field_X[a] - dxy < vx[1][0] and vx[1][0] < vector_field_X[a] + dxy:
                    if vector_field_Y[a] - dxy < vx[1][1] and vx[1][1] < vector_field_Y[a] + dxy:
                        XX_YY_vectors[a].append(vx)
    return XX_YY_vectors

def caluclate_vector_field(XX_YY_vectors, vector_field_X, vector_field_Y, dxy):
    vvvv1 = 0
    for a in range(len(XX_YY_vectors)):
        if len(XX_YY_vectors[a]) > 0:
            print(str(vector_field_X[a]) + " " + str(vector_field_Y[a]) + " " + str(len(XX_YY_vectors[a])))
            vvvv1 = vvvv1 + len(XX_YY_vectors[a])
    XX_YY_vector_field = []
    for a in range(len(XX_YY_vectors)):
        XXX_YYY = [0, 0]
        if len(XX_YY_vectors[a]) > 0:
            for b in range(len(XX_YY_vectors[a])):
                v11 = XX_YY_vectors[a][b]
                dx = 1 - abs((vector_field_X[a] - v11[1][0]) / dxy)
                dy = 1 - abs((vector_field_Y[a] - v11[1][1]) / dxy)

                XXX_YYY[0] += dx * v11[2][0]
                XXX_YYY[1] += dy * v11[2][1]

        XX_YY_vector_field.append(XXX_YYY)
    return XX_YY_vector_field

def read_from_cvs(file_name, separator= " ", inserto_data_to_begin_from_zero = False):
    my_file = open(file_name, 'r')
    # objects_id = []
    objects_positions = {}
    number_of_coordinates = -1
    last_frame_id = 0
    range_x = np.array((float("inf"), float("-inf")))
    range_y = np.array((float("inf"), float("-inf")))
    range_z = np.array((float("inf"), float("-inf")))
    for line in my_file:
        # 0 - id,
        # 1 - time (frame id),
        # 2 - x,
        # 3 - y,
        # 4 - z
        splitted_line = line.split(separator)
        if number_of_coordinates < 0:
            number_of_coordinates = len(splitted_line) - 2
        id = splitted_line[0]
        if number_of_coordinates == 2:
            val = np.array([float(splitted_line[2]), float(splitted_line[3])])
        else:
            val = np.array([float(splitted_line[2]), float(splitted_line[3]), float(splitted_line[4])])

        if range_x[0] > val[0]:
            range_x[0] = val[0]
        if range_x[1] < val[0]:
            range_x[1] = val[0]

        if range_y[0] > val[1]:
            range_y[0] = val[1]
        if range_y[1] < val[1]:
            range_y[1] = val[1]

        if number_of_coordinates != 2:
            if range_z[0] > val[2]:
                range_z[0] = val[2]
            if range_z[1] < val[2]:
                range_z[1] = val[2]

        if last_frame_id < int(splitted_line[1]):
            last_frame_id = int(splitted_line[1])

        if id in objects_positions:
            opl = objects_positions[id]
            opl.append((int(splitted_line[1]),val))
        else:
            op = (int(splitted_line[1]), val)
            opl = []
            opl.append(op)
            objects_positions[id] = opl

    objects_positions_help = {}
    if inserto_data_to_begin_from_zero:
        for key in objects_positions.keys():
            opl = objects_positions[key]
            opl_help = []
            id_help = 0
            opl_help = []
            for op in opl:
                id_now = op[0]
                data_now = op[1]
                for a in range(id_now - id_help):
                    opl_help.append(data_now.copy())
                id_help = id_now
                ffff = 1
                ffff = ffff + 1
            if len(opl_help) < last_frame_id:
                data_now = opl_help[len(opl_help) - 1]
                for a in range(last_frame_id - len(opl_help)):
                    opl_help.append(data_now.copy())
            objects_positions_help[key] = opl_help

    # make vectors
    all_vectors = {}
    for key in objects_positions.keys():
        opl = objects_positions[key]
        all_vectors[key] = []
        data_prev = None
        #id_now = None
        data_now = None
        for op in opl:
            if data_now is None:
                # data_now = op[1]
                # data_now = data_prev
                data_now = op[1]
            else:
                data_prev = data_now
                data_now = op[1]
                data_vector = data_now - data_prev
                all_vectors[key].append((op[0],data_prev.copy(),data_vector.copy()))


    import matplotlib.pyplot as plt
    # Creating arrow

    x_pos = []
    y_pos = []
    x_direct = []
    y_direct = []

    for key in all_vectors.keys():
        vvv = all_vectors[key]
        for vx in vvv:
            x_pos.append(vx[1][0])
            y_pos.append(-vx[1][1])
            x_direct.append(vx[2][0])
            y_direct.append(-vx[2][1])

    fig, ax = plt.subplots(figsize=(6, 11))
    #ax.quiver(y_pos, x_pos, y_direct, x_direct, width=0.001)
    ax.quiver(x_pos, y_pos, x_direct, y_direct, width=0.001)
    ax.set_title('Trajectories of all persons walking through bottleneck with width 90 cm.')
    ax.set_xlabel('x [cm]')
    ax.set_ylabel('y [cm]')

    # Show plot
    plt.show()

    return (objects_positions, objects_positions_help,
            range_x, range_y, range_z, last_frame_id)


#file_name = '../data/b090_combined.txt'
file_name = '../data/b090_combined.txt'
[op, opd, range_x, range_y, range_z, last_frame_id] = read_from_cvs(file_name, " ", True)
