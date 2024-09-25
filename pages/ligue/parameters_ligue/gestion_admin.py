import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
from dash import dcc, html, Input, Output,dash_table,State, callback
from flask_login import current_user
from dao.ligue_dao import get_collection



dash.register_page(__name__, path="/ligues/vos_ligues/parametres/gestion_admin",name="Modifier les droits d'admin")


layout=html.Div([
                html.Div(children="Choix", className="menu-title"),
                dcc.Dropdown(
                id='change_admin',
                options=[{"label": x, "value": x} for x in ['Ajouter des admins','Ceder le droit à un autre joueur','Rester tel quel']],
                clearable=False,
                className="dropdown",
                multi=False),
                html.Button('Confirmer le choix', id='button-confirm-choice', n_clicks=0),
                html.Div(id='liste_nouveau'),
                html.Div(id='text_change_admin')
                ])


def modifier_admin(ligue,nouvelle_liste,decision_changeradmin):
    if decision_changeradmin=='Ajouter des admins':
        nouvelle_liste.append(current_user.id)
    collection=get_collection(database='Ligues',collection_db='ligues_info')
    results_checkligue=list(collection.find({'ligue_name':ligue}))
    liste_joueur=results_checkligue[0]['liste_player']
    # indice_nouveaux_admin=[liste_joeuurs.index(admin) for admin in nouvelle_liste]
    nouveaux_roles=['admin' if joueur in nouvelle_liste else 'user' for joueur in liste_joueur ]
    collection.update_one({'ligue_name':ligue},{'$set':{'liste_role':nouveaux_roles}})
    return 'Roles modifié'


@callback(
    Output('liste_nouveau','children'),
    Input('shared-data-ligue','data'),
    Input('change_admin','value'),
    Input('button-confirm-choice','n_clicks'),
    )
def action_choice_drop_decisionadmin(shared_data,reponse,n_clicks):
    liste_joueurs=shared_data['liste_player']
    liste_joueurs_sans_admin=[elem for elem in liste_joueurs if elem!=current_user.id]
    if n_clicks==1:
        if reponse=='Ajouter des admins':
            result=html.Div([html.Div(children="Admins supplémentaires", className="menu-title"),dcc.Dropdown(
                id='candidats',
                options=[{"label": x, "value": x} for x in liste_joueurs_sans_admin],
                clearable=False,
                className="dropdown",
                multi=True),html.Button("Confirmer l'ajout d'admin(s)", id='button-confirm-change-admin', n_clicks=0)])
        elif reponse=='Ceder le droit à un ou plusieurs joueurs':
            result=html.Div([html.Div(children="Nouveaux admins", className="menu-title"),dcc.Dropdown(
                id='candidats',
                options=[{"label": x, "value": x} for x in liste_joueurs_sans_admin],
                clearable=False,
                className="dropdown",
                multi=True),html.Button("Confirmer l'octroi de droit", id='button-confirm-change-admin', n_clicks=0)])
        else:
            return html.P('Veuillez retourner à la page précedente')
        return result
    else:
        return dash.no_update





@callback(
    Output('text_change_admin','children'),
    Input('shared-data-ligue','data'),
    Input('candidats','value'),
    Input('button-confirm-change-admin','n_clicks'),
    Input('change_admin','value')
    )
def action_click_change_admin(shared_data,nouvelle_liste,n_clicks,reponse_changeadmin):

    if n_clicks==1:
        ligue=shared_data['ligue_name']
        if reponse_changeadmin!='Rester tel quel':
            return modifier_admin(ligue,nouvelle_liste,reponse_changeadmin)
        else:
            return ''
    else:
        return dash.no_update
