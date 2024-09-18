import dash
from dash import dcc, html, Input, Output,dash_table,State
import dash_bootstrap_components as dbc
from function_for_app import plot_team_basket
from layout_page.ligue import *
from layout_page.parameters import *
from layout_page.social import *
from layout_page.tournoi import *
from layout_page.user import *
from layout_page.lineup import *
from layout_page.exhibition import *
from layout_page.basket_annot_complete import *
from layout_page.basket_annot_simple import *
from layout_page.tennis_annot import *
from layout_page.volley_annot import *

from dao.ligue_dao import *
import pandas as pd
# from dash_auth import BasicAuth



app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
# USER_PWD = {
#     "username": "password",
#     "user2": "useSomethingMoreSecurePlease",
# }
# BasicAuth(app, USER_PWD)


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


# Dash layout

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa"
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem"
}

sidebar = html.Div(
    [
        html.P(children="🏀⚽🏆 ", className="header-emoji"),
        html.H3(children="Sport Helper", className="display-4"),
            html.Hr(),
        html.P("L'outil idéal pour vous accompagner dans vos compétitions", className="lead"),
        dbc.Nav(
            [dbc.NavLink("Home", href="/", active="exact"),
            dbc.NavLink("Exhibition", href="/exhibition", active="exact"),
            dbc.NavLink("Ligues", href="/ligues", active="exact"),
            dbc.NavLink("Tournoi", href="/tournoi", active="exact"),
            dbc.NavLink("Social", href="/social", active="exact"),
            dbc.NavLink("Choix des joueurs", href="/joueurs_du_match", active="exact"),
            dbc.NavLink("Paramètres", href="/parametres", active="exact")
            ],
            vertical="md",
            pills=True
        )
    ],
    style=SIDEBAR_STYLE
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Store(id='shared-data-store', storage_type='session'),
    dcc.Location(id="url"),
    sidebar, content])




# {'discipline_to_choose': 'default', 'periode-input': 'default', 'start-time-input': 900}



### Inscription ###
@app.callback(Output('sign_in-output', 'children'),
                [Input('sign_in_button', 'n_clicks')],
                [State('mail_newuser','value'),State('identifiant_newuser', 'value'), State('password_newuser', 'value')])
def update_signin(n_clicks,email, username, password):
    if n_clicks > 0:
        if username and password and email:
            collection=get_collection(database='Players',collection_db='joueurs')
            result=collection.find({'mail':email,'pseudo':username,'password':password})
            if len(list(result))==1:
                return html.P("Le profil existe deja", style={'color': 'green'})
            else:
                create_joueur(email,username,password)
                return html.P("Profil crée avec succès. Veuillez retourner à la page précedente", style={'color': 'green'})

        else:
            return html.P("Veuillez remplir tous les champs.", style={'color': 'red'})



### Connexion ###
@app.callback(Output('login-output', 'children'),
    [Input('login-button', 'n_clicks')],
    [State('identifiant1', 'value'), State('password1', 'value')])
def update_login(n_clicks, username, password):
    if n_clicks > 0:
        if username and password:
            collection=get_collection(database='Players',collection_db='joueurs')
            result=collection.find({'pseudo_joueur':username,'password_joueur':password})
            if len(list(result))==1:
                return html.P("Connecté avec succès!", style={'color': 'green'})
            else:
                return html.P("Identifiant ou mot de passe incorrect", style={'color': 'red'})
        else:
            return html.P("Veuillez remplir tous les champs.", style={'color': 'red'})
# @app.callback(
#     Output('url', 'pathname'),
#     Input('validate-button', 'n_clicks'),
#     prevent_initial_call=True
# )
# def navigate(n_clicks):
#     if n_clicks > 0:
#         return '/exhibition/party'  # Navigate to the desired page
#     return dash.no_update

@app.callback(
    Output('url', 'pathname'),
    Input('validate-button', 'n_clicks'),
    State('shared-data-store', 'data'),
    prevent_initial_call=True
)
def navigate(n_clicks,shared_data):
    discipline=shared_data['discipline_to_choose']
    # premier click va permettre d'avoir la valeur de shared_data, deuxième permet d'obtenir discipline
    if n_clicks >=2 and discipline =='basket':
        return '/exhibition/party_basket'  # Navigate to the desired page
    elif n_clicks >=2 and discipline =='tennis':
        return '/exhibition/party_tennis'  # Navigate to the desired page
    elif n_clicks >=2 and discipline =='volley':
        return '/exhibition/party_volley'  # Navigate to the desired page
    return dash.no_update



# Callback to update the graph
@app.callback(
    Output('graph_equipe1', 'figure'),
    Input('meneur_1', 'value'),
    Input('arriere_1', 'value'),
    Input('ailier_1', 'value'),
    Input('ailier_fort_1', 'value'),
    Input('pivot_1', 'value'),
    Input('nom_1', 'value'))
def update_graph(meneur, arriere, ailier, ailier_fort, pivot, nom):
    # List of selected players
    liste_equipe = [meneur, arriere, ailier, ailier_fort, pivot]
    # Generate the figure using plot_team_basket
    fig = plot_team_basket(liste_equipe,nom)
    return fig


#version simple

# exhibition
# Callback for storing data from Layout 1
@app.callback(
    Output('shared-data-store', 'data'),
    [Input('validate-button', 'n_clicks')],
    [State('discipline_to_choose', 'value'),
    State('periode-input', 'value'),
    State('start-time-input', 'value'),
    State('donnees_team1', 'value'),
    State('donnees_team2', 'value'),
    State('nomequipe1', 'value'),
    State('nomequipe2', 'value')
    ]
)
def store_data(n_clicks, input_value1,input_value2,input_value3,input_value4,input_value5,input_value6,input_value7):
    if n_clicks is None or n_clicks == 0:
        print("validate-button has not been clicked yet.")
        return dash.no_update
    dicto={'discipline_to_choose':input_value1,'periode-input':input_value2,'start-time-input':input_value3,'donnees_team1':input_value4,'donnees_team2':input_value5,
    'nomequipe1':input_value6,'nomequipe2':input_value7}
    
    print('not yet')
    print('yes')
    # dicto['data']=df_donnees_joueurs
    # dicto.update({'data': df_donnees_joueurs})
    print(f"Storing data: {dicto}")  # Debugging statement
    return dicto



# Useful for layout
@app.callback(
    Output('nom_equipe1', 'children'),Output('nom_equipe2', 'children'),  # To dynamically update the buttons
    [
    # State({'type': 'output_table_team', 'index': dash.dependencies.ALL}, 'data'),
    Input('shared-data-store', 'data')]  #,# Dropdown to choose the annotation system
)
def get_nom_equipe(shared_data):
    """ Retourne le layout des boutons"""
    # Recreate the DataFrame from the stored data
    # Call the display_annot_buttons function with the current DataFrame and annotation system
    # print('on est a update_buttons_display')
    nom_equipe1=shared_data['nomequipe1']
    nom_equipe2=shared_data['nomequipe2']
    return nom_equipe1,nom_equipe2


# Useful for layout
@app.callback(
    Output('buttons-container', 'children'),Output('stat-container', 'children'),  # To dynamically update the buttons
    [
    # State({'type': 'output_table_team', 'index': dash.dependencies.ALL}, 'data'),
    State('shared-data-store', 'data'),
    Input('sys_annot', 'value')]  #,# Dropdown to choose the annotation system
)
def update_display(shared_data,annot_system):
    """ Retourne le layout des boutons"""
    # Recreate the DataFrame from the stored data
    # Call the display_annot_buttons function with the current DataFrame and annotation system
    # print('on est a update_buttons_display')
    print('not yet, transforation des données partagés pour display boutons et stat')
    df=get_nom_exhibition(shared_data)
    print('yes')
    donnees_button=display_buttons(df,annot_system)
    donnees_stat=display_stat(df)
    return donnees_button,donnees_stat


# Callback to handle play/pause button and the countdown
@app.callback(
    [Output('interval-component_team', 'disabled'),
     Output('play-pause-button_team', 'children')],
    [Input('play-pause-button_team', 'n_clicks')],
    [State('interval-component_team', 'disabled')],
    allow_duplicate=True
)
def toggle_timer_team(n_clicks, is_disabled):
    if n_clicks % 2 == 1:
        # If odd clicks (Play), enable the interval (timer starts)
        return False, "Pause"
    else:
        # If even clicks (Pause), disable the interval (timer pauses)
        return True, "Play"

@app.callback(
    Output('countdown-display_team', 'children'), 
    Output('interval-component_team', 'n_intervals'),
    [Input('interval-component_team', 'n_intervals'),
     Input('play-pause-button_team', 'n_clicks')],
    [State('interval-component_team', 'disabled'),
     State('shared-data-store', 'data'),
     State('current-periode-input', 'value')]
)
def update_timer_team(n_intervals, play_pause_clicks, is_disabled, shared_data,periode):
    ctx = dash.callback_context
    # Default values if shared_data is None
    countdown_start = shared_data.get('start-time-input', 900)
    # print([countdown_start,n_intervals])

    discipline = shared_data.get('discipline_to_choose', 'football')
    total_periods = shared_data.get('periode-input', 4)
    remaining_time = int(countdown_start) - n_intervals
    if remaining_time <= 0 :
        remaining_time=0
        if 'play-pause-button_team' in ctx.triggered[0]['prop_id'] and periode<total_periods:
            if not play_pause_clicks % 2 == 1:  # Odd number of clicks means play  (complementaire=pause)
                remaining_time = int(shared_data.get('start-time-input', 900))  # Reset time for the new period
                n_intervals=0


    # Format the time in MM:SS format
    minutes, seconds = divmod(remaining_time, 60)
    time = f"{minutes:02}:{seconds:02}"

    # Format the period based on discipline
    # periode = f"{current_period}MT" if discipline.split('-')[0] == 'football' else f"QT{current_period}"
    return time,n_intervals



# Callback to update each team information and update the table
@app.callback(
    [Output("output_table_team_render", "data"),
    Output("output_table2_team", "data"),
    Output("scorecounter1_team", "children"),
    Output("scorecounter2_team", "children")],
    # Output("periode-output", "children")],
    [Input({'type': '3pt-button', 'index': dash.dependencies.ALL}, 'n_clicks'),
    Input({'type': '3pt-reussi-button', 'index': dash.dependencies.ALL}, 'n_clicks'),
    Input({'type': '3pt-echoue-button', 'index': dash.dependencies.ALL}, 'n_clicks'),
    Input({'type': '2pt-button', 'index': dash.dependencies.ALL}, 'n_clicks'),
    Input({'type': '2pt-reussi-button', 'index': dash.dependencies.ALL}, 'n_clicks'),
    Input({'type': '2pt-echoue-button', 'index': dash.dependencies.ALL}, 'n_clicks'),
    Input({'type': 'lf-button', 'index': dash.dependencies.ALL}, 'n_clicks'),
    Input({'type': 'lf-reussi-button', 'index': dash.dependencies.ALL}, 'n_clicks'),
    Input({'type': 'lf-echoue-button', 'index': dash.dependencies.ALL}, 'n_clicks'),
    Input({'type': 'reb-button', 'index': dash.dependencies.ALL}, 'n_clicks'),
    Input({'type': 'ast-button', 'index': dash.dependencies.ALL}, 'n_clicks'),
    Input({'type': 'stl-button', 'index': dash.dependencies.ALL}, 'n_clicks'),
    Input({'type': 'blk-button', 'index': dash.dependencies.ALL}, 'n_clicks'),
    Input({'type': 'to-button', 'index': dash.dependencies.ALL}, 'n_clicks'),
    State('scorecounter1_team', 'children'),
    State('scorecounter2_team', 'children'),
    State('output_table_team_render', 'data'),
    State('output_table2_team', 'data'),
    State('countdown-display_team','children'),
    Input('current-periode-input','value'),
    Input('sys_pt_basket_team','value'),
    State('shared-data-store', 'data')
    ]
)
def update_person_info_team(trois_pt_clicks,trois_pt_reussi_clicks,trois_pt_echoue_clicks,
                        deux_pt_clicks,deux_pt_reussi_clicks,deux_pt_echoue_clicks,
                        lf_clicks,lf_reussi_clicks,lf_echoue_clicks,
                        reb_clicks,ast_clicks,stl_clicks,blk_clicks,to_clicks,
                        score1,score2,table_data,event_data,time,periode,sys_point,shared_data):
    score1=int(score1)
    score2=int(score2)
    # print(f"input update_person_info_team: {table_data}")
    df_event = pd.DataFrame(event_data)
    df = pd.DataFrame(table_data) if table_data else get_nom_exhibition(shared_data)
    # df = pd.DataFrame(df_table)
    # print('voila les données pour mise à jour team')
    # print(df)
    # Determine which button was clicked
    ctx = dash.callback_context
    print(f"trigger: {ctx.triggered}")
    if not ctx.triggered:
        print('no trigger')
        return df.to_dict('records'),df_event.to_dict('records'),str(score1),str(score2)
    # Extract the button information in JSON format
    triggered_button = ctx.triggered[0]['prop_id']
    button_info = eval(triggered_button.split('.')[0])  # Safely parse the button's JSON structure
    button_type = button_info['type']
    person_id = button_info['index']
    variable=button_type.split('-button')[0]

    # si un boutton est appuyé    (par defaut le xtx.triggered est long et le bouton "3pt-button" aurait été appuyé)
    if not len(ctx.triggered)>1:
        df.at[person_id,variable] += 1
        equipe=df.loc[person_id,'team']
        id_team=df.loc[person_id,'id_team']
        joueur=df.loc[person_id,'player']
        if id_team=='t1':
            score1=score_to_update_click(variable,score1,sys_point)
        elif id_team=='t2':
            score2=score_to_update_click(variable,score2,sys_point)
        
        df_event=update_dataframe_general(df_event,joueur,equipe,periode,time,variable,score1,score2)
        # Return the updated messages and the updated table data
    return  df.to_dict('records'),df_event.to_dict('records'),str(score1),str(score2)




@app.callback(
    Output('buttons-container-tennis', 'children'),Output('stat-container-tennis', 'children'),  # To dynamically update the buttons
    [
    # State({'type': 'output_table_team', 'index': dash.dependencies.ALL}, 'data'),
    State('shared-data-store', 'data'),
    Input('nb_set_gagnant', 'value')
    ]
    )
def update_display_tennis(shared_data,nb_set_gagnant):
    """ Retourne le layout des boutons"""
    # Recreate the DataFrame from the stored data
    # Call the display_annot_buttons function with the current DataFrame and annotation system
    # print('on est a update_buttons_display')
    print('not yet, transforation des données partagés pour display boutons et stat')
    df=get_nom_exhibition_tennis(shared_data,nb_set_gagnant)
    print('yes')
    donnees_button=display_buttons_tennis(df)
    donnees_stat=display_stat_tennis(df)
    return donnees_button,donnees_stat


# Callback to update each team information and update the table
@app.callback(
    [Output("output_table_team_render_tennis", "data"),
    Output("output_table2_tennis", "data"),
    Output('set_actuel','children')],
    # Output("periode-output", "children")],
    [Input({'type': 'point-button', 'index': dash.dependencies.ALL}, 'n_clicks'),
    State('output_table_team_render_tennis', 'data'),
    State('output_table2_tennis', 'data'),
    Input('nb_set_gagnant','value'),
    State('set_actuel','value'),
    State('shared-data-store', 'data')
    ]
)
def update_person_info_team_tennis(pt_click,table_data,event_data,nb_set_gagnant,set_actuel,shared_data):
    
    # print(f"input update_person_info_team: {table_data}")
    df_event = pd.DataFrame(event_data)
    df = pd.DataFrame(table_data) if table_data else get_nom_exhibition_tennis(shared_data,nb_set_gagnant)
    print(df)
    if not set_actuel:
        set_actuel='set1'

    
    # df = pd.DataFrame(df_table)
    # print('voila les données pour mise à jour team')
    # print(df)
    
    
    # Determine which button was clicked
    ctx = dash.callback_context
    print(f"trigger: {ctx.triggered}")
    # if not ctx.triggered:
    #     return df.to_dict('records'),df_event.to_dict('records'),str(score1),str(score2)
    # Extract the button information in JSON format
    triggered_button = ctx.triggered[0]['prop_id']
    button_info = eval(triggered_button.split('.')[0])  # Safely parse the button's JSON structure
    button_type = button_info['type']
    person_id = button_info['index']
    variable=button_type.split('-button')[0]

    # si un boutton est appuyé    (par defaut le xtx.triggered est long et le bouton "3pt-button" aurait été appuyé)
    if not len(ctx.triggered)>1:
        
        equipe=df.loc[person_id,'team']
        id_team=df.loc[person_id,'id_team']
        indice_idteam=df.loc[df.id_team==id_team].index.tolist()

        indice_equipe=df.loc[df.id_team=='t1'].index.tolist()
        nombre_joueurs=len(indice_equipe)
        indice_autreequipe=df.loc[df.id_team=='t2'].index.tolist()
        score1=df.loc[indice_equipe,'point_set_actuel'].unique().tolist()[0]
        score2= df.loc[indice_autreequipe,'point_set_actuel'].unique().tolist()[0]
        joueur=df.loc[person_id,'player']
        if id_team=='t1':
            score1,score2,event=score_to_update_click_tennis(score1,score2)
        elif id_team=='t2':
            score2,score1,event=score_to_update_click_tennis(score2,score1)
        df.loc[indice_equipe,'point_set_actuel']= score1
        df.loc[indice_autreequipe,'point_set_actuel']= score2

        if event:
            df.loc[indice_idteam,set_actuel]+= 1
        #reinitialisation après un set gagné
        seuil_manche=6
        if df.loc[indice_equipe,set_actuel].values.tolist()==df.loc[indice_autreequipe,set_actuel].values.tolist()==5 or list(set(df[set_actuel].values.tolist())) in [[6,5],[5,6],[6,6],[7,6],[6,7]]:
            seuil_manche=7

        if df.loc[indice_idteam,set_actuel].values.tolist()==[seuil_manche]*nombre_joueurs:
            set_actuel='set'+str(int(set_actuel[3])+1)
            df.loc[indice_idteam,'nb_set_gagne']+= 1
            df.loc[indice_equipe,'point_set_actuel']= 0
            df.loc[indice_autreequipe,'point_set_actuel']= 0
        df_event=update_dataframe_tennis(df_event,joueur,equipe,set_actuel,variable,score1,score2)
        # Return the updated messages and the updated table data
    return  df.to_dict('records'),df_event.to_dict('records'),set_actuel




@app.callback(
    Output('buttons-container-volley', 'children'),Output('stat-container-volley', 'children'),  # To dynamically update the buttons
    [
    # State({'type': 'output_table_team', 'index': dash.dependencies.ALL}, 'data'),
    Input('shared-data-store', 'data')
    ]
    )
def update_display_volley(shared_data):
    """ Retourne le layout des boutons"""
    # Recreate the DataFrame from the stored data
    # Call the display_annot_buttons function with the current DataFrame and annotation system
    # print('on est a update_buttons_display')
    print('not yet, transforation des données partagés pour display boutons et stat')
    df=get_nom_exhibition_volley(shared_data)
    print('yes')
    donnees_button=display_buttons_volley(df)
    donnees_stat=display_stat_volley(df)
    return donnees_button,donnees_stat


# Callback to update each team information and update the table
@app.callback(
    [Output("output_table_team_render_volley", "data"),
    Output("output_table2_volley", "data"),
    Output('set_actuel_volley','children')],
    # Output("periode-output", "children")],
    [Input({'type': 'pointvolley-button', 'index': dash.dependencies.ALL}, 'n_clicks'),
    State('output_table_team_render_volley', 'data'),
    State('output_table2_volley', 'data'),
    State('set_actuel_volley','value'),
    State('shared-data-store', 'data')
    ]
)
def update_person_info_team_volley(pt_click,table_data,event_data,set_actuel,shared_data):
    
    # print(f"input update_person_info_team: {table_data}")
    df_event = pd.DataFrame(event_data)
    df = pd.DataFrame(table_data) if table_data else get_nom_exhibition_volley(shared_data)
    print(df)
    if not set_actuel:
        set_actuel='set1'

    
    # df = pd.DataFrame(df_table)
    # print('voila les données pour mise à jour team')
    # print(df)
    
    
    # Determine which button was clicked
    ctx = dash.callback_context
    print(f"trigger: {ctx.triggered}")
    # if not ctx.triggered:
    #     return df.to_dict('records'),df_event.to_dict('records'),str(score1),str(score2)
    # Extract the button information in JSON format
    triggered_button = ctx.triggered[0]['prop_id']
    button_info = eval(triggered_button.split('.')[0])  # Safely parse the button's JSON structure
    button_type = button_info['type']
    person_id = button_info['index']
    variable=button_type.split('-button')[0]

    # si un boutton est appuyé    (par defaut le xtx.triggered est long et le bouton "3pt-button" aurait été appuyé)
    if not len(ctx.triggered)>1:
        equipe=df.loc[person_id,'team']
        id_team=df.loc[person_id,'id_team']
        indice_idteam=df.loc[df.id_team==id_team].index.tolist()
        indice_equipe=df.loc[df.id_team=='t1'].index.tolist()
        nombre_joueurs=len(indice_equipe)
        indice_autreequipe=df.loc[df.id_team=='t2'].index.tolist()
        score1=df.loc[indice_equipe,set_actuel].unique().tolist()[0]
        score2= df.loc[indice_autreequipe,set_actuel].unique().tolist()[0]
        joueur=df.loc[person_id,'player']
        if id_team=='t1':
            score1,score2,event=score_to_update_click_volley(score1,score2)
        elif id_team=='t2':
            score2,score1,event=score_to_update_click_volley(score2,score1)
        df.loc[indice_equipe,set_actuel]= score1
        df.loc[indice_autreequipe,set_actuel]= score2

        if event:
            # df.loc[indice_equipe,set_actuel]=score1
            # df.loc[indice_autreequipe,set_actuel]=score2
            df.loc[indice_idteam,'nb_set_gagne']+= 1
            df.loc[indice_equipe,set_actuel]= 0
            df.loc[indice_autreequipe,set_actuel]= 0
            set_actuel='set'+str(int(set_actuel[3])+1)



        # #reinitialisation après un set gagné
        # seuil_manche=6
        # score_unique1,score_unique2=list(set(df[set_actuel].values.tolist()))
        # if df.loc[indice_equipe,set_actuel].values.tolist()==df.loc[indice_autreequipe,set_actuel].values.tolist()==24 or (np.abs(score_unique1-score_unique2)==1 and score_unique1>=24 and score_unique2>=24):
        #     seuil_manche=7

        # if df.loc[indice_idteam,set_actuel].values.tolist()==[seuil_manche]*nombre_joueurs:
        #     set_actuel='set'+str(int(set_actuel[3])+1)
        #     df.loc[indice_idteam,'nb_set_gagne']+= 1
        #     df.loc[indice_equipe,'point_set_actuel']= 0
        #     df.loc[indice_autreequipe,'point_set_actuel']= 0
        df_event=update_dataframe_volley(df_event,joueur,equipe,set_actuel,variable,score1,score2)
        # Return the updated messages and the updated table data
    return  df.to_dict('records'),df_event.to_dict('records'),set_actuel


@app.callback(Output("page-content", "children"), [Input("url", "pathname")],
    [State('shared-data-store', 'data')])
def render_page_content(pathname, shared_data):
    if pathname == "/":
        return layout_connecter
    elif pathname == "/exhibition":
        return layout_choix_discipline
    elif pathname == "/ligues":
        return html.P("Bienvenue sur l'application! Vous pourriez annoter vos matchs de basketball et de football en direct")
    elif pathname == "/tournoi":
        return layout_tournoi
    elif pathname == "/social":
        return layout_social
    elif pathname==('/social/demande_contact'):
        return layout_social_demande_contact
    elif pathname==('/social/classement'):
        return layout_social_classement
    elif pathname=='/joueurs_du_match':
        return  layout_choix_joueurs
    elif pathname == "/parametres":
        return layout_parameters
    elif pathname=='/parameters/account':
        return html.P("Bienvenue sur l'application! Vous pourriez annoter vos matchs de basketball et de football en direct")
    elif pathname=='/creer_compte':
        return layout_inscription
    elif pathname=='/redefinir_mdp':
        return layout_redefine_mdp
    elif pathname=='/exhibition/party_basket':
        print(f"data après validation: {shared_data}")
        return layout_match_basket_simple
    elif pathname=='/exhibition/party_tennis':
        print(f"data après validation: {shared_data}")
        return layout_match_tennis
    elif pathname=='/exhibition/party_volley':
        print(f"data après validation: {shared_data}")
        return layout_match_volley


   

if __name__ == '__main__':
    app.run_server(port=8100,debug=True)

