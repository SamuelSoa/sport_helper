import dash
from dash import dcc, html, Input, Output,dash_table,State,ALL
import dash_bootstrap_components as dbc
from function_for_app import plot_team_basket
from dao.ligue_dao import get_all_data_joueurs,get_ligue_alldata
import pandas as pd

#authentif
from flask import Flask, request, redirect, session
from flask_login import login_user, LoginManager, UserMixin, logout_user, current_user
from dash.exceptions import PreventUpdate
from utils.login_handler import restricted_page
import os


# Initialize the Flask server
server = Flask(__name__)

# Set a secret key to enable session management
server.config.update(SECRET_KEY=os.getenv("SECRET_KEY", "my-secret-key"))  # Use an environment variable or a fallback key








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
        html.P(children="🏀⚽🏐🎾🏆 ", className="header-emoji"),
        html.H3(children="Sport Helper", className="display-4"),
            html.Hr(),
        html.P("L'outil idéal pour vous accompagner dans vos compétitions", className="lead"),
            html.Div(id="user-status-header"),
        dbc.Nav(
            [dbc.NavLink("Home", href="/", active="exact"),
            dbc.NavLink("Créer un compte", href="/creer_compte", active="exact"),
            dbc.NavLink("Exhibition", href="/exhibition", active="exact"),
            dbc.NavLink("Ligues", href="/ligues", active="exact"),
            dbc.NavLink("Tournoi", href="/tournoi", active="exact"),
            dbc.NavLink("Social", href="/social", active="exact"),
            dbc.NavLink("Choix des joueurs", href="/joueurs_du_match", active="exact"),
            dbc.NavLink("Paramètres", href="/parametres", active="exact")
            ],
            vertical="md",
            pills=True
        )
    ],
    style=SIDEBAR_STYLE
)

# content = html.Div(id="page-content", style=CONTENT_STYLE)
content=html.Div([dash.page_container], style=CONTENT_STYLE)

app = dash.Dash(__name__,server=server, use_pages=True,external_stylesheets=[dbc.themes.BOOTSTRAP], prevent_initial_callbacks =True)

app.layout = html.Div([
    dcc.Location(id="url"),
    dcc.Store(id='shared-data-store', storage_type='session'),
    dcc.Store(id='shared-data-ligue', storage_type='session'),
    dcc.Store(id='shared-data-store-footbasket', storage_type='session'),
    sidebar, content])

# Login manager object will be used to login / logout users
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = "/login"

# Dummy user credentials for demonstration
VALID_USERNAME_PASSWORD = get_all_data_joueurs(nom_db='Players',nom_collection='joueurs')
# User class for login handling
class User(UserMixin):
    def __init__(self, username):
        self.id = username


@login_manager.user_loader
def load_user(username):
    """Load the user by username (ID)."""
    return User(username)

@server.route('/login', methods=['POST'])
def login_button_click():
    """Handle login request."""
    if request.form:
        username = request.form['username']
        password = request.form['password']
        if VALID_USERNAME_PASSWORD.get(username) is None:
            return """invalid username and/or password <a href='/login'>login here</a>"""
        if VALID_USERNAME_PASSWORD.get(username) == password:
            login_user(User(username))
            if 'url' in session:
                if session['url']:
                    url = session['url']
                    session['url'] = None
                    return redirect(url)  # Redirect to saved URL
            return redirect('/')  # Redirect to home
        return """invalid username and/or password <a href='/login'>login here</a>"""


@app.callback(
    Output("user-status-header", "children"),
    Output('url','pathname',allow_duplicate=True),
    Input("url", "pathname"),
    Input({'index': ALL, 'type':'redirect'}, 'n_intervals'),
    prevent_initial_call=True
)
def update_authentication_status(path, n):
    """Update user authentication status and handle redirects."""
    if n:
        if not n[0]:
            return '', dash.no_update
        else:
            return '', '/login'

    if current_user.is_authenticated:
        if path == '/login':
            return dcc.Link("logout", href="/logout"), '/'
        return dcc.Link("Se deconnecter", href="/logout"), dash.no_update
    else:
        if path in restricted_page:
            session['url'] = path  # Save URL to redirect after login
            return dcc.Link("Se connecter", href="/login"), '/login'

    if current_user and path not in ['/login', '/logout']:
        return dcc.Link("Se connecter", href="/login"), dash.no_update

    if path in ['/login', '/logout']:
        return '', dash.no_update


# Callback to update the graph
@app.callback(
    Output('graph_equipe1', 'figure'),
    Input('meneur_1', 'value'),
    Input('arriere_1', 'value'),
    Input('ailier_1', 'value'),
    Input('ailier_fort_1', 'value'),
    Input('pivot_1', 'value'),
    Input('nom_1', 'value'))
def update_graph(meneur, arriere, ailier, ailier_fort, pivot, nom):
    # List of selected players
    liste_equipe = [meneur, arriere, ailier, ailier_fort, pivot]
    # Generate the figure using plot_team_basket
    fig = plot_team_basket(liste_equipe,nom)
    return fig


#version simple

# exhibition







# Callback for storing data from Layout 1
@app.callback(
    Output('shared-data-store', 'data',allow_duplicate=True),
    [Input('validate-button', 'n_clicks')],
    [State('discipline_to_choose', 'value'),
    State('periode-input', 'value'),
    State('start-time-input', 'value'),
    State('donnees_team1', 'value'),
    State('donnees_team2', 'value'),
    State('nomequipe1', 'value'),
    State('nomequipe2', 'value')
    ],prevent_initial_call=True
)
def store_data(n_clicks, input_value1,input_value2,input_value3,input_value4,input_value5,input_value6,input_value7):
    if n_clicks is None or n_clicks == 0:
        print("validate-button has not been clicked yet.")
        return dash.no_update
    dicto={'discipline_to_choose':input_value1,'periode-input':input_value2,'start-time-input':input_value3,'donnees_team1':input_value4,'donnees_team2':input_value5,
    'nomequipe1':input_value6,'nomequipe2':input_value7}
    
    print('not yet')
    print('yes')
    # dicto['data']=df_donnees_joueurs
    # dicto.update({'data': df_donnees_joueurs})
    print(f"Storing data: {dicto}")  # Debugging statement
    return dicto





# Useful for layout
@app.callback(
    Output('nom_equipe1', 'children'),Output('nom_equipe2', 'children'),  # To dynamically update the buttons
    [
    # State({'type': 'output_table_team', 'index': dash.dependencies.ALL}, 'data'),
    Input('shared-data-store', 'data')]  #,# Dropdown to choose the annotation system
)
def get_nom_equipe(shared_data):
    """ Retourne le layout des boutons"""
    # Recreate the DataFrame from the stored data
    # Call the display_annot_buttons function with the current DataFrame and annotation system
    # print('on est a update_buttons_display')
    nom_equipe1=shared_data['nomequipe1']
    nom_equipe2=shared_data['nomequipe2']
    return nom_equipe1,nom_equipe2




if __name__ == '__main__':
    app.run_server(port=8100,debug=True)

