# ORDER OF RUN: #6
# Rough sets simulation, data from file
import cv2
from agent import Agent
import random
import numpy as np
from calculate_simulation_helper import plot_room, calculate_room_force_field_and_distance, is_color_correct, \
    order_agents, calculate_local_force_field_agents, calculate_wall_force_field, prepare_local_force_field_array
from data_reader import read_from_cvs

image_size = [512,512]
denisty_plot = np.ones(image_size)
local_force_field_size = [25, 25]

# Change gap_size to 9, 10, 12, 14, 16, 18, 20
gap_size = 9
# Change eps to 0.5, 0.7
eps = 0.5

# If save_to_file = None results will not be saved to png
save_to_file = None #'d:/Publikacje/Infromation Sciences Rough set/fig/sym_samples/from_file'+ str(gap_size) + '0_rough_' + str(eps) + '/'
save_to_file_id = 0
# Uncomment if 90
data_file_name = 'd:\\dane\\trajektorie\\b090_combined.txt '
# Uncomment if > 90
#data_file_name = 'data/b' + str(gap_size) + '0_combined.txt '

file_save_plot_data = "results\\simulation_rough_from_file\\plot_data" + str(gap_size) + '0_' + str(eps) + '_' + str(eps) + '.rs'
file_save_time_data = "results\\simulation_rough_from_file\\time_data" + str(gap_size) + '0_' + str(eps) + '_' + str(eps) + '.rs'

white = (255, 255, 255)
file_name = 'data//rough_setb' + str(gap_size) + '0_' + str(eps) + '_' + str(eps) + '.rs'

agents_x = 50
agents_y = 20
agent_max_distance = 3

[op, opd, range_x, range_y, range_z, last_frame_id] = read_from_cvs(data_file_name, " ", True)

# Calculate static fields
img = plot_room(image_size, gap_size)
force_field_wall= calculate_wall_force_field(img)
[force_field, distance_to_goal] = calculate_room_force_field_and_distance(image_size, img)
[local_force_field_size, local_force_field, local_force_field_size_half_x, local_force_field_size_half_y] \
    = prepare_local_force_field_array(local_force_field_size)

def stop_criterium(position):
    if position[1] > 346:#img.shape[1]-10:
        return True


rnd = random.Random()
def random_dir():
    directions = [(1, 1), (1, -1), (-1, 1), (-1, -1), (0, 1), (0, -1), (1, 0), (-1, 0)]
    rnd.shuffle(directions)
    return directions

#############################################################################
# Initialize agents
Agents = []
Agents_done = []
rnd.seed(1)
agent_size = np.ones((5, 5))
agent_size[0,0] = 0
agent_size[4,4] = 0
agent_size[0,4] = 0
agent_size[4,0] = 0
id = 0

from find_directions_rough import find_directions, genarate_sets, discretization, calculate_dir
import pickle

file = open(file_name, 'rb')
data = pickle.load(file)
[all_rough_sets, columns_to_take, t_dir_r, df, df_sampled, ranges] = data
file.close()


def calculate_ff_dir(x, y):
    xr = round(x)
    yr = round(y)
    if xr == 0 and yr == 0:
        return 0.0
    if xr == 1 and yr == 0:
        return 1.
    if xr == 1 and yr == 1:
        return 2.
    if xr == 0 and yr == 1:
        return 3.
    if xr == -1 and yr == 1:
        return 4.
    if xr == -1 and yr == 0:
        return 5.
    if xr == -1 and yr == -1:
        return 6.
    if xr == 0 and yr == -1:
        return 7.
    if xr == 1 and yr == -1:
        return 8.
    return 0.

from evaluate_agent import check_position

def calculate_move_rough(force_field, force_field_wall, local_force_field_grad, img_a, position, shape, color, rd, xyxy, max_distance):
    new_pos = []
    xy_c = position
    v_xy_force_field = force_field[xy_c[0], xy_c[1], 2:4]
    v_xy_wall = force_field_wall[xy_c[0], xy_c[1]]
    v_xy_agents = local_force_field_grad[12, 12]

    ff_dir = calculate_ff_dir(v_xy_force_field[0], v_xy_force_field[1])
    fw_x = v_xy_wall[0]
    fw_y = v_xy_wall[1]
    fa_x = v_xy_agents[0]
    fa_y = v_xy_agents[1]

    my_coord_val = [str(ff_dir), fw_x, fw_y, fa_x, fa_y]
    my_coord = discretization(my_coord_val, ranges)

    dir_help = find_directions(my_coord, all_rough_sets, columns_to_take, t_dir_r)
    move_done = False

    b = 0
    while not move_done and b < len(dir_help):
        a = 0
        while not move_done and  a < len(dir_help[b]):
            dd = dir_help[b][a][0]

            v_xy = calculate_dir(float(dd))
            position_new = np.copy(position)

            xyxy[0] = position_new[0] + v_xy[0]
            xyxy[1] = position_new[1] + v_xy[1]

            #xyxy[0] = position_new[0] + 0
            #xyxy[1] = position_new[1] + 1


            if check_position(position_new, xyxy, img_a, shape, color):
                new_pos = xyxy
                move_done = True
            a = a + 1
        b = b + 1
    if not move_done:
        new_pos = position_new

    return new_pos

def get_random(rd):
    my_sum = 0
    for a in range(len(rd)):
        my_sum += rd[a][1]
    ran_sum = random.randint(0, my_sum)

    sum = 0
    id = 0
    while sum < ran_sum:
        sum += rd[id][1]
        id += 1
    return id - 1


def calculate_move_rough_random(force_field, force_field_wall, local_force_field_grad, img_a, position, shape, color, rd, xyxy, max_distance):
    new_pos = []
    xy_c = position
    v_xy_force_field = force_field[xy_c[0], xy_c[1], 2:4]
    v_xy_wall = force_field_wall[xy_c[0], xy_c[1]]
    v_xy_agents = local_force_field_grad[12, 12]

    ff_dir = calculate_ff_dir(v_xy_force_field[0], v_xy_force_field[1])
    fw_x = v_xy_wall[0]
    fw_y = v_xy_wall[1]
    fa_x = v_xy_agents[0]
    fa_y = v_xy_agents[1]

    my_coord_val = [str(ff_dir), fw_x, fw_y, fa_x, fa_y]
    #print(my_coord_val)

    my_coord = discretization(my_coord_val, ranges)
    dir_help = find_directions(my_coord, all_rough_sets, columns_to_take, t_dir_r)
    move_done = False

    b = 0
    while not move_done and b < len(dir_help):
        a = 0
        dir_help_random = []

        while not move_done and len(dir_help[b]) > 0:
            id = get_random(dir_help[b])
            dd = dir_help[b].pop(id)[0]
            #dd = dir_help[0][a][0]

            v_xy = calculate_dir(float(dd))
            position_new = np.copy(position)

            xyxy[0] = position_new[0] + v_xy[0]
            xyxy[1] = position_new[1] + v_xy[1]

            #xyxy[0] = position_new[0] + 0
            #xyxy[1] = position_new[1] + 1


            if check_position(position_new, xyxy, img_a, shape, color):
                new_pos = xyxy
                move_done = True
            a = a + 1
        b = b + 1
    if not move_done:
        #new_pos = position_new
        new_pos = position

    return new_pos


#from numba import njit
from evaluate_agent import plot_agent, calculate_move, erase_agent
cc = 0
img = plot_room(image_size, gap_size)

import time
start = time.time()

img_colors = []
id_all = []
for key in opd:
    img_colors.append(np.array([rnd.randint(0, 255), rnd.randint(0, 255), rnd.randint(0, 255)]))
    id_all.append(id)

img_a = np.copy(img)
for a in Agents:
    plot_agent(img_a, a.shape, a.position, a.color)

end_me = False
id = 0
# Run simulation until all agents leave area
#while len(Agents) > 0 and not end_me:

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
            """
            if img_a[a][b][0] == 255 and img_a[a][b][1] == 255 or img_a[a][b][2] == 255:
                xxxx = 1
                xxxx += 1"""
            if (img_a[a][b][0] != 255 or img_a[a][b][1] != 255 or img_a[a][b][2] != 255) and \
                (img_a[a][b][0] > 0 or img_a[a][b][1] > 0 or img_a[a][b][2] > 0):
                denisty_plot[a][b] += 1


agents_id = 0
while len(op) > 0 or len(Agents) > 0:
    id_key = 0
    update_denisty_plot(denisty_plot, img_a)
    for key in opd:
        if key in op:
            opl = op[key]
            (id_now,coord) = opl[id_all[id_key]]
            if id_now == id:
                xy_c = np.array(transfor_coord(coord, image_size))
                #plot_agent(img_a, agent_size, xy_c, img_colors[id_key])

                a = Agent()
                a.position = np.array([xy_c[0], xy_c[1]])
                #a.color = np.array(img_colors[key])
                a.color = np.array((rnd.randint(30, 255), rnd.randint(30, 255), rnd.randint(30, 255)))
                a.max_distance = agent_max_distance
                # do not allow same color of two agents
                while is_color_correct(Agents, a):
                    a.color = np.array((rnd.randint(30, 255), rnd.randint(30, 255), rnd.randint(30, 255)))

                a.shape = agent_size
                a.random_dir = random_dir
                a.id = agents_id
                agents_id += 1
                Agents.append(a)

                op.pop(key)


    start = time.time()
    # Order agents, closest to goal is first
    Agents = order_agents(Agents, distance_to_goal)
    img_a = np.copy(img)
    for a in Agents:
        plot_agent(img_a, a.shape, a.position, a.color)

    # For each agent
    for a in Agents:
        a.img = img_a
        dist = 0
        #a.max_distance
        cc = 0
        while dist < a.max_distance and cc < 3:
        #for cc in range(3):
            rd = random_dir()
            xyxy = np.zeros(2).astype(int)
            # Calculate local force field
            local_force_field_grad = calculate_local_force_field_agents(local_force_field, local_force_field_size,
                                        local_force_field_size_half_x,
                                       local_force_field_size_half_y, a.position, img_a, a.color)
            # Make move
            new_pos = calculate_move_rough_random(force_field, force_field_wall, local_force_field_grad, img_a, a.position, a.shape, a.color, np.array(rd), xyxy, a.max_distance)
            # If agent moved (has new position)
            dist_help = np.linalg.norm(new_pos - a.position)
            if np.linalg.norm(new_pos - a.position) > 0.01:#  and check_position(a.position, new_pos, img_a, a.shape, a.color):
            #if True:
                # Remove agent from map
                erase_agent(img_a, a.shape, a.position)
                if new_pos[0] < 0: new_pos[0] = 0
                if new_pos[1] < 0: new_pos[1] = 0
                if new_pos[0] >= img.shape[1]: new_pos[0] = img.shape[1] - 1
                if new_pos[1] >= img.shape[0]: new_pos[1] = img.shape[0] - 1
                a.old_position.append(a.position)
                a.position = new_pos
                # Plot agent on map
                plot_agent(img_a, a.shape, a.position, a.color)
                dist += dist_help

            cc += 1
        #cv2.imshow("a", cv2.resize(img_a, (512, 512)))
        #cv2.waitKey(100)
    # Remove each agent which satisfied stop criteria
    for a in Agents:
        if stop_criterium(a.position):
            erase_agent(img_a, a.shape, a.position)
            Agents_done.append(a)
            Agents.remove(a)
    print(time.time() - start)
    cv2.imshow("a", cv2.resize(img_a,(512,512)))

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

    #img_a = np.copy(img)
    id = id + 1
    cv2.waitKey(1)

#################################################################################

from matplotlib import pyplot as plt
from matplotlib.colors import LogNorm
denisty_plot = denisty_plot[150:(512-150),150:(512-150)]

denisty_plot_mirror = np.zeros(denisty_plot.shape)
for a in range(denisty_plot.shape[0]):
    for b in range(denisty_plot.shape[1]):
        denisty_plot_mirror[a, b] = denisty_plot[denisty_plot.shape[0] - a - 1, b]

denisty_plot = denisty_plot_mirror
#denisty_plot = np.transpose(np.transpose(denisty_plot))
#denisty_plot = np.transpose(denisty_plot)
plt.pcolormesh(denisty_plot, norm=LogNorm(), cmap='inferno')
plt.colorbar()

import pickle
file = open(file_save_plot_data, 'wb')
pickle.dump(denisty_plot,file)
file.close()
file = open(file_save_time_data, 'wb')
agents_paths = []
for a in Agents_done:
    agents_paths.append(a.old_position)
pickle.dump(agents_paths,file)
file.close()


plt.show()

cv2.waitKey()
