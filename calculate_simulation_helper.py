import numpy as np
from scipy.ndimage import gaussian_filter
from numba import njit
import cv2

def prepare_local_force_field_array(local_force_field_size):
    local_force_field_size = np.array(local_force_field_size)
    local_force_field = np.zeros(local_force_field_size)#.astype(np.uint8)
    local_force_field_size_half_x = np.array([-int(local_force_field_size[0] / 2), int(local_force_field_size[0] / 2 + 1)])
    local_force_field_size_half_y = np.array([-int(local_force_field_size[1] / 2), int(local_force_field_size[1] / 2 + 1)])
    return [local_force_field_size, local_force_field, local_force_field_size_half_x, local_force_field_size_half_y]

def calculate_room_force_field_and_distance(image_size, img):
    dijk = calculate_room_force_field(image_size, img)
    distance_to_goal = np.copy(dijk)
    force_field = np.zeros((dijk.shape[0], dijk.shape[1], 4))
    dijk = np.transpose(dijk)
    gr = my_gradient(dijk)

    force_field[:, :, 2] = -gr[0]
    force_field[:, :, 3] = -gr[1]

    for x in range(force_field.shape[0]):
        for y in range(force_field.shape[1]):
            v_xy = np.array([force_field[x, y, 2], force_field[x, y, 3]])
            v_xy_norm = np.linalg.norm(v_xy)
            if v_xy_norm > 0:
                force_field[x, y, 2] = v_xy[0] / v_xy_norm
                force_field[x, y, 3] = v_xy[1] / v_xy_norm

    return [force_field, distance_to_goal]

def calculate_wall_force_field(img):
    img_copy = np.copy(img)
    # tutututu
    #gauss_wall = gaussian_filter(img_copy[:,:,0], sigma=5, radius=[5, 5])
    kernel = np.ones((11, 11), np.float32) / (11 * 11)
    gauss_wall = cv2.filter2D(img_copy[:,:,0], -1, kernel)

    gauss_wall = np.transpose(gauss_wall)
    gr_wall = np.gradient(gauss_wall)


    force_field_wall = np.zeros((gr_wall[0].shape[0], gr_wall[0].shape[1], 2))
    force_field_wall[:,:,0] = -gr_wall[0]
    force_field_wall[:,:,1] = -gr_wall[1]
    """
    for _x in range(force_field_wall.shape[0]):
        for _y in range(force_field_wall.shape[1]):
            v_xy = np.array([force_field_wall[_x,_y,0], force_field_wall[_x, _y, 1]])
            v_xy_norm = np.linalg.norm(v_xy)
            if v_xy_norm > 0:
                force_field_wall[_x, _y, 0] = 1 * v_xy[0] / v_xy_norm
                force_field_wall[_x, _y, 1] = 1 * v_xy[1] / v_xy_norm
    """
    return force_field_wall


def plot_room(image_size, gap_size = 10, white=(255, 255, 255)):
    img = np.zeros((image_size[0], image_size[1], 3)).astype(np.uint8)
    # left wall
    pol = int(image_size[0] / 2)
    cv2.rectangle(img, (0, pol), (pol - gap_size, image_size[1]), white, -1)
    cv2.rectangle(img, (pol + gap_size, pol), (image_size[0], image_size[1]), white, -1)

    #cv2.rectangle(img, (60, 0), (65, image_size[1]), (0,0,0), -1)

    return img


def calculate_room_force_field_helper(ll, dijk, pr, id):
    ll_new = []
    while len(ll) > 0:
        xx = ll.pop(0)
        if dijk[xx[0], xx[1]] == 0 and pr[xx[0], xx[1], 0] == 0:
            dijk[xx[0], xx[1]] = id
            #for _xy in [(-1,0),(0,1),(0,-1),(1,0)]:
            for _xy in [(-1, 0), (0, 1), (0, -1), (1, 0),(-1, -1), (-1, 1), (1, 1), (1, -1)]:
                if _xy[0] + xx[0] >= 0 and _xy[0] + xx[0] < dijk.shape[0] and _xy[1] + xx[1] >= 0 and _xy[1] + xx[1] < dijk.shape[1]:
                    if dijk[_xy[0] + xx[0], _xy[1] + xx[1]] == 0 and pr[_xy[0] + xx[0], _xy[1] + xx[1], 0] == 0:
                        ll_new.append((_xy[0] + xx[0], _xy[1] + xx[1]))
    return ll_new

def calculate_room_force_field(image_size, room):
    #pr = plot_room(image_size, gap_size)
    pr = room
    dijk = np.zeros(image_size)

    ll = []
    id = 1
    for a in range(image_size[1]):
        ll.append((image_size[0] - 1, a))

    while len(ll) > 0:
        ll = calculate_room_force_field_helper(ll, dijk, pr, id)
        id += 1
    return dijk


def my_gradient(local_force_field):
    x_array = np.zeros((local_force_field.shape[0], local_force_field.shape[1]))
    y_array = np.zeros((local_force_field.shape[0], local_force_field.shape[1]))
    for _x in range(local_force_field.shape[0]):
        for _y in range(local_force_field.shape[1]):
            id_x0 = 0
            id_x1 = 0
            if _x == 0 or (_x > 0 and local_force_field[_x - 1, _y] == 0):
                id_x0 = _x
            else:
                id_x0 = _x - 1
            if _x ==  local_force_field.shape[0] - 1 or (_x < local_force_field.shape[0] - 1 and local_force_field[_x + 1, _y] == 0):
                id_x1 = _x
            else:
                id_x1 = _x + 1
            x_array[_x, _y] = local_force_field[id_x1, _y] - local_force_field[id_x0, _y]

            id_y0 = 0
            id_y1 = 0
            if _y == 0 or (_y > 0 and local_force_field[_x, _y - 1] == 0):
                id_y0 = _y
            else:
                id_y0 = _y - 1
            if _y ==  local_force_field.shape[1] - 1 or (_y < local_force_field.shape[1] - 1 and local_force_field[_x, _y + 1] == 0):
                id_y1 = _y
            else:
                id_y1 = _y + 1
            x_array[_x, _y] = local_force_field[id_x1, _y] - local_force_field[id_x0, _y]
            y_array[_x, _y] = local_force_field[_x, id_y1] - local_force_field[_x, id_y0]
    return [x_array, y_array]


def is_color_correct(Agents, a):
    if a.color is None: return True
    for _a in Agents:
        if _a.color[0] == a.color[0] and _a.color[1] == a.color[1] and _a.color[2] == a.color[2]:
            return True
    return False


@njit
def initialize_agents_force_field(img, agents_force_field):
    for _x in range(img.shape[0]):
        for _y in range(img.shape[1]):
            if (img[_x,_y,0] > 0 or img[_x,_y,1] > 0 or img[_x,_y,2] > 0) and (img[_x,_y,0] != 255 or img[_x,_y,1] !=255 and img[_x,_y,2] != 255):
                agents_force_field[_x,_y] = 255
            else:
                agents_force_field[_x, _y] = 0
    return agents_force_field

@njit
def normalize_force_field(force_field):
    for _x in range(force_field.shape[0]):
        for _y in range(force_field.shape[1]):
            v_xy = np.array([force_field[_x, _y, 0], force_field[_x, _y, 1]])
            v_xy_norm = np.linalg.norm(v_xy)
            if v_xy_norm > 0:
                force_field[_x, _y, 0] = -1 * v_xy[0] / v_xy_norm
                force_field[_x, _y, 1] = -1 * v_xy[1] / v_xy_norm
    return force_field

def order_agents(Agents,distance_to_goal):
    return sorted(Agents, key=lambda x: distance_to_goal[x.position[1],x.position[0]])#, reverse=True)

@njit
def calculate_local_force_field_agents_fast(local_force_field, local_force_field_size, local_force_field_size_half_x, local_force_field_size_half_y, position, img, color):
    #x_start = position[0] - local_force_field_size_half[0]
    #y_start = position[1] - local_force_field_size_half[1]
    for _x in range(local_force_field_size_half_x[0], local_force_field_size_half_x[1]):
        for _y in range(local_force_field_size_half_y[0], local_force_field_size_half_y[1]):
            __x = _x + position[1]
            __y = _y + position[0]
            ddddd = img[position[1], position[0],:]
            if (__x >= 0 and __y >= 0 and __x < img.shape[0] and __y < img.shape[1]):
                ddd = img[__x,__y,0]
                ddd += 1
                if (img[__x,__y,0] == 0 and img[__x,__y,1] == 0 and img[__x,__y,2] == 0) \
                    or (img[__x,__y,0] == color[0] and img[__x,__y,1] == color[1] and img[__x,__y,2] == color[2]) \
                    or (img[__x,__y,0] == 255 and img[__x,__y,1] == 255 and img[__x,__y,2] == 255):
                        local_force_field[__x - local_force_field_size_half_x[0] - position[1],
                            __y - local_force_field_size_half_y[0] - position[0]] = 0
                else:
                    local_force_field[__x - local_force_field_size_half_x[0] - position[1],
                                           __y - local_force_field_size_half_y[0] - position[0]] = 255
            else:
                local_force_field[__x - local_force_field_size_half_x[0] - position[1],
                                  __y - local_force_field_size_half_y[0] - position[0]] = 0
    return local_force_field



def calculate_local_force_field_agents(local_force_field, local_force_field_size, local_force_field_size_half_x, local_force_field_size_half_y, position, img, color):
    local_force_field = calculate_local_force_field_agents_fast(local_force_field, local_force_field_size, local_force_field_size_half_x, local_force_field_size_half_y,
     position, img, color)

    #local_force_field = np.transpose(local_force_field)
    #cv2.imshow("a", cv2.resize(local_force_field, (256, 256)))
    #cv2.imshow("b1", cv2.resize(local_force_field, (256, 256)))

    # tututu
    #local_force_field = gaussian_filter(local_force_field, sigma=1, radius=[10, 10])
    kernel = np.ones((11, 11), np.float32) / (11 * 11)
    local_force_field = cv2.filter2D(local_force_field, -1, kernel)

    local_force_field = np.transpose(local_force_field)
    #cv2.imshow("a1", cv2.resize(local_force_field,(256, 256)))
    #cv2.waitKey()
    gr_local_force_field = np.gradient(local_force_field)


    local_force_field_grad = np.zeros((gr_local_force_field[0].shape[0], gr_local_force_field[0].shape[1], 2))



    local_force_field_grad[:, :, 0] = -gr_local_force_field[0]
    local_force_field_grad[:, :, 1] = -gr_local_force_field[1]

    #local_force_field_grad = normalize_force_field(local_force_field_grad)
    #cv2.imshow('a', cv2.resize(local_force_field_grad[1],(256,256)))
    #cv2.waitKey()
    return local_force_field_grad
