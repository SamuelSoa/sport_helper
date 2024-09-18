import dash
from dash import dcc, html, Input, Output,dash_table,State
import dash_bootstrap_components as dbc
from function_for_app import plot_team_basket

layout_connecter= html.Div(
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




layout_inscription= html.Div(
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


layout_redefine_mdp=html.Div(
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
