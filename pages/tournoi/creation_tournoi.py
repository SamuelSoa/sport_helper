import pandas as pd
import dash
import dash_bootstrap_components as dbc
import numpy as np
from dash import dcc, html, Input, Output,dash_table,State, callback
from dao.tournoi_dao import create_tournoi
from flask_login import current_user
from utils.login_handler import require_login


dash.register_page(__name__, path="/tournoi/creation_tournoi")
require_login(__name__)



layout= html.Div(
    # style={'backgroundColor': '#0D1117', 'color': '#C9D1D9', 'padding': '50px'},
    children=[
        html.Div(
            style={
                'textAlign': 'center',
                'padding': '20px',
                'border': '1px solid #30363D',
                'width': '350px',
                'margin': 'auto',
                'borderRadius': '10px',
                'backgroundColor': '#161B22',
            },
            children=[
                html.Label("Nom de la ligue", style={'textAlign': 'left'}),
                dcc.Input(
                    type="text",id='tournoi_name',
                    placeholder="Entrer le nom de tournoi souhaité",
                    style={
                        'width': '100%',
                        'padding': '10px',
                        'borderRadius': '5px',
                        'border': '1px solid #30363D',
                        'backgroundColor': '#0D1117',
                        'color': '#C9D1D9',
                        'marginBottom': '20px'
                    }
                ),
                html.Button(
                    "Valider la création",id='validate_creation_tournoi', 
                    style={
                        'width': '100%',
                        'padding': '10px',
                        'borderRadius': '5px',
                        'backgroundColor': '#238636',
                        'color': '#FFFFFF',
                        'border': 'none',
                        'cursor': 'pointer'
                    }
                ),
                 html.Div(children="Discipline", className="menu-title"),
        dcc.Dropdown(
            id="discipline_tournoi",
            options=[{"label": x, "value": y} for x, y in [['Basket', 'basket'], ['Tennis', 'tennis'], ['Football', 'football'], ['Volley', 'volley']]],
            value='basket',
            clearable=False,
            className="dropdown"
        ),
        html.Div(id='text_tournoi_cree', style={'margin': '20px', 'fontSize': 20}),
            ]
        )
    ]
)



# Ligue
@callback(
    Output('text_tournoi_cree', 'children'),
    Input('validate_creation_tournoi', 'n_clicks'),
    Input('tournoi_name', 'value'),
    State('discipline_tournoi', 'value'),
    prevent_initial_call=True
)
def send_tournament_to_db(n_clicks,nom_ligue,sys_ligue,discipline):
    if not current_user.is_authenticated:
        return html.Div(["Please ", dcc.Link("login", href="/login"), " to continue"])
    if n_clicks==1:
        print(current_user)
        expression=create_tournoi(nom_tournoi,current_user.id,discipline)
        return expression
    else:
        return dash.no_update