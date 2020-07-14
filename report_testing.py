#! python3

#TODO:
# work on applying the aggregation functions to the dataframe
# place this all in a function call

import sqlite3
import AHutils
import plotly.express as px
import plotly.graph_objects as go
import pandas
import math

#Connect to SQLite DB
print("Connecting to SQLite database...")
conn = sqlite3.connect('Data/Database/wowAH.db')
c = conn.cursor()



df = pandas.read_sql_query(AHutils.db_Query_ItemSummary(conn, 'Formula: Enchant Cloak - Greater Resistance'), conn)

#add weighted rolling average
#probably want to turn this into a function
#i believe this calculation is wrong, need to check
weightedRollingAvg = []
if len(df["MinBuy"]) >=5:
    for i in range(0,4):
        weightedRollingAvg.append(None)
    for i in range(4,len(df["MinBuy"])):
        MovAvg = 0
        MovAvg = MovAvg + df["MinBuy"][i] * 5
        MovAvg = MovAvg + df["MinBuy"][i-1] * 4
        MovAvg = MovAvg + df["MinBuy"][i-2] * 3
        MovAvg = MovAvg + df["MinBuy"][i-3] * 2
        MovAvg = MovAvg + df["MinBuy"][i-4]
        MovAvg = int(round(MovAvg/(5+4+3+2)))
        weightedRollingAvg.append(MovAvg)
df["WMA"] = weightedRollingAvg


# Percent Change since beginning of dataframe
begVal = df["MinBuy"][0]
PercentChange = []
if len(df["MinBuy"]) >=1:
    for i in range(0,len(df["MinBuy"])):
        tempVal = 0.0
        tempVal = round((df["MinBuy"][i] - begVal)/begVal, 4)*100
        PercentChange.append(tempVal)
df["Delta"] = PercentChange



#percent change from prior day
begVal = df["MinBuy"][0]
DailyPercentChange = []
if len(df["MinBuy"]) >= 1:
    DailyPercentChange.append(0.0)
    for i in range(1,len(df["MinBuy"])):
        tempVal = 0.0
        tempVal = round((df["MinBuy"][i] - df["MinBuy"][i-1])/df["MinBuy"][i-1], 4)*100
        DailyPercentChange.append(tempVal)
df["DailyDelta"] = DailyPercentChange
#print(len(PercentChange))
print(df)



fig = px.line(df, x="Date", y="WMA", color = "Item", title='Minimum Price')


fig.for_each_trace(
    lambda trace: trace.update(name=trace.name.replace("Item=", "")),
)

fig.show()


from plotly.subplots import make_subplots

# Create figure with secondary y-axis
fig2 = make_subplots(specs=[[{"secondary_y": True}]])

fig2.add_trace(
    go.Bar(x = df["Date"], y = df["Volume"], name = 'Volume'),
    secondary_y = False
)

fig2.add_trace(
    go.Scatter(x = df["Date"], y = df["Delta"], name = 'Delta'),
    secondary_y = True
)


fig.update_layout(
    title_text="% Change and Volume"
)
# Set x-axis title
fig.update_xaxes(title_text="Date")

# Set y-axes titles
fig.update_yaxes(title_text="<b>primary</b> yaxis title", secondary_y=False)
fig.update_yaxes(title_text="<b>secondary</b> yaxis title", secondary_y=True)

fig2.show()


c.close()
conn.close()




