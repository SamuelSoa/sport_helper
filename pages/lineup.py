from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
df_joueurs = {
    'Pseudo': ["Player1", "Player2", "Player3", "Player4", "Player5"]
}

df_equipe = pd.DataFrame({
    'equipe': ["Team1", "Team2", "Team3", "Team4", "Team5"],
    'abbreviation': ["t1", "t2", "t3", "t4", "t5"]
})


df_ligue = pd.DataFrame({
    'ligue': ["ligue1", "ligue2", "ligue3", "ligue4", "ligue5"],
    'abbreviation': ["l1", "l2", "l3", "l4", "l5"]
})






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

