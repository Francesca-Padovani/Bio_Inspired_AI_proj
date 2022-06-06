import os
import numpy as np
import cv2
from torch import meshgrid
from pso import PSO

n_particles = 10**2

# Image processing
img = "fratty.jpg"
#img = "dog.jpg"
image = cv2.imread(img,0)
image = cv2.resize(image, dsize=(256,256), interpolation=cv2.INTER_CUBIC)
# Find edges
image = cv2.GaussianBlur(image, ksize=(5,5), sigmaX=2, sigmaY=2)
v = np.median(image)
image = cv2.Canny(image, v*.7, v*1.3)
# Find contours
contours, hierarchy = cv2.findContours(image,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
drawing = np.full((image.shape[0], image.shape[1],1), 255, dtype=np.uint8)
for i in range(len(contours)):
    cv2.drawContours(drawing, contours, i, 0, 10, cv2.LINE_AA, hierarchy, 0)
image = cv2.GaussianBlur(drawing, ksize=(9,9),sigmaX=9, sigmaY=9)
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


pso = PSO(swarm.copy(), v.copy(), fitness, w=.5, c1=1, c2=.5, c3=10, c4=9, max_g = 500,
auto_coefs=True, distancing = True, fit_weight=.5)
 
while pso.next():
    continue

np.save("complete/contours.npy", np.asarray(pso.best_swarm[None, ...]))
