# Predictor de emojis
## 1. Creando los datos
Para crear los datos se ha creado una base de datos con 260 palabras y frases distintas las cuales estarán separadas por una coma de su respectivo emoji. Para este ejercicio he elegido usar 20  emojis, pues generar suficientesd datos para entrenar a más puede tornarse complicado. Cada emoji será representado con un número para ser usado en el modelo

|Emoji |Code | Emoji|Code|
| ---| ---| ---| ---|
|💔| 0|♥️| 1|
|😂| 2|😃| 3|
|😭| 4|🤬| 5|
|🥳|6 |👋| 7|
|🖕|8 |✌️|9 |
|🙏| 10|✈️| 11|
|🛍️| 12|🏖️|12 |
|🍔| 14|🍕|15 |
|🎂|16 |🍟| 17|
|🚗| 18|🚴|19 |

## 2. Transformando a vectores
Para crear los vectores correspondientes usaremos la librería de gensim.models, específicamente la función de `Word2vec`
```python
from gensim.models import Word2Vec

frases = open("Frases.txt",'r')
listaFrases = frases.readlines()
frases.close()

model = Word2Vec(listaFrases, vector_size=100, window=5, min_count=1, workers=4)

# Convert text into vectors using the word2vec model
vectors = []
for sentence in listaFrases:
    vector = np.zeros(100)
    for word in sentence:
        vector += model.wv[word]
    vectors.append(vector)
```

Esto nos va a devolver una lista de 260 vectores de 100 elementos cada uno, como se especificó en el parámetro`vector_size`

Ahora debemos de crear las  'llaves' o clasificaciones acorde al modelo. Para esto usaremos el siguiente código:
```python 
answers = []
for i in range(20):
    for j in range(13):
        answers.append(i)

```
Finalmente crearemos un dataframe de pandas para almacenar todos nuestros datos y a partir de ahí entrenar el modelo.

```python

answers = []
for i in range(20):
    for j in range(20):
        answers.append(i)
columns =[]
for i in range(0,101):
    columns.append('col'+str(i))


columnElements  = []
for i in range(100):
    newCol=[]
    for j in range(400):
        newCol.append(vectors[j][i])
    columnElements.append(newCol)  
columnElements.append(answers)

data = dict(zip(columns,columnElements)

```

## 3. Entrenando el modelo
Antes de cualquier cosa debemos separar nuestro set de datos en datos de entrenamiento y datos de prueba, esto lo hacemos con la función `train_test_split` 

```python
from sklearn.model_selection import train_test_split

X = vectors
y = answers

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

```

Para entrenar el modelo usamos la función `KNeighborsClassifier` de sklearn.
```python
from sklearn.neighbors import KNeighborsClassifier

kClassifier = KNeighborsClassifier(n_neighbors=3)
kClassifier.fit(X_train, y_train)
```
## 4. Probando el modelo
Primero usaremos una función llamada `score`la cual nos da la precisión promedio.
```python
print('Mean accuracy:',kClassifier.score(X_test, y_test))
>>>Mean accuracy: 0.14166666666666666
```
Tras agregar 240 datos más (pasando de 13 frases por emoji a 25) la precisión promedio aumentó de 0.141 a 0.15 después de trabajar con 20 datos por emoji y finalmente a 0.1533 al usar 25 datos por emoji.

Usando algunos ejemplos del test de entrenamiento estos son los resultados:

```python
for i in range(6):
    randTst = []
    randTst.append(X_test[i])
    print(listaFrases[vectors.index(randTst[0])])
    print(kClassifier.predict(randTst))
    >>>Comeré hamburguesas
[0]
Te da mucha risa
[7]
Haremos hamburguesas
[4]
Felices fiestas
[2]
Estoy deprimido
[4]
Vamos por comida rápida
[17]

```
Resumiendo los resultados en una tabla nos da lo siguiente:

|frase| código |emoji |Resultado|frase |código |emoji|Resultado|
|---|---|---|---|---|---|---|---|
|Comeré hamburguesas|0|♥️|❌|Felices fiestas |2|😂|❌|
|Te da mucha risa|7|👋|❌|Estoy deprimido |4|😭|✅|
|Haremos hamburguesas|4|😭|❌|Vamos por comida rápida|17|🍟|✅|

Este modelo debería aproximadamente predecir el emoji apropiado 1 de cada 6 veces. 

## 5. Análisis y conclusiones
Este modelo tiene una muy baja precisión. Probablemente sea influenciado por la limitada cantidad de datos. Los otros modelos tenían (por mínimo 900 datos) además de que no eran puramente modelos de clasificación. Como se pudo ver aumentar la cantidad de datos puede aumentar la precisión del modelo, y probablemente usar miles de datos podría aumentar demasiado la precisión del modelo


## 6. Notas
- Se cambió el parámetro dentro del ciclo que agrega las respuestas a la lista `answers`. Y este debe de corresponder a la cantidad de datos por emoji. 
- Si se desea agregar más datos para experimentación, es debido recordar que los datos están ordenados de la misma manera que lo están los códigos de los emojis (es decir, el corazón ocupa los primeros 25 lugares, el corazón roto los siguientes 25 y este patrón se repite para cada emoji). 