

from dao.ligue_dao import get_collection



def create_tournoi(nom_tournoi,username,discipline_tournoi):
    collection=get_collection(database='Tournoi',collection_db=f'data_{discipline_ligue}')
    results=list(collection.find({"tournoi_name":nom_tournoi}))
    random_string = generate_random_string(8)
    results_generator_idshare=list(collection.find({"id_share_tournoi":random_string}))
    while len(results_generator_idshare)>=1:
        random_string = generate_random_string(8)
        results_generator_idshare=list(collection.find({"id_share_tournoi":random_string}))
    post={"id_share_tournoi":random_string,'tournoi_name':nom_tournoi,'discipline_tournoi':discipline_tournoi,'liste_player':[username],'liste_equipe':[],'liste_role':['admin']}
    collection.insert_one(post)
    return f"Tournoi crée avec succès. Pour inviter vos camarades à la rejoindre, le code est {random_string}"



def join_tournoi(username,code_tournoi,discipline_tournoi):
    collection=get_collection(database='Tournoi',collection_db=f'data_{discipline_ligue}')
    results_tournoidb=list(collection.find({"id_share_tournoi":code_ligue}))
    print(results_tournoidb)
    if len(results_tournoidb)==1:
        print(results_tournoidb)
        liste_joueurs=results_tournoidb[0]['liste_player']
        if username in liste_joueurs:
            return 'Tournoi déja rejointe'
        query={"id_share_ligue":code_ligue}
        new_value = username  # Change this to the value you want to add
        # Update the document to add the new value to liste_aaa
        update = {"$push": {"liste_player": new_value,'liste_role':'user'}}
        # Execute the update
        result = collection.update_one(query, update)
        return 'Tournoi rejoint avec succès'
    else:
        return 'Veuillez recopier un code valide'




def create_equipe_tournoi(nom_tournoi,nom_equipe,liste_joueurs,discipline_tournoi):
    collection=get_collection(database='Tournoi',collection_db=f'data_{discipline_ligue}')
    results_tournoidb=list(collection.find({"tournoi_name":nom_tournoi}))
    print(results_tournoidb)
    if len(results_tournoidb)==1:
        liste_equipe_actuel=results_tournoidb[0]['liste_equipe']
        if len(liste_equipe_actuel)>=1:
            nom_equipes_actuels=[elem[0] for elem in liste_equipe_actuel]
            if nom_equipe in nom_equipes_actuels:
                return "Nom d'équipe déja utilisé"
            else:
                query={'tournoi_name':nom_tournoi}
                new_value=[nom_equipe,liste_joueurs]
                update = {"$push": {'liste_equipe':new_value}}
                result = collection.update_one(query, update)
                return 'Equipe crée avec succès'
        else:
            query={'ligue_name':nom_tournoi}
            new_value=[nom_equipe,liste_joueurs]
            update = {"$push": {'liste_equipe':new_value}}
            result = collection.update_one(query, update)
            return 'Equipe crée avec succès'    
    else:
        return 'Veuillez recopier un code valide'




def choice_player_from_tournoi(nom_tournoi,discipline_tournoi):
    collection=get_collection(database='Tournoi',collection_db=f'data_{discipline_ligue}')
    results_tournoidb=list(collection.find({"tournoi_name":nom_tournoi}))
    if len(results_tournoidb)==1:
        # print(results_checkligue)
        liste_joueurs=results_tournoidb[0]['liste_player']
        result=dcc.Dropdown(
                id="joueurs_createequipe_tournoi",
                options=[{"label": x, "value": x} for x in liste_joueurs],
                clearable=False,
                className="dropdown",
                multi=True
            )
        return result

def get_tournoi_alldata(code,discipline_tournoi):
    """ Retourne le nom d'une ligue, le systèe de la ligue , la liste d'équipe, de joueurs, et le role de chaque utilisateur"""
    collection=get_collection(database='Ligues',collection_db=f'data_{discipline_ligue}')
    results_checktournoidb=list(collection.find({"id_share_tournoi":code}))
    donnees=results_checktournoidb[0]
    donnees.pop('_id')
    print(f'resultat all data:{donnees}')
    # 'id_share_ligue': '#LU7V+15J', 'ligue_name': 'ligue2', 'sys_ligue': 'fix-teams', 'liste_player': ['joe', 'hello']}`
    return donnees




def get_all_tournoi(discipline_tournoi):
    cluster=MongoClient('mongodb+srv://mrsamu35:Samuel35-@players.lahd6.mongodb.net/?retryWrites=true&w=majority&appName=Players', tlsCAFile=ca)
    db=cluster['Tournoi']
    collection=db[f'data_{discipline_tournoi}']
    liste_all=collection.find()
    liste_ligue_joueur=[[elem['tournoi_name'],elem['id_share_tournoi'],elem['liste_player']] for elem in liste_all]
    liste_to_fill=[]
    for elem in liste_ligue_joueur:
        joueurs=elem[1]
        print(joueurs)
        if current_user.id in joueurs:
            liste_to_fill.append('-->'.join(elem[:2]))
    print(liste_to_fill)
    result=dcc.Dropdown(
            id="tournoi_rejoints",
            options=[{"label": x, "value": x} for x in liste_to_fill],
            clearable=False,
            className="dropdown"
        )
    return result


def dropdown_discipline():
    result=html.Div(
        [html.Div(children="Discipline", className="menu-title"),dcc.Dropdown(
            id="discipline_tournoi",
            options=[{"label": x, "value": y} for x, y in [['Basket', 'basket'], ['Tennis', 'tennis'], ['Football', 'football'], ['Volley', 'volley']]],
            clearable=False,
            className="dropdown"
        )])
    return result