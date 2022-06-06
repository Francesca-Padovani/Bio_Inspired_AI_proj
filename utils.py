import os
import glob
import shutil

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib import cm, markers

def make_gif_from_folder(folder, out_file_path, rm_folder = True):
    files = os.path.join(folder, '*.png')
    img, *imgs = [Image.open(f) for f in sorted(glob.glob(files))]
    img.show()
    img.save(fp=out_file_path, format='GIF', append_images=imgs,
            save_all=True, duration=200, loop=0)
    shutil.rmtree(folder, ignore_errors=True)

plt.rcParams['figure.figsize'] = [6,6]
plt.rcParams['figure.dpi'] = 100
plt.rcParams['font.size'] = 9


#cmap = cm.colors.LinearSegmentedColormap.from_list('Custom', [(0, '#e8e151'), (0.5, '#d6c5de'),(1, '#87005f')], N=256)

def plot_pso(meshgrid, image, swarm=None, v=None, color ='#000000', ax=None):
    X_grid,Y_grid = meshgrid
    Z_grid = image
    if swarm is not None:
        #X, Y = swarm.swapaxes(0, 1)
        X = swarm[:,1]
        Y = swarm[:,0]
        X = [round(i) for i in X]
        Y = [round(j) for j in Y]
        Z = []
        for i in range(len(X)):
            if X[i] >= image.shape[0] or Y[i] >= image.shape[1] or X[i] < 0  or Y[i] < 0:
                Z.append(10)
            else:
                Z.append(image[X[i],Y[i]])

    # create new ax if None
    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
    
    
    # add contour lines
    ax.contour(X_grid, Y_grid, Z_grid, levels=30, linewidths=0.1, colors='#999')
    cntr = ax.contourf(X_grid, Y_grid, Z_grid, levels=30, cmap="inferno", alpha=0.7)
    if swarm is not None:
        ax.scatter(X, Y, color=color)
        #for i, txt in enumerate(range(len(X))):
        #    ax.annotate(str(txt) + " " + str(image[X[i],Y[i]]), (X[i], Y[i]))


    # add labels and set equal aspect ratio
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_xlim(np.min(X_grid), np.max(X_grid))
    ax.set_ylim(np.min(Y_grid), np.max(Y_grid))
    ax.set_aspect(aspect='equal')
    plt.show()

def plot_best(axis, best_swarm, color):
    x = [p[0] for p in best_swarm]
    y = [p[1] for p in best_swarm]
    #axis.plot(np.array(y),np.array(x),'.', alpha = .5, color = color, mew = 0)

    #marker = np.random.choice(list(plt.markers))
    
    size = 10  (20 * np.random.rand())
    rgba = [np.random.random() for _ in range(4)]
    color1 = np.array([rgba])
    alpha = 1 / (size**0.5)
    plt.scatter(x,y, alpha=alpha, marker='D',
               color=color1, s = size)

    
    '''plt.scatter(x,y,
               s = (np.abs(x))/20,
               c = color1)'''

    
    '''size = 10  (20 * np.random.rand())
    alpha = 1 / (size**0.5)
    plt.scatter(x,y, s=size, alpha=alpha)'''
    

def plot_best_from_file(path, xlim, ylim):
    fig, ax = plt.subplots()
    plt.axis('off')
    plt.xlim(0,xlim)
    plt.ylim(ylim,0)
    swarms = np.array([])
    # colormap = cm.get_cmap("hsv")
    colormap =  ["c","y","m","darkslategrey"]
    i=0
    for file in path:
        swarms = np.load(file)
        for swarm in swarms:
            # color = np.random.rand(3,)
            color = colormap[i]
            plot_best(ax, swarm, color)
            i+=1
    plt.show()

if __name__ == "__main__":
    plot_best_from_file(["complete/colours.npy","complete/contours.npy"],256,256)




