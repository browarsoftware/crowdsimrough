# ORDER OF RUN: #4
# Social forces simulation 1,000 agents
import cv2
from agent import Agent
import random
import numpy as np
from calculate_simulation_helper import plot_room, calculate_room_force_field_and_distance, is_color_correct, \
    order_agents, calculate_local_force_field_agents, calculate_wall_force_field, prepare_local_force_field_array


for gap_size in [9, 10, 12, 14, 16, 18, 20]:
    image_size = [512,512]
    denisty_plot = np.ones(image_size)
    local_force_field_size = [25, 25]


    white = (255, 255, 255)
    file_save_plot_data = "results\\simulation_social_forces\\plot_data" + str(gap_size)
    file_save_time_data = "results\\simulation_social_forces\\time_data" + str(gap_size)
    gap_size = int(gap_size)#9#5
    agents_x = 50
    agents_y = 20


    # Calculate static fields
    img = plot_room(image_size, gap_size)
    force_field_wall= calculate_wall_force_field(img)
    [force_field, distance_to_goal] = calculate_room_force_field_and_distance(image_size, img)
    [local_force_field_size, local_force_field, local_force_field_size_half_x, local_force_field_size_half_y] \
        = prepare_local_force_field_array(local_force_field_size)

    def stop_criterium(position):
        if position[1] > img.shape[1]-10:
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

    for _x in range(agents_x):
        for _y in range(agents_y):
            a = Agent()
            a.position = np.array([_x * 10 + 3, _y * 10 + 5])
            #a.position = np.array([_x * 8 + 100, _y * 8 + 5])
            #a.position = np.array([_x * 10 + 5, _y * 10 + 125])
            a.color = np.array((rnd.randint(30, 255), rnd.randint(30, 255), rnd.randint(30, 255)))
            #do not allow same color of two agents
            while is_color_correct(Agents, a):
                a.color = np.array((rnd.randint(30, 255), rnd.randint(30, 255), rnd.randint(30, 255)))

            a.shape = agent_size
            a.random_dir = random_dir
            a.id = id
            id += 1
            Agents.append(a)

    from numba import njit
    @njit
    def update_denisty_plot(denisty_plot, img_a):
        for a in range(denisty_plot.shape[0]):
            for b in range(denisty_plot.shape[1]):
                if (img_a[a][b][0] != 255 or img_a[a][b][1] != 255 or img_a[a][b][2] != 255) and \
                    (img_a[a][b][0] > 0 or img_a[a][b][1] > 0 or img_a[a][b][2] > 0):
                    denisty_plot[a][b] += 1

    #from numba import njit
    from evaluate_agent import plot_agent, calculate_move, erase_agent
    cc = 0
    img = plot_room(image_size, gap_size)

    import time
    start = time.time()

    img_a = np.copy(img)
    for a in Agents:
        plot_agent(img_a, a.shape, a.position, a.color)

    # Run simulation until all agents leave area
    while len(Agents) > 0:
        start = time.time()
        # Order agents, closest to goal is first
        Agents = order_agents(Agents, distance_to_goal)
        img_a = np.copy(img)
        for a in Agents:
            plot_agent(img_a, a.shape, a.position, a.color)

        update_denisty_plot(denisty_plot, img_a)
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
            new_pos = calculate_move(force_field, force_field_wall, local_force_field_grad, img_a, a.position, a.shape, a.color, np.array(rd), xyxy, a.max_distance)
            new_pos_copy = []
            new_pos_id = 0
            while new_pos_id < new_pos.shape[0] and new_pos[new_pos_id,0] != 0 and new_pos[new_pos_id,0] != 0:
                new_pos_id += 1
            new_pos_id -= 1
            if new_pos_id < 0:
                new_pos = a.position
            else:
                new_pos_id_help = 0
                while new_pos_id_help < new_pos_id:
                    new_pos_copy.append(np.array([int(new_pos[new_pos_id_help,0]),int(new_pos[new_pos_id_help,1])]))
                    new_pos_id_help += 1
                new_pos = np.array([int(new_pos[new_pos_id,0]),int(new_pos[new_pos_id,1])])

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
        #img_a = np.copy(img)
        cv2.waitKey(1)
    #cv2.waitKey()

    #################################################################################
    from matplotlib import pyplot as plt
    from matplotlib.colors import LogNorm
    #denisty_plot = denisty_plot[150:(512-150),150:(512-150)]

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

