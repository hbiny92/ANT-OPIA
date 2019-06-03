import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import *
import plotly.offline as offline
import plotly
from plotly import tools


d = {'POS': 0.44911800810700564, 'NEG': 0.42160036321757527,
     'NEUT': 0.043949363187391406, 'COMP': 0.0, 'None': 0.0853322654880278}
newdf = pd.DataFrame.from_dict(d, orient='index')
newdf.reset_index(inplace=True)
newdf.columns = ['sentiment', 'score']
print(newdf, '\n')

print(newdf[:1], '\n')
print(newdf.sentiment, '\n')  # 감성표현 열 출력
print(newdf.score, '\n')  # 스코어 열 출력
print(newdf.iloc[0]['score'])

fig = {
    "data": [
      {
          "values": [newdf.iloc[0]['score'],
                     newdf.iloc[1]['score'],
                     newdf.iloc[2]['score'],
                     newdf.iloc[3]['score'],
                     newdf.iloc[4]['score']],
          "labels": [
              "Postive", "Negative", "Neutral", "Composite", "None"
          ],
          "domain": {"x": [0.6, .4]},
          "name":"tendency",
          "hoverinfo": "label+percent+name",
          "hole": .4,
          "type": "pie"
      }],
    "layout": {
        "annotations": [
            {
                "font": {
                    "size": 25},
                "showarrow": False,
                "text": "감성지수",
                "x": 0.5,
                "y": 0.5
            },

        ]
    }
}
plotly.offline.plot(fig)
