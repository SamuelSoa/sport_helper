import dash
from dash import dcc, html, Input, Output, State, dash_table
import pandas as pd
import dash_bootstrap_components as dbc
import numpy as np
from dash_auth import BasicAuth
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

df_event_volley=pd.DataFrame(columns=['player','team','set_actuel','event','score1','score2'])


def update_dataframe_volley(data_event,joueur,equipe,set_actuel,event,score1,score2):
    data_event.loc[len(data_event),['player','team','set_actuel','event','score1','score2']]=[joueur,equipe,set_actuel,event,score1,score2]
    return data_event

# def update_dataframe_team(data_event,equipe,periode,temps,event,score1,score2):
#     data_event.loc[len(data_event),['team','periode','time','event','score1','score2']]=[equipe,periode,temps,event,score1,score2]
#     return data_event



# def score_to_update_click_tennis(variable,score,autre_score):
#     event=False
#     if variable =='fin' and score in [40,'av']:
#         score=0;autre_score=0;event=True


#     elif variable=='point' and score in [0,15]:
#         score+=15
#     elif variable=='point' and score==30:
#         score=40
#     elif variable=='avantage':
#         score='av'
#     elif variable=='egalisation':
#         score=40
#         autre_score=40
#     return score,autre_score,event

def score_to_update_click_volley(score,autre_score):
    event=False
    score+=1
    if (score==25 and autre_score<24) or (score>=24 and autre_score>=24 and np.abs(score-autre_score)>=2):
        event=True
    return score,autre_score,event



layout_match_volley= html.Div([
    html.H1('Statistiques du match'),

     html.Div([
       html.Div('Set actuel', style={'fontSize': 20, 'marginRight': '10px', 'marginLeft': '10px'}),
        html.Div(id='set_actuel_volley', style={'fontSize': 20,'padding': '20px'})
       
       ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}),
    # Create a table-like structure with rows of buttons per person
    html.Div(id='buttons-container-volley', style={'padding': '20px'}),
    html.Br(),
    html.H1("Données de match"),
    html.Div(id='stat-container-volley', style={'padding': '20px'}),

    html.H1("Données d'évènements"),
    # Dash DataTable to display the updated dataframe
    dash_table.DataTable(
        id="output_table2_volley",
            export_format="csv",
        columns=[{"name": i, "id": i} for i in df_event_volley.columns],  # Display dataframe columns
        data=df_event_volley.to_dict('records'),  # Initialize the table with dataframe data
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

def display_stat_volley(df):
    layout_stat=dash_table.DataTable(
            id="output_table_team_render_volley",
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


def display_buttons_volley(df):
    layout_button=html.Div(
    [html.Div([#df=df_mattch_team
    html.Div(df.loc[i, 'player'], style={'display': 'inline-block', 'width': '100px'}),
        html.Div(df.loc[i, 'team'], style={'display': 'inline-block', 'width': '100px'}),
        html.Button('point', id={'type': 'pointvolley-button', 'index': i}, n_clicks=0)
    ], style={'padding': '10px'}) for i in df.index])
    return layout_button



def get_nom_exhibition_volley(shared_data):
    """ Retourne les données des équipes (initialisation du df) 
    df_result à utiliser pour le layout des boutons et des stats"""
    nombre_set_gagnant=3
    donnees_equipes1=shared_data['donnees_team1'].split(',')
    donnees_equipes2=shared_data['donnees_team2'].split(',')
    nom_equipe1=shared_data['nomequipe1']
    nom_equipe2=shared_data['nomequipe2']
    joueurs1=donnees_equipes1[1:]
    joueurs2=donnees_equipes2[1:]
    data = {
    'player':joueurs1+joueurs2 ,
    'team':[nom_equipe1]*len(joueurs1)+ [nom_equipe2]*len(joueurs2),
    'id_team':['t1']*len(joueurs1)+['t2']*len(joueurs2),
    'nb_set_gagne':[0]*len(joueurs1+joueurs2)}
    df_result = pd.DataFrame(data)
    list_set=['set'+str(elem) for elem in range(1,2*nombre_set_gagnant-1)]
    for i in list_set:
       df_result[i]=0
    print(f"voici les data apres application de get_exhibition{df_result}")
    return df_result














