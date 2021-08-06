import matplotlib.pyplot as plt 
import pandas as pd
import numpy as np
import math

pd.set_option("display.max_rows", None, "display.max_columns", None)

df = pd.read_csv('coordinates.csv', index_col='ID', skiprows=1, names=['ID', 'Label', 'X', 'Y', 'E'], dtype={"X" : "float64", "Y" : "float64", "E" : "float64"})
labels = ["AA", "BB", "CC", "DD", "EE", "FF", "GG", "HH", "II", "JJ"]
rdist = [100, 150, 200]


def distance(X1,Y1,E1,X2,Y2,E2):
    planard = math.sqrt((X2 - X1)**2 + (Y2 - Y1)**2)
    D = math.sqrt((0.9996*planard)**2 + (E2 - E1)**2) * (((E2+E1)/2 + 6371000)/ 6371000)
    return D


def algo(dataframe, drange):
    for i, rowi in dataframe.iterrows():
        lbldist = []
        for j, rowj in dataframe.iterrows():
            if i==j : continue
            d = distance(rowi["X"], rowi["Y"], rowi["E"], rowj["X"], rowj["Y"], rowj["E"])
            if d < drange : lbldist.append(d)
        print("" , end =".")

        if len(lbldist) == 0 : df.loc[i, str(drange)] = 0
        else : df.loc[i, str(drange)] = (sum(lbldist) / len(lbldist))
    return True


def algo(df1, df2, drange):
    lbldist = []
    for i, rowi in df1.iterrows():
        for j, rowj in df2.iterrows():
            if i==j : continue
            d = distance(rowi["X"], rowi["Y"], rowi["E"], rowj["X"], rowj["Y"], rowj["E"])
            if d < drange : lbldist.append(d)
        print("" , end =".")
    return lbldist


for r in range(0,3):
    df[str(rdist[r])] = 0
    for lbln in labels:
        print("\n" + lbln + " : ")
        algo(df.loc[df['Label'].str.contains(lbln)], rdist[r])

for r in range(0,3):
    for lbl1 in labels:
        for lbl2 in labels:
            if lbl1 is lbl2 : continue
            name = str(rdist[r]) + lbl1 + lbl2
            df[name] = ""
            print("\n" + lbl1 + " to " + lbl2 + " : DIST : " + str(rdist[r]) + " :")

            D = np.array(algo(df.loc[df['Label'].str.contains(lbl1)], df.loc[df['Label'].str.contains(lbl2)], rdist[r]))
            D = np.ma.masked_equal(D, 0)
            if len(D) == 0 :
                df.loc[0, name] = ("Mean : 0")
                df.loc[1, name] = ("Deviation : 0")
                df.loc[2, name] = ("Median : 0")
                df.loc[3, name] = ("Min : 0")
                df.loc[4, name] = ("Max : 0")
                df.loc[5, name] = ("Trees around min + 10m : 0")
            else :
                df.loc[0, name] = ("Mean : " + str(D.mean()))
                df.loc[1, name] = ("Deviation : " + str(D.std()))
                df.loc[2, name] = ("Median : " + str(np.ma.median(D)))
                df.loc[3, name] = ("Min : " + str(D.min()))
                df.loc[4, name] = ("Max : " + str(D.max()))
                df.loc[5, name] = ("Relations Around min + 10m : " + str(np.count_nonzero((D < (D.min() + 10.0)))))

df.to_csv('result.csv') 





