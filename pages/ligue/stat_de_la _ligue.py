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

dash.register_page(__name__, path="/ligues/vos_ligues/statistiques/statistiques_ligue",name='Vos ligues')
require_login(__name__)


layout=html.Div([
    html.H1('Panel des statistiques de la ligue'),
        html.Div(children="Saison(s)", className="menu-title"),
html.Div(id='dropdown-saison-statligue'),
html.Br(),
html.Div(id='dashtable_datasaisonmean'),
html.Br(),
html.Div(id='dashtable_classement')
])


@callback(
    Output('dropdown-saison-statligue','children'),
    Input('shared-data-ligue','data')
)
def get_dropdown_saison_statligue(shared_data_ligue):
    nom_ligue=shared_data_ligue['ligue_name']
    ligue_alldata=get_ligueevent_alldata(nom_ligue)

    saisons=list(set(np.array([elem['saison'] for elem in ligue_alldata]).flatten()))
    drop=dcc.Dropdown(
                    id='saisons-to-choose-statligue',
                    options=[{"label": x, "value": x} for x in saisons],
                    clearable=False,
                    className="dropdown",
                    multi=True)
    return drop

@callback(
    Output('dashtable_datasaisonmean','children'),
    Input('shared-data-ligue','data'),
    Input('saisons-to-choose-statligue','value')
)
def get_statevent_mean(shared_data_ligue,saisons):

    nom_ligue=shared_data_ligue['ligue_name']
    ligue_alldata=get_ligueevent_alldata(nom_ligue)
    liste_joueur=np.unique(np.array([elem['joueurs_equipe1']+elem['joueurs_equipe2'] for elem in ligue_alldata]).flatten())
    donnees_statistiques_match=get_stat_ligue_saison(nom_ligue,saisons)
    liste_collectif=[]

    stat_interet=['3pt','3pt-reussi','3pt-echoue','2pt','2pt-reussi','2pt-echoue','lf','lf-reussi','lf-echoue','faute','reb','ast','stl','blk','to','gametime']
    for joueur in liste_joueur:
        liste_individuel=pd.DataFrame()
        match_avec_joueur=[elem for elem in ligue_alldata if joueur in elem['joueurs_equipe1']+elem['joueurs_equipe2']]
        for donnees_match in match_avec_joueur:
            discipline=donnees_match['discipline']
            if discipline=='football':
                stat_interet=['but','but-normal','but-penalty','but-coupfranc','passe-decisive','csc','carton-jaune','carton-rouge','gametime']
            elif discipline=='volley':
                stat_interet=['point']
            elif discipline in ['free-solo','free-multi']:
                stat_interet=['ajout-point']
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
            liste_individuel = pd.concat([liste_individuel,ligne_joueur])
            print(f"liste_individuel {liste_individuel}")
        
        
        # concat_df=pd.DataFrame(liste_individuel).reset_index(drop=True)
        # print(concat_df)
        donnees_joueurs=pd.DataFrame({'Joueur':[joueur]})
        if shared_data_ligue['sys_ligue']=='fix-teams':
            nom_equipe_joueur=[elem[0] for elem in shared_data_ligue['liste_equipe'] if joueur in elem[1]][0]
            donnees_joueurs['Equipe']=nom_equipe_joueur
        print(f"d joueur apres add joueur {donnees_joueurs}")
        valeur=liste_individuel[stat_interet].mean().values.tolist()
        print(f"valeur moyenne {valeur}")
        donnees_joueurs[stat_interet]=valeur
        print(f"d joueur {donnees_joueurs}")
        liste_collectif.append(donnees_joueurs)
    df_liste=pd.concat(liste_collectif)
    if discipline=='basket':
        df_liste.drop(columns=['3pt-reussi','3pt-echoue','2pt-echoue','2pt-reussi','lf-echoue','lf-reussi'],inplace=True)
        
    print(df_liste)
    layout_stat=html.Div([
            html.Div(children="Statistiques par joueurs", className="menu-title"),

    dash_table.DataTable(
            id='stat_ligue_table',
                export_format="csv",
            columns=[{"name": i, "id": i} for i in df_liste.columns],  # Display dataframe columns
            data=df_liste.to_dict('records'),  # Initialize the table with dataframe data
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







def get_classement_individuel(shared_data_ligue,saisons):
    """ Peret d'avoir le classement d'une ligue fonctionnant avec des équipes variables"""

    nom_ligue=shared_data_ligue['ligue_name']
    discipline=shared_data_ligue['discipline_ligue']
    print(f'saison {saisons}')
    ligue_alldataevent=get_ligueevent_alldata(nom_ligue, { 'saison': { '$in':saisons } })
    liste_joueur=np.unique(np.array([elem['joueurs_equipe1']+elem['joueurs_equipe2'] for elem in ligue_alldataevent]).flatten())
    liste_collectif=[]
    for joueur in liste_joueur:
        # Initialisation du df classement de cheque personne
        if discipline=='football':
            liste_individuel=pd.DataFrame([[0,None,0,0,0,0,0,0]],columns=['Rang','Joueur','Matchs joués','Victoire','Nul','Defaite','Points marqués par ses équipes','Points concedés par ses équipes'])
        else:
            liste_individuel=pd.DataFrame([[0,None,0,0,0]],columns=['Rang','Joueur','Matchs joués','Victoire','Defaite'])
        # on repère les données de matchs dans lequel le joueur paticipe
        match_avec_joueur=[elem for elem in ligue_alldataevent if joueur in elem['joueurs_equipe1']+elem['joueurs_equipe2']]
        nb_match_joues=len(match_avec_joueur)
        for donnees_match in match_avec_joueur:

            #stat synthétiques de point
            stat_match_synthetique=pd.DataFrame(donnees_match['stat_finale'])
            print(match_avec_joueur)

            # Determination du score et du résultat
            equipe='equipe1' if joueur in donnees_match['joueurs_equipe1'] else 'equipe2'
            score='score1' if equipe=='equipe1' else 'score2'
            autre_score=[elem for elem in ['score1','score2'] if elem != score][0]
            liste_interet=stat_match_synthetique[[score,autre_score]].values.tolist()
            print(f"liste_interet: {liste_interet}")

            score_joueur,score_adversaire=stat_match_synthetique[[score,autre_score]].values.tolist()[0]
            if score_joueur<score_adversaire:
                liste_individuel['Defaite']+=1
            elif score_joueur>score_adversaire:
                liste_individuel['Victoire']+=1
            if discipline=='football' and score_joueur==score_adversaire:
                liste_individuel['Nul']+=1
            if discipline=='football':
                liste_individuel['Points marqués par ses équipes']+=score_joueur
                liste_individuel['Points concedés par ses équipes']+=score_adversaire
        
        if discipline =='football':
            liste_individuel['Différentiel']=liste_individuel['Points marqués par ses équipes']-liste_individuel['Points concedés par ses équipes']
        
        
        # Determination du nombre de point

        liste_individuel['Points']=3*liste_individuel['Victoire']+1*liste_individuel['Nul'] if discipline=='football' else 3*liste_individuel['Victoire']
        liste_individuel['Matchs joués']=nb_match_joues
        liste_collectif.append(liste_individuel)
    # on regroupe les données individuelles et on fait un classement
    df_liste=pd.concat(liste_collectif)
    df_liste['Joueur']=liste_joueur
    df_liste.sort_values(by='Points',inplace=True,ascending=False)
    df_liste['Rang']=range(1,len(df_liste)+1)
    layout_stat=html.Div([
                html.Div(children="Classement de la ligue", className="menu-title"),

        dash_table.DataTable(
            id='classement_ligue_individuel_table',
                export_format="csv",
            columns=[{"name": i, "id": i} for i in df_liste.columns],  # Display dataframe columns
            data=df_liste.to_dict('records'),  # Initialize the table with dataframe data
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







def get_classement_equipe(shared_data_ligue,saisons):
    """ Peret d'avoir le classement d'une ligue fonctionnant avec des équipes variables"""

    nom_ligue=shared_data_ligue['ligue_name']
    discipline=shared_data_ligue['discipline_ligue']
    ligue_alldataevent=get_ligueevent_alldata(nom_ligue, { 'saison': { '$in':saisons } })
    liste_equipe=shared_data_ligue['liste_equipe']
    liste_collectif=[]
    for equipe in liste_equipe:
        # Initialisation du df classement de cheque personne
        if discipline=='football':
            liste_individuel=pd.DataFrame([[None,0,0,0,0,0,0,0]],columns=['Equipe','Matchs joués','Victoire','Nul','Defaite','Points marqués','Points concedés','Points'])
        else:
            liste_individuel=pd.DataFrame([[None,0,0,0,0]],columns=['Equipe','Matchs joués','Victoire','Defaite','Points'])
        # on repère les données de matchs dans lequel le joueur paticipe
        match_avec_equipe=[elem for elem in ligue_alldataevent if equipe in [elem['nom_equipe1'],elem['nom_equipe2']]]
        nb_mathçjoues=len(match_avec_equipe)
        for donnees_match in match_avec_equipe:

            #stat synthétiques de point
            stat_match_synthetique=pd.DataFrame(donnees_match['stat_finale'])
            print(match_avec_equipe)

            score='score1' if equipe=='equipe1' else 'score2'
            autre_score=[elem for elem in ['score1','score2'] if elem != score][0]
            liste_interet=stat_match_synthetique[[score,autre_score]].values.tolist()
            print(f"liste_interet: {liste_interet}")
            score_joueur,score_adversaire=stat_match_synthetique[[score,autre_score]].values.tolist()[0]
            if score_joueur<score_adversaire:
                liste_individuel['Defaite']+=1
            elif score_joueur>score_adversaire:
                liste_individuel['Victoire']+=1
            if discipline=='football' and score_joueur==score_adversaire:
                liste_individuel['Nul']+=1
            if discipline=='football':
                liste_individuel['Points marqués']+=score_joueur
                liste_individuel['Points concedés']+=score_adversaire
        
        if discipline =='football':
            liste_individuel['Différentiel']=liste_individuel['Points marqués']-liste_individuel['Points concedés']
        
        
        # Determination du nombre de point

        liste_individuel['Points']=3*liste_individuel['Victoire']+1*liste_individuel['Nul'] if discipline=='football' else 3*liste_individuel['Victoire']
        liste_individuel['Matchs joués']=nb_mathçjoues
        liste_collectif.append(liste_individuel)
    # on regroupe les données individuelles et on fait un classement
    df_liste=pd.concat(liste_collectif)
    df_liste['Equipe']=liste_joueur
    df_liste.sort_values(by='Points',inplace=True,ascending=False)
    
    layout_stat=html.Div([
                html.Div(children="Classement de la ligue", className="menu-title"),

        dash_table.DataTable(
            id='classement_ligue_collectif_table',
                export_format="csv",
            columns=[{"name": i, "id": i} for i in df_liste.columns],  # Display dataframe columns
            data=df_liste.to_dict('records'),  # Initialize the table with dataframe data
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



@callback(
Output('dashtable_classement','children'),
Input('shared-data-ligue','data'),
Input('saisons-to-choose-statligue','value'))
def get_classement(shared_data_ligue,saisons):
    sys_ligue=shared_data_ligue['sys_ligue']
    if sys_ligue=='fix-teams':
        result=get_classement_equipe(shared_data_ligue,saisons)
    else:
        result=get_classement_individuel(shared_data_ligue,saisons)
    return result