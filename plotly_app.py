import sqlite3

import numpy
import plotly
import plotly.graph_objs as go

con = sqlite3.connect("c:\\Users\\GOD\\Desktop\\AnalysisOfGraphs\\db\\mydatabase.db")

myPair = 'GBP_USD_M5'
count_orders_and_persent = []
DATA = []
with con:
    cur = con.cursor()
    cur.execute("SELECT * FROM USD_CHF_D1")
    rows = cur.fetchall()

    for row in rows:
        DATA.append([row[0], row[1], row[2]])
        count_orders_and_persent.append('count orders: ' + str(row[3]) + '\n\r' +'count_profit_perset_of_all_points: ' + str(row[2]/(row[4]-row[5])))


DATA = numpy.array(DATA)

Xs = DATA[:, 0]
Ys = DATA[:, 1]
Zs = DATA[:, 2]

trace1 = go.Scatter3d(
    x=Xs,
    y=Ys,
    z=Zs,
    text = count_orders_and_persent,
    mode='markers',
    marker=dict(
        line=dict(width=1),
        size=5,
        color=Zs,
        colorscale='Jet',
        #opacity=0.8
    )
)

data = [trace1]
layout = go.Layout(
    margin=dict(
        l=0,
        r=0,
        b=0,
        t=0
    )
)
fig = go.Figure(data=data, layout=layout)
plotly.offline.plot(fig, filename='USD_CHF_D1.html')
