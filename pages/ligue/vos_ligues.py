import pandas as pd
import dash
import dash_bootstrap_components as dbc
import numpy as np
from dash import dcc, html, Input, Output,dash_table,State, callback
from flask_login import current_user
from utils.login_handler import require_login
from pymongo import MongoClient


dash.register_page(__name__, path="/ligues/vos_ligues",name='Vos ligues')
require_login(__name__)

def get_all_ligues():
    cluster=MongoClient('mongodb+srv://mrsamu35:Samuel35-@players.lahd6.mongodb.net/?retryWrites=true&w=majority&appName=Players')
    db=cluster['Ligues']
    collection=db['ligues_info']
    liste_all=collection.find()
    liste_ligue_joueur=[[elem['ligue_name'],elem['liste_player']] for elem in liste_all]
    liste_to_fill=[]
    print(liste_ligue_joueur)
    for elem in liste_ligue_joueur:
        joueurs=elem[1]
        print(joueurs)
        if current_user.id in joueurs:
            liste_to_fill.append(elem[0])
    result=dcc.Dropdown(
            id="ligues_rejointes",
            options=[{"label": x, "value": x} for x in liste_to_fill],
            clearable=False,
            className="dropdown"
        )
    return result

def layout():
    if not current_user.is_authenticated:
        return html.Div(["Please ", dcc.Link("login", href="/login"), " to continue"])

    return html.Div(
        [html.Div(children="Vos ligues", className="menu-title"),
       get_all_ligues()
        ]
    )




layout_vosligues=html.Div([
            # dcc.Location(id='url', refresh=False),  # Add this component
            html.Div([html.Div(id='name_ligue_dropdown'),html.Div(id='code_ligue')]),
            dbc.Nav(
            [ dbc.NavLink("Ajouter un resultat", href=f"/ligues/{html.div(id='code_ligue')}/add_result", active="exact"),
            dbc.NavLink("Rencontres à venir", href="/ligues/vos_ligues/rencontres_a_venir", active="exact"),
            dbc.NavLink("Statistiques", href="/ligues/vos_ligues/statistiques", active="exact")

            ],
            vertical="md",
            pills=True
        )
        ])



