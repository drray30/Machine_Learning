#data cleaning utilities in here

def readintopanda(filestr, sepa=','):
    import pandas as pd
    df= pd.read_csv(filestr,sep=sepa)
    return df

#getting single number out of a string,called clean_review
def def get_num(revstr):
    pattern=r"\d+"
    return(re.search(pattern,revstr).group(0))

#applying function to a specific column in dataframe
    #dataframe['columnname']=datafram['columnname'].apply(functioname

#Important functions in Python data handling
# dataframe.head/dataframe.tail
# dataframe.shape/dataframe.describe
# dataframe.dropduplicates()
# likes.idxmax()- to return index of max of a column
# dataframe.groupby('columnname to group by')['categoricalvar to count'].value_counts()

#code for making sure http files are opened on my mac
def httpopen():
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context
    return

#another code snippet for counting certain column values
# this counts value of each category in a categorical variable in datafram
counts = dataframe.columnname.value_counts()
# example 
# counts = openrice.food_type.value_counts() 
# output as below
'''
Hong Kong Style                  4791
Japanese                         2023
Western                          2017
Guangdong                        1998
International                     916
'''
# this uses the counts defined above as reference to give me the whole 
# dataframe 's value of counts indexed 
countseries = datafram.column.apply(lambda x: counts[x])
# counts = openrice.food_type.apply(lambda food: counts[food])
# output as below
'''
0        4791
1         916
2         696
3        4791
'''

#code to change dataframe to select rows based on threshold
dataframe = datframe[ dataframe.column >= boundaryvariable]
#openrice[ countseries > 250].food_type.value_counts()
#output as below
'''
0         True
1        False
2        False
3         True
4        False
'''


#function to convert multiple categories
def convert_multiple categories(x):
    if x in ['Shanghai','Yunnan',"Chiu Chow","Dim Sum Restaurant","Dai Pai Dong","Guangdong","Sichuan","Stir-Fry","Dim Sum Restaurant"]:
        return "Chinese"
    elif x in ['Western', 'International',"American", "French","Italian"]:
        return "Western"
    elif x in ['Fast Food', 'Hotel Restaurant',"Takeaway", "Snack Shop & Deli"]:
        return "Fast Food"
    elif x in ["Thai","Taiwan","Korean","Vietnamese"]:
        return "Other Asian"
    else:
        return x

#important plot definitions
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="whitegrid", color_codes=True)#changing background
sns.set(rc={'figure.figsize':(11.7,8.27)})#change size
sns.set_palette("husl")#change colors used

#types of plots using seaborn
sns.stripplot(x="food_type", y="likes", data=openrice)#stripplot
sns.boxplot(x="price_range", y="likes", data=openrice)#boxplot
sns.barplot(x="food_type", y="bookmarks", hue="price_range", data=openrice)#barplot
sns.lmplot(x="likes", y="bookmarks",data=openrice) #lineplot

#regplot on specific data
sns.regplot( x='likes',y='bookmarks'  ,data= openrice[openrice["likes"] < 200])


#plotting two plots next to each other
fig,axs = plt.subplots(2,1)

sns.pointplot(ax=axs[0], x="food_type",y="bookmarks", hue="price_range",data=dataframe,palette='Set1')
sns.pointplot(ax=axs[1], x="food_type",y="likes", hue="price_range",data=dataframe,palette='Set1')


#important plotly definitions
import cufflinks as cf #integrates plotly with python
import plotly
import plotly.offline as py
import plotly.graph_objs as go

cf.go_offline()# to be able to use plotly without logging in

#actual definitions for plotting data
data= go.Data([
            go.Bar(
              y = ydatacolumn,
              x = xdatacolumn,
              orientation='h'# orientation horizontal or vertical
        )])
layout = go.Layout(
        height = '1000',
        margin=go.Margin(l=300),
        title = "Chart Title"
)

# setting the figure to what needs to be plotted
fig  = go.Figure(data=data, layout=layout)

#actually plotting it
py.iplot(fig)

#plotting it to a file
py.plot(fig, filename = 'trial1.html')