import numpy as np

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
    return (objects_positions, objects_positions_help,
            range_x, range_y, range_z, last_frame_id)
