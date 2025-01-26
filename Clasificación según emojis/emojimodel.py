from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from gensim.models import Word2Vec
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
frases = open("Frases.txt",'r')
listaFrases = frases.readlines()
for i in range(len(listaFrases)):
    listaFrases[i]=listaFrases[i].replace('\n','') 
frases.close()

model = Word2Vec(listaFrases, vector_size=100, window=5, min_count=1, workers=4)


# Convert text into vectors using the word2vec model
vectors = []
for sentence in listaFrases:
    vector = np.zeros(100)
    for word in sentence:
        vector += model.wv[word]
    vectors.append(vector.tolist())
answers = []
for i in range(20):
    for j in range(25):
        answers.append(i)




X = vectors
y = answers


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

kClassifier = KNeighborsClassifier(n_neighbors=3)
kClassifier.fit(X_train, y_train)
print('Mean accuracy:',kClassifier.score(X_test, y_test))




for i in range(6):
    randTst = []
    randTst.append(X_test[i])
    print(listaFrases[vectors.index(randTst[0])])
    print(kClassifier.predict(randTst))