import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import statsmodels.api as sm

app = dash.Dash()

colors = dict(
    pace='#D9437D',
    spin='#367D9F',
    over_line='#888886'
)

# Data
df = pd.read_csv('../usmaan_test_data.csv')

# add count of delivery number
df['deliv'] = [n + 1 for n in range(len(df))]

# drop null bounces
df = df.dropna(subset=['bvrz']).copy()

# bvrz values
pace_bvrz_values = df.bvrz[df.pace == 1]
spin_bvrz_values = df.bvrz[df.pace == 0]

# value counts
pace_deliv_values = df.deliv[df.pace == 1]
spin_deliv_values = df.deliv[df.pace == 0]

# local regression using LOWESS
lowess = sm.nonparametric.lowess

pace_regression_x = lowess(pace_bvrz_values, pace_deliv_values)[:, 0]
pace_regression_y = lowess(pace_bvrz_values, pace_deliv_values)[:, 1]

spin_regression_x = lowess(spin_bvrz_values, spin_deliv_values)[:, 0]
spin_regression_y = lowess(spin_bvrz_values, spin_deliv_values)[:, 1]

# pace scatter plot values
trace1 = go.Scatter(
    x=pace_deliv_values,
    y=pace_bvrz_values,
    mode='markers',
    marker=dict(
        color=colors['pace'],
    ),
    opacity=0.3,
    name='pace'
)

# pace regression line
trace2 = go.Scatter(
    x=pace_regression_x,
    y=pace_regression_y,
    line=dict(
        width=4
    ),
    marker=dict(
        color=colors['pace']
    ),
    hoverinfo='none',
    showlegend=False
)

# spin scatter plot values
trace3 = go.Scatter(
    x=spin_deliv_values,
    y=spin_bvrz_values,
    mode='markers',
    marker=dict(
        color=colors['spin']
    ),
    opacity=0.3,
    name='spin'
)

# spin regression line
trace4 = go.Scatter(
    x=spin_regression_x,
    y=spin_regression_y,
    line=dict(
        width=4
    ),
    marker=dict(
        color=colors['spin']
    ),
    hoverinfo='none',
    showlegend=False
)

app.layout = html.Div(style={}, children=[
    html.H1(
        children='Cricviz Demo App',
        style={
            'textAlign': 'center'
        }
    ),

    html.Div(children='Bounce Velocity Ratio to Match Delivery Number', style={
        'textAlign': 'center'
    }),

    dcc.Graph(
        id='example-graph-2',
        figure={
            'data': [trace1, trace2, trace3, trace4],
            'layout': go.Layout(
                xaxis=dict(
                    title='Match Delivery',
                    autotick=False,
                    zeroline=False,
                    tick0=0,
                    dtick=200,
                ),
                yaxis=dict(
                    title='Bounce Velocity Ratio',
                    range=[0.38, 0.75]
                ),
                shapes=[
                    {
                        'type': 'line',
                        'x0': 800,
                        'y0': 0.4,
                        'x1': 800,
                        'y1': 0.8,
                        'line': {
                            'width': 1,
                            'color': colors['over_line']
                        }
                    },
                    {
                        'type': 'line',
                        'x0': 1100,
                        'y0': 0.4,
                        'x1': 1100,
                        'y1': 0.8,
                        'line': {
                            'width': 1,
                            'color': colors['over_line']
                        }
                    }
                ]
            )
        }
    )
])

# NOTE:
#       - layout is composed of a tree of "components" like html.Div
#       - dash_html_components provides html.H! -> <h1>...</h1> etc..
#       - can generate components with html/css/js with interactivity
#       - applications are described via keyword attributes
#       - peep the children property html.H1(children=...) == html.H1(...)

# * More about HTML
# - dash_html_components -> component class for every HTML tag
#                           keyword argument for all HTML arguments

# - html.H1('Hello Dash', style={'textAlign': 'center', 'color': '#7FDFF'})
#   becomes
#   <h1 style="text-align: center; color: #7FDFF">Hello Dash</h1>

if __name__ == '__main__':
    app.run_server(debug=True)
