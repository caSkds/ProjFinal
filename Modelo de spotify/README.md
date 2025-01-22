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
Esta variable es un poco dificil de analizar, ya que no es tan sencillo transformar a números variables categóricas como lo son los nombres de artistas ni tienen un orden particular (como lo podría ser excelente, bueno, regular, malo). Esta tarea es hecha más difícil por el hecho de que algunas variables tienen más de un artista separados por una coma. Podemos empezar por contar cuantos artistas distintos hay para darnos una idea de las dimensiones del problema. 

Podemos comenzar asegurándonos que todos los datos estén completos
```python 
artists = spotifyCsv['artist(s)_name']
errors = 0
for i in range(len(artists)):

    if artists[i] =='' or artists[i] == ' ' or type(artists[i]) != str:
        print("Wrong data: ",artists[i],",found at index: ",i)
        errors+=1
if errors ==0:
    print("No errors found") 
>>> No errors found
```
Ahora podemos intentar separar cada artista diferente:
```python
artists = spotifyCsv['artist(s)_name']
errors = 0
individualArtists = []
for i in range(len(artists)):
    if ',' in artists[i]:
        separatedArtists = artists[i].split(',')
        
        for j in range(len(separatedArtists)):
            individualArtists.append(separatedArtists[j])
    else:
        individualArtists.append(artists[i])

errors = 0
for i in range(len(individualArtists)):
    if individualArtists[i] =='' or individualArtists[i] == ' ' or type(individualArtists[i]) != str:
        print("Wrong data: ",individualArtists[i],"found at index: ",i)
        errors =errors + 1
if errors ==0:
    print("No errors found") 
>>> Wrong data:    found at index:  1162
```
Si revisamos ese índice nos damos cuenta de algo bastante curioso, 
```python 
artists = spotifyCsv['artist(s)_name']
errors = 0
individualArtists = []
for i in range(len(artists)):
    if ',' in artists[i]:
        separatedArtists = artists[i].split(',')
        
        for j in range(len(separatedArtists)):
            individualArtists.append(separatedArtists[j])
            if separatedArtists[j] =='' or separatedArtists[j] == ' ':
                print(artists[i])
    else:
        individualArtists.append(artists[i])
>>> Matuï¿½ï¿½, Wiu, 
```
Hay un elemento en el CSV que posterior a su coma no tiene nada. Por lo cual debemos de añadir un filtro extra para poder agregar la totalidad de los artistas.

```python
artists = spotifyCsv['artist(s)_name']
errors = 0
individualArtists = []
for i in range(len(artists)):
    if ',' in artists[i]:
        separatedArtists = artists[i].split(',')
        
        for j in range(len(separatedArtists)):
            
            if separatedArtists[j] !='' and separatedArtists[j] != ' ':
                individualArtists.append(separatedArtists[j])
    else:
        individualArtists.append(artists[i])

errors = 0
for i in range(len(individualArtists)):
    if individualArtists[i] =='' or individualArtists[i] == ' ' or type(individualArtists[i]) != str:
        print("Wrong data: ",individualArtists[i],"found at index: ",i)
        errors =errors + 1
if errors ==0:
    print("No errors found") 
>>> No errors found
```
Ahora conseguimos agregar cada artista diferente. Por lo tanto podemos contar cuantos artistas distintos hay, esto para darnos una idea de la dimensión del problema.

Para que no haya elementos repetidos, se ha tenido que usar el método `.strip()`para eliminar las comas antes y despuúes del nombre.

```python
artists = spotifyCsv['artist(s)_name']
errors = 0
individualArtists = []
diffArtists = []
for i in range(len(artists)):
    if ',' in artists[i]:
        separatedArtists = artists[i].split(',')
        
        for j in range(len(separatedArtists)):
            
            if separatedArtists[j] !='' and separatedArtists[j] != ' ':
                individualArtists.append(separatedArtists[j])
    else:
        individualArtists.append(artists[i])


for i in individualArtists:
    if i.replace(' ','') not in diffArtists:
        diffArtists.append(i.replace(' ','')))
print("Hay ",len(diffArtists)," artistas distintos")

>>> Hay  698  artistas distintos
```
Ahora podemos pensar en una manera de transformarlos a números. De entrada podemos descartar ['One-Hot Encoding'](#snapwise-2023-11-feb-techniques-for-converting-categorical-data-into-numerical-data-medium-httpsmediumcomrafiemon71techniques-for-converting-categorical-data-into-numerical-data-f1c9d0a3863f). Si bien sería un método excelente, la cantidad de variables harían una tarea demasiado dificil computar casi 700 variables distintas. Para esto usaremos una técnica parecida llamada ['Base N Encoding'](#shipra-saxena-2024-nov-27-what-are-categorical-data-encoding-methods--binary-encoding-analytics-vidhya-httpswwwanalyticsvidhyacomblog202008types-of-categorical-data-encoding) la cual nos permite reducir por mucho la cantidad de variables. Para esto sumaré los valores de los artistas que resulten de la codificación. Si bien hay la posibiliad de que se vea imprecisado los datos, no quiero que el orden del artista (al crear varias columnas para cada artista diferente) afecte la predicción. 

Para esto codificaremos de manera separada todos los artistas distintos. Posteriormente a cada canción sumaremos los valores correspondientes a cada uno de los artistas en esa canción y será su nuevo valor en la columna `artist(s) name`. 
```python
import category_encoders as ce
import numpy as np
#Read the csv 
spotifyCsv = pd.read_csv('spotify2023.csv', encoding='latin-1')




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

```


#### streams
Para streams podemos primero identificar el tipo de datos con los que trabajamos
```python
streams = spotifyCsv['streams']
dtypes = []
for i in streams:
    iDtype = type(i)
    if type(i) == float and math.isnan(i):
        iDtype = 'nan'
    if iDtype not in dtypes:
        dtypes.append(iDtype)
print("Datatypes in streams:", dtypes)
>>> Datatypes in streams: [<class 'str'>]
```
Podemos facilmente transformar los datos a números usando el siguiente código

```python
streams = spotifyCsv['streams']
newStreams = []
for i in streams:
    newStreams.append(int(i))

spotifyCsv['streams'] = newStreams
print(spotifyCsv)
>>>ValueError: invalid literal for int() with base 10: 'BPM110KeyAModeMajorDanceability53Valence75Energy69Acousticness7Instrumentalness0Liveness17Speechiness3'
```
Viendo este error, es preciso analizar a más detalle los datos disponibles
```python
newStreams = []
for i in range(len(streams)):
    try:
        int(streams[i])
    except:
        print("error at index: ",i)
        print(streams[i])
>>>error at index:  574
BPM110KeyAModeMajorDanceability53Valence75Energy69Acousticness7Instrumentalness0Liveness17Speechiness3
```
Viendo que solo es un dato donde está el error, vemos que hay un error en el dato de este índice. Por lo que haría sentido primero corregir este dato antes de proseguir, sin embargo podemos observar que los datos que están por error en esta string, están correctamente introducidos

|Mensaje erróneo|Variables a partir de BPM|
|---|---|
|BPM110KeyAModeMajorDanceability53Valence75Energy69Acousticness7Instrumentalness0Liveness17Speechiness3|110,A,Major,53,75,69,7,0,17,3|

Por lo tanto no es necesario aplicar preprocesamiento antes de proseguir, y solo ignorar esta variable para este dato en específico.

Sabiendo que falta 1 dato entre 953, podemos sustituir este por el valor promedio del resto de datos y reemplazar ese valor por el dato faltante. Para mantener uniformidad en el tipo de datos, he elegido que lo mejor sería redondear el promedio y pasarlo como `int`.

```python
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
```



#### in_deezer_playlists
Trabajando con esta variable podemos primero empezar con ver conn que tipo de datos nos encontramos


```python
deezerPlaylists = spotifyCsv['in_deezer_playlists']

dtypes = []
for i in deezerPlaylists:
    if type(i) not in dtypes:

        if type(i)== float and math.isnan(i):
            dtypes.append('NaN')
        else:
            dtypes.append(type(i))
print(dtypes)
>>> [<class 'str'>]
```
Afortunadamente solo tenemos un tipo de datos, y no hay datos faltantes. Viendo rápidamente el CSV nos damos cuenta de que este tipo de datos son solamente números. Por lo cual podemos hacer lo siguiente:

```python
deezerPlaylists = spotifyCsv['in_deezer_playlists']
newDeezerPlaylists = []
dtypes = []
for i in deezerPlaylists:
    newDeezerPlaylists.append(int(i))

spotifyCsv['in_deezer_playlists'] = newDeezerPlaylists
>>>ValueError: invalid literal for int() with base 10: '2,445'
```

Nos damos cuenta que hay valores con comas, por lo cual no es tan simple transformar todo con la función `int()`. Antes de proceder podemos primero contar cuantas comas hay para saber si debemos de discriminar por valores con más de una coma.

```python
commas = []
for i in deezerPlaylists:
    if ',' in i:
        if i.count(',') not in commas:
            commas.append(i.count(','))
print("Number of commas in all elements: ", commas)
>>> Number of commas in all elements:  [1]
```
Afortunadamente solo hay valores con una coma, por lo cual podemos de manera relativamente simple transformar estos valores y agregarlos a la lista que reemplazará este campo.

```python
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
```
#### in_shazam_charts
Esto es un poco extraño porque a primera vista pareciera como si esta variable fueran números, sin embargo al revisar el primer elemento notamos que son de clase `str`
```python
trackList = spotifyCsv['in_shazam_charts']
print(type(trackList[0]))
>>> <class 'str'>
```
Antes de intentar generalizar un método para todos los elementos debemos revisar si todos los elementos son de la misma clase. 
```python
spotifyCsv = pd.read_csv('spotify2023.csv', encoding='latin-1')

trackList = spotifyCsv['in_shazam_charts']
diffElements = 0
types = []
for i in range(len(trackList)):
    if type(trackList[i]) != str:
        diffElements = diffElements + 1
        if type(trackList[i]) not in types:
            types.append(type(trackList[i]))
print("Number of different elements: ", diffElements)
print("Types of different elements: ",types)

>>> Number of different elements:  50
    Types of different elements:  [<class 'float'>]
```
Antes de continuar debemos de filtar si no hay datos faltantes, pues `NaN`es de tipo flotante en python.
```python
import pandas as pd
import math 

#Read the csv 
spotifyCsv = pd.read_csv('spotify2023.csv', encoding='latin-1')

trackList = spotifyCsv['in_shazam_charts']

trackList = spotifyCsv['in_shazam_charts']
NaNs = 0

for i in range(len(trackList)):
    if type(trackList[i]) != str:
        if math.isnan(trackList[i]):
            NaNs = NaNs + 1
print("Number of NaNs: ", NaNs)
>>> Number of NaNs:  50
```
Ahora sabemos algo bastante interesante. Todo dato que está como flotante es porque es un dato faltante. En un set de 953 datos, implica que el 9.967% de los datos faltan , lo cual es [a penas por debajo del límite bajo el cual reemplazarlo por otros valores sesga nuestros datos](#9bennett-da-2001-how-can-i-deal-with-missing-data-in-my-study-aust-n-z-j-public-health-2554649). Por lo tanto podemos reemplazarlo por el valor promedio. Antes de eso, debemos de convertir los datos existentes a datos de punto flotante.

```python
spotifyCsv = pd.read_csv('spotify2023.csv', encoding='latin-1')

trackList = spotifyCsv['in_shazam_charts']
chartsSum = 0
newShazamCharts = []
for i in trackList:
    if type(i) ==str:
        newShazamCharts.append(float(i))
    else:
        newShazamCharts.append(i)

chartsAvg = chartsSum/953
print("The average is: ", chartsAvg)
>>> ValueError: could not convert string to float: '1,021'
```
Ahora sabemos que hay elementos con comas, lo cual implica que debemos de preprocesar los datos con comas. Antes de eso poedmos primero revisar que otros carácteres distintos hay además de la coma, si es que los hay.

```python
newCharacters = []
numbers = ['0','1','2','3','4','5','6','7','8','9']
for i in trackList:
    if type(i) ==str:
        try:
            float(i)
        except:
            for j in i:
                if j not in numbers and j not in newCharacters:
                    newCharacters.append(j)

print(newCharacters)
>>> [',']
```
Ahora sabemos que solo hay comas. Pero antes de saber como convertir a miles, me interesa saber si hay elementos donde haya más allá de una coma.

```python
commaCounts = []
for i in trackList:
    if type(i) ==str and i.count(',') > 0 and i.count(',') not in commaCounts:    
        commaCounts.append(i.count(','))

print(commaCounts)
>>> [1]
```

Ahora sabemos que solo tenemos una coma. Lo cual implica que podemos convertir los números antes de la coma, multiplicarlos por 1000 y sumar los que vengan después de la coma.
```python
trackList = spotifyCsv['in_shazam_charts']


avgSum = 0
NaNs = 0
for i in trackList:
    if type(i) == str:
        if ',' in i:
            thousands =0
            units = 0
            thousands = float(i.split(',')[0])
            units = float(i.split(',')[1])
            avgSum += thousands*1000 + units
            
        else:
            avgSum += float(i)
    else:
        NaNs+=1

avg = avgSum/(len(trackList)-NaNs)
print("The average is: ", avg)

>>> The average is:  59.99557032115172
```
Ahora tenemos el valor promedio, por lo que podemos sustituir los valores faltantes por 60 (Redondeando a números enteros)

```python
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
```

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
Para un set de datos de 953 elementos, esto implica que el 9.967% de los datos no contienen la nota asociada a su canción. Esto es [casi el límite bajo el cual se considera que pueden ocurrir sesgos en los datos al sustituirlos por otros valores](#9bennett-da-2001-how-can-i-deal-with-missing-data-in-my-study-aust-n-z-j-public-health-2554649). Por lo tanto se sustituirá sus valores por el promedio del resto de valores

Para esto primero tenemos que calcular el valor promedio de los valores que sí tenemos. Y antes de eso tenemos que establecer los valores. 

Para esto podemos filtrar a partir del tipo de datos. Por lo tanto primero identificamos cuantos tipos de datos distintos hay. Para esto, podemos usar la lista que creamos en el código pasado, la cual ya contiene todos los posibles valores para las notas. Ordenaremos las notas en el siguiente orden: `do,re,mi,fa,sol,la,si`. Sin embargo las notas se encuentran enlistadas con letras, por lo cual usaremos su [equivalente](#musicamanía-sf-las-notas-de-la-escalahttpsmusicamaniaazucreiscomsolfeolas-notaslas-notas-de-la-escala) y nos quedan así: `C,D,E,F,G,A,B`

Antes de transformarlo a números tenemos que observar que hay notas con un `#`a lado de sí mismas. Esto implica que hay un [semitono](#solfeando-sf-notas-musicales-httpswwwacademiasolfeandocomnotas-musicales). Dichas notas están elevadas un semitono. Por lo tanto nuestro nuevo orden queda así 
`C#,D,D#,E,F,F#,G,G#,A,A#,B`. A estas les asignaremos un valor del 1 al 7, con el `#`representando un 0.5 más. Por lo tanto quedaría así:

|C#|D|D#|E|F|F#|G|G#|A|A#|B|
|---|---|---|---|---|---|---|---|---|---|---|
|1.5|2|2.5|3|4|4.5|5|5.5|6|6.5|7|

```python
import pandas as pd


#Read the csv 
spotifyCsv = pd.read_csv('spotify2023.csv', encoding='latin-1')

trackList = []

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


NaNs = 0
def keyNumeralizer(key):
    counter=0
    for i in keys:
        if i == key:
            counter = keys[i]
        
    return counter


keySum = 0
for i in trackList:
    if keyNumeralizer(i) == 0:
        NaNs = NaNs + 1
    keySum = keySum + keyNumeralizer(i)


keyAvg= keySum/(len(trackList)-NaNs)
print("The average key is: ", keyAvg)

>>> The average key is:  4.269230769230769
```
Redondeando en intervalos de 0.5, podemos inferir que la nota promedio es`F#`. Por lo tanto cada valor que no sea identificado como una nota será reemplazado por 4.5

Ahora sí podemos reemplazar cada nota por un número usando el siguiente código:
```python
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
```



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


## Paso 2: Identificando variables más influyentes
Para hacer esto debemos de identificar las variables más influyentes. Antes de pensar en como identificar la correlación debemos reindexar la variable `track_ name` pues estamos considerando a los otros valores como las variables. 

```python 
spotifyCsv.set_index('track_name', inplace=True)
```
Ahora podemos armar una matriz de correlación, la cual nos mostrará la correlación entre cada uno de los datos. Primero debemos importar algunas librerías antes de continuar
```python 
import seaborn as sb
import matplotlib.pyplot as mp
```
Ahora podemos imprimir el mapa de calor, el cual tiene algunos parámetros diseñados para que muestre la totalidad de las variables y sea correctamente visualizado el coeficiente.

```python
heatmap = sb.heatmap(spotifyCsv.corr(method = 'pearson'), annot=True, annot_kws={'size': 6},xticklabels=True, yticklabels=True)
plt.show()
```
![Pearson coefficient heatmap](/ProjFinal/Modelo%20de%20spotify/heatmap.png)
Algo muy evidente es que los artistas no importan tanto como uno esperaría. Pero vamos a hacer esto más fácil de ver. Para esto analizaremos la matriz de correlación y obtendremos los nombres de las variables [cuyo valor absoluto sea mayor a 0.3, para que valga la pena considerarlos ](#keith-g-calkins-2005-julio-18applied-statistics---lesson-5--correlation-coefficients-andrews--universityhttpswwwandrewseducalkinsmathedrm611edrm05htmtextcorrelation-coefficients-whose-magnitude-are-between-03-and-05-indicateif-any-linear-correlation). 


```python
matrizCorrelacion = spotifyCsv.corr(method = 'pearson')
valoresSignificativos =(matrizCorrelacion.loc['streams'])
print(valoresSignificativos)
>>>artist_count           -0.136436
released_year          -0.228506
released_month         -0.024912
released_day            0.010587
in_spotify_playlists    0.789786
in_spotify_charts       0.245773
streams                 1.000000
in_apple_playlists      0.771917
in_apple_charts         0.320057
in_deezer_playlists     0.598104
in_deezer_charts        0.228575
in_shazam_charts        0.022266
bpm                    -0.002438
key                    -0.058434
mode                    0.042618
danceability_%         -0.105406
valence_%              -0.040810
energy_%               -0.026050
acousticness_%         -0.004483
instrumentalness_%     -0.044902
liveness_%             -0.048337
speechiness_%          -0.112302
artistCode0            -0.117194
artistCode1             0.008873
artistCode2            -0.050192
artistCode3            -0.044719
artistCode4            -0.029486
artistCode5            -0.001432
artistCode6            -0.098658
artistCode7            -0.071426
artistCode8            -0.086167
artistCode9            -0.061053
Name: streams, dtype: float64

```
Como podemos ver las únicas variables que cumplen el requisito anterior son las siguientes 4:
- `in_spotify_playlists`
- `in_apple_playlists`
- `in_apple_charts`
- `in_deezer_playlists`

Dado que son las úncias variables que siquiera hace sentido evaluar, el modelo de regresión solo será hecha con estas para minimzar el uso de recursos computacionales y el ruido potencial de incluir datos innecesarios en nuestras predicciones.

Nótese que la variable `streams`no ha sido considerada pues es el dato a predecir.


## Paso 3: Separar y normalizar datos
Ahora podemos enfocarnos en separar los datos a usar. Se usará un 70% de los datos para propósitos de entrenamiento. Para esto comenzaremos separando los valores que tomaremos en cuenta para la predicción y los valores a predecir .

```python 
spotifyCsv.set_index('track_name', inplace=True)
usefulVariables = ['in_spotify_playlists','in_apple_playlists','in_apple_charts','in_deezer_playlists','streams']
spotifyCsv = spotifyCsv.loc[:,usefulVariables]
```
Antes de separar los datos en datos de entrenamiento y de prueba hay un último paso que hay que hacer, que es normalizarlos para que sus valores vayan del 0 al 1 solamente.

```python 
def normalizer(x):
    normalizedList = spotifyCsv[x] 
    normalizedList = normalizedList/max(normalizedList)
    spotifyCsv[x] = normalizedList

normalizer('in_spotify_playlists')
normalizer('in_apple_playlists')
normalizer('in_apple_charts')
normalizer('in_deezer_playlists')
```
Ahora sí podemos separar nuestros datos en datos de entrenamiento y datos de prueba. Para esot usaremos la función `train_test_split`

```python
from sklearn.model_selection import train_test_split
X=spotifyCsv.drop('streams',axis=1)
y = spotifyCsv['streams']
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.3)
```


## Paso 4: Entrenar y evaluar modelo
Finalmente para entrenar el modelo podemos usar el método `fit()`

```python
from sklearn.linear_model import LinearRegression
linearModel = LinearRegression()
linearModel.fit(X_train,y_train)

```

Finalmente mediremos la precisión del modelo usando una métrica conocida como RMSE (Root Mean Square Error) la cual evalúa el promedio de las distancias entre los valores de prueba y los valores predichos
$$RMSE = \sqrt{\frac{1}{n}\sum_{i=1}^n (y_i-\hat{y}_i)}$$

Siendo el primero el valor que debería de obtener y el segundo la predicción hecha por el modelo que hemos hecho. 
```python
from sklearn import metrics
linearModel = LinearRegression()
linearModel.fit(X_train,y_train)
print('Root mean square error: ', metrics.root_mean_squared_error(y_test,linearModel.predict(X_test)))
>>>Root mean square error:  0.0926850837852167
```





## Notas importantes
1. Gran parte del código mostrado en este archivo no han quedado en el archivo final, tal como lo son las pruebas para evaluar el tipo de datos de cada variable. Sin embargo, se es libre de correr el código y (con las librerías usadas) mostrará el mismo resultado que el mostrado en este archivo

2. El mapa de calor de coreficientes de pearson ha quedado "comentado en el código", de manera que solo basta con quitar las comillas triples para visualizarlo.

3. Algunos de los métodos que han sido usados para filtrar los datos han quedado comentados, ya que múltiples variables no son siquiera relevantes para hacer cualquier tipo de predicción.
# Referencias
###### 9.Bennett DA. (2001). How can I deal with missing data in my study?. Aust N Z J Public Health, 25(5):464–9.

###### Musicamanía (s.f.) Las notas de la escala.https://musicamania.azucreis.com/solfeo/las-notas/las-notas-de-la-escala/

###### Solfeando (s.f.) Notas Musicales. https://www.academiasolfeando.com/notas-musicales/



###### SnapWise (2023, 11 Feb) Techniques for Converting Categorical Data into Numerical Data. Medium. https://medium.com/@rafiemon71/techniques-for-converting-categorical-data-into-numerical-data-f1c9d0a3863f


###### Shipra Saxena (2024, Nov 27) What are Categorical Data Encoding Methods | Binary Encoding. Analytics Vidhya. https://www.analyticsvidhya.com/blog/2020/08/types-of-categorical-data-encoding/


###### Keith G. Calkins (2005, Julio 18)Applied Statistics - Lesson 5  Correlation Coefficients. Andrews  University.https://www.andrews.edu/~calkins/math/edrm611/edrm05.htm#:~:text=Correlation%20coefficients%20whose%20magnitude%20are%20between%200.3%20and%200.5%20indicate,if%20any%20(linear)%20correlation.