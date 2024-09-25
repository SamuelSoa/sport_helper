import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
from dash import dcc, html, Input, Output,dash_table,State, callback
from dao.ligue_dao import get_data_by_filter

dash.register_page(__name__, path="/ligues/vos_ligues/ajouter_rencontre/parametrage_rencontre_free",name='Paramètrage de la rencontre')

layout = html.Div(
    children=[
        dcc.Location(id='url', refresh=True),  # Add this component
        html.P("Participants", className="lead"),
        html.Div(id='dropdown_1_freeindiv'),
        html.Br(),
        html.Button('Cliquez 2 fois', id='validate-button-rencontreligue-freeindiv', n_clicks=0)  # Use a button for validation
    ], className='wrapper'
)






@callback(Output('dropdown_1_freeindiv','children'),
        Input('shared-data-ligue','data')
        )
def get_dropdown_equipe1(shared_data):
    all_team=shared_data['liste_player']
    result=dcc.Dropdown(
                id='joueurs_freeindiv',
                options=[{"label": x, "value": x} for x in all_team],
                clearable=False,
                className="dropdown",
                multi=True
            )
    return result





@callback(
    Output('shared-data-store-ligue-freesolo', 'data',allow_duplicate=True),
    [Input('validate-button-rencontreligue-freeindiv', 'n_clicks')],
    [State('shared-data-ligue', 'data'),
    State('joueurs_freeindiv', 'value'),
    ],prevent_initial_call=True
)
def store_data_annot(n_clicks,shared_data,joueurs):
    discipline=shared_data['discipline_ligue']
    if n_clicks is None or n_clicks == 0:
        print("validate-button has not been clicked yet.")
        return dash.no_update
    dicto={'discipline_to_choose':discipline,'donnees-ligue':joueurs}
    # dicto['data']=df_donnees_joueurs
    # dicto.update({'data': df_donnees_joueurs})
    print(f"Storing data footbasket: {dicto}")  # Debugging statement
    return dicto





@callback(
    Output('url', 'pathname',allow_duplicate=True),
    Input('validate-button-rencontreligue-freeindiv', 'n_clicks'),
    prevent_initial_call=True
)
def navigate_ligue(n_clicks):
        # premier click va permettre d'avoir la valeur de shared_data, deuxième permet d'obtenir discipline
    if n_clicks >=2 :
        return '/party_free_solo_ligue'  # Navigate to the desired page
    return dash.no_update
