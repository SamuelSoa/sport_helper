import pymongo
from pymongo import MongoClient
import random
import certifi
import string
import pandas as pd
from flask_login import current_user
from dash import dcc
ca = certifi.where()

cluster=MongoClient('mongodb+srv://mrsamu35:Samuel35-@players.lahd6.mongodb.net/?retryWrites=true&w=majority&appName=Players', tlsCAFile=ca)

def generate_random_string(length):
    characters = string.ascii_uppercase + string.digits +'_-=+'
    random_string = '#'+''.join(random.sample(characters, length))
    return random_string
# Generate a random string with length 8
# random_string = generate_random_string(8)
# print(random_string)

def get_collection(database,collection_db):
    # client=MongoClient()
    # db=client.test_database
    # collection=db.test_collection
    # connexion to the cluster
    cluster=MongoClient('mongodb+srv://mrsamu35:Samuel35-@players.lahd6.mongodb.net/?retryWrites=true&w=majority&appName=Players', tlsCAFile=ca)
    #database
    db=cluster[database]
    collection=db[collection_db]
    return collection


def get_ligueevent_alldata(nom_ligue,condition=''):
    collection=get_collection(database='Ligues',collection_db=nom_ligue)
    results_checkligue=list(collection.find(condition))
    # 'id_share_ligue': '#LU7V+15J', 'ligue_name': 'ligue2', 'sys_ligue': 'fix-teams', 'liste_player': ['joe', 'hello']}`
    return results_checkligue


# def get_stat_ligue_equipe_saison(database,ligue,donnees,condition_equipe=None):
#     # client=MongoClient()
#     # db=client.test_database
#     # collection=db.test_collection
#     # connexion to the cluster
#     cluster=MongoClient('mongodb+srv://mrsamu35:Samuel35-@players.lahd6.mongodb.net/?retryWrites=true&w=majority&appName=Players', tlsCAFile=ca)
#     #database
#     db=cluster['Ligues']
#     collection=db[ligue]
#     if condition_equipe is not None:
#         results_checkligue=list(collection.find( 
#             {$or: [ {"nom_equipe1":random_string},{"nom_equipe2":random_string}]}
#             ))
#     else:
#         results_checkligue=list(collection.find())
#     liste_df=[pd.DataFrame(elem['statistiques']) for elem in results_checkligue]
#     return liste_df


def get_stat_ligue_saison(ligue,condition_saison):
    cluster=MongoClient('mongodb+srv://mrsamu35:Samuel35-@players.lahd6.mongodb.net/?retryWrites=true&w=majority&appName=Players', tlsCAFile=ca)
    #database
    db=cluster['Ligues']
    collection=db[ligue]
    results_checkligue=list(collection.find({'saison': {'$in': condition_saison}}))
    liste_df=[pd.DataFrame(elem['statistiques']) for elem in results_checkligue]
    return liste_df


def insert_one_post(database,collection_db,post):
    # client=MongoClient()
    # db=client.test_database
    # collection=db.test_collection
    # connexion to the cluster
    cluster=MongoClient('mongodb+srv://mrsamu35:Samuel35-@players.lahd6.mongodb.net/?retryWrites=true&w=majority&appName=Players', tlsCAFile=ca)
    #database
    db=cluster[database]
    collection=db[collection_db]
    collection.insert_one(post)
    return 'Données enregistrées'

def create_ligue(nom_ligue,sys_ligue,username,discipline_ligue):
    collection=get_collection(database='Ligues',collection_db='ligues_info')

    results=list(collection.find({"ligue_name":nom_ligue}))
    if len(results)<1:
        random_string = generate_random_string(8)
        results_generator_idshare=list(collection.find({"id_share_ligue":random_string}))
        while len(results_generator_idshare)>=1:
            random_string = generate_random_string(8)
            results_generator_idshare=list(collection.find({"id_share_ligue":random_string}))
        post={"id_share_ligue":random_string,'ligue_name':nom_ligue,'sys_ligue':sys_ligue,'discipline_ligue':discipline_ligue,'saison':[1],'liste_player':[username],'liste_equipe':[],'liste_role':['admin']}
        collection.insert_one(post)
        return f"Ligue crée avec succès. Pour inviter vos camarades à la rejoindre, le code est {random_string}"
    else:
        return 'Le nom de ligue est deja pris'





def join_ligue(username,code_ligue):
    collection=get_collection(database='Ligues',collection_db='ligues_info')
    results_checkligue=list(collection.find({"id_share_ligue":code_ligue}))
    print(results_checkligue)
    if len(results_checkligue)==1:
        print(results_checkligue)
        liste_joueurs=results_checkligue[0]['liste_player']
        if username in liste_joueurs:
            return 'Ligue déja rejointe'
        query={"id_share_ligue":code_ligue}
        new_value = username  # Change this to the value you want to add
        # Update the document to add the new value to liste_aaa
        update = {"$push": {"liste_player": new_value,'liste_role':'user'}}
        # Execute the update
        result = collection.update_one(query, update)
        return 'Ligue jointe avec succès'
    else:
        return 'Veuillez recopier un code valide'

def create_equipe(nom_ligue,nom_equipe,liste_joueurs):
    collection=get_collection(database='Ligues',collection_db='ligues_info')
    results_checkligue=list(collection.find({"ligue_name":nom_ligue}))
    print(results_checkligue)
    if len(results_checkligue)==1:
        liste_equipe_actuel=results_checkligue[0]['liste_equipe']
        if len(liste_equipe_actuel)>=1:
            nom_equipes_actuels=[elem[0] for elem in liste_equipe_actuel]
            if nom_equipe in nom_equipes_actuels:
                return "Nom d'équipe déja utilisé"
            else:
                query={'ligue_name':nom_ligue}
                new_value=[nom_equipe,liste_joueurs]
                update = {"$push": {'liste_equipe':new_value}}
                result = collection.update_one(query, update)
                return 'Equipe crée avec succès'
        else:
            query={'ligue_name':nom_ligue}
            new_value=[nom_equipe,liste_joueurs]
            update = {"$push": {'liste_equipe':new_value}}
            result = collection.update_one(query, update)
            return 'Equipe crée avec succès'    
    else:
        return 'Veuillez recopier un code valide'

nom_ligue='ligue1';nom_equipe='t1';liste_joueurs=['joe','hello']



def choice_player_from_ligue(nom_ligue):
    collection=get_collection(database='Ligues',collection_db='ligues_info')
    results_checkligue=list(collection.find({"ligue_name":nom_ligue}))
    if len(results_checkligue)==1:
        # print(results_checkligue)
        liste_joueurs=results_checkligue[0]['liste_player']
        result=dcc.Dropdown(
                id="joueurs_createequipe",
                options=[{"label": x, "value": x} for x in liste_joueurs],
                clearable=False,
                className="dropdown",
                multi=True
            )
        return result


def get_ligue_alldata(nom_ligue):
    """ Retourne le nom d'une ligue, le systèe de la ligue , la liste d'équipe, de joueurs, et le role de chaque utilisateur"""
    collection=get_collection(database='Ligues',collection_db='ligues_info')
    results_checkligue=list(collection.find({"ligue_name":nom_ligue}))
    donnees=results_checkligue[0]
    donnees.pop('_id')
    print(f'resultat all data:{donnees}')
    # 'id_share_ligue': '#LU7V+15J', 'ligue_name': 'ligue2', 'sys_ligue': 'fix-teams', 'liste_player': ['joe', 'hello']}`
    return donnees

def get_data_by_filter(variable_filtre,valeur_filtre,id_input,variable_interet):
    collection=get_collection(database='Ligues',collection_db='ligues_info')
    results_checkligue=list(collection.find({variable_filtre:valeur_filtre}))
    if len(results_checkligue)==1:
        # print(results_checkligue)
        liste_valeur_interet=results_checkligue[0][variable_interet]
        result=dcc.Dropdown(
                id=id_input,
                options=[{"label": x, "value": x} for x in liste_valeur_interet],
                clearable=False,
                className="dropdown",
                multi=True
            )
        return result
# def create_joueur(email,pseudo,password):
#     collection=get_collection(database='Players',collection_db='joueurs')

#     results=list(collection.find({"mail_joueur":email,'pseudo_joueur':pseudo,'password_joueur':password}))
#     if len(results)<1:
#         post={"mail_joueur":email,'pseudo_joueur':pseudo,'password_joueur':password}
#         collection.insert_one(post)
#         return 'Utilisateur inscrit avec succès'
#     else:
#         return "L'utilisateur existe deja"

def create_joueur(email,pseudo,password):
    collection=get_collection(database='Players',collection_db='joueurs')
    result_mail=list(collection.find({"mail_joueur":email}))
    if len(result_mail)>=1:
        return 'Mail déja utilisé'
    else:
        result_mail=list(collection.find({"pseudo_joueur":pseudo}))
        if len(result_mail)>=1:
            return 'Mail correct, pseudo déja utilisé'
        else:
            post={"mail_joueur":email,'pseudo_joueur':pseudo,'password_joueur':password}
            collection.insert_one(post)
            return 'Utilisateur inscrit avec succès'
           



# connexion to the cluster
# db=cluster['Players']
# collection=db['joueurs']
# # insert multiple post
# post1={"mail_joueur":2,'pseudo_joueur':'joe','password_joueur':'doe'}
# post2={"mail_joueur":3,'pseudo_joueur':'hello','password_joueur':'world'}
# collection.insert_many([post1,post2])


def get_all_data_joueurs(nom_db,nom_collection):
    """Renvoie la paire username:password pour les personnes inscrites sur l'application
    
    Arguments
    ----------
    db:str
        Nom de la base de données 
    nom_collection:str
        Nom de la collection avec les données utilisateurs
    
    """
    cluster=MongoClient('mongodb+srv://mrsamu35:Samuel35-@players.lahd6.mongodb.net/?retryWrites=true&w=majority&appName=Players', tlsCAFile=ca)
    db=cluster[nom_db]
    collection=db[nom_collection]
    liste=collection.find()
    dicto={}
    for elem in liste:
        dicto.update({elem['pseudo_joueur']:elem['password_joueur']})
    return dicto


def get_all_ligues():
    cluster=MongoClient('mongodb+srv://mrsamu35:Samuel35-@players.lahd6.mongodb.net/?retryWrites=true&w=majority&appName=Players', tlsCAFile=ca)
    db=cluster['Ligues']
    collection=db['ligues_info']
    liste_all=collection.find()
    liste_ligue_joueur=[[elem['ligue_name'],elem['liste_player']] for elem in liste_all]
    liste_to_fill=[]
    for elem in liste_ligue_joueur:
        joueurs=elem[1]
        print(joueurs)
        if current_user.id in joueurs:
            liste_to_fill.append(elem[0])
    print(liste_to_fill)
    result=dcc.Dropdown(
            id="ligues_rejointes",
            options=[{"label": x, "value": x} for x in liste_to_fill],
            clearable=False,
            className="dropdown"
        )
    return result



