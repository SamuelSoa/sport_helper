from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd


# layout_choix_discipline=html.Div(
#              children=[
#             html.Div(children="Discipline", className="menu-title"),
#             dcc.Dropdown(
#                 id="discipline_to_choose",
#                 options=[{"label": x, "value": y} for x,y in [['Basket 3v3','basket-3'],['Basket 5v5','basket-5'],['Football 5v5','football-5'],['Football 8v8','football-8']]],
#                 value='Basket 3v3',
#                 clearable=False,
#                 className="dropdown"
#             ),
#               html.Div(children="Nombre de periode", className="menu-title"),
#            dcc.Input(id="periode-input", type="number", value=4),
#             html.Div(children="Durée de chaque période (s)", className="menu-title"),
#            dcc.Input(id="start-time-input", type="number", value=15*60),
#            dcc.Store(id='settings-store'),
#             # Interval component to update every second
#             dcc.Interval(id='interval-component', interval=1000, n_intervals=0, disabled=True),
#             dbc.NavLink("Valider le parametrage", href="/exhibition/party", active="exact")
#            ],className='wrapper')

layout_choix_discipline = html.Div(
    children=[
        # dcc.Location(id='url', refresh=False),  # Add this component
        html.Div(children="Discipline", className="menu-title"),
        dcc.Dropdown(
            id="discipline_to_choose",
            options=[{"label": x, "value": y} for x, y in [['Basket', 'basket'], ['Tennis', 'tennis'], ['Football 5v5', 'football-5'], ['Volley', 'volley']]],
            value='basket',
            clearable=False,
            className="dropdown"
        ),
        html.Div(children="Nombre de periode", className="menu-title"),
        dcc.Input(id="periode-input", type="number", value=4),
        html.Div(children="Durée de chaque période (s)", className="menu-title"),
        dcc.Input(id="start-time-input", type="number", value=15*60),
        html.Div(children="Nom de la première équipe", className="menu-title"),
        dcc.Textarea(
        id='nomequipe1',
        value="" ,
        style={'width': '300px', 'height': '100px', 'resize': 'none', 'font-size': '14px'},
        ),
        html.Div(children="Nom des joueurs de la première équipe (séparé d'une virgule)", className="menu-title"),
        dcc.Textarea(
        id='donnees_team1',
        value="a,ab,ad,ac,aa,ae,ar,at,ag" ,
        style={'width': '300px', 'height': '100px', 'resize': 'none', 'font-size': '14px'},
        ),
        html.Div(children="Nom de la deuxième équipe", className="menu-title"),
        dcc.Textarea(
        id='nomequipe2',
        value="" ,
        style={'width': '300px', 'height': '100px', 'resize': 'none', 'font-size': '14px'},
        ),
        html.Div(children="Nom des joueurs de la deuxième équipe (séparé d'une virgule)", className="menu-title"),
        dcc.Textarea(
        id='donnees_team2',
        value="b,bv,bvk,bvd,bvvb,bv,bd",
        style={'width': '300px', 'height': '100px', 'resize': 'none', 'font-size': '14px'},
        ),
        dcc.Interval(id='interval-component', interval=1000, n_intervals=0, disabled=True),
        html.Br(),
        html.Button('Cliquez 2 fois', id='validate-button', n_clicks=0)  # Use a button for validation
    ], className='wrapper'
)

layout_choix_annotation=html.Div([
            # dcc.Location(id='url', refresh=False),  # Add this component
            html.P("Annotation d'un match", className="lead"),
            dbc.Nav(
            [dbc.NavLink("Annotation simple", href="/exhibition/party/simple", active="exact"),
            dbc.NavLink("Annotation complète", href="/exhibition/party/complete", active="exact")
            ],
            vertical="md",
            pills=True
        )
        ])






