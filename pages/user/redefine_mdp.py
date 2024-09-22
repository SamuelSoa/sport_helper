import pandas as pd
import dash
import dash_bootstrap_components as dbc
import numpy as np
from dash import dcc, html, Input, Output,dash_table,State, callback
dash.register_page(__name__, path="/redefinir_mdp")



layout=html.Div(
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
                html.H2("Reinitialisation du mot de passe", style={'color': '#FFFFFF'}),
                html.Label("Nouveau mot de passe", style={'textAlign': 'left'}),
                dcc.Input(
                    type="password",id='new_password1',
                    placeholder="Entrez le nouveau mot de passe",
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
                html.Label("Confirmation du nouveau mot de passe", style={'textAlign': 'left'}),
                dcc.Input(
                    type="password",id='new_password2',
                    placeholder="Entrez  de nouveau le  mot de passe",
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
                    "Modifier",id='submit-password_modified', 
                    style={
                        'width': '100%',
                        'padding': '10px',
                        'borderRadius': '5px',
                        'backgroundColor': '#238636',
                        'color': '#FFFFFF',
                        'border': 'none',
                        'cursor': 'pointer'
                    }
                )])])
