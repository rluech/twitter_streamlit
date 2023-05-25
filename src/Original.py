# Standard imports
import pandas as pd

# matplotlib
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
#plotly
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

#textblob
from textblob import TextBlob

#wordcloud
from wordcloud import WordCloud, STOPWORDS
import streamlit as st

####load the data ####
@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    return df
dfBO = load_data("data/BarackObama_tweet_data.csv")
dfBG = load_data("data/BillGates_tweet_data.csv")
dfEM = load_data("data/elonmusk_tweet_data.csv")
dfJB = load_data("data/JeffBezos_tweet_data.csv")
df_stat = load_data("data/user_stats.csv")
#dfWB = load_data("data/WarrenBuffett_tweet_data.csv")
##create dictionary of data frames
df_list = [dfBO, dfBG,dfEM, dfJB]
for df in df_list:
    df['created_at'] =  pd.to_datetime(df['created_at'])
    df['YY-MM'] = df['created_at'].dt.strftime('%Y-%m')
    df['polarity'] = df.apply(lambda row: TextBlob(row['text']).sentiment.polarity,1)
    df['subjectivity'] = df.apply(lambda row: TextBlob(row['text']).sentiment.subjectivity,1)

############################# Title & intro ################    
    
st.title("Twitter Celebrities")
st.header("**header**")
if st.checkbox("Who are they?"):
        st.subheader("General statistics")
        st.dataframe(data=df_stat)
        
swit = {"LetzteGeneration": 45515,
"PlayStationShowcase": 143929,
"CoppaItalia": 11646}
Ger = {"LetzteGeneration": 45590, "TinaTurner": 142759, "PlayStationShowcase": 143929}
US = {"PumpRules": 35705, "Survivor": 27823, "DeSaster": 46424, "TimeToHunt": 14424}
data_trends = {" United States": ["#PumpRules", "#TimeToHunt", "#DeSaster"], 'Switzerland': ["#LetzteGeneration", "#PlayStationShowcase", "#CoppaItalia"],"Germany":["#LetzteGeneration", "#PlayStationShowcase","#TinaTurner"]}

if st.checkbox("Trends"):
        st.dataframe(data=pd.DataFrame(data_trends))




st.subheader("tweets timeseries - compare your fav cel")
############# Giving some options ############################
BO = False
BG = False
EM = False
JB = False
st.subheader("Choose your fav./s:")
# Setting up columns
left_column, middle_column, right_column = st.columns([1, 1, 1])

if left_column.checkbox("All"):
    BO = True
    BG = True
    EM = True
    JB = True
if middle_column.checkbox("Barack Obama"):
    BO = True
if right_column.checkbox("Bill Gates"):
    BG = True
if left_column.checkbox("Elon Musk"):
    EM = True 
if middle_column.checkbox("Jeff Bezos"):
    JB = True 

########################### FIG 1 ##############################
  
#####
fig = go.Figure()
if BO == True:
        x_time= dfBO['YY-MM'].copy().unique()
        x_time.sort()
        fig.add_trace(go.Scatter(x = x_time, y = dfBO.groupby('YY-MM').created_at.count(), mode='lines',name = 'Barack Obama', hovertemplate=
         #   "<b>%{text}</b><br><br>" +
                "name: Barack Obama <br>"+
            "month: %{x}<br>\n" +
            "Total number of tweets: %{y}<br>" +
            #"Hashtag : %{marker.size:,}" +
            "<extra></extra>" ))
if BG == True:
        x_time= dfBG['YY-MM'].copy().unique()
        x_time.sort()
        fig.add_trace(go.Scatter(x = x_time, y = dfBG.groupby('YY-MM').created_at.count(), mode='lines',name = 'Bill Gates', hovertemplate=
         #   "<b>%{text}</b><br><br>" +
                "name: Bill Gates<br>"+
            "month: %{x}<br>" +
            "Total number of tweets: %{y}<br>" +
            #"Hashtag : %{marker.size:,}" +
            "<extra></extra>" ))
if EM == True:
        x_time= dfEM['YY-MM'].copy().unique()
        x_time.sort()
        fig.add_trace(go.Scatter(x = x_time, y = dfEM.groupby('YY-MM').created_at.count(), mode='lines',name = 'Elon Musk', hovertemplate=
         #   "<b>%{text}</b><br><br>" +
                "name: Elon Musk<br>"+
            "month: %{x}<br>" +
            "Total number of tweets: %{y}<br>" +
            #"Hashtag : %{marker.size:,}" +
            "<extra></extra>" ))
if JB == True:
        x_time= dfJB['YY-MM'].copy().unique()
        x_time.sort()
        fig.add_trace(go.Scatter(x = x_time, y = dfJB.groupby('YY-MM').created_at.count(), mode='lines',name = 'Jeff Bezos',hovertemplate=
         #   "<b>%{text}</b><br><br>" +
                "name: Jeff Bezos<br>"+
            "month: %{x}<br>" +
            "Total number of tweets: %{y}<br>" +
            #"Hashtag : %{marker.size:,}" +
            "<extra></extra>"))
fig.update_layout(
    title={"text": "tweets timeseries - compare your fav cel", "font": {"size": 26}},
    xaxis={"title": {"text": "Time", "font": {"size": 16}}},
    yaxis={"title": {"text": "number of tweets", "font": {"size": 16}}},
    paper_bgcolor='rgb(254, 246, 224)',
    plot_bgcolor='rgb(254, 246, 224)',
    #hovermode="x unified",
)
    
st.plotly_chart(fig)
################################# Hashtag ###############################
def hashtags_time(df,Y_M):
    hashtags_Y_M = []
    for hashtag in df[df['YY-MM'] == Y_M]['hashtags']:
        if hashtag !="[]":
            if hashtag not in hashtags_Y_M:
                hashtags_Y_M.append(eval(hashtag))
    return hashtags_Y_M


if BO == True:
        x_time= dfBO['YY-MM'].copy().unique()
        x_time.sort()
        Time = x_time
        exact_BO = st.selectbox("choose a Year", x_time)
        Y = hashtags_time(dfBO,exact_BO)
        list_hash = []
        for list_ in Y:
            for string_ in list_:
                list_hash.append(string_)
        st.text("Hashtages by B.O.  used at that time: " +str(set(list_hash)))
if BG == True:
        x_time= dfBG['YY-MM'].copy().unique()
        x_time.sort()
        Time = x_time
        exact_BG = st.selectbox("choose a Year", x_time)
        Y = hashtags_time(dfBG,exact_BG)
        list_hash = []
        for list_ in Y:
            for string_ in list_:
                list_hash.append(string_)
        st.text("Hashtages by B.G.  used at that time: " +str(set(list_hash)))
if EM == True:
        x_time= dfEM['YY-MM'].copy().unique()
        x_time.sort()
        Time = x_time
        exact_EM = st.selectbox("choose a Year", x_time)
        Y = hashtags_time(dfEM,exact_EM)
        list_hash = []
        for list_ in Y:
            for string_ in list_:
                list_hash.append(string_)
        st.text("Hashtages by E.M.  used at that time: " +str(set(list_hash)))
if JB == True:
        x_time= dfJB['YY-MM'].copy().unique()
        x_time.sort()
        Time = x_time
        exact_JB = st.selectbox("choose a Year", x_time)
        Y = hashtags_time(dfJB,exact_JB)
        list_hash = []
        for list_ in Y:
            for string_ in list_:
                list_hash.append(string_)
        st.text("Hashtages by J.B.  used at that time: " +str(set(list_hash)))
        
        
        
############################### Fig 2 #######################
st.subheader("wordcloud-text or mentions")

# Setting up columns
left_column, middle_column, right_column = st.columns([1, 0.1, 1])
crs = ['text','mentions']
cr = left_column.radio("Choose a crieteria ", crs)
data = ['Barack Obama','Bill Gates','Elon Musk','Jeff Bezos' ]
name = right_column.radio("Choose your fav", data)

def tweets_wordcloud_plot(data, column = ['text','mentions'][0]):
    
    # 'data' is one of the dataframes dfBO, dfBG, ..., etc.
    # 'column' is the columnname for which we plot the wordcloud, default is 'text'
    
    # preprocess text, slightly different depending which column we choose
    if column == 'text':
        words = ' '.join(data[column]).lower()
        words = [i for i in words.split() if len(i) > 2]
        words = [i for i in words if not i.startswith('http')]
        words = ' '.join(words)
    
    if column == 'mentions':
        words = []
        for i in data[column]:
            words.extend(eval(i))
        words = ' '.join(words).lower()
    
    # create wordcloud 
    wordcloud = WordCloud(
        width = 800, height = 800,
        background_color ='white',
        stopwords = set(STOPWORDS),
        min_font_size = 10
    ).generate(words)
    
    # plot the WordCloud image
    plt.figure(figsize = (8, 8), facecolor = None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad = 0)
    plt.show()

    st.set_option('deprecation.showPyplotGlobalUse', False)

    st.pyplot()

name_df = {'Barack Obama': dfBO, 'Bill Gates': dfBG,'Elon Musk': dfEM, 'Jeff Bezos': dfJB}
tweets_wordcloud_plot(name_df[name], cr)
    
    
    


############################# Fig 3 #########################
st.subheader('compare people integration rate')



############################ Fig 4 #################
st.subheader('Sentiment. over time')
#st.subheader('polarity-subjectivity')
############# Giving some options ############################
BO_ = False
BG_ = False
EM_ = False
JB_ = False
st.subheader("Choose your fav./s:")
# Setting up columns
left_column, middle_column, right_column = st.columns([1, 1, 1])

if left_column.checkbox("_All_"):
    BO_ = True
    BG_ = True
    EM_ = True
    JB_ = True
if middle_column.checkbox("_Barack Obama_"):
    BO_ = True
if right_column.checkbox("_Bill Gates_"):
    BG_ = True
if left_column.checkbox("_Elon Musk_"):
    EM_ = True 
if middle_column.checkbox("_Jeff Bezos_"):
    JB_ = True 

########################### FIG 1 ##############################
  
fig2 = go.Figure()
if BO_ == True:
        x_time= dfBO['YY-MM'].copy().unique()
        x_time.sort()
        fig2.add_trace(go.Scatter(x = x_time, y = dfBO.groupby('YY-MM').polarity.mean(), mode='lines',name = 'Barack Obama', hovertemplate=
         #   "<b>%{text}</b><br><br>" +
                "name: Barack Obama <br>"+
            "month: %{x}<br>\n" +
            "avg. polarity: %{y}<br>" +
            #"Hashtag : %{marker.size:,}" +
            "<extra></extra>" ))
if BG_ == True:
        x_time= dfBG['YY-MM'].copy().unique()
        x_time.sort()
        fig2.add_trace(go.Scatter(x = x_time, y = dfBG.groupby('YY-MM').polarity.mean(), mode='lines',name = 'Bill Gates', hovertemplate=
         #   "<b>%{text}</b><br><br>" +
                "name: Bill Gates<br>"+
            "month: %{x}<br>" +
            "avg. polarity: %{y}<br>" +
            #"Hashtag : %{marker.size:,}" +
            "<extra></extra>" ))
if EM_ == True:
        x_time= dfEM['YY-MM'].copy().unique()
        x_time.sort()
        fig2.add_trace(go.Scatter(x = x_time, y = dfEM.groupby('YY-MM').polarity.mean(), mode='lines',name = 'Elon Musk', hovertemplate=
         #   "<b>%{text}</b><br><br>" +
                "name: Elon Musk<br>"+
            "month: %{x}<br>" +
            "avg. polarity: %{y}<br>" +
            #"Hashtag : %{marker.size:,}" +
            "<extra></extra>" ))
if JB_ == True:
        x_time= dfJB['YY-MM'].copy().unique()
        x_time.sort()
        fig2.add_trace(go.Scatter(x = x_time, y = dfJB.groupby('YY-MM').polarity.mean(), mode='lines',name = 'Jeff Bezos',hovertemplate=
         #   "<b>%{text}</b><br><br>" +
                "name: Jeff Bezos<br>"+
            "month: %{x}<br>" +
            "avg. polarity: %{y}<br>" +
            #"Hashtag : %{marker.size:,}" +
            "<extra></extra>"))
fig2.update_layout(
    title={"text": "Sentiment timeseries ", "font": {"size": 26}},
    xaxis={"title": {"text": "Time", "font": {"size": 16}}},
    yaxis={"title": {"text": "Avg. polarity per month", "font": {"size": 16}}},
    paper_bgcolor='rgb(254, 246, 224)',
    plot_bgcolor='rgb(254, 246, 224)',
    #hovermode="x unified",
)

    
st.plotly_chart(fig2)

######################### Fig 3 #############################
   
fig3 = go.Figure()
if BO_ == True:
        x_time= dfBO['YY-MM'].copy().unique()
        x_time.sort()
        fig3.add_trace(go.Scatter(x =dfBO["subjectivity"], y = dfBO['polarity'], mode='markers',name = 'Barack Obama', hovertemplate=
         #   "<b>%{text}</b><br><br>" +
                "name: Barack Obama <br>"+
            "month: %{x}<br>\n" +
            "avg. polarity: %{y}<br>" +
            #"Hashtag : %{marker.size:,}" +
            "<extra></extra>" ))
if BG_ == True:
        x_time= dfBG['YY-MM'].copy().unique()
        x_time.sort()
        fig2.add_trace(go.Scatter(x =dfBG["subjectivity"], y = dfBG['polarity'], mode='markers',name = 'Bill Gates', hovertemplate=
         #   "<b>%{text}</b><br><br>" +
                "name: Bill Gates<br>"+
            "month: %{x}<br>" +
            "avg. polarity: %{y}<br>" +
            #"Hashtag : %{marker.size:,}" +
            "<extra></extra>" ))
if EM_ == True:
        x_time= dfEM['YY-MM'].copy().unique()
        x_time.sort()
        fig3.add_trace(go.Scatter(x = dfEM["subjectivity"], y = dfEM['polarity'], mode='markers',name = 'Elon Musk', hovertemplate=
         #   "<b>%{text}</b><br><br>" +
                "name: Elon Musk<br>"+
            "month: %{x}<br>" +
            "avg. polarity: %{y}<br>" +
            #"Hashtag : %{marker.size:,}" +
            "<extra></extra>" ))
if JB_ == True:
        x_time= dfJB['YY-MM'].copy().unique()
        x_time.sort()
        fig3.add_trace(go.Scatter(x =dfJB["subjectivity"], y = dfJB['polarity'], mode='markers',name = 'Jeff Bezos',hovertemplate=
         #   "<b>%{text}</b><br><br>" +
                "name: Jeff Bezos<br>"+
            "month: %{x}<br>" +
            "avg. polarity: %{y}<br>" +
            #"Hashtag : %{marker.size:,}" +
            "<extra></extra>"))
fig3.update_layout(
    title={"text": "Polarity vs. Subjectivity ", "font": {"size": 26}},
    xaxis={"title": {"text": "subjectivity", "font": {"size": 16}}},
    yaxis={"title": {"text": "polarity", "font": {"size": 16}}},
    paper_bgcolor='rgb(254, 246, 224)',
    plot_bgcolor='rgb(254, 246, 224)',
    #hovermode="x unified",
)

    
st.plotly_chart(fig3)

