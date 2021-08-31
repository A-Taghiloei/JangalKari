import numpy as np
import math
import pickle
import random

labels = ["AA", "BB", "CC", "DD", "EE", "FF", "GG", "HH", "II", "JJ"]
planted = {}
treenum = []
used = {}
blocked = {}

for i in labels:
    planted[i+"X"] = []
    planted[i+"Y"] = []

with open("fdata.pkl", 'rb') as handle:
    distdata = pickle.load(handle)

def distance(X1,Y1,E1,X2,Y2,E2):
    planard = math.sqrt((X2 - X1)**2 + (Y2 - Y1)**2)
    D = math.sqrt((0.9996*planard)**2 + (E2 - E1)**2) * (((E2+E1)/2 + 6371000)/ 6371000)
    return D


for lbl in labels:
    num = int(input("Number of "+lbl+" trees: "))
    treenum.append(num)


xcoord = float(input("start point X: "))
ycoord = float(input("start point Y: "))
length = int(input("Area Length :"))
width = int(input("Area width :"))

blocked["X"]=[]
blocked["Y"]=[]
while(True):
    x = input("Not Useful area X: ")
    if(x == "NAN"): break
    blocked["X"].append(float(x))
    y = input("Not Useful area Y: ")
    blocked["Y"].append(float(y))



def randomtree(lbl, num):
    result = []
    while(True):
        randx = random.uniform(xcoord, length)
        randy = random.uniform(ycoord, width)
        result = [randx, randy]
        for i in range(0, len(blocked["X"])):
            if((randx <= blocked["X"][i]+1 and randx >= blocked["X"][i]-1) and (randy <= blocked["Y"][i]+1 and randy >= blocked["Y"][i]-1)): 
                result = []
                break
        if(len(result) !=0 ): break
    return result


def checktree(tree, lbl):
    for i in range(len(used["X"])):
        if((tree[0] <= used["X"][i]+5 and tree[0] >= used["X"][i]-5) and (tree[1] <= used["Y"][i]+5 and tree[1] >= used["Y"][i]-5)):
            for key in labels:
                if((used["X"][i] in planted[key+"X"]) and (used["Y"][i] in planted[key+"X"])):
                    checkdistance = distance(tree[0], tree[1], 0, used["x"][i], used["Y"][i], 0)
                    name = key + lbl
                    if(name in distdata):
                        if((checkdistance <= distdata[name][0] + distdata[name][1]/2)and (checkdistance >= distdata[name][0] - distdata[name][1]/2)):
                            return True
                        else: return False
                    else:
                        name = lbl + key
                        if(checkdistance <= distdata[name][0] + distdata[name][1]/2 and checkdistance >= distdata[name][0] - distdata[name][1]/2):
                            return True
                        else: return False
    return True


used["X"] = []
used["Y"] = []
while(True):
    
    while(True):
        if(len(treenum) == 0) : break

        minnum = min(treenum)
        minindex = [i for i, j in enumerate(treenum) if j == minnum]
        if(minnum == 0):
            del treenum[minindex[0]]
            del labels[minindex[0]]
        else:
            break

    if(len(labels)==0): break
    
    random_index = random.randint(0,len(labels)-1) 

    while(True):
        plantedtree = randomtree(labels[random_index], treenum[random_index])
        if(checktree(plantedtree, labels[random_index])):
            planted[labels[random_index]+"X"].append(plantedtree[0])
            planted[labels[random_index]+"Y"].append(plantedtree[1])

            used["X"].append(plantedtree[0])
            used["Y"].append(plantedtree[1])

            treenum[random_index] = treenum[random_index] - 1
            break
        else:
            continue

print(planted)