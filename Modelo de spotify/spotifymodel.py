import pandas as pd
import math 
import category_encoders as ce
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
import sklearn
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics

#Read the csv 
spotifyCsv = pd.read_csv('spotify2023.csv', encoding='latin-1')



"""
#Changing artist names

artists = spotifyCsv['artist(s)_name']
individualArtists = []
for i in range(len(artists)):
    if ',' in artists[i]:
        separatedArtists = artists[i].split(',')
        
        for j in range(len(separatedArtists)):
            
            if separatedArtists[j] !='' and separatedArtists[j] != ' ':
                individualArtists.append(separatedArtists[j])
    else:
        individualArtists.append(artists[i])
individualDiffArtists = []
for i in individualArtists:
    if i.replace(' ','') not in individualDiffArtists:
        individualDiffArtists.append(i.replace(' ',''))
artistCoded = ce.BaseNEncoder(base=2,return_df=False).fit_transform(individualDiffArtists)
newCodedArtists = []

for i in artists:
    newCode = 0
    if ','in i:
        separatedArtists = i.split(',')
        for j in range(len(separatedArtists)):
            if separatedArtists[j] !='' and separatedArtists[j] != ' ':
                newCode += artistCoded[individualDiffArtists.index(separatedArtists[j].replace(' ',''))]
    else:
        newCode = artistCoded[individualDiffArtists.index(i.replace(' ',''))]
    newCodedArtists.append(newCode)
spotifyCsv.drop('artist(s)_name',axis=1,inplace=True)



for i in range(len(newCodedArtists[0])):
    name = 'artistCode' + str(i)
    for j in range(len(newCodedArtists)):
        spotifyCsv.loc[j,name] = newCodedArtists[j][i]
"""





#changing streams
streams = spotifyCsv['streams']
newStreams = []
toReplace = 0
toReplaceSum = 0
toReplaceIndex = []
for i in range(len(streams)):
    try:
        newStreams.append(int(streams[i]))
    except:
        newStreams.append(0)
        toReplace +=1
        toReplaceIndex.append(i)
for i in newStreams:
    toReplaceSum+=i

toReplace = toReplaceSum/(len(newStreams)-toReplace)

for i in toReplaceIndex:
    newStreams[i]  = int(round(toReplace))
spotifyCsv['streams'] = newStreams





#changing in deezer playlists

deezerPlaylists = spotifyCsv['in_deezer_playlists']
newDeezerPlaylists = []
for i in deezerPlaylists:
        if ',' in i:
            thousands =0
            units = 0
            thousands = int(i.split(',')[0])
            units = int(i.split(',')[1])
            newDeezerPlaylists.append(thousands*1000 + units)
            
        else:
            newDeezerPlaylists.append(int(i))
spotifyCsv['in_deezer_playlists'] = newDeezerPlaylists


"""

#changing the shazam charts
trackList = spotifyCsv['in_shazam_charts']

newShazamLists = []
for i in trackList:
    if type(i) == str:
        if ',' in i:
            thousands =0
            units = 0
            thousands = float(i.split(',')[0])
            units = float(i.split(',')[1])
            newShazamLists.append(thousands*1000 + units)
            
        else:
            newShazamLists.append(float(i))
    else:
        newShazamLists.append(60)
spotifyCsv['in_shazam_charts'] = newShazamLists
"""




"""
#Changing the keys
trackList = spotifyCsv['key']

keys ={
    'C#':1.5,
    'D' :2 ,
    'D#':2.5,
    'E':3,
    'F':4,
    'F#':4.5,
    'G':5,
    'G#':5.5,
    'A':6,
    'A#':6.5,
    'B':7
}



def keyNumeralizer(key):
    counter=0
    for i in keys:
        if i == key:
            counter = keys[i]
        
    return counter


keyNumList = []
for i in trackList:
    if keyNumeralizer(i) == 0:
        keyNumList.append(4.5)
    else:
        keyNumList.append(keyNumeralizer(i))
spotifyCsv['key'] = keyNumList
"""

"""
# Changing the modes
trackList = spotifyCsv['mode']
modeTracker = []
newModes = []
for i in trackList:
    if i == 'Major':
        newModes.append(1)
    else:
        newModes.append(0)
spotifyCsv['mode'] = newModes

"""

"""
#heatmap 
# Los parámetros usados han sido seleccionados para una correcta visualización
heatmap = sb.heatmap(spotifyCsv.corr(method = 'pearson'), annot=True, annot_kws={'size': 6},xticklabels=True, yticklabels=True)
plt.show()
"""
spotifyCsv.set_index('track_name', inplace=True)
usefulVariables = ['in_spotify_playlists','in_apple_playlists','in_apple_charts','in_deezer_playlists','streams']
spotifyCsv = spotifyCsv.loc[:,usefulVariables]

def normalizer(x):
    normalizedList = spotifyCsv[x] 
    normalizedList = normalizedList/max(normalizedList)
    spotifyCsv[x] = normalizedList

normalizer('in_spotify_playlists')
normalizer('in_apple_playlists')
normalizer('in_apple_charts')
normalizer('in_deezer_playlists')
normalizer('streams')


X=spotifyCsv.drop('streams',axis=1)
y = spotifyCsv['streams']
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2)
linearModel = LinearRegression()
linearModel.fit(X_train,y_train)
print('Mean square error: ', metrics.root_mean_squared_error(y_test,linearModel.predict(X_test)))