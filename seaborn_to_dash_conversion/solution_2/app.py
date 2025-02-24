import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

import pandas as pd
import numpy as np
import statsmodels.api as sm
import math
import datetime

from sql import get_matches, get_bounce_data

from utilities import (
    changeovers,
    print_inning_lines
)

######
# Data
######

# Matches data for the dropdown
#   [{id: ..., name: ...}, {...}, ...]
matches = get_matches(10)

######
# Dash
######

app = dash.Dash()

colors = dict(
    pace='#D9437D',
    spin='#367D9F',
    over_line='#888886'
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

    html.Div([
        dcc.Dropdown(
            id='match-ids',
            options=[{'label': x['name'], 'value': x['id']} for x in matches],
            value='193945',
            placeholder='England v West Indies at Leeds, 2nd Test, \
                         25-29 Aug 2017'
        ),
        html.Div(dcc.RadioItems(
            id='line-option',
            options=[
                {'label': 'Innings', 'value': 'innings'},
                {'label': 'Days', 'value': 'days'}
            ],
            value='innings',
            labelStyle={'display': 'inline-block',
                        'padding': '1%'}
        ), style={'text-align': 'center'}),
    ], style={'max-width': '30em',
              'margin': '0 auto',
              'padding-top': '1%'}),

    dcc.Graph(id='example-graph')
])


###############
# Dash Callback
###############

@app.callback(
    dash.dependencies.Output('example-graph', 'figure'),
    [dash.dependencies.Input('match-ids', 'value'),
     dash.dependencies.Input('line-option', 'value')])
def update_graph(match_id, line_option):

    match_data = get_bounce_data(int(match_id))

    ###################
    # Data Manipulation
    ###################

    # Bounce Data
    bounce_data_df = pd.DataFrame(match_data)

    # Add count of delivery number
    bounce_data_df['deliv'] = [n + 1 for n in range(len(bounce_data_df))]

    # Change the format of the date column
    bounce_data_df.date = bounce_data_df.date.apply(
        lambda x: x.date().strftime('%d-%m-%y'))

    # Drop null bounces
    bounce_data_df = bounce_data_df.dropna(subset=['bvrz']).copy()

    # bvrz values
    pace_bvrz_values = bounce_data_df.bvrz[bounce_data_df.pace == 1]
    spin_bvrz_values = bounce_data_df.bvrz[bounce_data_df.pace == 0]

    # deliv number counts
    pace_deliv_values = bounce_data_df.deliv[bounce_data_df.pace == 1]
    spin_deliv_values = bounce_data_df.deliv[bounce_data_df.pace == 0]

    # local regression method using LOWESS
    lowess = sm.nonparametric.lowess

    # regression values for both axis based on the lowess algorithm
    pace_regression_x = lowess(pace_bvrz_values, pace_deliv_values)[:, 0]
    pace_regression_y = lowess(pace_bvrz_values, pace_deliv_values)[:, 1]

    spin_regression_x = lowess(spin_bvrz_values, spin_deliv_values)[:, 0]
    spin_regression_y = lowess(spin_bvrz_values, spin_deliv_values)[:, 1]

    # x axis (delivery number) limits, rounded to the nearest 100
    #   - TODO: This could be updated to round based on the number of
    #           deliveries, for example, if there were 80 deliveries,
    #           round to the nearest
    #           10 etc and so on...
    delivery_number_min = int(round(bounce_data_df.deliv.min(), -2))
    delivery_number_max = int(round(bounce_data_df.deliv.max(), -2))

    # y axis (bvrz) limits
    bvrz_min = np.percentile(bounce_data_df['bvrz'], 1)
    bvrz_max = np.percentile(bounce_data_df['bvrz'], 99)

    # list of delivery numbers corrsponding to the change of innings
    innings_changovers = changeovers(bounce_data_df.inn)

    # list of delivery numbers corrsponding to the change of day
    day_changeovers = changeovers(bounce_data_df.date)

    ################################################################
    # Figure Data (Scatter Plots, Regression Lines & Vertical Lines)
    ################################################################

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

    # list of dicts
    #   - each dict contains the code to construct a single line
    inning_lines = print_inning_lines(innings_changovers, bvrz_min,
                                      bvrz_max, colors['over_line'])

    day_lines = print_inning_lines(day_changeovers, bvrz_min,
                                   bvrz_max, colors['over_line'])

    # line_option corresponds to the radio button input value
    lines = inning_lines if line_option == 'innings' else day_lines

    # return value is set to the *figure* parameter of the graph
    return {
        'data': [trace1, trace2, trace3, trace4],
        'layout': go.Layout(
            xaxis=dict(
                title='Match Delivery',
                zeroline=False,
                range=[delivery_number_min - 50, delivery_number_max]
            ),
            yaxis=dict(
                title='Bounce Velocity Ratio',
                range=[bvrz_min, bvrz_max]
            ),
            margin=dict(
                t=20
            ),
            shapes=lines
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)
