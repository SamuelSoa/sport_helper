import pandas as pd
import dash
import dash_bootstrap_components as dbc
import numpy as np
from dash import dcc, html, Input, Output,dash_table,State, callback
from flask_login import current_user
from utils.login_handler import require_login
from pymongo import MongoClient
from dao.tournoi_dao import create_equipe_tournoi,choice_player_from_tournoi

dash.register_page(__name__, path="/tournoi/vos_tournois/ajouter_equipe",name='Construire une équipe pour le tournoi')
require_login(__name__)



def layout():
    if not current_user.is_authenticated:
        return html.Div(["Please ", dcc.Link("login", href="/login"), " to continue"])
    return html.Div(
        [html.Div(children="Nom de l'équipe", className="menu-title"),
        dcc.Textarea(
        id='nom_equipe_createequipe_tournoi',
        value="t2" ,
        style={'width': '300px', 'height': '100px', 'resize': 'none', 'font-size': '14px'},
        ),
        html.Div(children="Nom des joueurs", className="menu-title"),
        html.Div(id='liste_joueurs_available_tournoi'),
        html.Button("Creer l'équipe", id='validate-button-createequipe-tournoi', n_clicks=0),  # Use a button for validation
        html.Br(),
        html.Div(id='text-createequipe-tournoi',children='Pas encore crée'),

        ]
    )



@callback(Output('liste_joueurs_available_tournoi','children'),
        Input('shared-data-tournoi','data')
        )
def get_dropdown_joueurs(shared_data):
    nom_tournoi=shared_data['tournoi_name']
    discipline_tournoi=shared_data['discipline_tournoi']
    return choice_player_from_tournoi(nom_tournoi,discipline_tournoi)



@callback(
    Output('text-tournoi-tournoi', 'children'),
    Input('shared-data-tournoi','data'),
    Input('nom_equipe_createequipe_tournoi','value'),
    Input('joueurs_createequipe_tournoi','value'),
    Input('validate-button-createequipe-tournoi', 'n_clicks'),
    prevent_initial_call=True
)
def create_equipe_in_tournoi(shared_data,nom_equipe,liste_joueurs,n_clicks):
    if n_clicks==1:
        nom_tournoi=shared_data['tournoi_name']
        discipline_tournoi=shared_data['discipline_tournoi']
        print(liste_joueurs)
        print(nom_tournoi)
        print(nom_equipe)
        result=create_equipe_tournoi(nom_tournoi,nom_equipe,liste_joueurs,discipline_tournoi)
        return result
    else:
        return dash.no_update

