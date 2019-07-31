import interLabel as label 
import pandas as pd
import numpy as np 

def comparaListas(list1, list2):
	for i in range(len(list1)):
		if list1[i]!=list2[i]: return False
	return True

def procurarElemento(elemento, lista):
	for i in lista:
		if comparaListas(elemento, i): return True
	return False

chamadas = ["./databases/iris.csv",3,"EFD", [3,3,3,3], 10]
bd = pd.read_csv(chamadas[0],sep=',',parse_dates=True)
rotular = label.LABELROTULATOR(bd, chamadas[1], chamadas[2], chamadas[3], 60, chamadas[4], 10)

'''
"./databases/iris.csv","EFD", 4, [3,3,3,3], 10"
("./databases/vidros.csv","EWD",7, [4,4,4,4,4,4,4,4,4],15),
("./databases/sementes.csv","EFD",3, [3,3,3,3,3,3,3], 5)'''
naoObedeceOutrosRotulos = [x for x in rotular.baseagrupada if not procurarElemento(x,rotular.rongData)]

print("tamanho da base: "+str(len(rotular.X)))
print("Rotulados certos: "+str(len(rotular.dados)))
print("Nao obedecem ao rotulo: "+str(len(rotular.notDados)))
print("Obedecem a outros rotulos: "+str(len(rotular.rongData)))
print("Nao obedecem a outros rotulos: "+str(len(naoObedeceOutrosRotulos)))

maisDeUmGrupo = [x for x in rotular.rongData for y in rotular.dados if comparaListas(x,y)]
print("Mais de um grupo: " +str(len(maisDeUmGrupo)))
#for i in maisDeUmGrupo: print(i)

grupoErrado = [x for x in rotular.notDados for y in rotular.rongData if comparaListas(x,y)]
print("Grupo errado: "+str(len(grupoErrado)))
for i in grupoErrado: print(i)

exclusivo = [x for x in rotular.dados for y in naoObedeceOutrosRotulos if comparaListas(x,y)]
print("Exclusivo: "+str(len(exclusivo)))
#for i in exclusivo: print(i)

erro = [x for x in rotular.notDados for y in naoObedeceOutrosRotulos if comparaListas(x,y)]
print("Erro: "+str(len(erro)))
#for i in erro: print(i)