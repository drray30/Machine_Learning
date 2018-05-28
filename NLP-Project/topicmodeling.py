# A stepwise approach to topic modeling for the airline industry
# This script assumes your reviews are stored in a csv file called  reviews.to_csv


import pandas as pd
from gensim.utils import simple_preprocess,simple_tokenize #text processing
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from gensim.models.phrases import Phraser
from gensim.models import Phrases
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF

def display_topics(model, feature_names, no_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print ("Topic %d:" % (topic_idx))
        print (" ".join([feature_names[i]for i in topic.argsort()[:-no_top_words - 1:-1]]))

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


#read the csv file containing reviews
df=pd.read_csv("reviews.csv")

#getting all the reviews in a list
text=df.loc[:,"cleanreviews"].copy()
corpus_raw=text.copy()
corpus=list(corpus_raw.values)
sentences =  list(filter(None, corpus))

#doing some simple preprocessing
process_list=[]
for sentence in sentences:
    try:
        process_list.append(simple_preprocess(sentence))
    except:
        pass

#read a customized stopwords file
txt = pd.read_csv('stopwords.txt', sep=" ", header=None)
newstoplist=txt[0].tolist()
stopwords = nltk.corpus.stopwords.words('english')
stopwords.extend(newstoplist)
new_list=[]

#Tokenization and removal of stopwords
for sent1 in process_list:
    newsent=" ".join(sent1)
    word_tokens = word_tokenize(newsent)
    filtered_sentence = [w for w in word_tokens if w not in stopwords]
        #print(filtered_sentence)
    new_list.append(filtered_sentence)

#introducing lemmatization
lemma = WordNetLemmatizer()
new_list2=[]
for sent1 in new_list:
        normalized = " ".join(lemma.lemmatize(word,'n') for word in sent1)
        x = normalized.split()
        y = [s for s in x if len(s) > 2]
        new_list2.append(y)

#Using Bigrams
texts=new_list2
phrases = Phrases(new_list2)
bigram = Phraser(phrases)
texts = [bigram[line] for line in new_list2]

# NMF is able to use tf-idf, so using TFIDF
no_features = 750
tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, max_features=no_features, stop_words=stopwords)
tfidf = tfidf_vectorizer.fit_transform(final_list)
tfidf_feature_names = tfidf_vectorizer.get_feature_names()

# Run NMF
no_topics=5 #Multiple runs gave this as the optimum number
nmf = NMF(n_components=no_topics, random_state=1, alpha=.4, l1_ratio=.5, init='nndsvd').fit(tfidf)
no_top_words =10
display_topics(nmf, tfidf_feature_names, no_top_words)

#getting the topics for all reviews
A = tfidf_vectorizer.transform(final_list)
W = nmf.components_
H = nmf.transform(A)

#labeling each review
sortedH=(-H).argsort(axis=1)

#creating the topics
df['topic1']=sortedH[:,0]
df['topic2']=sortedH[:,1]
df['topic3']=sortedH[:,2]
df['topic4']=sortedH[:,3]
df['topic5']=sortedH[:,4]

#labeling them
df['topicname1']=df['topic1'].apply(maintopic)
df['topicname2']=df['topic2'].apply(maintopic)
df['topicname3']=df['topic3'].apply(maintopic)
df['topicname4']=df['topic4'].apply(maintopic)
df['topicname5']=df['topic5'].apply(maintopic)

#Finally save the labelled file by exporting df to csv
df.to_csv("LabelledReviews.csv")
