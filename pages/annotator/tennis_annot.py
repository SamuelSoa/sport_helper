import pandas as pd
import dash
import dash_bootstrap_components as dbc
import numpy as np
from dash import dcc, html, Input, Output,dash_table,State, callback


dash.register_page(__name__, path="/exhibition/party_tennis")

df_event_tennis=pd.DataFrame(columns=['player','team','set_actuel','event','score1','score2'])


def update_dataframe_tennis(data_event,joueur,equipe,set_actuel,event,score1,score2):
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

def score_to_update_click_tennis(score,autre_score):
    event=False
    marquage_sans_prolong=(score==40 and autre_score in [0,15,30])
    marquage_prolong=(score=='av' and autre_score==40)
    if  score in [0,15]:
        score+=15
    elif score==30:
        score=40
    elif [score,autre_score]==[40,40]:
        score='av'
    elif [score,autre_score]==[40,'av']:
        score=autre_score=40
    elif marquage_sans_prolong or marquage_prolong :
        score=0;autre_score=0;event=True
    return score,autre_score,event



layout= html.Div([
    html.H1('Statistiques du match'),
    
    html.Div(children="Nombre de set gagnant", className="menu-title"),
        dcc.Input(id="nb_set_gagnant", type="number", value=4),
    
     html.Div([
       html.Div('Set actuel', style={'fontSize': 20, 'marginRight': '10px', 'marginLeft': '10px'}),
        html.Div(id='set_actuel', style={'fontSize': 20,'padding': '20px'})
       
       ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}),
    # Create a table-like structure with rows of buttons per person
    html.Div(id='buttons-container-tennis', style={'padding': '20px'}),
    html.Br(),
    html.H1("Données de match"),
    html.Div(id='stat-container-tennis', style={'padding': '20px'}),

    html.H1("Données d'évènements"),
    # Dash DataTable to display the updated dataframe
    dash_table.DataTable(
        id="output_table2_tennis",
            export_format="csv",
        columns=[{"name": i, "id": i} for i in df_event_tennis.columns],  # Display dataframe columns
        data=df_event_tennis.to_dict('records'),  # Initialize the table with dataframe data
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

def display_stat_tennis(df):
    layout_stat=dash_table.DataTable(
            id="output_table_team_render_tennis",
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


def display_buttons_tennis(df):
    layout_button=html.Div(
    [html.Div([#df=df_mattch_team
    html.Div(df.loc[i, 'player'], style={'display': 'inline-block', 'width': '100px'}),
        html.Div(df.loc[i, 'team'], style={'display': 'inline-block', 'width': '100px'}),
        html.Button('point', id={'type': 'point-button', 'index': i}, n_clicks=0)
    ], style={'padding': '10px'}) for i in df.index])
    return layout_button



def get_nom_exhibition_tennis(shared_data,nombre_set_gagnant):
    """ Retourne les données des équipes (initialisation du df) 
    df_result à utiliser pour le layout des boutons et des stats"""
    joueurs1=shared_data['donnees_team1'].split(',')
    joueurs2=shared_data['donnees_team2'].split(',')
    nom_equipe1=shared_data['nomequipe1']
    nom_equipe2=shared_data['nomequipe2']
    data = {
    'player':joueurs1+joueurs2 ,
    'team':[nom_equipe1]*len(joueurs1)+ [nom_equipe2]*len(joueurs2),
    'id_team':['t1']*len(joueurs1)+['t2']*len(joueurs2),
    'nb_set_gagne':[0]*len(joueurs1+joueurs2),
    'point_set_actuel':[0]*len(joueurs1+joueurs2)}
    df_result = pd.DataFrame(data)
    list_set=['set'+str(elem) for elem in range(1,2*nombre_set_gagnant-1)]
    for i in list_set:
       df_result[i]=0
    print(f"voici les data apres application de get_exhibition{df_result}")
    return df_result



### Tennis ###


@callback(
    Output('buttons-container-tennis', 'children'),Output('stat-container-tennis', 'children'),  # To dynamically update the buttons
    [
    # State({'type': 'output_table_team', 'index': dash.dependencies.ALL}, 'data'),
    State('shared-data-store', 'data'),
    Input('nb_set_gagnant', 'value')
    ]
    )
def update_display_tennis(shared_data,nb_set_gagnant):
    """ Retourne le layout des boutons"""
    # Recreate the DataFrame from the stored data
    # Call the display_annot_buttons function with the current DataFrame and annotation system
    # print('on est a update_buttons_display')
    print('not yet, transforation des données partagés pour display boutons et stat')
    df=get_nom_exhibition_tennis(shared_data,nb_set_gagnant)
    print('yes')
    donnees_button=display_buttons_tennis(df)
    donnees_stat=display_stat_tennis(df)
    return donnees_button,donnees_stat


# Callback to update each team information and update the table
@callback(
    [Output("output_table_team_render_tennis", "data"),
    Output("output_table2_tennis", "data"),
    Output('set_actuel','children')],
    # Output("periode-output", "children")],
    [Input({'type': 'point-button', 'index': dash.dependencies.ALL}, 'n_clicks'),
    State('output_table_team_render_tennis', 'data'),
    State('output_table2_tennis', 'data'),
    Input('nb_set_gagnant','value'),
    State('set_actuel','value'),
    State('shared-data-store', 'data')
    ]
)
def update_person_info_team_tennis(pt_click,table_data,event_data,nb_set_gagnant,set_actuel,shared_data):
    
    # print(f"input update_person_info_team: {table_data}")
    df_event = pd.DataFrame(event_data)
    df = pd.DataFrame(table_data) if table_data else get_nom_exhibition_tennis(shared_data,nb_set_gagnant)
    print(df)
    if not set_actuel:
        set_actuel='set1'

    
    # df = pd.DataFrame(df_table)
    # print('voila les données pour mise à jour team')
    # print(df)
    
    
    # Determine which button was clicked
    ctx = dash.callback_context
    print(f"trigger: {ctx.triggered}")
    # if not ctx.triggered:
    #     return df.to_dict('records'),df_event.to_dict('records'),str(score1),str(score2)
    # Extract the button information in JSON format
    triggered_button = ctx.triggered[0]['prop_id']
    button_info = eval(triggered_button.split('.')[0])  # Safely parse the button's JSON structure
    button_type = button_info['type']
    person_id = button_info['index']
    variable=button_type.split('-button')[0]

    # si un boutton est appuyé    (par defaut le xtx.triggered est long et le bouton "3pt-button" aurait été appuyé)
    if not len(ctx.triggered)>1:
        
        equipe=df.loc[person_id,'team']
        id_team=df.loc[person_id,'id_team']
        indice_idteam=df.loc[df.id_team==id_team].index.tolist()

        indice_equipe=df.loc[df.id_team=='t1'].index.tolist()
        nombre_joueurs=len(indice_equipe)
        indice_autreequipe=df.loc[df.id_team=='t2'].index.tolist()
        score1=df.loc[indice_equipe,'point_set_actuel'].unique().tolist()[0]
        score2= df.loc[indice_autreequipe,'point_set_actuel'].unique().tolist()[0]
        joueur=df.loc[person_id,'player']
        if id_team=='t1':
            score1,score2,event=score_to_update_click_tennis(score1,score2)
        elif id_team=='t2':
            score2,score1,event=score_to_update_click_tennis(score2,score1)
        df.loc[indice_equipe,'point_set_actuel']= score1
        df.loc[indice_autreequipe,'point_set_actuel']= score2

        if event:
            df.loc[indice_idteam,set_actuel]+= 1
        #reinitialisation après un set gagné
        seuil_manche=6
        if df.loc[indice_equipe,set_actuel].values.tolist()==df.loc[indice_autreequipe,set_actuel].values.tolist()==5 or list(set(df[set_actuel].values.tolist())) in [[6,5],[5,6],[6,6],[7,6],[6,7]]:
            seuil_manche=7

        if df.loc[indice_idteam,set_actuel].values.tolist()==[seuil_manche]*nombre_joueurs:
            set_actuel='set'+str(int(set_actuel[3])+1)
            df.loc[indice_idteam,'nb_set_gagne']+= 1
            df.loc[indice_equipe,'point_set_actuel']= 0
            df.loc[indice_autreequipe,'point_set_actuel']= 0
        df_event=update_dataframe_tennis(df_event,joueur,equipe,set_actuel,variable,score1,score2)
        # Return the updated messages and the updated table data
    return  df.to_dict('records'),df_event.to_dict('records'),set_actuel












