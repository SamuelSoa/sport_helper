import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
from dash import dcc, html, Input, Output,dash_table,State, callback
from dao.ligue_dao import get_data_by_filter
import datetime


dash.register_page(__name__, path="/ligues/vos_ligues/ajouter_rencontre/parametrage_rencontre",name='Paramètrage de la rencontre')

layout = html.Div(
    children=[
        dcc.Location(id='url', refresh=True),  # Add this component
        html.Div(children="Equipe 1", className="menu-title"),
        html.Div(id='dropdown_1'),
        html.P("Joueurs de l'équipe participants", className="lead"),
        html.Div(id='donnees_team1-ligue-dropdown'),
        html.Div(children="Joueurs de l'équipe participants", className="menu-title"),
        html.Div(id='dropdown_2'),
        html.Div(id='donnees_team2-ligue-dropdown'),
        html.P("Pour le football et le basket", className="lead"),
        html.Div(children="Nombre de periode", className="menu-title"),
        dcc.Input(id="periode-input-ligue", type="number", value=4),
        html.Div(children="Durée de chaque période (s)", className="menu-title"),
        dcc.Input(id="start-time-input-ligue", type="number", value=10),
        dcc.Interval(id='interval-component-ligue', interval=1000, n_intervals=0, disabled=True),
        html.Br(),
       
        html.Button('Cliquez 2 fois', id='validate-button-rencontreligue', n_clicks=0)  # Use a button for validation
    ], className='wrapper'
)

# layout_choix_annotation=html.Div([
#             # dcc.Location(id='url', refresh=False),  # Add this component
#             html.P("Annotation d'un match", className="lead"),
#             dbc.Nav(
#             [dbc.NavLink("Annotation simple", href="/exhibition/party/simple", active="exact"),
#             dbc.NavLink("Annotation complète", href="/exhibition/party/complete", active="exact")
#             ],
#             vertical="md",
#             pills=True
#         )
#         ])






@callback(Output('dropdown_1','children'),
        Input('shared-data-ligue','data')
        )
def get_dropdown_equipe1(shared_data):
    all_team=[elem[0] for elem in shared_data['liste_equipe']]
    sys_ligue=shared_data['sys_ligue']
    if sys_ligue=='fix-teams':
        result_team1=dcc.Dropdown(
                    id='result_equipe1',
                    options=[{"label": x, "value": x} for x in all_team],
                    clearable=False,
                    className="dropdown",
                    multi=True
                )
    else:
        result_team1=dcc.Textarea(
        id='result_equipe1',
        value="t1" ,
        style={'width': '300px', 'height': '100px', 'resize': 'none', 'font-size': '14px'},
        )

    return result_team1



@callback(Output('dropdown_2','children'),
        Input('shared-data-ligue','data'),
        Input('result_equipe1','value')
        )
def get_dropdown_equipe2(shared_data,equipe1):
    print(f"equipe1 dropdown:{equipe1}")
    sys_ligue=shared_data['sys_ligue']
    if sys_ligue=='fix-teams':
        all_team=[elem[0] for elem in shared_data['liste_equipe']]
        team_restante=[elem for elem in all_team if elem not in equipe1]
        result_team2=dcc.Dropdown(
                    id='result_equipe2',
                    options=[{"label": x, "value": x} for x in team_restante],
                    clearable=False,
                    className="dropdown",
                    multi=True
                )
    else:
        result_team2=dcc.Textarea(
        id='result_equipe2',
        value="t2" ,
        style={'width': '300px', 'height': '100px', 'resize': 'none', 'font-size': '14px'},
        )
    return result_team2


@callback(Output('donnees_team1-ligue-dropdown','children'),
        Input('shared-data-ligue','data'),
        Input('result_equipe1','value')
        )
def get_data_equipe1(shared_data,equipe1):
    
    liste_equipe=shared_data['liste_equipe'] 
    sys_ligue=shared_data['sys_ligue']
    if sys_ligue=='fix-teams':
        liste_equipe1=[elem[1] for elem in liste_equipe if elem[0]==equipe1[0] ][0]
        div1=dcc.Dropdown(
                    id='donnees_team1-ligue',
                    options=[{"label": x, "value": x} for x in liste_equipe1],
                    clearable=False,
                    value=liste_equipe1,
                    className="dropdown",
                    multi=True)
        return div1
    else:
        all_team=[elem for elem in shared_data['liste_player']]
        div1=dcc.Dropdown(
                    id='donnees_team1-ligue',
                    options=[{"label": x, "value": x} for x in all_team],
                    clearable=False,
                    className="dropdown",
                    multi=True)
        return div1
    

@callback(Output('donnees_team2-ligue-dropdown','children'),
        Input('shared-data-ligue','data'),
        Input('result_equipe2','value'),
        Input('donnees_team1-ligue','value')
        )
def get_data_equipe2(shared_data,equipe2,donnees1):
    
    liste_equipe=shared_data['liste_equipe'] 
    sys_ligue=shared_data['sys_ligue']
    if sys_ligue=='fix-teams':
        liste_equipe2=[elem[1] for elem in liste_equipe if elem[0]==equipe2[0] ][0]
        
        div2=dcc.Dropdown(
                    id='donnees_team2-ligue',
                    options=[{"label": x, "value": x} for x in liste_equipe2],
                    clearable=False,
                    value=liste_equipe2,
                    className="dropdown",
                    multi=True)
        return div2
    else:
        all_team=[elem for elem in shared_data['liste_player']]
        joueurs_restant=[elem for elem in all_team if elem not in donnees1]
        div2=dcc.Dropdown(
                    id='donnees_team2-ligue',
                    options=[{"label": x, "value": x} for x in joueurs_restant],
                    clearable=False,
                    className="dropdown",
                    multi=True)
        return div2
    



@callback(
    Output('shared-data-store-footbasket', 'data',allow_duplicate=True),
    [Input('validate-button-rencontreligue', 'n_clicks')],
    [State('shared-data-ligue', 'data'),
    State('periode-input-ligue', 'value'),
    State('start-time-input-ligue', 'value'),
    State('donnees_team1-ligue', 'value'),
    State('donnees_team2-ligue', 'value'),
    State('result_equipe1', 'value'),
    State('result_equipe2', 'value')
    ],prevent_initial_call=True
)
def store_data_annot(n_clicks,shared_data,input_value2,input_value3,input_value4,input_value5,input_value6,input_value7):
    discipline=shared_data['discipline_ligue']
    if n_clicks is None or n_clicks == 0:
        print("validate-button has not been clicked yet.")
        return dash.no_update
    print(f'donnees equipes:{input_value4},{input_value5}')
    date=datetime.date.today().strftime('%d/%m/%Y')
    heure=datetime.datetime.now().strftime('%H:%M:%S')
    dicto={'discipline_to_choose':discipline,'periode-input-ligue':input_value2,'start-time-input-ligue':input_value3,'donnees_team1-ligue':input_value4,'donnees_team2-ligue':input_value5,
    'nomequipe1-ligue':input_value6[0] if type(input_value6)==list else input_value6,'nomequipe2-ligue':input_value7[0] if type(input_value7)==list else input_value7,'date_enregistrement':date,
    'heure_enregistrement':heure}
    # dicto['data']=df_donnees_joueurs
    # dicto.update({'data': df_donnees_joueurs})
    print(f"Storing data footbasket: {dicto}")  # Debugging statement
    return dicto





@callback(
    Output('url', 'pathname',allow_duplicate=True),
    Input('validate-button-rencontreligue', 'n_clicks'),
    State('shared-data-ligue', 'data'),
    prevent_initial_call=True
)
def navigate_ligue(n_clicks,shared_data):
    discipline=shared_data['discipline_ligue']
    print(f"discipline navigate:{discipline}")
    print(f"clique:{n_clicks}")
    # premier click va permettre d'avoir la valeur de shared_data, deuxième permet d'obtenir discipline
    if n_clicks >=2 and discipline =='basket':
        return '/party_basket_ligue'  # Navigate to the desired page
    elif n_clicks >=2 and discipline =='tennis':
        return '/party_tennis_ligue'  # Navigate to the desired page
    elif n_clicks >=2 and discipline =='volley':
        return '/party_volley_ligue'  # Navigate to the desired page
    elif n_clicks >=2 and discipline =='football':
        return '/party_foot_ligue'  # Navigate to the desired page
    elif n_clicks >=2 and discipline =='free-multi':
        return '/party_free_multi_ligue'  # Navigate to the desired page
    return dash.no_update


