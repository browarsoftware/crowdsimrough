# Helper functions for agent motion
from numba import njit
import math
@njit
def plot_agent(img, shape,position, color):
    agent_width = shape.shape[0]
    agent_height = shape.shape[1]
    agent_left = - int(agent_width / 2)
    agent_right = agent_left + agent_width
    agent_bottom = - int(agent_height / 2)
    agent_top = agent_bottom + agent_height

    x1 = 0
    for x in range(agent_left,agent_right, 1):
        y1 = 0
        for y in range(agent_bottom, agent_top, 1):
            if shape[x1, y1] > 0:
                if position[1] + y >= 0 and position[1] + y < img.shape[0] and position[0] + x >= 0 and position[0] + x < img.shape[1]:
                    img[position[1] + y, position[0] + x, 0] = color[0]
                    img[position[1] + y, position[0] + x, 1] = color[1]
                    img[position[1] + y, position[0] + x, 2] = color[2]
            y1 += 1
        x1 += 1

@njit
def erase_agent(img, shape, position):
    agent_width = shape.shape[0]
    agent_height = shape.shape[1]
    agent_left = - int(agent_width / 2)
    agent_right = agent_left + agent_width
    agent_bottom = - int(agent_height / 2)
    agent_top = agent_bottom + agent_height

    x1 = 0
    for x in range(agent_left,agent_right, 1):
        y1 = 0
        for y in range(agent_bottom, agent_top, 1):
            if shape[x1, y1] > 0:
                if position[1] + y >= 0 and position[1] + y < img.shape[0] and position[0] + x >= 0 and position[0] + x < img.shape[1]:
                    img[position[1] + y, position[0] + x, 0] = 0
                    img[position[1] + y, position[0] + x, 1] = 0
                    img[position[1] + y, position[0] + x, 2] = 0
            y1 += 1
        x1 += 1

@njit
def check_if_equal_fast(pos, xyxy):
    if pos[0] != xyxy[0] or pos[1] != xyxy[1]:
        return False
    return True

@njit
def check_collison_fast(img, position, agent_left, agent_right, agent_bottom, agent_top, shape, color0, color1, color2):
    x1 = 0
    for x in range(agent_left, agent_right, 1):
        y1 = 0
        for y in range(agent_bottom, agent_top, 1):
            if position[1] + y >= 0 and position[1] + y < img.shape[0] and position[0] + x >= 0 and position[0] + x < \
                    img.shape[1]:
                if shape[x1, y1] > 0:
                    if (img[position[1] + y, position[0] + x, 0] > 0 and img[position[1] + y, position[0] + x, 0] != color0) \
                        or (img[position[1] + y, position[0] + x, 1] > 0 and img[position[1] + y, position[0] + x, 1] != color1) \
                        or (img[position[1] + y, position[0] + x, 2] > 0 and img[position[1] + y, position[0] + x, 2] != color2):
                            return True
            else:
                return True
            y1 += 1
        x1 += 1
    return False

@njit
def signum(x):
    if x < 0:
        return -1
    if x > 0:
        return 1
    return 0

@njit
def check_collison(img, position, shape, color):
    agent_width = shape.shape[0]
    agent_height = shape.shape[1]
    agent_left = - int(agent_width / 2)
    agent_right = agent_left + agent_width
    agent_bottom = - int(agent_height / 2)
    agent_top = agent_bottom + agent_height
    #position = np.array(position)
    return check_collison_fast(img, position, agent_left, agent_right, agent_bottom, agent_top,
                               shape, color[0], color[1], color[2])

@njit
def check_position(position, xyxy, img, shape, color):
    if not check_if_equal_fast(position, xyxy) and not check_collison(img, xyxy, shape, color):
        return True
    return False

import numpy as np
@njit
def calculate_move(force_field, force_field_wall, force_field_agents, img, position, shape, color, rd, xyxy, max_distance):
    speed = 1
    # self.img_with_agents = np.copy(self.img)
    #img_with_agents = img
    pos_arr = np.zeros((int(max_distance) + 2, 2))
    pos_arr_id = 0

    if position[0] < 0 or position[0] >= force_field.shape[0] or position[1] < 0 or position[1] >= \
            force_field.shape[1]:
        #return position
        return  pos_arr

    """OK
    v_xy_force_field = 5 * force_field[position[0], position[1], 2:4]
    v_xy_wall = 0.25 * force_field_wall[position[0], position[1]]
    v_xy_agents = 8 * force_field_agents[12, 12]
    """
    #EXP
    """
    v_xy_force_field = 5 * force_field[position[0], position[1], 2:4]
    v_xy_wall = 0.25 * force_field_wall[position[0], position[1]]
    v_xy_agents = 8 * force_field_agents[12, 12]
    """
    # EXP 2
    v_xy_force_field = 5 * force_field[position[0], position[1], 2:4]
    v_xy_wall = 0.25 * force_field_wall[position[0], position[1]]
    #v_xy_agents = 8 * force_field_agents[12, 12]
    v_xy_agents = 8 * force_field_agents[12, 12]

    found = True
    v_xy = v_xy_force_field + v_xy_wall + v_xy_agents

    #v_xy = v_xy_agents
    v_xy_copy = np.copy(v_xy)

    if np.linalg.norm(v_xy) > speed:
        v_xy = speed * v_xy / np.linalg.norm(v_xy)

    distance_so_far = 0
    position_new = np.copy(position)
    while distance_so_far < max_distance and found:
        found = False
        #ii += 1
        xyxy[0] = int(round(position_new[0] + v_xy[0]))
        xyxy[1] = int(round(position_new[1] + v_xy[1]))
        #znaleziony kierunek
        if check_position(position_new, xyxy, img, shape, color):
            hx = int(round(v_xy[0]))
            hy = int(round(v_xy[1]))
            distance_so_far += math.sqrt(hx * hx + hy * hy)
            found = True
        if not found:
            #dluzszy wektor
            if math.fabs(v_xy[0]) >= math.fabs(v_xy[1]):
                xyxy[0] = position_new[0] + speed * signum(v_xy[0])
                xyxy[1] = position_new[1]
                if check_position(position_new, xyxy, img, shape, color):
                    distance_so_far += 1
                    found = True
            else:
                xyxy[0] = position_new[0]
                xyxy[1] = position_new[1] + speed * signum(v_xy[1])
                if check_position(position_new, xyxy, img, shape, color):
                    distance_so_far += 1
                    found = True

            if not found:
                #skos
                xyxy[0] = position_new[0] + speed * signum(v_xy[0])
                xyxy[1] = position_new[1] + speed * signum(v_xy[1])
                if not check_if_equal_fast(position_new, xyxy) and not check_collison(img, xyxy, shape, color):
                    distance_so_far += math.sqrt(2)
                    found = True
            if not found:
                #dol-gora
                xyxy[0] = position_new[0] + speed * signum(v_xy[0])
                xyxy[1] = position_new[1]
                if not check_if_equal_fast(position_new, xyxy) and not check_collison(img, xyxy, shape, color):
                    distance_so_far += 1
                    found = True
            if not found:
                #prawo-lewo
                xyxy[0] = position_new[0]
                xyxy[1] = position_new[1] + speed * signum(v_xy[1])
                if not check_if_equal_fast(position_new, xyxy) and not check_collison(img, xyxy, shape, color):
                    distance_so_far += 1
                    # agent_xy = xyxy
                    found = True


            ##############################
            # try one random steps in all directions
            #rd = random_dir()
            a = 0
            while not found and a < len(rd):
                _rd = rd[a]
                # xyxy = [self.position[0] + _rd[0], self.position[1] + _rd[1]]
                xyxy[0] = position_new[0] + speed * _rd[0]
                xyxy[1] = position_new[1] + speed * _rd[1]
                if not check_if_equal_fast(position_new, xyxy) and not check_collison(img, xyxy, shape, color):
                    distance_so_far += math.sqrt(_rd[0] * _rd[0] + _rd[1] * _rd[1])
                    found = True
                a += 1
        if found:
            position_new[0] = xyxy[0]
            position_new[1] = xyxy[1]
            pos_arr[pos_arr_id, 0] = xyxy[0]
            pos_arr[pos_arr_id, 1] = xyxy[1]
            pos_arr_id += 1
    if found:
        #return xyxy
        return pos_arr
    else:
        #return position_new
        return np.zeros((int(max_distance) + 2, 2))

