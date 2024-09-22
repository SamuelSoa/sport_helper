import pandas as pd
import dash
import dash_bootstrap_components as dbc
import numpy as np
from dash import dcc, html, Input, Output,dash_table,State, callback
# dash.register_page(__name__, path="/",name='Home')



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
                html.H2("Se connecter à l'application", style={'color': '#FFFFFF'}),
                html.Label("Pseudo ou email", style={'textAlign': 'left'}),
                dcc.Input(
                    type="email",id='identifiant1',
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
                    type="password",id='password1',
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
                    "Se connecter", id='login-button',
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
                    html.Div(id='login-output', style={'marginTop': '20px'}),  # Where message is printed
                html.Div(
                    html.A("Mot de passe oublié?", href="redefinir_mdp", style={'color': '#58A6FF'}),
                    style={'textAlign': 'right', 'marginTop': '10px'}
                ),
                html.Div(
                    [
                        html.A("Nouveau sur l'application? Creez un compte", href="creer_compte", style={'color': '#58A6FF'})
                    ],
                    style={'textAlign': 'center', 'marginTop': '20px'}
                )
            ]
        )
    ]
)





### Connexion ###
@callback(Output('login-output', 'children'),
    [Input('login-button', 'n_clicks')],
    [State('identifiant1', 'value'), State('password1', 'value')])
def update_login(n_clicks, username, password):
    if n_clicks > 0:
        if username and password:
            collection=get_collection(database='Players',collection_db='joueurs')
            result=collection.find({'pseudo_joueur':username,'password_joueur':password})
            if len(list(result))==1:
                return html.P("Connecté avec succès!", style={'color': 'green'})
            else:
                return html.P("Identifiant ou mot de passe incorrect", style={'color': 'red'})
        else:
            return html.P("Veuillez remplir tous les champs.", style={'color': 'red'})