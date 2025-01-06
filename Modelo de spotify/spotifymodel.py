import pandas as pd


#Read the csv 
spotifyCsv = pd.read_csv('spotify2023.csv', encoding='latin-1')

trackList = []

trackList = spotifyCsv['key']
NaNCounter = 0
for i in trackList:
    if type(i)!=str:
        NaNCounter += 1

print("Number of NaNs:", NaNCounter)


'''
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
'''

