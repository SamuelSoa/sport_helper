import pandas as pd
import dash
import dash_bootstrap_components as dbc
import numpy as np
from dash import dcc, html, Input, Output,dash_table,State, callback
from flask_login import current_user
from utils.login_handler import require_login
from pymongo import MongoClient
from dao.ligue_dao import get_all_ligues,get_ligue_alldata

dash.register_page(__name__, path="/ligues/vos_ligues",name='Vos ligues')
require_login(__name__)



def layout():
    if not current_user.is_authenticated:
        return html.Div(["Please ", dcc.Link("login", href="/login"), " to continue"])
    return html.Div(
        [html.Div(children="Vos ligues", className="menu-title"),
       get_all_ligues(),
        html.Button("Afficher votre ligue", id='button-displayligue', n_clicks=0),  # Use a button for validation
        html.Div(id='view_ligue', style={'padding': '20px'})

        ]
    )






@callback(
    Output('view_ligue','children'),
    Output('shared-data-ligue','data'),
    Input('ligues_rejointes','value'),
    Input('button-displayligue','n_clicks')
)
def get_view_ligue(ligue,n_clicks):
    if ligue:
        if n_clicks>=1:
            dicto=get_ligue_alldata(ligue)
            if dicto['sys_ligue']=='fixed-teams':
                layout_vosligues=html.Div([
                            # dcc.Location(id='url', refresh=False),  # Add this component
                            html.Div([html.P(ligue),html.P(dicto['id_share_ligue'])],className='wrapper'),
                            dbc.Nav(
                            [
                            dbc.NavLink("Ajouter une rencontre", href=f"/ligues/vos_ligues/ajouter_rencontre", active="exact"),
                            dbc.NavLink("Ajouter une équipe", href=f"/ligues/vos_ligues/ajouter_equipe", active="exact"),
                            # dbc.NavLink("Rencontres à venir", href="/ligues/vos_ligues/rencontres_a_venir", active="exact"),
                            dbc.NavLink("Statistiques", href="/ligues/vos_ligues/statistiques", active="exact"),
                            dbc.NavLink("Résultats", href="/ligues/vos_ligues/resultats", active="exact"),
                            dbc.NavLink("Paramètres", href="/ligues/vos_ligues/parametres", active="exact")



                            # dbc.NavLink("Statistiques", href="/ligues/"+ligue.replace(' ','')+"/statistiques", active="exact")
                            ],
                            vertical="md",
                            pills=True
                        )
                        ])
            else:
                layout_vosligues=html.Div([
                            # dcc.Location(id='url', refresh=False),  # Add this component
                            html.Div([html.P(ligue),html.P(dicto['id_share_ligue'])],className='wrapper'),
                            dbc.Nav(
                            [
                            dbc.NavLink("Ajouter un resultat", href=f"/ligues/vos_ligues/ajouter_rencontre", active="exact"),
                            # dbc.NavLink("Rencontres à venir", href="/ligues/vos_ligues/rencontres_a_venir", active="exact"),
                            dbc.NavLink("Statistiques", href="/ligues/vos_ligues/statistiques", active="exact"),
                            dbc.NavLink("Résultats", href="/ligues/vos_ligues/resultats", active="exact"),
                            dbc.NavLink("Paramètres", href="/ligues/vos_ligues/parametres", active="exact")

                            ],
                            vertical="md",
                            pills=True
                        )
                        ])
           
            print(ligue)
            print(dicto)
            return layout_vosligues,dicto
        else:
            return dash.no_update,dash.no_update
    else:
        return dash.no_update,dash.no_update
    



# @callback(
#     Output('view_ligue','children'),
#     Input('ligues_rejointes','value')
# )
# def get_view_ligue(ligue):
#     if ligue:
#         layout_vosligues=html.Div([
#                     # dcc.Location(id='url', refresh=False),  # Add this component
#                     html.Div([html.Div(id='ligues_rejointes'),html.Div(id='code_ligue')]),
#                     dbc.Nav(
#                     [
#                     dbc.NavLink("Ajouter un resultat", href=f"/ligues/"+ligue.replace(' ','')+"/add_result", active="exact"),
#                     dbc.NavLink("Rencontres à venir", href="/ligues/"+ligue.replace(' ','')+"/rencontres_a_venir", active="exact"),
#                     dbc.NavLink("Statistiques", href="/ligues/"+ligue.replace(' ','')+"/statistiques", active="exact")
#                     ],
#                     vertical="md",
#                     pills=True
#                 )
#                 ])
#         return layout_vosligues
#     else:
#         return dash.no_update
    

