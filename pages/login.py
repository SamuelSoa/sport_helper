import dash
from dash import html, dcc


dash.register_page(__name__)

# Login screen
# layout = html.Form(
#     [
#         html.H2("Please log in to continue:", id="h1"),
#         dcc.Input(placeholder="Enter your username", type="text", id="uname-box", name='username'),
#         dcc.Input(placeholder="Enter your password", type="password", id="pwd-box", name='password'),
#         html.Button(children="Login", n_clicks=0, type="submit", id="login-button"),
#         html.Div(children="", id="output-state")
#     ], method='POST'
# )


layout= html.Form(
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
                # html.H2("Please log in to continue:", id="h1"),
                html.H2("Se connecter à l'application", id="h1", style={'color': '#FFFFFF'}),
                html.Label("Pseudo", style={'textAlign': 'left'}),
                dcc.Input(
                    type="text",id='uname-box', name='username',
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
                    type="password",id='pwd-box', name='password',
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
                    n_clicks=0,type='submit',
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
                ),
        html.Div(children="", id="output-state")
            ]
        )
    ],method='POST'
)