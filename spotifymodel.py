import pandas as pd

#Read the csv 
spotifyCsv = pd.read_csv('spotify2023.csv', encoding='latin-1')

trackList = []
trackList = spotifyCsv['artist(s)_name']
dupedelements = 0
print(len(trackList))
for i in range(len(trackList)):
    currentTest = trackList[i]
    currentCount = trackList[i].count(trackList[i])
    if currentCount > 1:
        print(i, currentTest,currentCount)
        dupedelements = dupedelements + 1
print("Number of duplicates: ",dupedelements)