import pandas as pd
import dash
import dash_bootstrap_components as dbc
import numpy as np
from dash import dcc, html, Input, Output,dash_table,State, callback
from flask_login import current_user
from utils.login_handler import require_login
from pymongo import MongoClient
from dao.ligue_dao import get_all_ligues

dash.register_page(__name__, path="/ligues/vos_ligues/ajouter_rencontre",name='Vos ligues')
require_login(__name__)




layout=html.Div([
            # dcc.Location(id='url', refresh=False),  # Add this component
            html.Div(id='display_view_quelajout')
        ])




@callback(Output('display_view_quelajout','children'),
Input('shared-data-ligue','data'))
def get_view_ajouter_ligue(shared_data):
    discipline=shared_data['discipline_ligue']
    if discipline != 'free-solo':
        result= html.Div([html.P("Quel type d'ajout ?", className="lead"),
        dbc.Nav(
            [dbc.NavLink("Annotation en direct", href="/ligues/vos_ligues/ajouter_rencontre/parametrage_rencontre", active="exact"),
            dbc.NavLink("Annotation à posteriori", href="/ligues/vos_ligues/ajouter_rencontre/annotation_posteriori", active="exact")
            ],
            vertical="md",
            pills=True
        )])
    else:
        result= html.Div([html.P("Quel type d'ajout ?", className="lead"),dbc.Nav(
            [dbc.NavLink("Annotation en direct", href="/ligues/vos_ligues/ajouter_rencontre/parametrage_rencontre_free", active="exact"),
            dbc.NavLink("Annotation à posteriori", href="/ligues/vos_ligues/ajouter_rencontre/parametrage_rencontre_free", active="exact")
            ],
            vertical="md",
            pills=True
        )])
    return result