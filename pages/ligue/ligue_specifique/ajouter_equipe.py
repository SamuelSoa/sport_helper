import pandas as pd
import dash
import dash_bootstrap_components as dbc
import numpy as np
from dash import dcc, html, Input, Output,dash_table,State, callback
from flask_login import current_user
from utils.login_handler import require_login
from pymongo import MongoClient
from dao.ligue_dao import create_equipe,choice_player_from_ligue

dash.register_page(__name__, path="/ligues/vos_ligues/ajouter_equipe",name='Ajouter une équipe à la ligue')
require_login(__name__)



def layout():
    if not current_user.is_authenticated:
        return html.Div(["Please ", dcc.Link("login", href="/login"), " to continue"])
    return html.Div(
        [html.Div(children="Nom de l'équipe", className="menu-title"),
        dcc.Textarea(
        id='nom_equipe_createequipe',
        value="t2" ,
        style={'width': '300px', 'height': '100px', 'resize': 'none', 'font-size': '14px'},
        ),
        html.Div(children="Nom des joueurs", className="menu-title"),
        html.Div(id='liste_joueurs_available'),
        html.Button("Creer l'équipe", id='validate-button-createequipe', n_clicks=0),  # Use a button for validation
        html.Br(),
        html.Div(id='text-createequipe',children='Pas encore crée'),

        ]
    )



@callback(Output('liste_joueurs_available','children'),
        Input('shared-data-ligue','data')
        )
def get_dropdown_joueurs(shared_data):
    nom_ligue=shared_data['ligue_name']
    return choice_player_from_ligue(nom_ligue)



@callback(
    Output('text-createequipe', 'children'),
    Input('shared-data-ligue','data'),
    Input('nom_equipe_createequipe','value'),
    Input('joueurs_createequipe','value'),
    Input('validate-button-createequipe', 'n_clicks'),
    prevent_initial_call=True
)
def create_equipe_in_ligue(shared_data,nom_equipe,liste_joueurs,n_clicks):
    if n_clicks==1:
        nom_ligue=shared_data['ligue_name']
        print(liste_joueurs)
        print(nom_ligue)
        print(nom_equipe)
        result=create_equipe(nom_ligue,nom_equipe,liste_joueurs)
        return result
    else:
        return dash.no_update

