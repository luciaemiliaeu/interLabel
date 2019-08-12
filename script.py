import interLabel as label 
import pandas as pd
import numpy as np 


chamadas = [("./databases/iris.csv",3,"EFD", [3,3,3,3], 10), 
("./databases/vidros.csv",7,"EWD", [4,4,4,4,4,4,4,4,4],15), 
("./databases/sementes.csv",3,"EFD", [3,3,3,3,3,3,3], 5)]
for i in chamadas:
	bd = pd.read_csv(i[0],sep=',',parse_dates=True)
	results = pd.DataFrame(columns=['#WrongCluster','Silhouette', 'DaviesBouldin', 	'#WrongCluster_','Silhouette_', 'DaviesBouldin_'])
	for j in range(10):
		rotular = label.LABELROTULATOR(bd, i[1], i[2], i[3], 60, i[4], 10).info
		results.loc[results.index.size,:] = rotular
		results.to_csv('./results/Resultado-'+str(i[0].split('.')[1].split('/')[2])+'.csv', sep='\t' )

for a in range(20):
	print("\a")
'''
"./databases/iris.csv","EFD", 4, [3,3,3,3], 10"
("./databases/vidros.csv","EWD",7, [4,4,4,4,4,4,4,4,4],15),
("./databases/sementes.csv","EFD",3, [3,3,3,3,3,3,3], 5)'''


