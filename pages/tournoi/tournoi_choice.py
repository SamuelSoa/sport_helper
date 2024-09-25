import pandas as pd
import dash
import dash_bootstrap_components as dbc
import numpy as np
from dash import dcc, html, Input, Output,dash_table,State, callback


dash.register_page(__name__, path="/tournoi",name='Tournoi')

layout=html.Div([
            dcc.Location(id='url', refresh=False),  # Add this component
            html.P("Tournoi", className="lead"),
            dbc.Nav(
            [dbc.NavLink("Vos tournoi", href="/tournoi/vos_tournoi", active="exact"),
            dbc.NavLink("Créer un tournoi", href="tournoi/creation_tournoi", active="exact"),
            dbc.NavLink("Rejoindre un tournoi", href="/tournoi/rejoindre_tournoi", active="exact")
            ],
            vertical="md",
            pills=True
        )
        ])


