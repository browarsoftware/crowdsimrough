# Plot input data to screen or file
import cv2
import numpy as np
from data_reader import read_from_cvs
from calculate_simulation_helper import plot_room
from evaluate_agent import plot_agent

file_name = 'data/b090_combined.txt'
# If save_to_file = None results will not be saved to png
save_to_file = 'fig/reference90/'
save_to_file_id = 0
image_size = [512,512]
white = (255, 255, 255)

gap_size = 9

agent_size = np.ones((5, 5))
agent_size[0,0] = 0
agent_size[4,4] = 0
agent_size[0,4] = 0
agent_size[4,0] = 0

img = plot_room(image_size, gap_size)
[op, opd, range_x, range_y, range_z, last_frame_id] = read_from_cvs(file_name, " ", True)

def calculate_linear_coeff(x0_x1, y0_y1):
    a = (y0_y1[0] - y0_y1[1]) / (x0_x1[0] - x0_x1[1])
    b = y0_y1[0] - (a * x0_x1[0])
    return (a, b)

image_size = [512,512]
(a0, b0) = calculate_linear_coeff((-1000, 1000), (0, image_size[0] - 1))
(a1, b1) = calculate_linear_coeff((-1000, 1000), (0, image_size[1] - 1))

def transfor_coord(xy_old, image_size):
    xy_new = [0, 0]
    xy_new[0] = int(xy_old[0] / 5 + (image_size[0] / 2))
    xy_new[1] = int(xy_old[1] / 5 + (image_size[1] / 2))
    return  xy_new

import random as rnd
id = 0
id_all = []
img_colors = []
for key in opd:
    img_colors.append((rnd.randint(0, 255), rnd.randint(0, 255), rnd.randint(0, 255)))
    id_all.append(0)
for id in range(last_frame_id):
    img_a = np.copy(img)
    id_key = 0
    for key in opd:
        opl = op[key]
        (id_now,coord) = opl[id_all[id_key]]
        if id_now == id:
            [x_c, y_c] = transfor_coord(coord, image_size)
            plot_agent(img_a, agent_size, (x_c, y_c), img_colors[id_key])

            if id_all[id_key] < len(opl) -1:
                id_all[id_key] = id_all[id_key] + 1
        id_key = id_key + 1

    print(id)
    img_a = img_a.astype(np.uint8)
    cv2.imshow("a", img_a)
    if save_to_file is not None:
        file_name_help = save_to_file
        if save_to_file_id < 10:
            file_name_help += '0'
        if save_to_file_id < 100:
            file_name_help += '0'
        if save_to_file_id < 1000:
            file_name_help += '0'
        if save_to_file_id < 10000:
            file_name_help += '0'
        file_name_help += str(save_to_file_id) + '.png'
        cv2.imwrite(file_name_help, img_a)
        save_to_file_id += 1
    cv2.waitKey(1)
