#An example code for predicting the topic and sentiment , given an example review

#For further code on training the TFIDF, TOKENIZER model as well as the Keras model, see other .py files in this folder
import pandas as pd
import numpy as np
import nltk
import gensim
from gensim.utils import simple_preprocess
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from keras.models import load_model
from keras.preprocessing.text import text_to_word_sequence
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences


def maintopic(numarr):
    if numarr==0:
        return "Inflight Service"
    elif numarr==1:
        return "Time Delay"
    elif numarr==2:
        return "Seat Comfort"
    elif numarr==3:
        return "Preboarding Services"
    elif numarr==4:
        return "Business Class Services"
    else:
        return "Unknown topic"

#read the stopwords
stopwords = nltk.corpus.stopwords.words('english')

def gettopicsentiment(trialreview,stopwords=stopwords,tfidfmodel=tfidfmodel,pretrainedmodel=nmfmodel,tokenizermodel=tokenizermodel,kerasmodel=kerasmodel):
    sentence=simple_preprocess(trialreview)
    newsent=" ".join(sent for sent in sentence)
    #tokenize the words
    word_tokens=word_tokenize(newsent)
    #remove stopwords
    filtered_sentence = [w for w in word_tokens if w not in stopwords]
    #lemmatization for better results
    lemma = WordNetLemmatizer()
    lemmsent=" ".join(lemma.lemmatize(word,'n') for word in filtered_sentence)
    x = lemmsent.split()
    preptext = [s for s in x if len(s) > 2]
    wordlist=[]
    newtext=" ".join(preptext)
    wordlist.append(newtext)
    tfidfvec=tfidfmodel.transform(wordlist)
    H=pretrainedmodel.transform(tfidfvec)
    sortedH=(-H).argsort(axis=1)
    toptopics=[]
    firstindex=sortedH[0,0]
    
    #Checking for which topics are more relevant
    if H[0,firstindex]>0:
        toptopics.append(maintopic(firstindex))
    secondindex=sortedH[0,1]
    if H[0,secondindex]>0:
        toptopics.append(maintopic(secondindex))
    thirdindex=sortedH[0,2]
    if H[0,thirdindex]>0:
        toptopics.append(maintopic(thirdindex))
    fourthindex=sortedH[0,3]
    if H[0,fourthindex]>0:
        toptopics.append(maintopic(fourthindex))
    fifthindex=sortedH[0,4]
    if H[0,fifthindex]>0:
        toptopics.append(maintopic(fifthindex))
    strtopics="<br>".join([topic for topic in toptopics])


    #doing sentiment analysis using pretrained keraresult = text_to_word_sequence(trialreview)
    reviewarray=[]
    reviewarray.append(trialreview)
    reviewarray.append("another trial")
    arr=[]
    for text in reviewarray:
        textnew=contract_text(text)
        result = text_to_word_sequence(textnew)
        arr.append(result)
    encoded_docs = tokenizermodel.texts_to_matrix(arr,mode='tfidf')
    padded = pad_sequences(encoded_docs, maxlen=500, dtype='int32', value=0)
    #encoded_string=" ".join(encoded_docs)
    ypred=kerasmodel.predict_classes(padded)
    #print(ypred)
    if ypred[0]==0:
        strsentiment= "Negative"
        #self.lblSentiment.setText(strsentiment)
    elif ypred[0]==1:
        strsentiment="Neutral"
        #self.lblSentiment.setText(strsentiment)
    elif ypred[0]==2:
        strsentiment="Positive"
        #self.lblSentiment.setText(strsentiment)
    return(strtopics,strsentiment)
