import pandas as pd
import math
import matplotlib.pyplot as plt
from scipy import stats as stats
import seaborn as sb
from sklearn.model_selection import train_test_split
from sklearn.metrics import root_mean_squared_error
from sklearn.ensemble import RandomForestRegressor
"""
videogameSet = pd.read_csv('vgchartz-2024.csv')
videogameSet.set_index('img', inplace=True)
names = videogameSet['title'].tolist()




videogameSet = pd.read_csv('vgchartz-2024.csv')
videogameSet.set_index('img', inplace=True)
# Esto se añadió después, pues se descubrió que valores
#de tipo NaN fueron incluidos en las nuevas variables
videogameSet.fillna(0, inplace=True)
"""
"""
# This part of the code checks for NaN values
def nanChecker(field):
    fieldList  = videogameSet[field]
    fieldList = fieldList.tolist()
    nanVal = float('nan')
    dTypes = []

    for i in fieldList:
        if type(i) not in dTypes and i != nanVal:
            dTypes.append(type(i))
        elif i == nanVal and 'nan' not in dTypes:
            dTypes.append('nan')
    print('Datatypes for ',field,':',dTypes)

nanChecker('total_sales')
nanChecker('na_sales')
nanChecker('jp_sales')
nanChecker('pal_sales')
nanChecker('other_sales')
nanChecker('critic_score')
"""





"""
#creating new non-repeating names
newNames = []
for i in range(len(names)):
    names[i] = names[i].replace(' ','')
for i in names:
    if i not in newNames:
        newNames.append(i)


#creating arrays of lenght of not repeating names
newSales = [0]*len(newNames)
meanCount = [1]*len(newNames)
newNaSales = [0]*len(newNames)
newJpSales = [0]*len(newNames)
newPalSales = [0]*len(newNames)
newOtherSales = [0]*len(newNames)
newCriticScore = [0]*len(newNames)



def replacer(newList,field,operation):
    fieldList  = videogameSet[field].tolist()
    for i in range(len(names)):
        if names.count(names[i])==1:
            newList[newNames.index(names[i])] = fieldList[i]
        else:
            if operation =='sum':
                newList[newNames.index(names[i])] += fieldList[i]
            elif operation == 'mean':
                meanCount[newNames.index(names[i])] +=1
                newList[newNames.index(names[i])] = newList[newNames.index(names[i])] + (1/meanCount[newNames.index(names[i])])*(fieldList[i] - newList[newNames.index(names[i])])

replacer(newSales,'total_sales','sum')
replacer(newNaSales,'na_sales','sum')
replacer(newJpSales,'jp_sales','sum')
replacer(newPalSales,'pal_sales','sum')
replacer(newOtherSales,'other_sales','sum')
replacer(newCriticScore,'critic_score','mean')
"""

"""
#Histogram of total sales
plt.hist(newSales,bins=500)
plt.show()
"""

"""
#Code for reviewing percentiles
j =99.5
for i in range(10):
    print(stats.scoreatpercentile(newSales,j))
    j= j+0.05
    
"""
"""
#creating the popularity attribute
popularity = [0]*len(newSales)
for i in range(len(newSales)):
    if newSales[i] >= 10:
        popularity[i] = 2
    elif newSales[i] >= 1:
        popularity[i] = 1
    else:
        popularity[i] = 0
"""
"""
#creating the new dataframe
newdFData = pd.DataFrame({'name':newNames,'sales':newSales,'na_sales':newNaSales,'jp_sales':newJpSales,'pal_sales':newPalSales,'other_sales':newOtherSales,'critic_score':newCriticScore,'popularity':popularity})
newdFData.set_index('name',inplace=True)
newdFData.to_csv('newvgamedata.csv',index=False)
"""

newvGameCSV = pd.read_csv('newvgamedata.csv')
"""
#heatmap
heatmap = sb.heatmap(newvGameCSV.corr(method = 'pearson'), annot=True, annot_kws={'size': 6},xticklabels=True, yticklabels=True)
plt.show()
"""

newvGameCSV.drop('critic_score', axis=1, inplace=True)
newvGameCSV.drop('jp_sales', axis=1, inplace=True)

def normalizer(field):
    normalizedList = newvGameCSV[field].tolist()
    maxVal = max(normalizedList)    
    for i in range(len(normalizedList)):
        normalizedList[i] = normalizedList[i]/maxVal
    newvGameCSV[field] = normalizedList

normalizer('sales')
normalizer('na_sales')
normalizer('pal_sales')
normalizer('other_sales')


X = newvGameCSV.drop('popularity',axis=1)
y = newvGameCSV['popularity']
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.3)
treeModel  = RandomForestRegressor()
treeModel.fit(X_train,y_train)
print('Mean square error: ', root_mean_squared_error(y_test,treeModel.predict(X_test)))