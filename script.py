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


