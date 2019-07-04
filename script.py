import interLabel as label 
import pandas as pd
import numpy as np 

chamadas = ["./databases/sementes.csv",3, [3,3,3,3,3,3,3], 5]
bd = pd.read_csv(chamadas[0],sep=',',parse_dates=True)
rotular = label.LABELROTULATOR(bd, chamadas[1], "EFD", chamadas[2], 60, chamadas[3], 1)


'''("./databases/vidros.csv",7, [4,4,4,4,4,4,4,4,4],15),
("./databases/sementes.csv",3, [3,3,3,3,3,3,3], 5)'''


print("Mais de um cluster:")
for i in rotular.rongcluster: print(i[0], i[1])

print("\nNão pertence ao rótulo:")
print(rotular.notDados)

print("\nPertence a outro grupo:")
lista_final = [x for x in rotular.notDados if x in rotular.rongData]
print(np.asarray(lista_final))