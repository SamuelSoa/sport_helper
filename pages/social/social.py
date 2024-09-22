

import pandas as pd
import dash
import dash_bootstrap_components as dbc
import numpy as np
from dash import dcc, html, Input, Output,dash_table,State, callback
dash.register_page(__name__, path="/social",name='Social')


df_ligue = pd.DataFrame({
    'ligue': ["ligue1", "ligue2", "ligue3", "ligue4", "ligue5"],
    'abbreviation': ["l1", "l2", "l3", "l4", "l5"]
})

df_joueurs = {
    'Pseudo': ["Player1", "Player2", "Player3", "Player4", "Player5"]
}


layout=html.Div([
            dbc.Nav(
            [dbc.NavLink("Défi", href="/social/defi", active="exact"),
            dbc.NavLink("Demande de contact à une autre ligue", href="/social/demande_contact", active="exact"),
            dbc.NavLink("Classements", href="/social/classement", active="exact")
            ],
            vertical="md",
            pills=True
        )
            # html.Button('Mon compte', id='submit-val', n_clicks=0),
            # html.Button('Deconnexion', id='decconect_button', n_clicks=0),
            # html.Div(id='container-button-basic',
            #         children='Enter a value and press submit')
        ])


layout_social_classement=html.Div(
            children=[
            html.Div(children="Vos ligues possédées", className="menu-title"),
            dcc.Dropdown(
                id="ligue",
                options=[{"label": x, "value": y} for x,y in df_ligue[['abbreviation','ligue']].values.tolist()],
                value=df_ligue['ligue'][0],
                clearable=False,
                className="dropdown"
            ),   dash_table.DataTable(id="tab_cah",
                                    filter_action='native',
                                    style_header={
                                        'backgroundColor': 'rgb(30, 30, 30)',
                                        'color': 'white'
                                    },
                                    style_data={
                                        'backgroundColor': 'rgb(50, 50, 50)',
                                        'color': 'white'
                                                })])



                                                
layout_social_demande_contact=html.Div(
            children=[
            html.Div(children="Vos ligues possédées", className="menu-title"),
            dcc.Dropdown(
                id="ligue_organizer",
                options=[{"label": x, "value": x} for x in df_joueurs['Pseudo']],
                value=df_joueurs['Pseudo'][0],
                clearable=False,
                className="dropdown"
            ),  
            html.Div(children="Nom de la ligue à contacter", className="menu-title"),
            dcc.Dropdown(
                id="ligue_send",
                options=[{"label": x, "value": x} for x in df_joueurs['Pseudo']],
                value=df_joueurs['Pseudo'][0],
                clearable=False,
                className="dropdown"
            )            ,
            html.Button('Envoyer la demande', id='submit-demande-contact', n_clicks=0)            ],
            className='wrapper')
