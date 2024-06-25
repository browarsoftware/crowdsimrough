# ORDER OF RUN: #1
import math

import cv2
import numpy as np
from data_reader import read_from_cvs
from calculate_simulation_helper import plot_room, calculate_local_force_field_agents, prepare_local_force_field_array
from evaluate_agent import plot_agent, erase_agent

# change files to 90, 100, 120, 140, 160, 180, 200
file_name = 'data/b090_combined.txt'
result_to_file = "data/results_to_file_b90.txt"
#file_name = 'data/b200_combined.txt'
#result_to_file = "data/results_to_file_b200.txt"
# change gap size to 9, 10, 12, 14, 16, 18, 20
gap_size = 9
#gap_size = 20

image_size = [512,512]
local_force_field_size = [25, 25]

white = (255, 255, 255)


agent_size = np.ones((5, 5))
agent_size[0,0] = 0
agent_size[4,4] = 0
agent_size[0,4] = 0
agent_size[4,0] = 0

img = plot_room(image_size, gap_size)
from calculate_simulation_helper import calculate_wall_force_field, calculate_room_force_field_and_distance
force_field_wall= calculate_wall_force_field(img)
[force_field, distance_to_goal] = calculate_room_force_field_and_distance(image_size, img)
[local_force_field_size, local_force_field, local_force_field_size_half_x, local_force_field_size_half_y] \
    = prepare_local_force_field_array(local_force_field_size)

[op, opd, range_x, range_y, range_z, last_frame_id] = read_from_cvs(file_name, " ", True)



def calculate_linear_coeff(x0_x1, y0_y1):
    a = (y0_y1[0] - y0_y1[1]) / (x0_x1[0] - x0_x1[1])
    b = y0_y1[0] - (a * x0_x1[0])
    return (a, b)

image_size = [512,512]


def transfor_coord(xy_old, image_size):
    xy_new = [0, 0]
    xy_new[0] = int(xy_old[0] / 5 + (image_size[0] / 2))
    xy_new[1] = int(xy_old[1] / 5 + (image_size[1] / 2))
    return  xy_new


import random as rnd
id = 0
id_all = []
img_colors = []
iiiii = 0
f = open(result_to_file, "w")

f.write("key;id_now;ff_x;ff_y;fw_x;fw_y;fa_x;fa_y;t_x;t_y\n")

for key in opd:
    img_colors.append(np.array([rnd.randint(0, 255), rnd.randint(0, 255), rnd.randint(0, 255)]))
    id_all.append(id)

for id in range(last_frame_id):
    img_a = np.copy(img)

    id_key = 0
    for key in opd:
        opl = op[key]
        (id_now,coord) = opl[id_all[id_key]]
        if id_now == id:
            xy_c = np.array(transfor_coord(coord, image_size))
            plot_agent(img_a, agent_size, xy_c, img_colors[id_key])

        if id_now == id:
            id_help = id_all[id_key] + 1
            xy_c_next = None
            xy_translation = None

            if id_help < len(opl):
                (id_now_next, coord_next) = opl[id_help]
                xy_c_next = np.array(transfor_coord(coord_next, image_size))


            xy_c = np.array(transfor_coord(coord, image_size))
            if xy_c_next is not None:
                xy_translation = xy_c_next - xy_c

            erase_agent(img_a, agent_size, xy_c)
            local_force_field_grad = calculate_local_force_field_agents(local_force_field, local_force_field_size,
                                                                        local_force_field_size_half_x,
                                                                        local_force_field_size_half_y, xy_c,
                                                                        img_a, img_colors[id_key])


            if xy_c_next is not None:
                iiiii += 1
                if iiiii > 200:
                    xxxu = 1

                v_xy_force_field = force_field[xy_c[0], xy_c[1], 2:4]
                v_xy_wall = force_field_wall[xy_c[0], xy_c[1]]
                v_xy_agents = local_force_field_grad[12, 12]

                v_xy_force_field_n = np.copy(v_xy_force_field)
                v_xy_wall_n = np.copy(v_xy_wall)
                v_xy_agents_n = np.copy(v_xy_agents)

                my_norm = np.linalg.norm(v_xy_force_field_n)
                if math.fabs(my_norm) > 0.0001:
                    v_xy_force_field_n /= my_norm
                else:
                    v_xy_force_field_n = np.array([0,0])

                my_norm = np.linalg.norm(v_xy_wall_n)
                if math.fabs(my_norm) > 0.0001:
                    v_xy_wall_n /= my_norm
                else:
                    v_xy_wall_n = np.array([0,0])

                my_norm = np.linalg.norm(v_xy_agents_n)
                if math.fabs(my_norm) > 0.0001:
                    v_xy_agents_n /= my_norm
                else:
                    v_xy_agents_n = np.array([0,0])


                str_to_write = str(key) + ";" + str(id_now) \
                               + ";" + str(v_xy_force_field[0]) + ";" + str(v_xy_force_field[1]) \
                               + ";" + str(v_xy_wall[0]) + ";" + str(v_xy_wall[1]) \
                               + ";" + str(v_xy_agents[0]) + ";" + str(v_xy_agents[1]) \
                               + ";" + str(xy_translation[0]) + ";" + str(xy_translation[1])

                f.write(str_to_write + "\n")

                xx = 1
            plot_agent(img_a, agent_size, xy_c, img_colors[id_key])
            if id_all[id_key] < len(opl) -1:
                id_all[id_key] = id_all[id_key] + 1
        id_key = id_key + 1

    print(id)
    print(iiiii)
    img_a = img_a.astype(np.uint8)
    cv2.imshow("a", img_a)
    cv2.waitKey(1)

f.close()