import pandas as pd
import numpy as np
import pickle
from itertools import chain


pd.set_option("display.max_rows", None, "display.max_columns", None)

df = pd.read_csv('coordinates.csv', index_col='ID', skiprows=1, names=['ID', 'Label', 'X', 'Y', 'E'], dtype={"X" : "float64", "Y" : "float64", "E" : "float64"})
labels = ["AA", "BB", "CC", "DD", "EE", "FF", "GG", "HH", "II", "JJ"]

with open("alldata.pkl", 'rb') as handle:
    alldata = pickle.load(handle)


fdata = {}
for i in range(0, 10):
    for j in range(i, 10):
        avlist = []
        for k in range(0, len(alldata[(labels[i]+labels[j])])):
            if(len(alldata[(labels[i]+labels[j])][k]) == 0) : continue
            else : avlist.append(alldata[(labels[i]+labels[j])][k])
        av = 0
        normal = list(chain.from_iterable(avlist))
        normal = [x for x in normal if x <= 18.0]
        normal = np.array(normal)

        for k in range(0, len(avlist)):
            av += (sum([x for x in avlist[k] if x <= 18.0]) / len(normal))
        
        name = labels[i]+labels[j]
        df[name] = ""
        
        if len(avlist) == 0 :
            fdata[name] = [0.0, 0.0]
            df.loc[0, name] = ("Mean : 0")
            df.loc[1, name] = ("Deviation : 0")
        else :
            fdata[name] = [av, normal.std()]
            df.loc[0, name] = ("Mean : " + str(av))
            df.loc[1, name] = ("Deviation : " + str(normal.std()))

df.to_csv('resultcalc.csv') 

f = open("fdata.pkl","wb")
pickle.dump(fdata, f, protocol=pickle.HIGHEST_PROTOCOL)
f.close
