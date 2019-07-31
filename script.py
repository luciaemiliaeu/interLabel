import interLabel as label 
import pandas as pd
import numpy as np 


chamadas = ["./databases/iris.csv",3,"EFD", [3,3,3,3], 10]
bd = pd.read_csv(chamadas[0],sep=',',parse_dates=True)
rotular = label.LABELROTULATOR(bd, chamadas[1], chamadas[2], chamadas[3], 60, chamadas[4], 10)

'''
"./databases/iris.csv","EFD", 4, [3,3,3,3], 10"
("./databases/vidros.csv","EWD",7, [4,4,4,4,4,4,4,4,4],15),
("./databases/sementes.csv","EFD",3, [3,3,3,3,3,3,3], 5)'''


print("tamanho da base: "+str(len(rotular.X)))
print("Rotulados certos: "+str(len(rotular.dados)))
print("Nao obedecem ao rotulo: "+str(len(rotular.notDados)))
print("Obedecem a outros rotulos: "+str(len(rotular.wrongData)))
print("Nao obedecem a outros rotulos: "+str(len(rotular.naoObedeceOutrosRotulos)))

print("Mais de um grupo: " +str(len(rotular.maisDeUmGrupo)))
for i in rotular.maisDeUmGrupo: print(i)

print("Grupo errado: "+str(len(rotular.grupoErrado)))
for i in rotular.grupoErrado: print(i)

print("Exclusivo: "+str(len(rotular.exclusivo)))
#for i in exclusivo: print(i)

print("Erro: "+str(len(rotular.erro)))
for i in rotular.erro: print(i)