import pandas as pd
import dash
import numpy as np
import dash_bootstrap_components as dbc
import numpy as np
from dash import dcc, html, Input, Output,dash_table,State, callback
from flask_login import current_user
from utils.login_handler import require_login
from pymongo import MongoClient
from dao.ligue_dao import get_ligueevent_alldata,get_stat_ligue_saison

dash.register_page(__name__, path="/ligues/vos_ligues/resultats",name='Résultat de la ligue')
require_login(__name__)


def create_match_row(match):
    return dbc.Row(
        [
            dbc.Col(html.Div(f"{match['date']}", className="text-center"), width="auto"),
            dbc.Col(html.Div(f"{match['heure']}", className="text-center"), width="auto"),

            # dbc.Col(html.Div(f"{match['rank1']}", className="text-center"), width="auto"),
            # dbc.Col(html.Img(src=f"/assets/{match['team1_icon']}.png", height="40px"), width="auto"),
            dbc.Col(html.Div(match["team1"], className="text-left"), width=3),
            dbc.Col(html.Div(f"{match['score1']} - {match['score2']}", className="text-center font-weight-bold"), width="auto"),
            # dbc.Col(html.Img(src=f"/assets/{match['team2_icon']}.png", height="40px"), width="auto"),
            dbc.Col(html.Div(match["team2"], className="text-right"), width=3),
            # dbc.Col(html.Div(f"{match['rank2']}", className="text-center"), width="auto"),
            dbc.Col(html.A(html.I(className="fas fa-calendar-alt"), href="#", className="text-right"), width="auto"),
            dbc.Col(html.A(match['match_sheet'], href="#", className="text-right"), width="auto"),
        ],
        align="center",  # Align items vertically in the middle
        className="my-2"  # Add vertical spacing between rows
    )


# layout = dbc.Container(
#     [
#         html.H1("Match Results"),
#         html.Hr(),
#         # Create rows for each match
#         dbc.Row([create_match_row(match) for match in matches])
#     ],
#     fluid=True,
# )

layout=html.Div([
           html.H1("Match Results"),
html.Hr(),
    html.Div(children="Saison(s)", className="menu-title"),

html.Div(id='dropdown-saison-resultats'),
html.Div(id='resultat_ligue')
])



@callback(
           
    Output('dropdown-saison-resultats','children'),
    Input('shared-data-ligue','data')
)
def get_dropdown_saison_statligue(shared_data_ligue):
    nom_ligue=shared_data_ligue['ligue_name']
    ligue_alldata=get_ligueevent_alldata(nom_ligue)

    saisons=list(set(np.array([elem['saison'] for elem in ligue_alldata]).flatten()))
    drop=dcc.Dropdown(
                    id='saisons-to-choose-resultat',
                    options=[{"label": x, "value": x} for x in saisons],
                    clearable=False,
                    className="dropdown",
                    multi=True)
    return drop




@callback(
    Output('resultat_ligue','children'),
    Input('shared-data-ligue','data'),
    Input('saisons-to-choose-resultat','value')
)
def get_resultats_match(shared_data_ligue,saisons):
    nom_ligue=shared_data_ligue['ligue_name']
    ligue_alldata=get_ligueevent_alldata(nom_ligue, { 'saison': { '$in':saisons } })
    dates=[elem['date_enregistrement'] for elem in ligue_alldata if elem['saison'] in [saisons]]
    heure=[elem['heure_enregistrement'] for elem in ligue_alldata if elem['saison'] in [saisons]]
    donnees_synthetiques=[pd.DataFrame(elem['stat_finale']) for elem in ligue_alldata]
    match_to_dict=[{"date": dates[i],"heure": heure[i], "team1": donnees_synthetiques[i]['equipe1'], "score1": donnees_synthetiques[i]['score1'].values[0], 
      "team2": donnees_synthetiques[i]['equipe2'], "score2": donnees_synthetiques[i]['score2'].values[0], "match_sheet": "Feuille de match"} for i in range(len(dates))]
    return  dbc.Row([create_match_row(match) for match in match_to_dict])