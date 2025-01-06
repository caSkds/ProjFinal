# Modelo de Spotify
## Paso 1: limpieza de datos
### Elementos duplicados
El primer paso para limpiar los datos fue identificar duplicados. Para esto empezamos revisando los nombres de cada uno de las canciones disponibles. Para esto se hizo una lista con todos los nombres de canciones encontrados bajo el atributo `track_name`, se iteró por esa lista y se contó las veces que aparecía una cuenta mayor a 1 (spoiler: no apareció una sola vez)

```
import pandas as pd

#Read the csv 
spotifyCsv = pd.read_csv('spotify2023.csv', encoding='latin-1')

trackList = []
trackList = spotifyCsv['track_name']
dupedelements = 0
print(len(trackList))
for i in range(len(trackList)):
    currentTest = trackList[i]
    currentCount = trackList[i].count(trackList[i])
    if currentCount > 1:
        print(i, currentTest,currentCount)
        dupedelements = dupedelements + 1
print("Number of duplicates: ",dupedelements)

>>> Number of duplicates:  0
```
## Normalización de variables
Ahora toca analizar las variables que hay