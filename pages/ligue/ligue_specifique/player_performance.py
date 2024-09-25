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

dash.register_page(__name__, path="/ligues/vos_ligues/statistiques/player_performance",name='Vos ligues')
require_login(__name__)


layout=html.Div([
    html.H1('Panel des statistiques des joueurs'),
html.Div(id='dropdown-saison-statligue2'),
html.Br(),
html.Div(id='dropdown-player-statligue'),
html.Br(),
html.Div(id='dashtable_datasaison')
])


@callback(
    Output('dropdown-saison-statligue2','children'),
    Input('shared-data-ligue','data'),

)
def get_dropdown_saison_statligue(shared_data_ligue):
    nom_ligue=shared_data_ligue['ligue_name']
    ligue_alldata=get_ligueevent_alldata(nom_ligue)

    saisons=list(set(np.array([elem['saison'] for elem in ligue_alldata]).flatten()))
    drop=html.Div([html.Div(children="Saison(s)", className="menu-title"),dcc.Dropdown(
                    id='saisons-to-choose-statligue2',
                    options=[{"label": x, "value": x} for x in saisons],
                    clearable=False,
                    className="dropdown",
                    multi=True)])
    return drop

@callback(
    Output('dropdown-player-statligue','children'),
    Input('shared-data-ligue','data'),
    Input('saisons-to-choose-statligue2','value')

)
def get_dropdown_player_statligue(shared_data_ligue,saisons):
    nom_ligue=shared_data_ligue['ligue_name']
    ligue_alldata=get_ligueevent_alldata(nom_ligue)
    print(f"alldata {ligue_alldata}")
    liste_joueur=np.unique(np.array([elem['joueurs_equipe1']+elem['joueurs_equipe2'] for elem in ligue_alldata if elem['saison'][0] in saisons]).flatten())
    drop=html.Div([html.Div(children="Joueur", className="menu-title"),dcc.Dropdown(
                    id='player-to-choose-statligue',
                    options=[{"label": x, "value": x} for x in liste_joueur],
                    clearable=False,
                    className="dropdown",
                    multi=False)])
    return drop



    
@callback(
    Output('dashtable_datasaison','children'),
    Input('shared-data-ligue','data'),
    Input('saisons-to-choose-statligue2','value'),
        Input('player-to-choose-statligue','value')

)
def get_allboxscore_player(shared_data_ligue,saisons,joueur):

    nom_ligue=shared_data_ligue['ligue_name']
    ligue_alldata=get_ligueevent_alldata(nom_ligue)
    liste_joueur=np.unique(np.array([elem['joueurs_equipe1']+elem['joueurs_equipe2'] for elem in ligue_alldata]).flatten())
    donnees_statistiques_match=get_stat_ligue_saison(nom_ligue,saisons)
    liste_collectif=[]

    stat_interet=['3pt','3pt-reussi','3pt-echoue','2pt','2pt-reussi','2pt-echoue','lf','lf-reussi','lf-echoue','faute','reb','ast','stl','blk','to','gametime']
    liste_individuel=pd.DataFrame()
    match_avec_joueur=[elem for elem in ligue_alldata if joueur in elem['joueurs_equipe1']+elem['joueurs_equipe2']]
    for donnees_match in match_avec_joueur:
        date=donnees_match['date_enregistrement']
        heure=donnees_match['heure_enregistrement']
        discipline=donnees_match['discipline']
        if discipline=='football':
            stat_interet=['but','but-normal','but-penalty','but-coupfranc','passe-decisive','csc','carton-jaune','carton-rouge','gametime']
        elif discipline=='volley':
            stat_interet=['point']
        elif discipline=='basket':
            sys_annot=donnees_match['sys_annot']
            if sys_annot=='annot_simple':
                stat_interet=['3pt','3pt-reussi','3pt-echoue','3pt(%)','2pt','2pt-reussi','2pt-echoue','2pt(%)','lf','lf-reussi','lf-echoue','lf(%)','faute','gametime']
            else:
                stat_interet=['3pt','3pt-reussi','3pt-echoue','3pt(%)','2pt','2pt-reussi','2pt-echoue','2pt(%)','lf','lf-reussi','lf-echoue','lf(%)','faute','reb','ast','stl','blk','to','gametime']                
        stat_match=pd.DataFrame(donnees_match['statistiques'])
        ligne_joueur=stat_match.loc[stat_match['player']==joueur].reset_index(drop=True)
        # liste_individuel.append(ligne_joueur)

        if discipline=='basket':
            for variable in ['3pt','2pt','lf']:
                if ligne_joueur[variable].values[0]==0:
                    pourcentage=None
                else:
                    pourcentage=ligne_joueur[variable+'-reussi']/ligne_joueur[variable]
                ligne_joueur[variable+"(%)"]=pourcentage
        elif discipline=='football':
            ligne_joueur['but']=ligne_joueur['but-normal']+ligne_joueur['but-penalty']+ligne_joueur['but-coupfranc']
        ligne_joueur['date']=date;ligne_joueur['heure']=heure 
        liste_individuel = pd.concat([liste_individuel,ligne_joueur])
        print(f"liste_individuel {liste_individuel}")
    
    
    # concat_df=pd.DataFrame(liste_individuel).reset_index(drop=True)
    # print(concat_df)
    donnees_joueurs=pd.DataFrame({'Joueur':[joueur]*len(match_avec_joueur)})
    if shared_data_ligue['sys_ligue']=='fix-teams':
        nom_equipe_joueur=[elem[0] for elem in shared_data_ligue['liste_equipe'] if joueur in elem[1]][0]
        donnees_joueurs['Equipe']=nom_equipe_joueur
    valeur=liste_individuel[stat_interet+['date','heure']].values.tolist()
    print(f"valeur moyenne {valeur}")
    donnees_joueurs[stat_interet+['date','heure']]=valeur
    donnees_joueurs.reset_index(drop=True,inplace=True)
    
    # if discipline=='basket':
    #     df_liste.drop(columns=['pause','id_team'])
        
    print(donnees_joueurs)
    layout_stat=html.Div([
            html.Div(children=f"Statistiques de {joueur}", className="menu-title"),

    dash_table.DataTable(
            id='stat_ligue_table',
                export_format="csv",
            columns=[{"name": i, "id": i} for i in donnees_joueurs.columns],  # Display dataframe columns
            data=donnees_joueurs.to_dict('records'),  # Initialize the table with dataframe data
            filter_action='native',  # Enable filtering
            style_header={
                'backgroundColor': 'rgb(30, 30, 30)',
                'color': 'white'
            },
            style_data={
                'backgroundColor': 'rgb(50, 50, 50)',
                'color': 'white'
            },
            sort_action='native'
        )])
    return layout_stat