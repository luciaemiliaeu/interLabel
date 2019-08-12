import sys
sys.path.append("../rotulador")

import rotuladorLopes as rotulador
import pandas as pd 
import numpy as np
from sklearn.cluster import KMeans
from sklearn import metrics
from sklearn.metrics import pairwise_distances
from sklearn.metrics import davies_bouldin_score
import matplotlib.pyplot as plt 

class LABELROTULATOR(object):
	def __init__ (self, base, num_cluster, discre_method, discre_bins, perc_trei_rot, V, folds_rot):
		#Agurpamento
		self.X = base.drop(['classe'],axis = 1).get_values()
		self.Y = KMeans(n_clusters=num_cluster, random_state=0).fit(self.X).labels_
		
		
		#Rotulação
		self.rotulos = rotulador.Rotulador(self.X, self.Y, discre_method, discre_bins, perc_trei_rot, V, folds_rot).rotulo
		#for i in self.rotulos: print(i)
		
		# Mudança dos elementos de cluster
		self.otherCluster, self.multLabel, self.wrongCluster, self.exclusive, self.error, silhouette, dbIndex = self.calMetrics(self.X, self.Y, self.rotulos)
		
		
		self.newLabels, self.newRightData = self.changeLabel(self.otherCluster, self.wrongCluster)
		newData = pd.DataFrame(self.multLabel+self.exclusive+self.error+self.newRightData)
		newcluster = newData.loc[:, newData.shape[1]-1].get_values()
		newX = newData.drop(newData.columns[[newData.shape[1]-1]], axis=1).get_values()

		#Repete a rotulação 
		newRotulos = rotulador.Rotulador(newX, newcluster, discre_method, discre_bins, perc_trei_rot, V, folds_rot).rotulo
		#for i in newRotulos: print(i)

		#Recalcula métricas
		a,b,c,d,e, silhouette_, dbIndex_= self.calMetrics(newX, newcluster, newRotulos)

		self.info = [len(self.wrongCluster),silhouette,dbIndex, len(c), silhouette_, dbIndex_]


	def plot(self, x, y, **kwds):
		data = pd.DataFrame(x)
		data.loc[:,'Cluster'] = pd.Series(y, index=data.index)
		pd.plotting.radviz(data, 'Cluster',**kwds)
		

	def calMetrics(self, X, Y, rotulos):
		#Separação dos dados (Matriz de confusão)

		rightLabel, wrongLabel, otherClusterData,  otherCluster, noOtherCluster = self.selectData(X,Y,rotulos)
		
		silhouette = metrics.silhouette_score(X, Y, metric='euclidean')
		dbIndex = davies_bouldin_score(X, Y)  

		multLabel = [x for x in otherClusterData if self.procurarElemento(x,rightLabel)]
		wrongCluster = [x for x in wrongLabel if self.procurarElemento(x,otherClusterData)]
		exclusive = [x for x in rightLabel  if self.procurarElemento(x,noOtherCluster)]
		error = [x for x in wrongLabel if self.procurarElemento(x,noOtherCluster)]

		'''print("tamanho da base: "+str(len(X)))
		print("Rotulados certos: "+str(len(rightLabel)))
		print("Nao obedecem ao rotulo: "+str(len(wrongLabel)))
		print("Obedecem a outros rotulos: "+str(len(otherClusterData)))
		print("Nao obedecem a outros rotulos: "+str(len(noOtherCluster)))
		
		print("Mais de um grupo: " +str(len(multLabel)))
		#for i in rotular.multLabel: print(i)
		
		print("Grupo errado: "+str(len(wrongCluster)))
		#for i in rotular.wrongCluster: print(i)

		print("Exclusivo: "+str(len(exclusive)))
		#for i in rotular.exclusive: print(i)

		print("Erro: "+str(len(error)))
		#for i in rotular.error: print(i)
		'''

		return otherCluster, multLabel, wrongCluster, exclusive, error, silhouette, dbIndex
	
	def selectData(self, X, Y, rotulos):
		data = pd.DataFrame(X)
		data.loc[:,'Cluster'] = pd.Series(Y, index=data.index)
		baseagrupada = data.get_values()
		
		
		rightLabel=[]
		wrongLabel=[]
		
		otherClusterData=[]
		otherCluster = []

		data = pd.DataFrame(X)
		data.loc[:,'Cluster'] = pd.Series(Y, index=data.index)
		grouped = data.groupby(['Cluster'])

		for n_cluster, values in grouped:
			for dado in values.get_values().tolist():
				for rotulo in rotulos:
					if self.check(dado, rotulo[1]):
						if rotulo[0] == n_cluster: 
							rightLabel.append(dado)
						else:
							otherClusterData.append(dado)
							otherCluster.append((dado,rotulo[0]))
					else:
						if rotulo[0] == n_cluster: wrongLabel.append(dado)

		notOtherCluster = [x for x in baseagrupada if not self.procurarElemento(x,otherClusterData)]
		
		return np.asarray(rightLabel), np.asarray(wrongLabel), np.asarray(otherClusterData), otherCluster, notOtherCluster
	
	def check(self, dado, rotulos):
		#print(dado, rotulos) 
		for rotulo in rotulos:
			if all([dado[rotulo[0]] >= rotulo[1], dado[rotulo[0]] <= rotulo[2]]): 
				pass
			else: 
				return False
		return True 
	
	def changeLabel(self, dados, grupoErrado):
		for x in dados:
			for y in grupoErrado:
				if self.comparaListas(x[0],y):
					x[0][-1]=x[1]
					y[-1]=x[1]
		return dados, grupoErrado
	
	#Procura uma lista (elemento) em uma lista de listas (lista)
	def procurarElemento(self, elemento, lista):
		for i in lista:
			if self.comparaListas(elemento, i): return True
		return False

	def comparaListas(self, list1, list2):
		for i in range(len(list1)):
			if list1[i]!=list2[i]: return False
		return True






