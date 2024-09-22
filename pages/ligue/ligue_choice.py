import pandas as pd
import dash
import dash_bootstrap_components as dbc
import numpy as np
from dash import dcc, html, Input, Output,dash_table,State, callback


dash.register_page(__name__, path="/ligues",name='Ligues')

layout=html.Div([
            # dcc.Location(id='url', refresh=False),  # Add this component
            html.P("Ligue", className="lead"),
            dbc.Nav(
            [dbc.NavLink("Vos ligues", href="/ligues/vos_ligues", active="exact"),
            dbc.NavLink("Créer une ligue", href="ligues/creation_ligue", active="exact"),
            dbc.NavLink("Rejoindre une ligue", href="/ligues/rejoindre_ligue", active="exact"),
            dbc.NavLink("Créer une fédération", href="ligues/creation_federation", active="exact")

            ],
            vertical="md",
            pills=True
        )
        ])


