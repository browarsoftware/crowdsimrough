import math
import numpy as np
from numba import njit

class Agent:
    def __init__(self):
        self.position = None
        self.img = None
        self.img_with_agents = None
        self.shape = None
        self.max_distance = 3
        self.color = None
        self.random_dir = None
        self.id = 0
        self.v_xy = np.array([0, 0])
        self.old_position = []

    def erase_agent(self, img):
        agent_width = self.shape.shape[0]
        agent_height = self.shape.shape[1]
        agent_left = - int(agent_width / 2)
        agent_right = agent_left + agent_width
        agent_bottom = - int(agent_height / 2)
        agent_top = agent_bottom + agent_height

        x1 = 0
        for x in range(agent_left,agent_right, 1):
            y1 = 0
            for y in range(agent_bottom, agent_top, 1):
                if self.shape[x1, y1] > 0:
                    if self.position[1] + y >= 0 and self.position[1] + y < img.shape[0] and self.position[0] + x >= 0 and self.position[0] + x < img.shape[1]:
                        img[self.position[1] + y, self.position[0] + x, 0] = 0
                        img[self.position[1] + y, self.position[0] + x, 1] = 0
                        img[self.position[1] + y, self.position[0] + x, 2] = 0
                y1 += 1
            x1 += 1

    def plot_agent(self, img):
        agent_width = self.shape.shape[0]
        agent_height = self.shape.shape[1]
        agent_left = - int(agent_width / 2)
        agent_right = agent_left + agent_width
        agent_bottom = - int(agent_height / 2)
        agent_top = agent_bottom + agent_height

        x1 = 0
        for x in range(agent_left,agent_right, 1):
            y1 = 0
            for y in range(agent_bottom, agent_top, 1):
                if self.shape[x1, y1] > 0:
                    if self.position[1] + y >= 0 and self.position[1] + y < img.shape[0] and self.position[0] + x >= 0 and self.position[0] + x < img.shape[1]:
                        img[self.position[1] + y, self.position[0] + x, 0] = self.color[0]
                        img[self.position[1] + y, self.position[0] + x, 1] = self.color[1]
                        img[self.position[1] + y, self.position[0] + x, 2] = self.color[2]
                y1 += 1
            x1 += 1

    def check_collison(self, img, position):
        agent_width = self.shape.shape[0]
        agent_height = self.shape.shape[1]
        agent_left = - int(agent_width / 2)
        agent_right = agent_left + agent_width
        agent_bottom = - int(agent_height / 2)
        agent_top = agent_bottom + agent_height
        position = np.array(position)
        return check_collison_fast(img, position, agent_left, agent_right, agent_bottom, agent_top,
                                   self.shape, self.color[0], self.color[1], self.color[2])

    def signum(self, x):
        if x < 0:
            return -1
        if x > 0:
            return 1
        return 0

    def check_if_equal(self, pos, xyxy):
        return check_if_equal_fast(pos, xyxy)

    def calculate_move(self, force_field):
        #self.img_with_agents = np.copy(self.img)
        self.img_with_agents = self.img
        if self.position[0] < 0 or self.position[0] >= force_field.shape[0] or self.position[1] < 0 or self.position[1] >= force_field.shape[1]:
            return self.position

        v_xy = force_field[self.position[0], self.position[1], 2:4]

        if self.id == 1:
            a = 0
        #xyxy = [int(round(self.position[0] + v_xy[0])), int(round(self.position[1] + v_xy[1]))]
        xyxy = np.zeros(2).astype(int)
        xyxy[0] = int(round(self.position[0] + v_xy[0]))
        xyxy[1] = int(round(self.position[1] + v_xy[1]))

        found = False
        if not self.check_if_equal(self.position, xyxy) and not self.check_collison(self.img_with_agents, xyxy):
            # agent_xy = xyxy
            found = True
        if not found:
            if math.fabs(v_xy[0]) >= math.fabs(v_xy[1]):
                #xyxy = [self.position[0] + self.signum(v_xy[0]), self.position[1]]
                xyxy[0] = self.position[0] + self.signum(v_xy[0])
                xyxy[1] = self.position[1]

                if not self.check_if_equal(self.position, xyxy) and not self.check_collison(self.img_with_agents, xyxy):
                    # agent_xy = xyxy
                    found = True
            else:
                #xyxy = [self.position[0], self.position[1] + self.signum(v_xy[1])]
                xyxy[0] = self.position[0]
                xyxy[1] = self.position[1] + self.signum(v_xy[1])
                if not self.check_if_equal(self.position, xyxy) and not self.check_collison(self.img_with_agents, xyxy):
                    # agent_xy = xyxy
                    found = True
        if not found:
            #xyxy = [self.position[0] + self.signum(v_xy[0]), self.position[1] + self.signum(v_xy[1])]
            xyxy[0] = self.position[0] + self.signum(v_xy[0])
            xyxy[1] = self.position[1] + self.signum(v_xy[1])
            if not self.check_if_equal(self.position, xyxy) and not self.check_collison(self.img_with_agents, xyxy):
                # agent_xy = xyxy
                found = True
        if not found:
            #xyxy = [self.position[0] + self.signum(v_xy[0]), self.position[1]]
            xyxy[0] = self.position[0] + self.signum(v_xy[0])
            xyxy[1] = self.position[1]
            if not self.check_if_equal(self.position, xyxy) and not self.check_collison(self.img_with_agents, xyxy):
                # agent_xy = xyxy
                found = True
        if not found:
            #xyxy = [self.position[0], self.position[1] + self.signum(v_xy[1])]
            xyxy[0] = self.position[0]
            xyxy[1] = self.position[1] + self.signum(v_xy[1])
            if not self.check_if_equal(self.position, xyxy) and not self.check_collison(self.img_with_agents, xyxy):
                # agent_xy = xyxy
                found = True
        ##############################
        # try one random steps in all directions
        rd = self.random_dir()
        a = 0
        while not found and a < len(rd):
            _rd = rd[a]
            #xyxy = [self.position[0] + _rd[0], self.position[1] + _rd[1]]
            xyxy[0] = self.position[0] + _rd[0]
            xyxy[1] = self.position[1] + _rd[1]
            if not self.check_if_equal(self.position, xyxy) and not self.check_collison(self.img_with_agents, xyxy):
                found = True
            a += 1

        if found:
            return xyxy
        else:
            return self.position





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
            y1 += 1
        x1 += 1
    return False

@njit
def check_if_equal_fast(pos, xyxy):
    if pos[0] != xyxy[0] or pos[1] != xyxy[1]:
        return False
    return True