import pandas as pd
import dash
import dash_bootstrap_components as dbc
import numpy as np
from dash import dcc, html, Input, Output,dash_table,State, callback
from flask_login import current_user
from utils.login_handler import require_login
from dao.tournoi_dao import join_tournoi
dash.register_page(__name__, path="/ligues/rejoindre_tournoi",name='Rejoindre un tournoi')
require_login(__name__)



def layout():
    if not current_user.is_authenticated:
        return html.Div(["Please ", dcc.Link("login", href="/rejoindre_tournoi"), " to continue"])
    return html.Div(
        [html.Div(children="Code du tournoi", className="menu-title"),
        dcc.Input(id="code_tournoi"),
        html.Br(), html.Div(children="Discipline", className="menu-title"),
        dcc.Dropdown(
            id="discipline_tournoi",
            options=[{"label": x, "value": y} for x, y in [['Basket', 'basket'], ['Tennis', 'tennis'], ['Football', 'football'], ['Volley', 'volley']]],
            value='basket',
            clearable=False,
            className="dropdown"
        ),
        html.Button('Rejoindre le tournoi', id='validate-button-jointournoi', n_clicks=0),  # Use a button for validation
        html.Br(),
        html.Div(id='text-joinligue',children='Pas encore rejoint'),

        ]
    )


@callback(
    Output('text-jointournoi', 'children'),
    Input('validate-button-jointournoi', 'n_clicks'),
    Input('code_tournoi', 'value'),
        Input('discipline_tournoi', 'value'),

    prevent_initial_call=True
)
def join_tournoi_app(n_clicks,code,discipline_tournoi):
    if n_clicks==1:
        result=join_tournoi(username=current_user.id,code_tournoi=code,discipline_tournoi=discipline_tournoi)
        return 'Tournoi joint avec succès'
    else:
        return dash.no_update