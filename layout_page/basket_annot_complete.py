import dash
from dash import dcc, html, Input, Output, State, dash_table
import pandas as pd
import dash_bootstrap_components as dbc

data = {
    'pseudo_joueur': ['j1', 'j2', 'j3','j4','j5','j6','j7','j8','j9','j10'],
    '3pt': [0,0,0,0,0,0,0,0,0,0],
    '3pt-reussi': [0,0,0,0,0,0,0,0,0,0],
    '3pt-echoue': [0,0,0,0,0,0,0,0,0,0],
    '2pt': [0,0,0,0,0,0,0,0,0,0],
    '2pt-reussi': [0,0,0,0,0,0,0,0,0,0],
    '2pt-echoue': [0,0,0,0,0,0,0,0,0,0],
    'lf': [0,0,0,0,0,0,0,0,0,0],
    'lf-reussi': [0,0,0,0,0,0,0,0,0,0],
    'lf-echoue': [0,0,0,0,0,0,0,0,0,0],
    'reb': [0,0,0,0,0,0,0,0,0,0],
    'ast': [0,0,0,0,0,0,0,0,0,0],
    'stl': [0,0,0,0,0,0,0,0,0,0],
    'blk': [0,0,0,0,0,0,0,0,0,0],
    'to': [0,0,0,0,0,0,0,0,0,0]
}
df_match = pd.DataFrame(data)
df_event=pd.DataFrame(columns=['joueur','time','event','score1','score2'])

def update_dataframe(data_event,joueur,temps,event,score1,score2):
    data_event.loc[len(data_event),['joueur','time','event','score1','score2']]=[joueur,temps,event,score1,score2]
    return data_event


def score_to_update_click(variable,score):
    if variable=='3pt-reussi':
        score+=3
    elif variable=='2pt-reussi':
        score+=2
    elif variable=='lf-reussi':
        score+=1
    return score

layout_match= html.Div([
    html.H1('Statistiques du match'),
   html.Div([
        html.Div('Counter 1:', style={'fontSize': 20, 'marginRight': '10px'}),
        html.Div(id='scorecounter1', children='0', style={'margin': '20px', 'fontSize': 20}),
        html.Div(' - ', style={'fontSize': 20, 'marginRight': '10px', 'marginLeft': '10px'}),
        html.Div(id='scorecounter2', children='0', style={'margin': '20px', 'fontSize': 20}),
        html.Div('Counter 2', style={'fontSize': 20, 'marginLeft': '10px'})
    ], style={'display': 'flex', 'alignItems': 'center'}),
    # Display countdown timer
    html.Div(id='countdown-display', style={'fontSize': 40, 'textAlign': 'center', 'marginTop': '20px'}),
    # Play/Pause Button
    html.Button('Play', id='play-pause-button', n_clicks=0, style={'fontSize': 20, 'marginTop': '20px'}),

    # Interval component for ticking every second
    dcc.Interval(
        id='interval-component',
        interval=1000,  # 1 second
        n_intervals=0,
        disabled=True  # Initially disabled until Play is clicked
    ),
    dcc.Store(id='countdown-value', data=60),
    # Create a table-like structure with rows of buttons per person
    html.Div(
        [html.Div([
            html.Div(df_match.loc[i, 'pseudo_joueur'], style={'display': 'inline-block', 'width': '100px'}),
            html.Button('3pt tentative', id={'type': '3pt-button', 'index': i}, n_clicks=0),
            html.Button('3pt reussi', id={'type': '3pt-reussi-button', 'index': i}, n_clicks=0),
            html.Button('3pt loupé', id={'type': '3pt-echoue-button', 'index': i}, n_clicks=0),

            html.Button('2pt tentative', id={'type': '2pt-button', 'index': i}, n_clicks=0),
            html.Button('2pt reussi', id={'type': '2pt-reussi-button', 'index': i}, n_clicks=0),
            html.Button('2pt loupé', id={'type': '2pt-echoue-button', 'index': i}, n_clicks=0),

            html.Button('LF tentative', id={'type': 'lf-button', 'index': i}, n_clicks=0),
            html.Button('LF reussi', id={'type': 'lf-reussi-button', 'index': i}, n_clicks=0),
            html.Button('LF loupé', id={'type': 'lf-echoue-button', 'index': i}, n_clicks=0),

            html.Button('Reb', id={'type': 'reb-button', 'index': i}, n_clicks=0),
            html.Button('AST', id={'type': 'ast-button', 'index': i}, n_clicks=0),
            html.Button('STL', id={'type': 'stl-button', 'index': i}, n_clicks=0),
            html.Button('BLK', id={'type': 'blk-button', 'index': i}, n_clicks=0),
            html.Button('TO', id={'type': 'to-button', 'index': i}, n_clicks=0),

        ], style={'padding': '10px'}) for i in df_match.index]
    ),
    # Dash DataTable to display the updated dataframe
    dash_table.DataTable(
        id="output_table",
            export_format="csv",
        columns=[{"name": i, "id": i} for i in df_match.columns],  # Display dataframe columns
        data=df_match.to_dict('records'),  # Initialize the table with dataframe data
        # filter_action='native',  # Enable filtering
        style_header={
            'backgroundColor': 'rgb(30, 30, 30)',
            'color': 'white'
        },
        style_data={
            'backgroundColor': 'rgb(50, 50, 50)',
            'color': 'white'
        }
    ),
    
    html.H1("Données d'évènements"),
    # Dash DataTable to display the updated dataframe
    dash_table.DataTable(
        id="output_table2",
            export_format="csv",
        columns=[{"name": i, "id": i} for i in df_event.columns],  # Display dataframe columns
        data=df_event.to_dict('records'),  # Initialize the table with dataframe data
        # filter_action='native',  # Enable filtering
        style_header={
            'backgroundColor': 'rgb(30, 30, 30)',
            'color': 'white'
        },
        style_data={
            'backgroundColor': 'rgb(50, 50, 50)',
            'color': 'white'
        }
    )
])