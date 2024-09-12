import dash
from dash import dcc, html, Input, Output,dash_table,State
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import pandas as pd
from function_for_app import plot_team_basket
from layout_page import *

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
df_joueurs = {
    'Pseudo': ["Player1", "Player2", "Player3", "Player4", "Player5"]
}

df_equipe = {
    'equipe': ["Team1", "Team2", "Team3", "Team4", "Team5"],
    'abbreviation': ["t1", "t2", "t3", "t4", "t5"]
}


df_ligue = {
    'ligue': ["ligue1", "ligue2", "ligue3", "ligue4", "ligue5"],
    'abbreviation': ["l1", "l2", "l3", "l4", "l5"]
}

# Dash layout

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa"
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem"
}

sidebar = html.Div(
    [
        html.P(children="🏀", className="header-emoji"),
        html.H3(children="Basketball Analytics", className="display-4"),
            html.Hr(),
        html.P("Analyse de données de basketball", className="lead"),
        dbc.Nav(
            [dbc.NavLink("Home", href="/", active="exact"),
            dbc.NavLink("Exhibition", href="/exhibition", active="exact"),
            dbc.NavLink("Ligues", href="/ligues", active="exact"),
            dbc.NavLink("Tournoi", href="/tournoi", active="exact"),
            dbc.NavLink("Social", href="/social", active="exact"),
            dbc.NavLink("Paramètres", href="/parametres", active="exact"),
            dbc.NavLink("Choix des joueurs", href="/joueurs_du_match", active="exact")
            ],
            vertical="md",
            pills=True
        )
    ],
    style=SIDEBAR_STYLE
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

layout_choix_joueurs=html.Div(
             children=[
            html.Div(children="Point Guard", className="menu-title"),
            dcc.Dropdown(
                id="meneur_1",
                options=[{"label": x, "value": x} for x in df_joueurs['Pseudo']],
                value=df_joueurs['Pseudo'][0],
                clearable=False,
                className="dropdown"
            ),
            html.Div(children="Shooting Guard", className="menu-title"),
            dcc.Dropdown(
                id="arriere_1",
                options=[{"label": y, "value": y} for y in df_joueurs['Pseudo']],
                value=df_joueurs['Pseudo'][1],
                clearable=False,
                className="dropdown"
            ),
            html.Div(children="Small Forward", className="menu-title"),
            dcc.Dropdown(
                id="ailier_1",
                options=[{"label": y, "value": y} for y in df_joueurs['Pseudo']],
                value=df_joueurs['Pseudo'][2],
                clearable=False,
                className="dropdown"
            ),
            html.Div(children="Power Forward", className="menu-title"),
            dcc.Dropdown(
                id="ailier_fort_1",
                options=[{"label": y, "value": y} for y in df_joueurs['Pseudo']],
                value=df_joueurs['Pseudo'][3],
                clearable=False,
                className="dropdown"
            ),
            html.Div(children="Center", className="menu-title"),
            dcc.Dropdown(
                id="pivot_1",
                options=[{"label": y, "value": y} for y in df_joueurs['Pseudo']],
                value=df_joueurs['Pseudo'][4],
                clearable=False,
                className="dropdown"
            ),    
            html.Div(children="Nom de l'équipe", className="menu-title"),
            dcc.Input(id='nom_1',type='text')
            ,
            dcc.Graph(id='graph_equipe1')
            ],
            className='wrapper')

layout_parameters=html.Div([
            dbc.Nav(
            [dbc.NavLink("Mon compte", href="/parameters/account", active="exact"),
            dbc.NavLink("Deconnexion", href="/deconnextion", active="exact")
            ],
            vertical="md",
            pills=True
        )
            # html.Button('Mon compte', id='submit-val', n_clicks=0),
            # html.Button('Deconnexion', id='decconect_button', n_clicks=0),
            # html.Div(id='container-button-basic',
            #         children='Enter a value and press submit')
        ])

layout_tournoi=html.Div([
            html.P("Création d'un tournoi", className="lead"),
            
            dbc.Nav(
            [dbc.NavLink("Créer un tournoi", href="/tournoi/creation", active="exact"),
            dbc.NavLink("Tournois actuelles", href="/tournoi/tournoi_actuel", active="exact")
            ],
            vertical="md",
            pills=True
        )
            # html.Button('Mon compte', id='submit-val', n_clicks=0),
            # html.Button('Deconnexion', id='decconect_button', n_clicks=0),
            # html.Div(id='container-button-basic',
            #         children='Enter a value and press submit')
        ])

layout_creer_tournoi=html.Div(
            children=[
            html.Div(children="Intitulé du tournoi", className="menu-title"),
            dcc.Input(id='nom_1',type='text'),
            html.Div(children="Equipes participantes", className="menu-title"),
            dcc.Dropdown(
                id="equipes_tournoi",
                options=[{"label": x, "value": y} for x,y in df_equipe[['abbreviation','equipe']]],
                clearable=False,
                className="dropdown",
                multi=True
            )])



layout_social=html.Div([
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
                options=[{"label": x, "value": y} for x,y in df_ligue['abbreviation','ligue']],
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

@callback(
    Output('container-button-basic', 'children'),
    Input('submit-demande-contact', 'n_clicks'),
    prevent_initial_call=True
)
def check_send_message(n_clicks, value):
    return 'Le message a bien été envoyé'

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
            html.Button('Envoyer la demaande', id='submit-demande-contact', n_clicks=0)            ],
            className='wrapper')



# Callback to update the graph
@app.callback(
    Output('graph_equipe1', 'figure'),
    Input('meneur_1', 'value'),
    Input('arriere_1', 'value'),
    Input('ailier_1', 'value'),
    Input('ailier_fort_1', 'value'),
    Input('pivot_1', 'value'),
    Input('nom_1', 'value')
)
def update_graph(meneur, arriere, ailier, ailier_fort, pivot, nom):
    # List of selected players
    liste_equipe = [meneur, arriere, ailier, ailier_fort, pivot]
    # Generate the figure using plot_team_basket
    fig = plot_team_basket(liste_equipe,nom)
    return fig


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return html.P("Bienvenue sur l'application! Vous pourriez annoter vos matchs de basketball et de football en direct")
    elif pathname == "/exhibition":
        return html.P("Bienvenue sur l'application! Vous pourriez annoter vos matchs de basketball et de football en direct")
    elif pathname == "/ligues":
        return html.P("Bienvenue sur l'application! Vous pourriez annoter vos matchs de basketball et de football en direct")
    elif pathname == "/tournoi":
        return layout_tournoi
    elif pathname == "/social":
        return layout_social
    elif pathname==('/social/demande_contact'):
        return layout_social_demande_contact
    elif pathname==('/social/classement'):
        return layout_social_classement
    elif pathname=='/joueurs_du_match':
        return  layout_choix_joueurs
    elif pathname == "/parametres":
        return layout_parameters
    elif pathname=='/parameters/account':
        return html.P("Bienvenue sur l'application! Vous pourriez annoter vos matchs de basketball et de football en direct")

   

if __name__ == '__main__':
    app.run_server(port=8100)

