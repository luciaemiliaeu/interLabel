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
		
		data = pd.DataFrame(self.X)
		data.loc[:,'Cluster'] = pd.Series(self.Y, index=data.index)
		self.baseagrupada = data.get_values()
		
		# Rotulaçaõ do conjunto de treino e seleção dos elementos pertencentes ao rótulo 
		# dados -> componente x dos elementos pertencentes ao rótulo
		# cluster -> componente y dos elementos pertencentes ao rótulo
		# notDados -> elementos não pertencentes ao rótulo
		# rognData -> elementos que um cluster que não obedecem ao rótulo deste
		# rongCluster -> tuplas de elementos e clusters para os quais o elemento obedece ao rótulo
		
		self.rotulos = rotulador.Rotulador(self.X, self.Y, discre_method, discre_bins, perc_trei_rot, V, folds_rot).rotulo
		for i in self.rotulos: print(i)
		self.dados, self.notDados, self.wrongData,  self.rongcluster, self.cluster = self.selectData()

	def selectData(self):
		rightData=[]
		notData=[]
		wrongData=[]
		wrongcluster = []

		data = pd.DataFrame(self.X)
		data.loc[:,'Cluster'] = pd.Series(self.Y, index=data.index)
		grouped = data.groupby(['Cluster'])

		for n_cluster, values in grouped:
			for dado in values.get_values().tolist():
				for rotulo in self.rotulos:
					if self.check(dado, rotulo[1]):
						if rotulo[0] == n_cluster: 
							rightData.append(dado)
						else:
							wrongData.append(dado)
							wrongcluster.append((dado,rotulo[0]))
					else:
						if rotulo[0] == n_cluster: notData.append(dado)
		
		cluster = [i[-1] for i in rightData]
		return np.asarray(rightData), np.asarray(notData), np.asarray(wrongData), wrongcluster, np.asarray(cluster)
	
	def check(self, dado, rotulos):
		#print(dado, rotulos) 
		for rotulo in rotulos:
			if all([dado[rotulo[0]] >= rotulo[1], dado[rotulo[0]] <= rotulo[2]]): 
				pass
			else: 
				return False
		return True 
	
	#def change



