import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
from dash import dcc, html, Input, Output,dash_table,State, callback
from flask_login import current_user
from dao.ligue_dao import get_collection



dash.register_page(__name__, path="/ligues/vos_ligues/parametres/finir_saison",name='Finir la saison')


layout=html.Div([
            html.Div(children="Choix", className="menu-title"),
dcc.Dropdown(
                id='finish_season',
                options=[{"label": x, "value": x} for x in ['Oui','Non']],
                clearable=False,
                className="dropdown",
                multi=False),
                html.Button('Confirmer la fin de la saison', id='button-confirm-finish-season', n_clicks=0),
                html.Div(id='text_finir_saison')
                ])


def changer_saison(ligue):
    collection=get_collection(database='Ligues',collection_db='ligues_info')
    results_checkligue=list(collection.find({'ligue_name':ligue}))
    saison_actuelle=results_checkligue[0]['saison']
    collection.update_one({'ligue_name':ligue},{'$push':{'saison':saison_actuelle+1}})
    return 'Saison modifié'

@callback(
    Output('text_finir_saison','children'),
    Input('shared-data-ligue','data'),
    Input('finish_season','value'),
    Input('button-confirm-finish-season','n_clicks'),
    )
def action_click_finir_season(shared_data,reponse,n_clicks):
    if n_clicks==1:
        if reponse=='Oui':
            return changer_saison(shared_data['ligue_name'])
        else:
            return 'Veuillez retourner à la page précedente'
    else:
        return dash.no_update
