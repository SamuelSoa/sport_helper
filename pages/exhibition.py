import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
from dash import dcc, html, Input, Output,dash_table,State, callback


dash.register_page(__name__, path="/exhibition",name='Exhibition')

layout = html.Div(
    children=[
        # dcc.Location(id='url', refresh=False),  # Add this component
        html.Div(children="Discipline", className="menu-title"),
        dcc.Dropdown(
            id="discipline_to_choose",
            options=[{"label": x, "value": y} for x, y in [['Basket', 'basket'], ['Tennis', 'tennis'], ['Football', 'football'], ['Volley', 'volley']]],
            value='basket',
            clearable=False,
            className="dropdown"
        ),
        
        html.Div(children="Nom de la première équipe", className="menu-title"),
        dcc.Textarea(
        id='nomequipe1',
        value="t1" ,
        style={'width': '300px', 'height': '100px', 'resize': 'none', 'font-size': '14px'},
        ),
        html.Div(children="Nom des joueurs de la première équipe (séparé d'une virgule)", className="menu-title"),
        dcc.Textarea(
        id='donnees_team1',
        value="at,ag" ,
        style={'width': '300px', 'height': '100px', 'resize': 'none', 'font-size': '14px'},
        ),
        html.Div(children="Nom de la deuxième équipe", className="menu-title"),
        dcc.Textarea(
        id='nomequipe2',
        value="t2" ,
        style={'width': '300px', 'height': '100px', 'resize': 'none', 'font-size': '14px'},
        ),
        html.Div(children="Nom des joueurs de la deuxième équipe (séparé d'une virgule)", className="menu-title"),
        dcc.Textarea(
        id='donnees_team2',
        value="bv,bd",
        style={'width': '300px', 'height': '100px', 'resize': 'none', 'font-size': '14px'},
        ),
        html.P("Pour le football et le basket", className="lead"),
        html.Div(children="Nombre de periode", className="menu-title"),
        dcc.Input(id="periode-input", type="number", value=4),
        html.Div(children="Durée de chaque période (s)", className="menu-title"),
        dcc.Input(id="start-time-input", type="number", value=10),
        dcc.Interval(id='interval-component', interval=1000, n_intervals=0, disabled=True),
        html.Br(),
        html.Button('Cliquez 2 fois', id='validate-button', n_clicks=0)  # Use a button for validation
    ], className='wrapper'
)

# layout_choix_annotation=html.Div([
#             # dcc.Location(id='url', refresh=False),  # Add this component
#             html.P("Annotation d'un match", className="lead"),
#             dbc.Nav(
#             [dbc.NavLink("Annotation simple", href="/exhibition/party/simple", active="exact"),
#             dbc.NavLink("Annotation complète", href="/exhibition/party/complete", active="exact")
#             ],
#             vertical="md",
#             pills=True
#         )
#         ])




@callback(
    Output('url', 'pathname',allow_duplicate=True),
    Input('validate-button', 'n_clicks'),
    State('shared-data-store', 'data'),
    prevent_initial_call=True
)
def navigate(n_clicks,shared_data):
    discipline=shared_data['discipline_to_choose']
    # premier click va permettre d'avoir la valeur de shared_data, deuxième permet d'obtenir discipline
    if n_clicks >=2 and discipline =='basket':
        return '/exhibition/party_basket'  # Navigate to the desired page
    elif n_clicks >=2 and discipline =='tennis':
        return '/exhibition/party_tennis'  # Navigate to the desired page
    elif n_clicks >=2 and discipline =='volley':
        return '/exhibition/party_volley'  # Navigate to the desired page
    elif n_clicks >=2 and discipline =='football':
        return '/exhibition/party_foot'  # Navigate to the desired page
    return dash.no_update

