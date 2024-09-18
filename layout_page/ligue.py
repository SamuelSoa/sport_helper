import dash
from dash import dcc, html, Input, Output,dash_table
import dash_bootstrap_components as dbc
from function_for_app import plot_team_basket
import pandas as pd



layout_creer_ligue= html.Div(
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
                )
            ]
        )
    ]
)
