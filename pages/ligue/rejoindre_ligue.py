import pandas as pd
import dash
import dash_bootstrap_components as dbc
import numpy as np
from dash import dcc, html, Input, Output,dash_table,State, callback
from flask_login import current_user
from utils.login_handler import require_login
from dao.ligue_dao import join_ligue
dash.register_page(__name__, path="/ligues/rejoindre_ligue",name='Rejoindre une ligue')
require_login(__name__)



def layout():
    if not current_user.is_authenticated:
        return html.Div(["Please ", dcc.Link("login", href="/rejoindre_ligue"), " to continue"])
    return html.Div(
        [html.Div(children="Code de la ligue", className="menu-title"),
        dcc.Input(id="code_ligue"),
        html.Br(),
        html.Button('Rejoindre la ligue', id='validate-button-joinleague', n_clicks=0),  # Use a button for validation
        html.Br(),
        html.Div(id='text-joinligue',children='Pas encore rejointe'),

        ]
    )


@callback(
    Output('text-joinligue', 'children'),
    Input('validate-button-joinleague', 'n_clicks'),
    Input('code_ligue', 'value'),
    prevent_initial_call=True
)
def join_ligue_app(n_clicks,code):
    if n_clicks==1:
        result=join_ligue(current_user.id,code)
        return result
    else:
        return dash.no_update