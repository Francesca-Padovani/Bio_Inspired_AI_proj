import numpy as np

class PSO:
    def __init__(self, 
                swarm, 
                v, 
                fitness, 
                w=.8, 
                c1=2, 
                c2=2, 
                c3=1, 
                c4=1, 
                max_g=200, 
                auto_coefs = False, 
                distancing = False, 
                fit_weight = .5):
        self.swarm = swarm
        self.v = v
        self.fitness = fitness
        self.N = len(self.swarm)
        self.auto_coefs = auto_coefs
        self.w = w
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3
        self.c4 = c4
        self.max_g = max_g
        self.distancing = distancing
        self.fit_weight = fit_weight

        self.p_best = self.swarm
        self.p_best_val = self.fitness(self.swarm)

        self.best_fit = np.sum(self.fitness(self.swarm))
        self.coverage = 0
        self.best_coverage = 0
        self.best_swarm = self.swarm

        self.iter = 0
        self.iter_no_improvement = 0
        self.is_running = True
        if self.auto_coefs:
            self.w_max = w
            self.c1_max = c1
            self.c2_max = c2
            self.c3_max = c3
            self.c4_max = c4
        self.l_bests = self.swarm
        self.l_bests_val = self.fitness(self.swarm)
        

    def __str__(self):
        return f'[{self.iter}] $w$:{self.w:.2f} - $c1$:{self.c1:.2f} - $c2$:{self.c2:.2f} - $c3$:{self.c3:.2f} - $c4$:{self.c4:.2f}'

    def next(self):
        if self.iter > 0:
            if self.auto_coefs:
                self.update_coefs()
            self.move_particles()
            self.update_best()
        self.iter += 1
        self.is_running = self.is_running and self.iter < self.max_g
        return self.is_running

    def update_coefs(self):
        t = self.iter / self.max_g
        # inertia
        self.w =  self.w_max - self.w_max * t
        # cognitive and social components
        self.c1 = self.c1_max - self.c1_max * t
        self.c2 = self.c2_max - self.c2_max * t
        if self.distancing:
            self.c3 = self.c3_max * t
            self.c4 = self.c4_max * t

    
    def move_particles(self):
        # inertia
        new_v = self.v * self.w
        # cognitive component
        U1 = np.random.random(self.N)
        U1 = np.tile(U1[:,None], (1,2))
        new_v += self.c1 * U1 * (self.p_best - self.swarm)
        # social component
        U2 = np.random.random(self.N)
        U2 = np.tile(U2[:,None], (1,2))
        new_v += self.c2 * U2 * (self.l_bests - self.swarm)
        # repulsion from the swarm centroid
        if self.distancing:
            U3 = np.random.random(self.N)
            U3 = np.tile(U3[:,None], (1,2))
            for i,particle in enumerate(self.swarm):
                partial_swarm = np.delete(self.swarm,i,axis = 0)
                centroid = np.mean(partial_swarm, axis=0)
                distance = np.floor(particle-centroid)
                if distance[0] == 0:
                    distance[0] = 1
                if distance[1] == 0:
                    distance[1] = 1
                repulsion = 10 / distance
                new_v[i] += self.c3 * U3[i] * repulsion
        # repulsion from the nearest particle
            U4 = np.random.random(self.N)
            U4 = np.tile(U4[:,None], (1,2))
            self.coverage = 0
            for i,particle in enumerate(self.swarm):
                partial_swarm = np.delete(self.swarm,i,axis = 0)
                nearest = self.find_nearest(partial_swarm, particle)
                distance = np.floor(particle-nearest)
                self.coverage += np.sum(distance)**2
                if distance[0] == 0:
                    distance[0] = 1
                if distance[1] == 0:
                    distance[1] = 1
                repulsion = 10 / distance 
                new_v[i] += self.c4 * U4[i] * repulsion

        self.is_running = np.sum(self.v - new_v) != 0

        #update positions and velocities
        self.v = new_v
        self.swarm = self.swarm + new_v
    
    def update_best(self):
        fits = self.fitness(self.swarm)
        n = len(self.swarm)
        for i in range(n):
            # update personal best
            if fits[i] < self.p_best_val[i]:
                self.p_best_val[i] = fits[i]
                self.p_best[i] = self.swarm[i]
            # update social bests
            if i == 0:
                neighbors = [fits[n-1],fits[i],fits[i+1]]
                neighbors_pos = [self.swarm[n-1], self.swarm[i], self.swarm[i+1]]
            elif i == n-1:
                neighbors = [fits[i-1],fits[i],fits[0]]
                neighbors_pos = [self.swarm[i-1], self.swarm[i], self.swarm[0]]
            else:
                neighbors = [fits[i-1],fits[i],fits[i+1]]
                neighbors_pos = [self.swarm[i-1], self.swarm[i], self.swarm[i+1]] 
            self.l_bests_val[i] = np.min(neighbors)
            self.l_bests[i] = neighbors_pos[np.argmin(neighbors)]
        
        # update best swarm
        #print(np.sum(fits) - self.coverage, self.best_fit + self.coverage)

        if (np.sum(fits) * self.fit_weight - self.coverage * (1-self.fit_weight)) < (self.best_fit * self.fit_weight - self.coverage * (1-self.fit_weight)):
            self.iter_no_improvement = 0
            self.best_fit = np.sum(fits)
            self.best_coverage = self.coverage
            self.best_swarm = self.swarm
        else:
            self.iter_no_improvement += 1
            if self.iter_no_improvement == 100:
                self.iter = self.max_g


    def find_nearest(self, array, value):
        array = np.asarray(array)
        i = np.sum((np.abs(array - value)), axis=1).argmin(axis=0)
        return array[i]