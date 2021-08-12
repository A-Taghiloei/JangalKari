import matplotlib.pyplot as plt 
import pandas as pd
import numpy as np
import math
import pickle

pd.set_option("display.max_rows", None, "display.max_columns", None)

df = pd.read_csv('coordinates.csv', index_col='ID', skiprows=1, names=['ID', 'Label', 'X', 'Y', 'E'], dtype={"X" : "float64", "Y" : "float64", "E" : "float64"})
labels = ["AA", "BB", "CC", "DD", "EE", "FF", "GG", "HH", "II", "JJ"]
alldata = {}
for i in range(0,10):     
    for j in range(i, 10):
        alldata[(labels[i]+labels[j])] = []
        if(i==j):continue
        alldata[(labels[i]+labels[j]+"n")] = []

def distance(X1,Y1,E1,X2,Y2,E2):
    planard = math.sqrt((X2 - X1)**2 + (Y2 - Y1)**2)
    D = math.sqrt((0.9996*planard)**2 + (E2 - E1)**2) * (((E2+E1)/2 + 6371000)/ 6371000)
    return D

def algo(df1, df2):
    lbldist = []
    for i, rowi in df1.iterrows():
        for j, rowj in df2.iterrows():
            if i==j : continue
            d = distance(rowi["X"], rowi["Y"], rowi["E"], rowj["X"], rowj["Y"], rowj["E"])
            lbldist.append(d)
    if(len(lbldist)!=0):print("" , end =".")
    return list(set(lbldist))

X = np.array(df['X'].tolist())
xmin = X.min()
#xymin = df.loc[df.X == xmin, 'Y'].tolist()[0]
xmax = X.max()
Y = np.array(df['Y'].tolist())
ymin = Y.min()
ymax = Y.max()

xstep = 10
ystep = 10

ynow = [ymin, ymin + ystep]
while(ynow[0] <= ymax + ystep):
    xnow = [xmin , xmin + xstep]
    while(xnow[0] <= xmax + xstep):
        for i in range(0, 10):
            for j in range(i, 10):
                df1 = df.loc[(df['Label'].str.contains(labels[i])) & (df['X'] >= xnow[0]) & (df['X'] < xnow[1]) & (df['Y'] >= ynow[0]) & (df['Y'] < ynow[1])]
                df2 = df.loc[(df['Label'].str.contains(labels[j])) & (df['X'] >= xnow[0]) & (df['X'] < xnow[1]) & (df['Y'] >= ynow[0]) & (df['Y'] < ynow[1])]
                alldata[(labels[i]+labels[j])].append(algo(df1, df2))
                if(i==j):continue
                alldata[(labels[i]+labels[j]+"n")].append([len(df1), len(df2)])
        xnow[0] = xnow[1]
        xnow[1] += xstep
    ynow[0] = ynow[1]
    ynow[1] += ystep

f = open("alldata.pkl","wb")
pickle.dump(alldata, f, protocol=pickle.HIGHEST_PROTOCOL)
f.close