import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
from dash import dcc, html, Input, Output,dash_table,State, callback
from flask_login import current_user
from dao.ligue_dao import get_collection



dash.register_page(__name__, path="/ligues/vos_ligues/parametres",name='Parametres')



layout=html.Div([
            html.Div(id='view_ligue_parameters')
        ])





@callback(
    Output('view_ligue_parameters','children'),
    Input('shared-data-ligue','data') 
)
def get_view_parameter_ligue(shared_data):

    index_username=shared_data['liste_player'].index(current_user.id)
    statut_utilisateur=shared_data['liste_role'][index_username]
    if statut_utilisateur=='admin':
        layout_vosligues=html.Div([
                                    dbc.Nav(
                [
                dbc.NavLink("Finir la saison", href="/ligues/vos_ligues/parametres/finir_saison", active="exact"),
                dbc.NavLink("Gestion des administrateurs", href="/ligues/vos_ligues/parametres/gestion_admin", active="exact")
                # dbc.NavLink("Suprimmer la ligue", href="/ligues/vos_ligues/parametres/supprimer la ligue", active="exact")
                ],
                vertical="md",
                pills=True
            )
                                ])
    else:
        layout_vosligues=html.Div([])


    return layout_vosligues
       



@callback(
    Output('drop_finir_season','children'),
    Input('submit-end-season','n_clicks'))
def action_click_finir_season(n_clicks):
    if n_clicks==1:
        return html.Div([dcc.Dropdown(
                id='finish_season',
                options=[{"label": x, "value": x} for x in ['Oui','Non']],
                clearable=False,
                className="dropdown",
                multi=False)],
                html.Button('Confirmer la fin de la saison', id='button-confirm-finish-season', n_clicks=0)
                )
    else:
        return dash.no_update




def changer_saison(ligue):
    collection=get_collection(database='Ligues',collection_db='ligues_info')
    results_checkligue=list(collection.find({'ligue_name':ligue}))
    saison_actuelle=results_checkligue[0]['saison']
    collection.updateOne({'ligue_name':ligue},{'$set':{'saison':saison_actuelle+1}})
    return 'Saison modifié'

@callback(
    Output('text_finir_ligue','children'),
    Input('shared-data-ligue','data'),
    Input('finish_season','n_clicks'),
    Input('button-confirm-finish-season','value'),
    )
def action_click_finir_season(shared_data,reponse,n_clicks):
    if n_clicks==1:
        if reponse=='Oui':
            return changer_saison(shared_data['ligue_name'])
        else:
            return 'Veuillez retourner à la page précedente'
    else:
        return dash.no_update
