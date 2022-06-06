import os
import numpy as np
import matplotlib.pyplot as plt
import cv2
from torch import meshgrid
from pso import PSO

n_particles = 10**2
n_swarms = 3
best_swarms = []

# Image processing
# img = "dog.jpg"
img = "fratty.jpg"
img = cv2.imread(img,1)
img = cv2.resize(img, dsize=(256,256), interpolation=cv2.INTER_CUBIC)
img = cv2.GaussianBlur(img, ksize=(9,9), sigmaX=5, sigmaY=5)
X = np.arange(img.shape[0])
Y = np.arange(img.shape[1])
meshgrid = np.meshgrid(X,Y)
fig, ax = plt.subplots()
plt.xlim(0,img.shape[0])
plt.ylim(0,img.shape[1])

for i in np.arange(n_swarms):
    image = img[:,:,i]
    

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

    pso = PSO(swarm.copy(), v.copy(), fitness, w=.5, c1=1, c2=.5, c3=4, c4=4, auto_coefs=True, distancing = True, fit_weight=.4)
    
    while pso.next():
        continue

    # Save best swarm
    best_swarms.append(np.array(pso.best_swarm))
    colors = ["red","green","blue"]

np.save("complete/colours.npy", np.asarray(best_swarms))