import pandas as pd
import dash
import dash_bootstrap_components as dbc
import numpy as np
from dash import dcc, html, Input, Output,dash_table,State, callback
from flask_login import current_user
from utils.login_handler import require_login
from pymongo import MongoClient
from dao.ligue_dao import get_all_ligues

dash.register_page(__name__, path="/ligues/vos_ligues/statistiques",name='Vos ligues')
require_login(__name__)


layout=html.Div([
html.Div(id='button_choice_stat')
])



@callback(
    Output('button_choice_stat','children'),
    Input('shared-data-ligue','data')
)
def render_button_stat(shared_data_ligue):
    sys_ligue=shared_data_ligue['sys_ligue']
    if sys_ligue=='fix-teams':
        layout_stat_general=dbc.Nav(
                            [
                            dbc.NavLink("Parcourir les statistiques par équipe", href=f"/ligues/vos_ligues/statistiques/statistiques_teams", active="exact"),
                            dbc.NavLink("Statistiques de la ligue", href="/ligues/vos_ligues/statistiques/statistiques_ligue", active="exact"),
                            dbc.NavLink("Performance des joueurs", href="/ligues/vos_ligues/statistiques/player_performance", active="exact")

                            ],
                            vertical="md",
                            pills=True
                        )

    elif sys_ligue=='variable-teams':
        layout_stat_general=dbc.Nav(
                    [
                    dbc.NavLink("Statistiques de la ligue", href="/ligues/vos_ligues/statistiques/statistiques_ligue", active="exact"),
                    dbc.NavLink("Performance des joueurs", href="/ligues/vos_ligues/statistiques/player_performance", active="exact")

                    ],
                    vertical="md",
                    pills=True
                )
    print('on y est')
    return layout_stat_general
