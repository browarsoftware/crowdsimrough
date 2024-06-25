# ORDER OF RUN: #7
# Reference data
import cv2
import numpy as np
from data_reader import read_from_cvs
from calculate_simulation_helper import plot_room
from evaluate_agent import plot_agent, erase_agent

file_name = 'data/b140_combined.txt'
file_save_plot_data = "results/reference/plot_data140"
file_save_time_data = "results/reference/time_data120"


image_size = [512,512]
denisty_plot = np.ones(image_size)
white = (255, 255, 255)

gap_size = 12

agent_size = np.ones((5, 5))
agent_size[0,0] = 0
agent_size[4,4] = 0
agent_size[0,4] = 0
agent_size[4,0] = 0

from scipy.ndimage import gaussian_filter
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


from numba import njit
@njit
def update_denisty_plot(denisty_plot, img_a):
    for a in range(denisty_plot.shape[0]):
        for b in range(denisty_plot.shape[1]):
            if (img_a[a][b][0] != 255 or img_a[a][b][1] != 255 or img_a[a][b][2] != 255) and \
                (img_a[a][b][0] > 0 or img_a[a][b][1] > 0 or img_a[a][b][2] > 0):
                denisty_plot[a][b] += 1


import random as rnd
id = 0
id_all = []
img_colors = []
for key in opd:
    img_colors.append((rnd.randint(0, 255), rnd.randint(0, 255), rnd.randint(0, 255)))
    id_all.append(0)


Agents_done = []
for a in range(len(img_colors)):
    Agents_done.append([])

for id in range(last_frame_id):
    img_a = np.copy(img)
    #img = np.zeros((image_size[0], image_size[1], 3))
    #image_size = (512, 512)
    id_key = 0
    for key in opd:
        opl = op[key]
        (id_now,coord) = opl[id_all[id_key]]
        if id_now == id:
            #x_c = int(a0 * coord[0] + b0)
            #y_c = int(a1 * coord[1] + b1)

            [x_c, y_c] = transfor_coord(coord, image_size)
            #img[x_c,y_c] = img_colors[id_key]
            Agents_done[id_key].append([x_c, y_c])
            #img_a = cv2.circle(img_a, (x_c, y_c), 2, img_colors[id_key], -1)
            plot_agent(img_a, agent_size, (x_c, y_c), img_colors[id_key])

            if id_all[id_key] < len(opl) -1:
                id_all[id_key] = id_all[id_key] + 1
        id_key = id_key + 1

    print(id)
    img_a = img_a.astype(np.uint8)
    update_denisty_plot(denisty_plot, img_a)
    cv2.imshow("a", img_a)
    cv2.waitKey(1)

###############################################################################################

from matplotlib import pyplot as plt
from matplotlib.colors import LogNorm

xx = 0
yy = 0
for a in range(denisty_plot.shape[0]):
    for b in range(denisty_plot.shape[1]):
        if denisty_plot[a,b] > 1:
            if a > xx:
                xx = a
            if b > yy:
                yy = b

denisty_plot = denisty_plot[150:(512-150),150:(512-150)]

denisty_plot_mirror = np.zeros(denisty_plot.shape)
for a in range(denisty_plot.shape[0]):
    for b in range(denisty_plot.shape[1]):
        denisty_plot_mirror[a, b] = denisty_plot[denisty_plot.shape[0] - a - 1, denisty_plot.shape[1] - b - 1]

denisty_plot = denisty_plot_mirror
#denisty_plot = np.transpose(np.transpose(denisty_plot))
#denisty_plot = np.transpose(denisty_plot)
plt.pcolormesh(denisty_plot, norm=LogNorm(), cmap='inferno')
plt.colorbar()

import pickle
file = open(file_save_plot_data, 'wb')
data = pickle.dump(denisty_plot,file)
file.close()

file = open(file_save_time_data, 'wb')
pickle.dump(Agents_done,file)
file.close()


plt.show()

cv2.waitKey()
