import pandas as pd
import dash
import dash_bootstrap_components as dbc
import numpy as np
from dash import dcc, html, Input, Output,dash_table,State, callback
from dao.ligue_dao import create_ligue
from flask_login import current_user
from utils.login_handler import require_login


dash.register_page(__name__, path="/ligues/creation_ligue")
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
                    type="text",id='ligue_name',
                    placeholder="Entrer le nom de la ligue souhaitée",
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
                html.Div(children="Système de ligue", className="menu-title"),
        dcc.Dropdown(
            id="sys_ligue",
            options=[{"label": x, "value": y} for x, y in [['Equipe fixe', 'fix-teams'], ['Equipe variable', 'variable-teams']]],
            clearable=False,
            value='fix-teams',
            className="dropdown"
        ),
                html.Button(
                    "Valider la création",id='validate_creation_ligue', 
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
            id="discipline_ligue",
            options=[{"label": x, "value": y} for x, y in [['Basket', 'basket'], ['Tennis', 'tennis'], ['Football', 'football'], ['Volley', 'volley']]],
            value='basket',
            clearable=False,
            className="dropdown"
        ),
        html.Div(id='text_ligue_cree', style={'margin': '20px', 'fontSize': 20}),
            ]
        )
    ]
)



# Ligue
@callback(
    Output('text_ligue_cree', 'children'),
    Input('validate_creation_ligue', 'n_clicks'),
    Input('ligue_name', 'value'),
    State('sys_ligue', 'value'),
    State('discipline_ligue', 'value'),

    prevent_initial_call=True
)
def send_ligue_to_db(n_clicks,nom_ligue,sys_ligue,discipline):
    if not current_user.is_authenticated:
        return html.Div(["Please ", dcc.Link("login", href="/login"), " to continue"])
    if n_clicks==1:
        print(current_user)
        expression=create_ligue(nom_ligue,sys_ligue,current_user.id,discipline)
        return expression
    else:
        return dash.no_update