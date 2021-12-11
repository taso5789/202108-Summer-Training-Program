from agent import Agent
from graph import Graph
from matplotlib import animation, rc, gridspec
from IPython.display import HTML
from scipy.stats import norm 
import copy
import math
import numpy as np
import pandas as pd
import random as rnd
import matplotlib.pyplot as plt


class Simulation:
    def __init__(self, population, social_size, speed, mar_dec_r):
        self.agents = self.__generate_agents(population, social_size, speed, mar_dec_r)

    def __generate_agents(self, population, social_size, speed, mar_dec_r):
        agentsA = [Agent() for id in range(population)]
        for index, focal in enumerate(agentsA):
            focal.sex = "Male" if index % 2 == 0 else "Female"
            focal.isMarriage = False
            focal.point = np.random.normal(0,1)
            radian = math.radians(rnd.randint(1,360))
            focal.x = rnd.randint(1,social_size)
            focal.y = rnd.randint(1,social_size)
            focal.initial_x = focal.x
            focal.initial_y = focal.y
            focal.v_x = math.cos(radian)*speed
            focal.v_y = math.sin(radian)*speed
            focal.soc_spc_R = 0.0
            focal.mar_dec_r = mar_dec_r
        agentsB = copy.deepcopy(agentsA)
        return agentsA, agentsB        

    def __initialize_agents(self):
        
        for focal_list in self.agents:
            for focal in focal_list:
                focal.isMarriage = False
                focal.x = focal.initial_x
                focal.y = focal.initial_y
    
    def __search_fiancee(self, social_size, speed, pattern):
        """make agents try to marry"""
        agents_list = rnd.sample(self.agents[pattern], len(self.agents[pattern]))
        for focal in agents_list:
            # update agents' position
            focal.update_xy(social_size, speed)
            # make married agents do nothing anymore
            if focal.isMarriage==True: continue
            # make list of unmarried agents in the neighborhood
            fiancee_list = focal.get_opposite_sex(self.agents[pattern], focal.mar_dec_r)
            # finish if there are no unmarried agents in the neighborhood
            if len(fiancee_list)<=0: continue
            # consider to marry in order if there are unmarried agents in the neighborhood 
            fiancee_list = sorted(fiancee_list, key=lambda x: x.point, reverse=True)
            for fiancee in fiancee_list:
                isMarriage = False
                couple = [focal, fiancee]
                male = [i for i in couple if i.sex=="Male"]
                female = [i for i in couple if i.sex=="Female"]
                cnd1 = False
                if male[0].point>=female[0].point: cnd1 = True
                cnd2 = False
                cnd2_1 = False
                cnd2_2 = False
                for i in couple:
                    target_sex_point = [j.point for j in couple if j!=i][0]
                    other_sex_list = i.get_opposite_sex(self.agents[pattern], i.soc_spc_R)
                    best_other_sex_point = max(other_sex.point for other_sex in other_sex_list) if len(other_sex_list) > 0 else 0
                    if pattern == 1: best_other_sex_point = norm.ppf((1-i.get_neighbor_marriage_rates(self.agents[pattern], i.soc_spc_R))*norm.cdf(best_other_sex_point))
                    if i == focal and target_sex_point >= best_other_sex_point: cnd2_1 = True
                    if i == fiancee and target_sex_point >= best_other_sex_point: cnd2_2 = True
                if cnd2_1 and cnd2_2: cnd2 = True
                if cnd1 and cnd2: isMarriage = True
                if isMarriage:
                    focal.isMarriage = True
                    fiancee.isMarriage = True
                    break

    def __count_fm(self):
        """calculate marriage rate"""
        fmA = len([focal for focal in self.agents[0] if focal.isMarriage == True])/len(self.agents[0])*100
        fmB = len([focal for focal in self.agents[1] if focal.isMarriage == True])/len(self.agents[1])*100
        return fmA, fmB

    def __play_game(self, episode, Dr, social_size, speed, tmax, population, ani_dir_num):
        """do simulation"""
        # initialization
        self.__initialize_agents()
        initial_fm = self.__count_fm()
        fm_histA = [initial_fm[0]]
        fm_histB = [initial_fm[1]]
        print(f"Episode:{episode}, Dr:{Dr:.1f}, Time: 0, FmA:{initial_fm[0]:.3f}, FmB:{initial_fm[1]:.3f}")
        # set paramaters below
        for focal in self.agents[0]:
            focal.soc_spc_R = Dr
        for focal in self.agents[1]:
            focal.soc_spc_R = Dr
        # output animation only when episode==0
        if episode==0:
            T = []
            statasMM_sum_left= []
            statasMF_sum_left= []
            statasNM_sum_left= []
            statasNF_sum_left= []
            statasMM_sum_right= []
            statasMF_sum_right= []
            statasNM_sum_right= []
            statasNF_sum_right= []
            fig = plt.figure(figsize=(8.5,5))
            gs = gridspec.GridSpec(2, 2, height_ratios=(3, 1))
            ax = [plt.subplot(gs[0, 0]), plt.subplot(gs[0, 1]), plt.subplot(gs[1, 0]), plt.subplot(gs[1, 1])]
            plt.close()
            ims = []
            legend_flag = True
        for t in range(tmax):
            if t==0: continue
            if episode==0:
                T.append(t)
                im = []
                # without norm
                xlistMM, ylistMM, xlistMF, ylistMF, xlistNM, ylistNM, xlistNF, ylistNF = Graph().detect_position(self.agents[0])
                # subplot0：scatter plot
                im += Graph().scatter_plot(im, 0, xlistMM, ylistMM, xlistMF, ylistMF, xlistNM, ylistNM, xlistNF, ylistNF, ax)
                # subplot2：transition chart
                statasMM_sum_left.append(len(xlistMM))
                statasMF_sum_left.append(len(xlistMF))
                statasNM_sum_left.append(len(xlistNM))
                statasNF_sum_left.append(len(xlistNF))
                im += ax[2].stackplot(T, statasMM_sum_left, statasMF_sum_left, statasNM_sum_left, statasNF_sum_left, colors=["b", "r", "c", "m"], alpha=0.7)
                # with norm
                xlistMM, ylistMM, xlistMF, ylistMF, xlistNM, ylistNM, xlistNF, ylistNF = Graph().detect_position(self.agents[1])
                # subplot1：scatter plot
                im += Graph().scatter_plot(im, 1, xlistMM, ylistMM, xlistMF, ylistMF, xlistNM, ylistNM, xlistNF, ylistNF, ax)
                # subplot3：transition chart
                statasMM_sum_right.append(len(xlistMM))
                statasMF_sum_right.append(len(xlistMF))
                statasNM_sum_right.append(len(xlistNM))
                statasNF_sum_right.append(len(xlistNF))
                im += ax[3].stackplot(T, statasMM_sum_right, statasMF_sum_right, statasNM_sum_right, statasNF_sum_right, colors=["b", "r", "c", "m"], alpha=0.7)
                # set environments of figures
                if legend_flag:  # draw a legend only once
                    # subplot0：scatter plot
                    ax[0].legend(loc='lower center', bbox_to_anchor=(1.1, 1.1), ncol=4)
                    ax[0].set_xlim(0, social_size)
                    ax[0].set_ylim(0, social_size)
                    ax[0].tick_params(labelbottom=False,labelleft=False,labelright=False,labeltop=False, length=0)
                    ax[0].tick_params(length=0)
                    ax[0].set_title("No Norm")
                    # subplot2：transition chart
                    ax[2].tick_params(labelbottom=False,labelleft=True,labelright=False,labeltop=False)
                    ax[2].axhline(population/2, ls = "--", color = "black")
                    # subplot1：scatter plot
                    ax[1].set_xlim(0, social_size)
                    ax[1].set_ylim(0, social_size)
                    ax[1].tick_params(labelbottom=False,labelleft=False,labelright=False,labeltop=False, length=0)
                    ax[1].tick_params(length=0)
                    ax[1].set_title("With Norm")
                    # subplot3：transition chart
                    ax[3].tick_params(labelbottom=False,labelleft=True,labelright=False,labeltop=False)
                    ax[3].axhline(population/2, ls = "--", color = "black")
                    legend_flag = False
                ims.append(im)  
            self.__search_fiancee(social_size, speed, 0)
            self.__search_fiancee(social_size, speed, 1)
            fm = self.__count_fm()
            fm_histA.append(fm[0])
            fm_histB.append(fm[1])
            if t == tmax-1:
                fm_convergedA = np.mean(fm_histA[t-99:t])
                fm_convergedB = np.mean(fm_histB[t-99:t])
        print(f"Episode:{episode}, Dr:{Dr:.1f}, Time:{t}, FmA:{fm_convergedA:.3f}, FmB:{fm_convergedB:.3f}")
        if episode==0:
            ani = animation.ArtistAnimation(fig, ims, interval=70)
            rc('animation', html='jshtml')
            ani.save(f"riron/empirical_macro_economics/animation/Dr_{ani_dir_num}/episode_{episode}.gif")
        return fm_convergedA, fm_convergedB

    def run_one_episode(self, episode, social_size, speed, tmax, mar_dec_r, population):
        """output resutls to csv files while moving parameters"""
        resultA = pd.DataFrame({'Dr': [], 'FmA': []})
        resultB = pd.DataFrame({'Dr': [], 'FmB': []})
        ani_dir_num = 1
        for Dr in 2.0*mar_dec_r*np.arange(1.0, 11.0, 1.0):
            fm_converged = self.__play_game(episode, Dr, social_size, speed, tmax, population, ani_dir_num)
            new_resultA = pd.DataFrame([[format(Dr, '.1f'), fm_converged[0]]], columns = ['Dr', 'FmA'])
            new_resultB = pd.DataFrame([[format(Dr, '.1f'), fm_converged[1]]], columns = ['Dr', 'FmB'])
            resultA = resultA.append(new_resultA)
            resultB = resultB.append(new_resultB)
            resultA.to_csv(f"riron/empirical_macro_economics/graph/without_norm/episodes/episode{episode}.csv")
            resultB.to_csv(f"riron/empirical_macro_economics/graph/with_norm/episodes/episode{episode}.csv")
            ani_dir_num += 1