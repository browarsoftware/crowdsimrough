# ORDER OF RUN: #5
# Social forces simulation, data from file
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

white = (255, 255, 255)

# Change path to 90, 100, 120, 140, 160, 180, 200
data_file_name = 'data/b090_combined.txt '
file_save_plot_data = "results/simulation_forces_from_file/plot_data90"
file_save_time_data = "results/simulation_forces_from_file/time_data90"
#data_file_name = 'd:\\dane\\trajektorie\\b180_combined.txt '
#file_save_plot_data = "results\\simulation_from_file\\plot_data220"
#file_save_time_data = "results\\simulation_from_file\\time_data220"
[op, opd, range_x, range_y, range_z, last_frame_id] = read_from_cvs(data_file_name, " ", True)

# Change gap_size to 9, 10, 12, 14, 16, 18, 20
gap_size = 9
agents_x = 50
agents_y = 20
agent_max_distance = 3

# If save_to_file = None results will not be saved to png
save_to_file = None #'d:/Publikacje/Infromation Sciences Rough set/fig/sym_samples/from_filesimulation'+ str(gap_size) + '0/'
save_to_file_id = 0

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

from numba import njit
@njit
def update_denisty_plot(denisty_plot, img_a):
    for a in range(denisty_plot.shape[0]):
        for b in range(denisty_plot.shape[1]):
            if (img_a[a][b][0] != 255 or img_a[a][b][1] != 255 or img_a[a][b][2] != 255) and \
                (img_a[a][b][0] > 0 or img_a[a][b][1] > 0 or img_a[a][b][2] > 0):
                denisty_plot[a][b] += 1

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


#from numba import njit
from evaluate_agent import plot_agent, calculate_move, erase_agent
cc = 0
img = plot_room(image_size, gap_size)

import time
start = time.time()

def transfor_coord(xy_old, image_size):
    xy_new = [0, 0]
    xy_new[0] = int(xy_old[0] / 5 + (image_size[0] / 2))
    xy_new[1] = int(xy_old[1] / 5 + (image_size[1] / 2))
    return  xy_new

img_colors = []
id_all = []
for key in opd:
    img_colors.append(np.array([rnd.randint(0, 255), rnd.randint(0, 255), rnd.randint(0, 255)]))
    id_all.append(id)

img_a = np.copy(img)
for a in Agents:
    plot_agent(img_a, a.shape, a.position, a.color)

# Run simulation until all agents leave area
#while len(Agents) > 0:
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

        rd = random_dir()
        xyxy = np.zeros(2).astype(int)
        # Calculate local force field
        local_force_field_grad = calculate_local_force_field_agents(local_force_field, local_force_field_size,
                                    local_force_field_size_half_x,
                                   local_force_field_size_half_y, a.position, img_a, a.color)
        # Make move
        new_pos = calculate_move(force_field, force_field_wall, local_force_field_grad, img_a, a.position, a.shape,
                                 a.color, np.array(rd), xyxy, a.max_distance)
        new_pos_copy = []
        new_pos_id = 0
        while new_pos_id < new_pos.shape[0] and new_pos[new_pos_id, 0] != 0 and new_pos[new_pos_id, 0] != 0:
            new_pos_id += 1
        new_pos_id -= 1
        if new_pos_id < 0:
            new_pos = a.position
        else:
            new_pos_id_help = 0
            while new_pos_id_help < new_pos_id:
                new_pos_copy.append(np.array([int(new_pos[new_pos_id_help, 0]), int(new_pos[new_pos_id_help, 1])]))
                new_pos_id_help += 1
            new_pos = np.array([int(new_pos[new_pos_id, 0]), int(new_pos[new_pos_id, 1])])

        # If agent moved (has new position)
        if np.linalg.norm(new_pos - a.position) > 0.01:
            # Remove agent from map
            erase_agent(img_a, a.shape, a.position)
            if new_pos[0] < 0: new_pos[0] = 0
            if new_pos[1] < 0: new_pos[1] = 0
            if new_pos[0] >= img.shape[1]: new_pos[0] = img.shape[1] - 1
            if new_pos[1] >= img.shape[0]: new_pos[1] = img.shape[0] - 1
            a.old_position.append(a.position)
            for old_pos in new_pos_copy:
                a.old_position.append(old_pos)
            a.position = new_pos
            # Plot agent on map
            plot_agent(img_a, a.shape, a.position, a.color)

        cc += 1
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
