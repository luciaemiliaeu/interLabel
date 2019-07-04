import sys
sys.path.append("../rotulador")

import rotuladorLopes as rotulador
import pandas as pd 
import numpy as np
from sklearn.cluster import KMeans

class LABELROTULATOR(object):
	def __init__ (self, base, num_cluster, discre_method, discre_bins, perc_trei_rot, V, folds_rot):
		#Agurpamento
		self.X = base.drop(['classe'],axis = 1).get_values()
		self.Y = KMeans(n_clusters=num_cluster, random_state=0).fit(self.X).labels_
		
		# Rotulaçaõ do conjunto de treino e seleção dos elementos pertencentes ao rótulo 
		# dados -> componente x dos elementos pertencentes ao rótulo
		# cluster -> componente y dos elementos pertencentes ao rótulo
		# notDados -> elementos não pertencentes ao rótulo
		# rognData -> elementos que um cluster que não obedecem ao rótulo deste
		# rongCluster -> tuplas de elementos e clusters para os quais o elemento obedece ao rótulo
		self.rotulos = rotulador.Rotulador(self.X, self.Y, discre_method, discre_bins, perc_trei_rot, V, folds_rot).rotulo
		self.dados, self.cluster, self.notDados, self.rongData, self.rongcluster = self.selectData()

	def selectData(self):
		newData=[]
		notData=[]
		rongData=[]
		rongcluster = []

		data = pd.DataFrame(self.X)
		data.loc[:,'Cluster'] = pd.Series(self.Y, index=data.index)
		grouped = data.groupby(['Cluster'])

		for n_cluster, values in grouped:
			for i in values.get_values().tolist():
				for j in self.rotulos:
					if n_cluster == j[0]:
						if self.check(i, j[1]):
							newData.append(i)
						else: notData.append(i)
					else:
						if self.check(i, j[1]):
							rongData.append(i)
							rongcluster.append((i,j[0]))	

		cluster = [i[-1] for i in newData]
		return np.asarray(newData), np.asarray(cluster), np.asarray(notData), np.asarray(rongData), rongcluster
	
	def check(self, dado, rotulos): 	 	
		for j in rotulos:
			for i in range(len(dado)):
				if all([i == j[0], dado[i] >= j[1], dado[i] <= j[2]]):
					return True
		return False



