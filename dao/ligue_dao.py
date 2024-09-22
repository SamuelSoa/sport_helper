import pymongo
from pymongo import MongoClient
import random
import certifi
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

def create_ligue(nom_ligue,sys_ligue,username):
    collection=get_collection(database='Ligues',collection_db='ligues_info')

    results=list(collection.find({"ligue_name":nom_ligue}))
    if len(results)<1:
        random_string = generate_random_string(8)
        results_generator_idshare=list(collection.find({"id_share_ligue":random_string}))
        while len(results_generator_idshare)>=1:
            random_string = generate_random_string(8)
            results_generator_idshare=list(collection.find({"id_share_ligue":random_string}))
        post={"id_share_ligue":random_string,'ligue_name':nom_ligue,'sys_ligue':sys_ligue,'liste_player':[username]}
        collection.insert_one(post)

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
        update = {"$push": {"liste_player": new_value}}
        # Execute the update
        result = collection.update_one(query, update)
        return 'Ligue jointe avec succès'
    else:
        return 'Veuillez recopier un code valide'

def create_equipe(nom_equipe):
    collection=get_collection(database='Players',collection_db='equipes')
    results=list(collection.find({"nom_equipe":nom_equipe}))
    if len(results)<1:
        random_string = generate_random_string(8)
        results_generator_idshare=list(collection.find({"id_share_equipe":random_string}))
        while len(results_generator_idshare)>=1:
            random_string = generate_random_string(8)
            results_generator_idshare=list(collection.find({"id_share_equipe":random_string}))
        post={"id_share_equipe":random_string,"nom_equipe":nom_equipe}
        collection.insert_one(post)

    
def create_joueur(email,pseudo,password):
    collection=get_collection(database='Players',collection_db='joueurs')
    results=list(collection.find({"mail_joueur":email,'pseudo_joueur':pseudo,'password_joueur':password}))
    if len(results)<1:
        post={"mail_joueur":email,'pseudo_joueur':pseudo,'password_joueur':password}
        collection.insert_one(post)




# connexion to the cluster
# db=cluster['Players']
# collection=db['joueurs']
# # insert multiple post
# post1={"mail_joueur":2,'pseudo_joueur':'joe','password_joueur':'doe'}
# post2={"mail_joueur":3,'pseudo_joueur':'hello','password_joueur':'world'}
# collection.insert_many([post1,post2])


def get_all_data_joueurs(nom_db,nom_collection):
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
    print(liste_ligue_joueur)
    for elem in liste_ligue_joueur:
        joueurs=elem[1]
        print(joueurs)
        if current_user.id in joueurs:
            liste_to_fill.append(elem[0])
    result=dcc.Dropdown(
            id="ligues_rejointes",
            options=[{"label": x, "value": x} for x in liste_to_fill],
            clearable=False,
            className="dropdown"
        )
    return result