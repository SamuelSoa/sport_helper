import pandas as pd
import dash
import dash_bootstrap_components as dbc
import numpy as np
from dash import dcc, html, Input, Output,dash_table,State, callback
from dao.ligue_dao import get_collection,create_joueur
dash.register_page(__name__, path="/creer_compte")


layout= html.Div(
    # style={'backgroundColor': '#0D1117', 'color': '#C9D1D9', 'padding': '50px'},
    style={ 'color': '#C9D1D9', 'padding': '50px'},

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
                html.H2("S'inscrire à l'application", style={'color': '#FFFFFF'}),
                html.Label("Email", style={'textAlign': 'left'}),
                dcc.Input(
                    type="email",id='mail_newuser',
                    placeholder="Entrez votre mail",
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
                html.Label("Pseudo", style={'textAlign': 'left'}),
                dcc.Input(
                    type="email",id='identifiant_newuser',
                    placeholder="Entrez votre identifiant",
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
                html.Label("Mot de passe", style={'textAlign': 'left'}),
                dcc.Input(
                    type="password",id='password_newuser',
                    placeholder="Entrez votre mot de passe",
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
                    "Valider l'inscription",  id='sign_in_button',
                    n_clicks=0,
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
                 html.Div(id='sign_in-output', style={'marginTop': '20px'}),  # Where message is printed

            ]
        )
    ]
)
### Inscription ###
@callback(Output('sign_in-output', 'children'),
                [Input('sign_in_button', 'n_clicks')],
                [State('mail_newuser','value'),State('identifiant_newuser', 'value'), State('password_newuser', 'value')])
def update_signin(n_clicks,email, username, password):
    if n_clicks > 0:
        if username and password and email:
            collection=get_collection(database='Players',collection_db='joueurs')
            result=collection.find({'mail':email,'pseudo':username,'password':password})
            if len(list(result))==1:
                return html.P("Le profil existe deja", style={'color': 'green'})
            else:
                create_joueur(email,username,password)
                return html.P("Profil crée avec succès. Veuillez retourner à la page précedente", style={'color': 'green'})

        else:
            return html.P("Veuillez remplir tous les champs.", style={'color': 'red'})

