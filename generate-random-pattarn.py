import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches

scale_x, scale_y = 32, 32
SAMPLE = 15
positon_x, position_y = np.random.normal(0,1,SAMPLE), np.random.normal(0,1,SAMPLE)
scale = np.random.normal(0,1,SAMPLE**2)

fig, ax = plt.subplots(figsize=(8, 8))

for i in range(SAMPLE):
    c = patches.Circle( xy=(positon_x[i], position_y[i]), radius=scale[i] )
    ax.add_patch(c)

plt.show()
