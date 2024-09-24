import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
from dash import dcc, html, Input, Output,dash_table,State, callback
from flask_login import current_user


# dash.register_page(__name__, path"/ligues/vos_ligues/parametres",name='Parametres')



layout=html.Div([

            html.Button('Finir la saison', id='submit-end-season', n_clicks=0),
            html.Button('Supprimer la ligeu', id='submit-end-ligue', n_clicks=0)

            # html.Button('Deconnexion', id='decconect_button', n_clicks=0),
            # html.Div(id='container-button-basic',
            #         children='Enter a value and press submit')
        ])





@callback(
    Output('view_ligue_parameters','children'),
    Input('shared-data-ligue','data') 
)
def get_view_parameter_ligue(shared_data):

    index_username=shared_data['liste_player'].index(current_user.id)
    statut_utilisateur=shared_data['liste_role'][index_username]
    if statut_utilisateur=='admin':
        layout_vosligues=html.Div([
                                    dbc.Nav(
                [
                dbc.NavLink("Finir la saison", href="/ligues/vos_ligues/parametres/end_saison", active="exact"),
                dbc.NavLink("Céder votre droit d'administrateur à quelqu'un d'autre", href="/ligues/vos_ligues/parametres/give", active="exact"),
                dbc.NavLink("Céder votre droit d'administrateur à d'autres personnes", href="/ligues/vos_ligues/parametres/end_saison", active="exact"),
                dbc.NavLink("Suprimmer la ligue", href="/ligues/vos_ligues/parametres/supprimer la ligue", active="exact")
                ],
                vertical="md",
                pills=True
            )
                                ])
    else:
        layout_vosligues=html.Div([])


    return layout_vosligues
       
    