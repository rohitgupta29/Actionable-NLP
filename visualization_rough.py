# Bar, Heatmap and pie chart

import matplotlib.pyplot as plt
import plotly.express as px
#pie chart
"""df with name, id, sentiment.
use pie chart."""
from db_utils import read_name_sentiment_add_pattern
df = read_name_sentiment_add_pattern()
# print(df)
# df["sentiment_binary"] = df["tweet_sentiment"].apply(lambda x: 0 if x < 0 else 1)
# print(df["sentiment_binary"].value_counts())
# print(df['sentiment_pattern'])
# print(df["twitter_sentiment_pattern"].head())

# def pie_chart():
#     fig = plt.figure(figsize = (10,7))
#     plt.pie(df["sentiment_binary"].value_counts(), labels = ["Positive","Negative"])
#     plt.show()
#
# print(pie_chart())



# import plotly.express as px
# import pandas as pd
# fig = px.bar(df,x = "name", y = "sentiment_binary", title = "graph" )
# fig.show()
#
#
# data = df['sentiment_today'].apply(lambda x: int(x))
# data_list = data.to_list()



#
# def show_sentiment_today():
#     import matplotlib.pyplot as plt;
#     plt.rcdefaults()
#     import numpy as np
#
#     objects = df['name'].to_list()
#     y_pos = np.arange(len(objects))
#     performance = df["sentiment_today"].apply(lambda x: int(x)).to_list()[:6]
#
#     plt.bar(y_pos, performance, align='center', alpha=0.5)
#     plt.xticks(y_pos, objects)
#     plt.ylabel('Polarity')
#     plt.title('Tweet Sentiments Today')
#     plt.show()

# show_sentiment_today()
#
# def show_sentiment_today_fancy():
#     import matplotlib.pyplot as plt
#     plt.rcdefaults()
#     import numpy as np
#
#     objects = df['name'].to_list()
#     y_pos = np.arange(len(objects))
#     performance = df["sentiment_today"].apply(lambda x: int(x)).to_list()[:6]
#
#     plt.bar(y_pos, performance, align='center', alpha=0.5)
#     # Get the axes object
#     ax = plt.gca()
#     # remove the existing ticklabels
#     ax.set_xticklabels([])
#     # remove the extra tick on the negative bar
#     ax.set_xticks([idx for (idx, x) in enumerate(performance) if x > 0])
#     ax.spines["bottom"].set_position(("data", 0))
#     ax.spines["top"].set_visible(False)
#     ax.spines["right"].set_visible(False)
#     # placing each of the x-axis labels individually
#     label_offset = 0.5
#     for language, (x_position, y_position) in zip(objects, enumerate(performance)):
#         if y_position > 0:
#             label_y = -label_offset
#         else:
#             label_y = y_position - label_offset
#         ax.text(x_position, label_y, language, ha="center", va="top")
#     # Placing the x-axis label, note the transformation into `Axes` co-ordinates
#     # previously data co-ordinates for the x ticklabels
#     ax.text(0.5, -0.05, "Names", ha="center", va="top", transform=ax.transAxes)
#
#     plt.show()
#
# show_sentiment_today_fancy()


#
# import matplotlib.pyplot as plt
import numpy as np
#https://towardsdatascience.com/dealing-with-list-values-in-pandas-dataframes-a177e534f173

# def clean_alt_list(list_):
#     list_ = list_.replace(', ', '","')
#     list_ = list_.replace('[', '["')
#     list_ = list_.replace(']', '"]')
#     return list_
#
# employees = df['name'].to_list()
# tweet = ["Latest Tweet",2,3,4,5,6,7,8,9,10,11,12,13,14,"15th"]
#
#
# def heatmap_2d():
# data = df['twitter_sentiment_pattern'].apply(eval).to_list()
# print(data)
# data = data.iloc[:10].apply(eval).to_list()
# fig,ax = plt.subplots()
# ax.imshow(data, cmap = "autumn", interpolation='nearest')
# ax.set_xticks(np.arange(len(tweet)))
# ax.set_yticks(np.arange(len(employees)))
# #
# ax.set_xticklabels(tweet)
# ax.set_yticklabels(employees)
#
# # Rotate the tick labels and set their alignment.
# plt.setp(ax.get_xticklabels(), rotation=60,ha="right",
#         rotation_mode="anchor")
#
# plt.title("Sentiment Pattern of tweets over 15 Days")
# plt.show()

# heatmap_2d()
# plt.savefig("Heatmap.jpg")
# # # #
# #
# # # References -
# # # https://matplotlib.org/stable/gallery/images_contours_and_fields/image_annotated_heatmap.html
# # #https://towardsdatascience.com/dealing-with-list-values-in-pandas-dataframes-a177e534f173
#
# if __name__ == "__main__":
#     print(show_sentiment_today_fancy())


# # Filter by Sentiment
# sentiment_selection = (-40,-1)
# mask = df["tweet_sentiment"].between(*sentiment_selection)
# df_attend =  df[mask]
# print(df[mask].columns)



#
# bar_chart = px.bar(df_attend[['name','tweet_sentiment']],
#                    x = 'name',
#                    y = 'tweet_sentiment',
#                    text = 'tweet_sentiment',
#                    color_discrete_sequence= ['#F63366']*len(df_attend),
#                    template= 'plotly_white'
#                    )
# bar_chart.show()
