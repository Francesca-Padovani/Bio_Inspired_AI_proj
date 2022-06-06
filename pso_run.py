import os
import numpy as np
import matplotlib.pyplot as plt
import cv2
from torch import meshgrid

from pso import PSO
from utils import plot_pso, make_gif_from_folder

n_particles = 7**2

# Image processing
#img = "dog.jpg"
#img = "dot.png"
#img = "line.png"
#img = "dog1.jpg"
img = "fratty.jpg"
image = cv2.imread(img,0)
image = cv2.resize(image, dsize=(256,256), interpolation=cv2.INTER_CUBIC)
image = cv2.GaussianBlur(image, ksize=(9,9), sigmaX=5, sigmaY=5)
image = cv2.flip(image,0)
X = np.arange(image.shape[0])
Y = np.arange(image.shape[1])
meshgrid = np.meshgrid(X,Y)


def fitness(pos):
    x,y = pos[:,0], pos[:,1]
    x = [round(i) for i in x]
    y = [round(j) for j in y]
    fit = []
    for i in range(n_particles):
        if x[i] >= image.shape[0] or y[i] >= image.shape[1] or x[i] < 0  or y[i] < 0:
            fit.append(max((x[i]+image.shape[0])**2, (y[i]+image.shape[1])**2))
        else:
            fit.append(image[x[i],y[i]]**2)
    return fit


# Create swarm
offset = 0.5
X_coords, Y_coords = np.meshgrid(
                        np.arange(start=offset, stop=np.sqrt(n_particles)+offset),
                        np.arange(start=offset, stop=np.sqrt(n_particles)+offset)
                    )

swarm = np.vstack([X_coords.ravel(), Y_coords.ravel()]).swapaxes(0, 1)
swarm *= (image.shape[0] // np.sqrt(n_particles)-offset)
v = (np.random.random((n_particles, 2))- .5) / 10

pso = PSO(swarm.copy(), v.copy(), fitness, w=.5, c1=1.5, c2=.5, c3=3, c4=3, max_g = 50,
auto_coefs=True, distancing = True, fit_weight=.5)
# Good parameters
# The algorithm converges when the parameters are set to the theoretical values for convergence, e.g. w=.8, c1=c2=1.1

root = 'src/'
filename = '_tmp.gif'
save = True

if save:
    tmp_dir = os.path.join(root, '_tmp')
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)

while pso.next():
    fig = plt.figure()
    save_path = None if not save else os.path.join(tmp_dir, f'{pso.iter:05d}.png')

    ax = fig.add_subplot(1, 1, 1)
    plot_pso(meshgrid, image, pso.swarm, pso.v, ax=ax)
    ax.set_title(str(pso))
        
    if save_path is None:
        plt.show()
    else:
        plt.savefig(save_path)
    plt.close()

if save:
    make_gif_from_folder(tmp_dir, os.path.join(root, filename))
    # Save best swarm
    with open("src/swarm.txt", "w") as f:
        for particle in pso.best_swarm:
            str_line = str(particle)
            f.write(str_line + "\n")

    x = [p[0] for p in pso.best_swarm]
    y = [p[1] for p in pso.best_swarm]
    
    plt.plot(np.array(y),np.array(x),'o', color = "green")
    plt.xlim(0,image.shape[0])
    plt.ylim(0,image.shape[1])
#plt.show()