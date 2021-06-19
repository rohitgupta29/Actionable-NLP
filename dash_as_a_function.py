import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.express as px
import pandas as pd
from wordcloud import STOPWORDS
from src.plt_wordcloud import wordcloud_by_tweets

from src.db_utils import read_name_sentiment_add_pattern
df = read_name_sentiment_add_pattern()

from src.db_utils import read_name_tweet_ner_key_phrase
df_tweets = read_name_tweet_ner_key_phrase()

from src.db_utils import read_tweet_features_on_sentiment_type as df_divide
df_positive,df_negative = df_divide()

# df_tweets=df_tweets.fillna("no tweet today")
STOPWORDS = ["https", "co", "RT","S","LA","T","ALWAYS"] + list(STOPWORDS)

import matplotlib.pyplot as plt
#wordcloud
word_cloud_overall = wordcloud_by_tweets(df_tweets['tweet'],"Sentiment")
word_cloud_positive = wordcloud_by_tweets(df_positive['tweet'],"Positive")
word_cloud_negative = wordcloud_by_tweets(df_negative['tweet'],"Positive")

#Heatmap
employees = df['name'].iloc[:10].to_list()
tweet = ["Latest Tweet",2,3,4,5,6,7,8,9,"10th"]
data_heatmap = df['twitter_sentiment_pattern'].iloc[:10].apply(eval).to_list()

fig_heatmap = px.imshow(data_heatmap,
                color_continuous_scale=px.colors.sequential.Emrld,
                title = "10 tweet sentiment pattern",
                labels = dict(x = "Tweet index", y = "Names"),
                x= tweet,
                y = employees)
fig_heatmap.update_xaxes(side= "top")

#for pie chart
try:
    df["sentiment_binary"] = df["tweet_sentiment"].apply(lambda x: "negative" if x < 0 else "positive")
    day_sentiment_counts = df['sentiment_binary'].value_counts()

    # # pie chart
    fig_pie = px.pie(names = day_sentiment_counts.index,values = day_sentiment_counts.values,color = day_sentiment_counts.index, hole = 0.5)
    fig_pie.update_traces(textinfo="label + percent",insidetextfont =dict(color = "white") )
    fig_pie.update_layout(legend= {"itemclick":False})
except Exception as e:
    print("please add data")

#bar graph_overall
fig_bar = px.bar(
    data_frame= df,
    x = 'name',
    y = 'tweet_sentiment',
    opacity= 0.9,
    orientation="v",
    barmode= 'relative',
    title="Updated Tweet Sentiment"
)

#Bar graph for negative tweets
# Filter by Sentiment

sentiment_selection_negative = (-40,-1)
sentiment_selection_positive = (1,50)
mask_positive = df["tweet_sentiment"].between(*sentiment_selection_positive)
mask_negative = df["tweet_sentiment"].between(*sentiment_selection_negative)
df_attend_negative = df[mask_negative]
df_attend_positive = df[mask_positive]
# print(df[mask].columns)
#
bar_negative = px.bar(df_attend_negative[['name','tweet_sentiment']],
                   x = 'name',
                   y = 'tweet_sentiment',
                   text = 'tweet_sentiment',
                   color_discrete_sequence= ['#F63366']*len(df_attend_negative),
                   template= 'plotly_white'
                   )

bar_positive = px.bar(df_attend_positive[['name','tweet_sentiment']],
                   x = 'name',
                   y = 'tweet_sentiment',
                   text = 'tweet_sentiment',
                   color_discrete_sequence= ['#F63366']*len(df_attend_positive),
                   template= 'plotly_white'
                   )

# df_chart_summary
df_tweets_summary = df_tweets[["id","name","tweet_sentiment","rcsa","tweet"]]


app = dash.Dash(__name__)


def create_dash_application(flask_app):
    dash_app = dash.Dash(
        server=flask_app,name="Dashboard",
        url_base_pathname='/dash/')

    dash_app.layout = html.Div(children=[
        #1- Bar
        html.Div([
            html.H1(children="Sentiments of the Tweets today"),

            html.Div(children="""
            The pattern will tell us about how these twitter users feel today.
            """),

            dcc.Graph(
                id='graph1',
                figure=fig_bar
            )
        ]),

        # 2 Pie
        html.Div([
            html.H1(children="Today's Overall sentiments"),
            html.Div(children="""
            The Pie Chart
            """),

            dcc.Graph(
                id='graph2',
                figure=fig_pie
            ),
        ]),
        # 3. WordCloud
        html.Div([
            html.H1(children="Significant words used in the Overall Tweets"),
            html.Div(
                children=[html.Img(src="data:image/png;base64," + word_cloud_overall,
                                   style={'height': '50%', 'width': '50%'})])
        ]),
        #4. Heatmap
        html.Div([
            html.H1(children="Heatmap of Twitter users vs type of sentiment"),
            html.Div(children="""
            Insights on tweets with positive and negative sentiment
            """),

            dcc.Graph(
                id='graph3',
                figure=fig_heatmap
            ),
        ]),
        # 5. Positive Bar
        html.Div([
            html.H1(children="Pattern of Positive Tweets"),

            html.Div(children="""
                    The pattern will tell us about the positive sentiments today.
                    """),

            dcc.Graph(
                id='graph5',
                figure=bar_positive
            )
        ]),
        # 6. Positive WordCloud
        html.Div([
            html.H1(children="Words people use for their Tweets being positive"),
            html.Div(
                children=[html.Img(src="data:image/png;base64," + word_cloud_positive,
                                   style={'height': '50%', 'width': '50%'})])
        ]),
        # 7.Negative Tweets
        html.Div([
            html.H1(children="Negative Tweet Sentiment"),

            html.Div(children="""
                It tells us who don't feel much good today about somthing.
                """),

            dcc.Graph(
                id='graph4',
                figure=bar_negative
            )
        ]),
        # 8. Negative WordCloud
        html.Div([
            html.H1(children="Words people express to show their negative sentiment about somthing."),
            html.Div(
                children=[html.Img(src="data:image/png;base64," + word_cloud_negative, style={'height': '50%', 'width': '50%'})])
        ]),
        html.Div([
            html.H1(children="OverAll Summary of Tweets"),
            html.Div(children=
                        dash_table.DataTable(
                            id='table',
                            columns=[{"name":i,"id":i} for i in df_tweets_summary.columns],
                            data=df_tweets_summary.to_dict('records'),
                            style_header={'backgroundColor': 'rgb(30, 30, 30)'},
                            style_cell={
                            'backgroundColor': 'rgb(50, 50, 50)',
                            'color': 'white'
                            },))

        ])
        ])


    return dash_app


# for staked bar graph - https://stackoverflow.com/questions/65306294/pandas-stacked-bar-chart-of-a-column-of-dictionaries-of-key-and-values
# https://plotly.com/python/bar-charts/


# for dataframe styling - https://www.youtube.com/watch?v=twHtUFR7rtw
