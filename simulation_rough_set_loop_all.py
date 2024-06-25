# ORDER OF RUN: #7
# Simulation rough set, 1,000 agents
import cv2
from agent import Agent
import random
import numpy as np
from calculate_simulation_helper import plot_room, calculate_room_force_field_and_distance, is_color_correct, \
    order_agents, calculate_local_force_field_agents, calculate_wall_force_field, prepare_local_force_field_array

image_size = [512,512]
#for gap_size in [9,10,12,14,16,18,20]:
for gap_size in [20]:
    for eps in [0.5]:
        denisty_plot = np.ones(image_size)
        local_force_field_size = [25, 25]

        file_save_plot_data = "results/simulation_rough/plot_data" + str(gap_size) + '0_' + str(eps) + '_' + str(eps) + '.rs'
        file_save_time_data = "results/simulation_rough/time_data" + str(gap_size) + '0_' + str(eps) + '_' + str(eps) + '.rs'

        white = (255, 255, 255)
        file_name = 'data/rough_setb' + str(gap_size) + '0_' + str(eps) + '_' + str(eps) + '.rs'


        denisty_plot = np.ones(image_size)

        local_force_field_size = [25, 25]
        #image_size = [1000,1000]


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
                a.position = np.array([_x * 10 + 3, _y * 10 + 3])
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


        from find_directions_rough import find_directions, genarate_sets, discretization, calculate_dir
        import pickle
        #[all_rough_sets, columns_to_take, t_dir_r, df, ranges] = genarate_sets('results_to_file_imp_no_zero.txt', eps0=0.5, eps1=0.5)
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
                dist = 0
                a.max_distance
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
            #img_a = np.copy(img)
            cv2.waitKey(1)

        #################################################################################
        from matplotlib import pyplot as plt
        from matplotlib.colors import LogNorm
        #denisty_plot = denisty_plot[150:(512-150),150:(512-150)]

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
