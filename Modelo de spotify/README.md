# Modelo de Spotify
## Paso 1: limpieza de datos
### Elementos duplicados
El primer paso para limpiar los datos fue identificar duplicados. Para esto empezamos revisando los nombres de cada uno de las canciones disponibles. Para esto se hizo una lista con todos los nombres de canciones encontrados bajo el atributo `track_name`, se iteró por esa lista y se contó las veces que aparecía una cuenta mayor a 1 (spoiler: no apareció una sola vez)

```python
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
### Analizando las variables
Ahora toca analizar las variables que hay. Las que más nos llaman la atención son aquellas que no sean tipo int64 (a excepción del título de la canción, el cual después será transformado al índice del set de datos), pues harán dificil la tarea de analizar la correlación entre las variables. Encontramos que son 6 variables distintas, las cuales analizaremos una por una 


#### artist(s)_name
#### streams
#### in_deezer_playlists
#### in_shazam_charts
#### key
Para analizar este parámetro primero podemos comenzar analizando cuantas notas distintas hay. Para esto usamos el siguiente código para revisar cuantas notas diferentes hay así como imprimir cuantas tenemos

```python
import pandas as pd


#Read the csv 
spotifyCsv = pd.read_csv('spotify2023.csv', encoding='latin-1')

trackList = []

trackList = spotifyCsv['key']
keyTracker =[]
for i in trackList:
    if i not in keyTracker:
        keyTracker.append(i)
print("Number of keys: ", len(keyTracker))
print(keyTracker)
>>>Number of keys:  12
['B', 'C#', 'F', 'A', 'D', 'F#', nan, 'G#', 'G', 'E', 'A#', 'D#']
```
Analizando las notas distintas, al inicio creí que `nan` era un error, quizá una edición por parte mía accidental. Sin embargo, después de descargar nuevamente el set de datos y volver a correr el código, siguió apareciendo `nan`, lo cual nos indica que hay llaves que no se presentan en los datos. 

Antes de reemplazar cada `nan`por un valor específico, primero debemos de ver cuantos datos son `nan`para ver si son muchos como para que sea mejor ignoarar la variable.

Para esto podemos filtrar a partir del tipo de datos. Por lo tanto primero identificamos cuantos tipos de datos distintos hay. Para esto, podemos usar la lista que creamos en el código pasado, la cual ya contiene todos los posibles valores para las notas.

```python
import pandas as pd


#Read the csv 
spotifyCsv = pd.read_csv('spotify2023.csv', encoding='latin-1')

trackList = []

trackList = spotifyCsv['key']
keyTracker =[]
for i in trackList:
    if i not in keyTracker:
        keyTracker.append(i)
for i in keyTracker:
    print(type(i))
>>>
<class 'str'>
<class 'str'>
<class 'str'>
<class 'str'>
<class 'str'>
<class 'str'>
<class 'float'>
<class 'str'>
<class 'str'>
<class 'str'>
<class 'str'>
<class 'str'>
```

Ahora que conocemos que solo hay 2 tipos de datos, podemos contar cuantos `nan`hay contando los datos que no sean de tipo `str`

```python
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
>>> Number of NaNs: 95
```
Para un set de datos de 955 elementos, esto implica que el 9.947% de los datos no contienen la nota asociada a su canción. Esto es casi el límite bajo el cual se considera que pueden ocurrir sesgos en los datos al sustituirlos por otros valores. Por lo tanto se sustituirá sus valores por el promedio del resto de valores

#### mode
Analizando las primeras 2 entradas pude encontrar solamente 2 modeos: major y minor. Sin embargo para evitar confiar en la intuición lo comprobamos con una función cuando menos parecida a la pasada:
```python
import pandas as pd

#Read the csv 
spotifyCsv = pd.read_csv('spotify2023.csv', encoding='latin-1')

trackList = []
trackList = spotifyCsv['mode']
modeTracker = []
for i in trackList:
    if i not in modeTracker:
        modeTracker.append(i)
print("Number of different modes: "len(modeTracker))
print(modeTracker)

>>> Number of different modes:  2
    ['Major', 'Minor']
```
Como podemos ver solo hay 2 modos distintos: Major y Minor. Para analizarlos de manera numérica transformaremos Minor a 0 y Major a 1. Por lo tanto podemos cambiar los valores usando el siguiente código:

```python
trackList = spotifyCsv['mode']
print(spotifyCsv['mode'])
modeTracker = []
newModes = []
for i in trackList:
    if i == 'Major':
        newModes.append(1)
    else:
        newModes.append(0)

spotifyCsv['mode'] = newModes
```

# Referencias
9.Bennett DA. (2001). How can I deal with missing data in my study?. Aust N Z J Public Health, 25(5):464–9.