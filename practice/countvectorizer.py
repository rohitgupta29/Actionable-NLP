import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize import TreebankWordTokenizer
from sklearn.model_selection import train_test_split

from sklearn.metrics.classification import classification_report,accuracy_score
from sklearn.model_selection import cross_val_predict
from sklearn.naive_bayes import GaussianNB, MultinomialNB
    



path = './C50train/'
authors = os.listdir(path)[:5]
vect = CountVectorizer()
def vector_properties(vect= CountVectorizer() , tokenizer = TreebankWordTokenizer()):
    vect.set_params(tokenizer = tokenizer.tokenize)

    #removing english words
    vect.set_params(stop_words = 'english')

    #include 1-gram and 2-grams
    vect.set_params(ngram_range = (1,2))

    #set max_df
    vect.set_params(max_df = 0.5)

    #set min_df
    vect.set_params(min_df = 2)

    return vect


vect = vector_properties(CountVectorizer(),TreebankWordTokenizer())
print(vect)

def text_and_label(authors):
    trainX = np.array([])
    labels = []
    for auth in authors:
        files = os.listdir(path + auth + '/')
        tmpX,tmpY = np.array([]),[]
        for file in files:
            f = open(path + auth + '/' + file, 'r')
            data = f.read().replace('\n','')
            tmpX = np.append(tmpX,data)
            tmpY = tmpY + [auth]
            f.close()
            
        trainX = np.append(trainX,tmpX)
        labels = labels + tmpY
    return trainX , labels

# trainX,labels = text_and_label(authors)    
# print(trainX,labels)
    
def splitting(trainX,labels):
    
    X_train,X_test,y_train,y_test = train_test_split(trainX, labels, train_size = 0.8)
    X_train = pd.Series(X_train)
    X_test = pd.Series(X_test)
    return X_train,X_test,y_train,y_test


 
 
def main():
    import pandas as pd
    
    vect = vector_properties(CountVectorizer(),TreebankWordTokenizer())
    trainX,labels = text_and_label(authors)
    
    X_train,X_test,y_train,y_test = splitting(trainX,labels)
    vect.fit(X_train)
    vect.get_feature_names()[:10]
    
    train_vectors = vect.transform(X_train)
    test_vectors = vect.transform(X_test)
    data = pd.DataFrame(train_vectors.toarray(),columns = vect.get_feature_names()).head()
    print(data)
    nb = GaussianNB()
    nb.fit(train_vectors.toarray(),y_train)
    y_pred = cross_val_predict(nb, test_vectors.toarray(), y_test, cv = 10)
    report = classification_report(y_test,y_pred)
    print("Classification Report : ", report)
    accuracy =  accuracy_score(y_pred,y_test)
    print("Accuracy: " ,accuracy)
    return report,accuracy

if __name__ == "__main__":
    main()

    


  
