import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np

N = 100
random_x = np.linspace(0, 1, N)
random_y0 = np.random.randn(N) + 5
random_y1 = np.random.randn(N)
random_y2 = np.random.randn(N) - 5

# Create traces
trace0 = go.Scatter(
    x=random_x,
    y=random_y0,
    mode='lines',
    name='lines'
)

trace1 = go.Scatter(
    x=random_x,
    y=random_y1,
    mode='lines+markers',
    name='lines+markers'
)

trace2 = go.Scatter(
    x=random_x,
    y=random_y2,
    mode='markers',
    name='markers'
)

data = [trace0, trace1, trace2]

layout = go.Layout(
    width=600,
    height=600
)

fig = go.Figure(data=data, layout=layout)

py.iplot(fig, filename='line-mode')
