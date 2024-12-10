import random as rnd
import numpy as np

class Agent:
    def __init__(self):
        self.sex = None
        self.isMarriage = None
        self.point = 0.0
        self.x = 0.0
        self.y = 0.0
        self.initial_x = 0.0
        self.initial_y = 0.0
        self.v_x = 0.0
        self.v_y = 0.0
        self.soc_spc_R = 0.0
        self.mar_dec_r = 0.0

    def get_opposite_sex(self, agents, radius):
        """get a list of unmarried opposite sex agents"""
        opposite_sex_list = [opposite for opposite in agents if (opposite.x-self.x)**2+(opposite.y-self.y)**2<=radius**2 and opposite.isMarriage == False and opposite.sex != self.sex]
        return opposite_sex_list

    def get_neighbor_marriage_rates(self, agents, radius):
        """get marriage rates in the neighborhood"""
        married_agents_list = [agent for agent in agents if (agent.x-self.x)**2+(agent.y-self.y)**2<=radius**2 and agent.isMarriage == True]
        all_agents_list = [agent for agent in agents if (agent.x-self.x)**2+(agent.y-self.y)**2<=radius**2]
        fm_R = len(married_agents_list)/len(all_agents_list) if len(all_agents_list) != 0 else 0
        return fm_R

    def update_xy(self, social_size, speed):
        """update agents' position"""
        if self.x + self.v_x < 0 or social_size < self.x + self.v_x:
            self.v_x *= -1
        if self.y + self.v_y < 0 or social_size < self.y + self.v_y:
            self.v_y *= -1
        self.x = self.x + self.v_x
        self.y = self.y + self.v_y
