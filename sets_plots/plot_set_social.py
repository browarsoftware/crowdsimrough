import numpy as np
import matplotlib.pyplot as plt
import pickle
eps = 0.75
gap_size = 90
file = open('../data/rough_setb' + str(gap_size) + '_' + str(eps) + '_' + str(eps) + '.rs', 'rb')
my_title = 'Rough set visualization (bottleneck width= ' + str(gap_size) +'  cm, eps=' + str(eps) + ")"
feature_x = 'Social distance force x'
feature_y = 'Social distance force y'
data = pickle.load(file)
[all_rough_sets, columns_to_take, t_dir_r, df, df_sampled, ranges] = data
file.close()
unique_rows = np.unique(df_sampled, axis=0)


unique_rows = np.delete(unique_rows, 0, 1)
unique_rows = np.delete(unique_rows, 0, 1)
unique_rows = np.delete(unique_rows, 0, 1)

last_column = unique_rows.shape[1] - 1
my_min = np.min(unique_rows,axis=0)
my_max = np.max(unique_rows,axis=0)

import matplotlib as mpl
symbols = []

ccccc = all_rough_sets[7]
my_rot = [180,135,90,45,0,-45,-90,-135]
for a in range(8):
    t = mpl.markers.MarkerStyle(marker='<')
    t._transform = t.get_transform().rotate_deg(my_rot[a])
    symbols.append(t)
#symbols = ['o', '^', 's', 'd', 'v', 'p','X', '*']
colors = ['red','green','blue','cyan','magenta','gray','black','orange']
dir_name = ['E','SE','S','SW','W','NW','N','NE']
# Plot data
fig, ax = plt.subplots(figsize=(8, 9))
ax.title.set_text(my_title)
for a in range(8):
    mask = (unique_rows[:, last_column] == a)
    ur_ = np.copy(unique_rows[mask, :])
    col_list = [colors[a]] * ur_.shape[0]
    scat = ax.scatter(ur_[:,0]+0.5, ur_[:,1]+0.5, edgecolors=col_list, s=100, marker=symbols[a],
                      facecolors='none',
                      label=dir_name[a])
    a = a + 1

major_ticks = np.arange(my_min[0], my_max[0]+2, 10)
minor_ticks = np.arange(my_min[0], my_max[0]+2, 1)
ax.set_xticks(major_ticks)
ax.set_xticks(minor_ticks, minor=True)

major_ticks = np.arange(my_min[1], my_max[1]+2, 10)
minor_ticks = np.arange(my_min[1], my_max[1]+2, 1)
ax.set_yticks(major_ticks)
ax.set_yticks(minor_ticks, minor=True)

ax.legend(loc='upper left', scatterpoints=1)
ax.set(xlabel=feature_x, ylabel=feature_y)
plt.grid(which='both')

fig.tight_layout()
plt.show()
