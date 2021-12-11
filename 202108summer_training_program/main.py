from simulation import Simulation
from graph import Graph
import numpy as np
import random as rnd
import time


def run():
    population = 200         # num of agents
    social_size = population # size of society
    speed = population/50    # agent's walking step
    mar_dec_r = 1            # range of marriage decision
    num_episode = 100        # num of simulation
    tmax = 1000              # max time step of each simulation
    seed = 0                 # random seed
    rnd.seed(seed)
    np.random.seed(seed)
    simulation = Simulation(population, social_size, speed, mar_dec_r)
    for episode in range(num_episode):
    	simulation.run_one_episode(episode, social_size, speed, tmax, mar_dec_r, population)
    Graph().draw_graph(0)
    Graph().draw_graph(1)

if __name__ == '__main__':
    start = time.time()
    run()
    elapsed_time = time.time() - start
    print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")