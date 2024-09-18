import dash
from dash import dcc, html, Input, Output, State, dash_table
import pandas as pd
import dash_bootstrap_components as dbc


# data = {
#     'nom_equipe': ['Team 1', 'Team 2'],
#     '3pt': [0,0],
#     '3pt-reussi': [0,0],
#     '3pt-echoue': [0,0],
#     '2pt': [0,0],
#     '2pt-reussi': [0,0],
#     '2pt-echoue': [0,0],
#     'lf': [0,0],
#     'lf-reussi': [0,0],
#     'lf-echoue': [0,0]
# }

# data = {
#     'player': ['j1', 'j2', 'j3','j4','j5','j6','j7','j8','j9','j10'],
#     'team': ['t1', 't1', 't1','t1','t1','t2','t2','t2','t2','t2'],
#     '3pt': [0,0,0,0,0,0,0,0,0,0],
#     '3pt-reussi': [0,0,0,0,0,0,0,0,0,0],
#     '3pt-echoue': [0,0,0,0,0,0,0,0,0,0],
#     '2pt': [0,0,0,0,0,0,0,0,0,0],
#     '2pt-reussi': [0,0,0,0,0,0,0,0,0,0],
#     '2pt-echoue': [0,0,0,0,0,0,0,0,0,0],
#     'lf': [0,0,0,0,0,0,0,0,0,0],
#     'lf-reussi': [0,0,0,0,0,0,0,0,0,0],
#     'lf-echoue': [0,0,0,0,0,0,0,0,0,0],
#     'reb': [0,0,0,0,0,0,0,0,0,0],
#     'ast': [0,0,0,0,0,0,0,0,0,0],
#     'stl': [0,0,0,0,0,0,0,0,0,0],
#     'blk': [0,0,0,0,0,0,0,0,0,0],
#     'to': [0,0,0,0,0,0,0,0,0,0]
# }
# df_match_team = pd.DataFrame(data)

df_event_team=pd.DataFrame(columns=['player','team','periode','time','event','score1','score2'])


def update_dataframe_general(data_event,joueur,equipe,periode,temps,event,score1,score2):
    data_event.loc[len(data_event),['player','team','periode','time','event','score1','score2']]=[joueur,equipe,periode,temps,event,score1,score2]
    return data_event

# def update_dataframe_team(data_event,equipe,periode,temps,event,score1,score2):
#     data_event.loc[len(data_event),['team','periode','time','event','score1','score2']]=[equipe,periode,temps,event,score1,score2]
#     return data_event



def score_to_update_click(variable,score,sys_point):
    if sys_point=='point_normal':
        if variable=='3pt-reussi':
            score+=3
        elif variable=='2pt-reussi':
            score+=2
        elif variable=='lf-reussi':
            score+=1
    elif sys_point=='point_mini':
        if variable=='3pt-reussi':
            score+=2
        elif variable=='2pt-reussi':
            score+=1
        elif variable=='lf-reussi':
            score+=1
    return score


layout_match_basket_simple= html.Div([
    html.H1('Statistiques du match'),
     html.Div(children="Période actuelle", className="menu-title"),
        dcc.Input(id="current-periode-input", type="number", value=1),
     html.Div(children="Système de point (si basket)", className="menu-title"),
        dcc.Dropdown(
            id="sys_pt_basket_team",
            options=[{"label": x, "value": y} for x, y in [['3PT=3,2PT=2', 'point_normal'], ['3PT=2,2PT=1', 'point_mini']]],
            clearable=False,
            className="dropdown"
        ),
        html.Div(children="Type d'annotation", className="menu-title"),
        dcc.Dropdown(
            id="sys_annot",
            options=[{"label": x, "value": y} for x, y in [['Simple', 'annot_simple'], ['Complet', 'annot_complet']]],
            clearable=False,
            className="dropdown"
        ),
   html.Div([
        # html.Div(id='periode-output', style={'margin': '20px', 'fontSize': 20}),
        html.Div(id='nom_equipe1',children='Team 1', style={'fontSize': 20, 'marginRight': '10px'}),
        # html.Div('Counter 1:', style={'fontSize': 20, 'marginRight': '10px'}),
        html.Div(id='scorecounter1_team', children='0', style={'margin': '20px', 'fontSize': 20}),
        html.Div(' - ', style={'fontSize': 20, 'marginRight': '10px', 'marginLeft': '10px'}),
        html.Div(id='scorecounter2_team', children='0', style={'margin': '20px', 'fontSize': 20}),
        html.Div(id='nom_equipe2',children='Team 2', style={'fontSize': 20, 'marginLeft': '10px'})
        
    ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}),
   html.Div('Chrono:', style={'fontSize': 20, 'marginRight': '10px'}),
    html.Div(id='countdown-display_team', style={'fontSize': 40, 'textAlign': 'center', 'marginTop': '20px'}),
    # Play/Pause Button
    html.Button('Play', id='play-pause-button_team', n_clicks=0, style={'fontSize': 20, 'marginTop': '20px', 'textAlign': 'center', 'display': 'block', 'margin': '0 auto'}),

    # Interval component for ticking every second
    dcc.Interval(
        id='interval-component_team',
        interval=1000,  # 1 second
        n_intervals=0,
        disabled=True  # Initially disabled until Play is clicked
    ),
    dcc.Store(id='countdown-value_team',data=60),
    # Create a table-like structure with rows of buttons per person
    html.Div(id='buttons-container', style={'padding': '20px'}),
     html.Br(),
    html.H1("Données de match"),
    html.Div(id='stat-container', style={'padding': '20px'}),

    html.H1("Données d'évènements"),
    # Dash DataTable to display the updated dataframe
    dash_table.DataTable(
        id="output_table2_team",
            export_format="csv",
        columns=[{"name": i, "id": i} for i in df_event_team.columns],  # Display dataframe columns
        data=df_event_team.to_dict('records'),  # Initialize the table with dataframe data
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


def display_stat(df):
    layout_stat=dash_table.DataTable(
            id="output_table_team_render",
                export_format="csv",
            columns=[{"name": i, "id": i} for i in df.columns],  # Display dataframe columns
            data=df.to_dict('records'),  # Initialize the table with dataframe data
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
    return layout_stat


def display_buttons(df,sys_annot):
    if sys_annot=='annot_simple':
        layout_button=html.Div(
        [html.Div([#df=df_mattch_team
        html.Div(df.loc[i, 'player'], style={'display': 'inline-block', 'width': '100px'}),
            html.Div(df.loc[i, 'team'], style={'display': 'inline-block', 'width': '100px'}),
            html.Button('3pt tentative', id={'type': '3pt-button', 'index': i}, n_clicks=0),
            html.Button('3pt reussi', id={'type': '3pt-reussi-button', 'index': i}, n_clicks=0),
            html.Button('3pt loupé', id={'type': '3pt-echoue-button', 'index': i}, n_clicks=0),

            html.Button('2pt tentative', id={'type': '2pt-button', 'index': i}, n_clicks=0),
            html.Button('2pt reussi', id={'type': '2pt-reussi-button', 'index': i}, n_clicks=0),
            html.Button('2pt loupé', id={'type': '2pt-echoue-button', 'index': i}, n_clicks=0),

            html.Button('LF tentative', id={'type': 'lf-button', 'index': i}, n_clicks=0),
            html.Button('LF reussi', id={'type': 'lf-reussi-button', 'index': i}, n_clicks=0),
            html.Button('LF loupé', id={'type': 'lf-echoue-button', 'index': i}, n_clicks=0)

        ], style={'padding': '10px'}) for i in df.index])
       
    elif sys_annot=='annot_complet':
        layout_button=html.Div(
        [html.Div([#df=df_mattch
            html.Div(df.loc[i, 'player'], style={'display': 'inline-block', 'width': '100px'}),
            html.Div(df.loc[i, 'team'], style={'display': 'inline-block', 'width': '100px'}),
            html.Div([
            html.Button('3pt', id={'type': '3pt-button', 'index': i}, n_clicks=0),
            html.Button('3pt reussi', id={'type': '3pt-reussi-button', 'index': i}, n_clicks=0),
            html.Button('3pt loupé', id={'type': '3pt-echoue-button', 'index': i}, n_clicks=0),

            html.Button('2pt', id={'type': '2pt-button', 'index': i}, n_clicks=0),
            html.Button('2pt reussi', id={'type': '2pt-reussi-button', 'index': i}, n_clicks=0),
            html.Button('2pt loupé', id={'type': '2pt-echoue-button', 'index': i}, n_clicks=0),

            html.Button('LF', id={'type': 'lf-button', 'index': i}, n_clicks=0),
            html.Button('LF reussi', id={'type': 'lf-reussi-button', 'index': i}, n_clicks=0),
            html.Button('LF loupé', id={'type': 'lf-echoue-button', 'index': i}, n_clicks=0),

            html.Button('Reb', id={'type': 'reb-button', 'index': i}, n_clicks=0),
            html.Button('AST', id={'type': 'ast-button', 'index': i}, n_clicks=0),
            html.Button('STL', id={'type': 'stl-button', 'index': i}, n_clicks=0),
            html.Button('BLK', id={'type': 'blk-button', 'index': i}, n_clicks=0),
            html.Button('TO', id={'type': 'to-button', 'index': i}, n_clicks=0)], style={'display': 'flex', 'flex-wrap': 'wrap', 'gap': '5px'})
        ], style={'padding': '10px'}) for i in df.index]
    )
    
    return layout_button




def get_nom_exhibition(shared_data):
    """ Retourne les données des équipes (initialisation du df) 
    df_result à utiliser pour le layout des boutons et des stats"""
    donnees_equipes1=shared_data['donnees_team1'].split(',')
    donnees_equipes2=shared_data['donnees_team2'].split(',')
    nom_equipe1=shared_data['nomequipe1']
    nom_equipe2=shared_data['nomequipe2']
    joueurs1=donnees_equipes1[1:]
    joueurs2=donnees_equipes2[1:]
    data = {
    'player':joueurs1+joueurs2 ,
    'team':[nom_equipe1]*len(joueurs1)+ [nom_equipe2]*len(joueurs2),
    'id_team':['t1']*len(joueurs1)+['t2']*len(joueurs2)}
    df_result = pd.DataFrame(data)
    for i in ['3pt','3pt-reussi','3pt-echoue','2pt','2pt-reussi','2pt-echoue','lf','lf-reussi','lf-echoue','reb','ast','stl','blk','to']:
       df_result[i]=0
    print(f"voici les data apres application de get_exhibition{df_result}")

    return df_result