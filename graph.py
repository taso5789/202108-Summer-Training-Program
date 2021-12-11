from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class Graph:
    def detect_position(self, agents):
        """detect each agent's position"""
        # married males
        xlistMM, ylistMM = [], []
        # married females
        xlistMF, ylistMF = [], []
        # unmarried males
        xlistNM, ylistNM = [], []
        # unmarried females
        xlistNF, ylistNF = [], []
        # plot agents' current positions
        for focal in agents:
        	if focal.sex == "Male" and focal.isMarriage:
        		xlistMM.append(focal.x)
        		ylistMM.append(focal.y)
        	elif focal.sex == "Female" and focal.isMarriage:
        		xlistMF.append(focal.x)
        		ylistMF.append(focal.y)
        	elif focal.sex == "Male" and not focal.isMarriage:
        		xlistNM.append(focal.x)
        		ylistNM.append(focal.y)
        	elif focal.sex == "Female" and not focal.isMarriage:
        		xlistNF.append(focal.x)
        		ylistNF.append(focal.y)
        return xlistMM, ylistMM, xlistMF, ylistMF, xlistNM, ylistNM, xlistNF, ylistNF

    def scatter_plot(self, image, n, xlistMM, ylistMM, xlistMF, ylistMF, xlistNM, ylistNM, xlistNF, ylistNF, ax):
    	"""plot scatter plot"""
    	image += ax[n].plot(xlistMM, ylistMM, ".", markersize=12, label="married_male", color="b")
    	image += ax[n].plot(xlistMF, ylistMF, ".", markersize=12, label="married_female", color="r")
    	image += ax[n].plot(xlistNM, ylistNM, ".", markersize=12, label="unmarried_male", color="c")
    	image += ax[n].plot(xlistNF, ylistNF, ".", markersize=12, label="unmarried_female", color="m")
    	return image

    def draw_graph(self, pattern):
    	""" output path """
    	if pattern == 0:
    		p = Path('/Users/USERNAME/riron/empirical_macro_economics/graph/without_norm')
    		title = 'The social living range "R" vs the marriage rates without norm'
    	elif pattern == 1:
    		p = Path('/Users/USERNAME/riron/empirical_macro_economics/graph/with_norm')
    		title = 'The social living range "R" vs the marriage rates with norm'
    	else:
    		print('Something is wrong in draw_graph method in graph.py.')
    	q = Path('/'.join([str(p), 'episodes']))
    	file_name = '*.csv'
    	csv_files = q.glob(file_name) 
    	column_name = ('episode', 'Dr', 'Fm')
    	episode = 0
    	for file in csv_files:
    		df_temp = pd.read_csv(file, names=column_name)
    		df_temp.episode = df_temp.episode.replace(0, episode)
    		df_temp = df_temp[1:len(df_temp)]
    		df = df_temp if episode == 0 else df.append(df_temp)
    		episode += 1
    	df['episode'] = df['episode'].astype(int)
    	df['Dr'] = df['Dr'].astype(float)
    	df['Fm'] = df['Fm'].astype(float)
    	plt.rcParams["figure.figsize"] = [16,12]
    	plt.rcParams["font.size"] = 18
    	df.plot(kind='scatter', x='Dr', y='Fm', label="the observed marriage rates")
    	plt.xticks(2.0*np.arange(1.0, 11.0, 1.0))
    	plt.title(title)
    	# calculate average on each value of Dr
    	df_avg = []
    	for Dr in 2.0*np.arange(1.0, 11.0, 1.0):
    		df_avg_temp = [Dr, df[df['Dr']==float(Dr)].mean()['Fm']]
    		df_avg_columns = ['Dr', 'Fm']
    		df_avg = pd.DataFrame(df_avg_temp, df_avg_columns).T if float(Dr)==2.0 else df_avg.append(pd.DataFrame(df_avg_temp, df_avg_columns).T)
    	plt.plot(df_avg['Dr'], df_avg['Fm'], color = 'red', marker = 'v', label="the average marriage rates")
    	plt.xlabel("R")
    	plt.ylabel("Marriage Rate(%)")
    	plt.legend()
    	if pattern == 0:
    		plt.savefig('/'.join([str(p), 'graph_without_norm.png']))
    	elif pattern == 1:
    		plt.savefig('/'.join([str(p), 'graph_with_norm.png']))
    	else:
    		print('Something is wrong in draw_graph method in graph.py.')
    	plt.show()