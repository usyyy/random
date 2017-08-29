import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
from scipy import stats

app = dash.Dash()

app.css.append_css(
    {"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

# Data 
df = pd.read_csv('../usmaan_test_data.csv')

# add count of delivery number
df['deliv'] = [n + 1 for n in range(len(df))]

# drop null bounces
df = df.dropna(subset=['bvrz']).copy()
df.head()

# bvrz values
pace_bvrz_values = df.bvrz[df.pace == 1]
pace_bvrz_values.head(2)
spin_bvrz_values = df.bvrz[df.pace == 0]
spin_bvrz_values.head(2)

# value counts
pace_deliv_values = df.deliv[df.pace == 1]
spin_deliv_values = df.deliv[df.pace == 0]

# regression values
pace_slope, pace_intercept, pace_r_value, pace_p_value, pace_std_err = stats.linregress(
    pace_deliv_values, pace_bvrz_values)

spin_slope, spin_intercept, spin_r_value, spin_p_value, spin_std_err = stats.linregress(
    spin_deliv_values, spin_bvrz_values)

# pace scatter plot values
trace1 = go.Scatter(
    x=pace_deliv_values,
    y=pace_bvrz_values,
    mode='markers',
    marker=dict(
        color='#D9437D'
    ),
    opacity=0.2,
    name='pace'
)

# pace regression line
trace2 = go.Scatter(
    x=pace_deliv_values,
    y=pace_intercept + pace_slope * pace_deliv_values,
    line=go.Line(width=4),
    marker=dict(
        color='#D9437D'
    ),
    showlegend=False
)

# spin scatter plot values
trace3 = go.Scatter(
    x=spin_deliv_values,
    y=spin_bvrz_values,
    mode='markers',
    marker=dict(
        color='#367D9F'
    ),
    opacity=0.2,
    name='spin'
)

# spin regression line
trace4 = go.Scatter(
    x=spin_deliv_values,
    y=spin_intercept + spin_slope * spin_deliv_values,
    line=go.Line(width=4),
    marker=dict(
        color='#367D9F'
    ),
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
                    title="Match Delivery",
                    range=[-30, 1400],
                    showline=False,
                    zeroline=False
                ),
                yaxis=dict(
                    title="Bounce Velocity Ratio",
                    range=[0.38, 0.75]
                )
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
