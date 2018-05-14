#code file for python

def read_data(row1,col1):
    a = [[0] * col1 for i in range(n)]
    for i in range(0,row1):
        a[i]=[int(b) for b in input().split()]
    return a

#reading a text file
def readmyfile(filepath):
    with open(filepath,"r") as f:
        text = f.read()
    return text
#count sentences in a text file
def countsentences(text):
    sentences = text.split("\n")
    #print("The sentences are:" + str(len(sentences)))

#count words in a text file
def countwords(text):
    unwanted=".,()-!?"
    text = text.strip(unwanted)
    words=text.split()
    #print("The words are:" + str(len(words)))
    return words

#print(word frequency) in a text file
def wordfreq(words):
    unique=set(words)
    dict_words={a:0 for  a in unique }# create dictionary of unique words with zero count initialised
    for eachword in words:
        if eachword in unique:
            dict_words[eachword]=dict_words[eachword]+1
    return(dict_words)

#using dataframes to present chapterwise data, where person, place
# are lists with interest names to be counted for occurences in each chapter
def chaptercounts(people,place):
    df2= pd.DataFrame()
    dictpeople={ person:dict_words[person] for person in people}
    dictplace={ place:dict_words[place] for place in places}
    dictcombined={**dictpeople,**dictplace}

    df = pd.DataFrame()
    for person,count in dictcombined.items():
        df[person] = [count]

    df2= pd.DataFrame()
    dictfull={ person:dict_words[person] for person in people}
    dictchapl={ place:dict_words[place] for place in places}
    dictchap={**dictpeople,**dictplace}
    newdict={i:dict_words[person] for i in range(1,len(chapters))}
    return newdict