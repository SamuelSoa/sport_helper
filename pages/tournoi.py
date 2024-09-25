import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
from dash import dcc, html, Input, Output,dash_table,State, callback


dash.register_page(__name__, path="/tournoi",name='Tournoi')


df_equipe = pd.DataFrame({
    'equipe': ["Team1", "Team2", "Team3", "Team4", "Team5"],
    'abbreviation': ["t1", "t2", "t3", "t4", "t5"]
})
layout=html.Div([
            html.P("Création d'un tournoi", className="lead"),
            dbc.Nav(
            [dbc.NavLink("Créer un tournoi", href="/tournoi/creation", active="exact"),
            dbc.NavLink("Tournois actuelles", href="/tournoi/tournoi_actuel", active="exact")
            ],
            vertical="md",
            pills=True
        )
            # html.Button('Mon compte', id='submit-val', n_clicks=0),
            # html.Button('Deconnexion', id='decconect_button', n_clicks=0),
            # html.Div(id='container-button-basic',
            #         children='Enter a value and press submit')
        ])

layout_creer_tournoi=html.Div(
            children=[
            html.Div(children="Intitulé du tournoi", className="menu-title"),
            dcc.Input(id='nom_1',type='text'),
            html.Div(children="Equipes participantes", className="menu-title"),
            dcc.Dropdown(
                id="equipes_tournoi",
                options=[{"label": x, "value": y} for x,y in df_equipe[['abbreviation','equipe']].values.tolist()],
                clearable=False,
                className="dropdown",
                multi=True
            )])
