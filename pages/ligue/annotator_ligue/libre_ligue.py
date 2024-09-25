# import pandas as pd
# import dash
# import dash_bootstrap_components as dbc
# import numpy as np
# from dash import dcc, html, Input, Output,dash_table,State, callback
# import datetime

# from pages.ligue.annotator_ligue.basket_ligue import display_stat_by_id,get_nom_equipe_ligue


# dash.register_page(__name__, path="/party_freediscipline_ligue")


# df_event_libre=pd.DataFrame(columns=['player','team','event','score1','score2'])


# def update_dataframe_libre(data_event,joueur,equipe,event,score1,score2):
#     data_event.loc[len(data_event),['player','team','event','score1','score2']]=[joueur,equipe,event,score1,score2]
#     return data_event


# def score_to_update_click_libre(variable,score,autre_score):
#     if variable=='retrait':
#         score-=1
#     elif variable=='ajout-point':
#         score+=1
#     return score,autre_score,event



# layout= html.Div([
#     html.H1('Panel du match'),
#     # Create a table-like structure with rows of buttons per person
#     html.Div(id='buttons-container-libre-ligue', style={'padding': '20px'}),
#     html.Br(),
#     html.H1("Statistiques du match"),
#     html.Div(id='stat-container-libre-ligue', style={'padding': '20px'}),
#     html.Div(id='stat-container-libre2-ligue', style={'padding': '20px'}),
#     html.H1("Données d'évènements"),
#     # Dash DataTable to display the updated dataframe
#     dash_table.DataTable(
#         id="output_table2_libre-ligue",
#             export_format="csv",
#         columns=[{"name": i, "id": i} for i in df_event_libre.columns],  # Display dataframe columns
#         data=df_event_libre.to_dict('records'),  # Initialize the table with dataframe data
#         # filter_action='native',  # Enable filtering
#         style_header={
#             'backgroundColor': 'rgb(30, 30, 30)',
#             'color': 'white'
#         },
#         style_data={
#             'backgroundColor': 'rgb(50, 50, 50)',
#             'color': 'white'
#         }
#     ),
#     html.Button('Cliquez 1 fois pour sauvegarder', id='validate-button-exportperf-libre', n_clicks=0) ,
#     html.Div(id='text-exportperf-libre',style={'fontSize': 40, 'textAlign': 'center', 'marginTop': '20px'})
# ])

# def display_stat_libre(df):
#     layout_stat=dash_table.DataTable(
#             id="output_table_team_render_libre-ligue",
#                 export_format="csv",
#             columns=[{"name": i, "id": i} for i in df.columns],  # Display dataframe columns
#             data=df.to_dict('records'),  # Initialize the table with dataframe data
#             # filter_action='native',  # Enable filtering
#             style_header={
#                 'backgroundColor': 'rgb(30, 30, 30)',
#                 'color': 'white'
#             },
#             style_data={
#                 'backgroundColor': 'rgb(50, 50, 50)',
#                 'color': 'white'
#             }
#         )
#     return layout_stat




# def display_buttons_libre(df):
#     layout_button=html.Div(
#     [html.Div([#df=df_mattch_team
#     html.Div(df.loc[i, 'player'], style={'display': 'inline-block', 'width': '100px'}),
#         html.Div(df.loc[i, 'team'], style={'display': 'inline-block', 'width': '100px'}),
#         html.Button('ajout-point', id={'type': 'pointlibre-button', 'index': i}, n_clicks=0),
#         html.Button('retrait-point', id={'type': 'pointlibre-button', 'index': i}, n_clicks=0)
#     ], style={'padding': '10px'}) for i in df.index])
#     return layout_button



# def get_nom_exhibition_libre_ligue(shared_data):
#     """ Retourne les données des équipes (initialisation du df) 
#     df_result à utiliser pour le layout des boutons et des stats"""
#     nombre_set_gagnant=3
#     joueurs1=shared_data['donnees_team1-ligue']
#     joueurs2=shared_data['donnees_team2-ligue']
#     nom_equipe1=shared_data['nomequipe1-ligue']
#     nom_equipe2=shared_data['nomequipe2-ligue']
#     data = {
#     'player':joueurs1+joueurs2 ,
#     'team':[nom_equipe1]*len(joueurs1)+ [nom_equipe2]*len(joueurs2),
#     'id_team':['t1']*len(joueurs1)+['t2']*len(joueurs2)}
#     df_result = pd.DataFrame(data)
#     variable=['ajout-point','retrait-point']
#     for i in variables:
#            df_result[i]=0
#     print(f"voici les data apres application de get_exhibition{df_result}")
#     return df_result


# ### libre ###
# @callback(
#     Output('buttons-container-libre-ligue', 'children'),Output('stat-container-libre-ligue', 'children'),  # To dynamically update the buttons
#     [
#     # State({'type': 'output_table_team', 'index': dash.dependencies.ALL}, 'data'),
#     Input('shared-data-store-footbasket', 'data')
#     ]
#     )
# def update_display_libre(shared_data):
#     """ Retourne le layout des boutons"""
#     # Recreate the DataFrame from the stored data
#     # Call the display_annot_buttons function with the current DataFrame and annotation system
#     # print('on est a update_buttons_display')
#     print('not yet, transforation des données partagés pour display boutons et stat')
#     df=get_nom_exhibition_libre_ligue(shared_data)
#     df2=get_nom_exhibition_libre_individuel_ligue(shared_data)

#     print('yes')
#     donnees_button=display_buttons_libre(df)
#     donnees_stat=display_stat_by_id(df,'output_table_team_render_libre-ligue')

#     return donnees_button,donnees_stat


# # Callback to update each team information and update the table
# @callback(
#     [Output("output_table_team_render_libre-ligue", "data"),
#     Output("output_table2_libre-ligue", "data")],
#     # Output("periode-output", "children")],
#     [Input({'type': 'pointlibre-button', 'index': dash.dependencies.ALL}, 'n_clicks'),
#     State('output_table_team_render_libre-ligue', 'data'),
#     State('output_table2_libre-ligue', 'data'),
#     State('shared-data-store-footbasket', 'data')
#     ]
# )
# def update_person_info_team_libre(pt_click,table_data,event_data,shared_data):
    
#     # print(f"input update_person_info_team: {table_data}")
#     df_event = pd.DataFrame(event_data)
#     df = pd.DataFrame(table_data) if table_data else get_nom_exhibition_libre(shared_data)

#     print(df)
    

    
#     # df = pd.DataFrame(df_table)
#     # print('voila les données pour mise à jour team')
#     # print(df)
    
    
#     # Determine which button was clicked
#     ctx = dash.callback_context
#     print(f"trigger: {ctx.triggered}")
#     # if not ctx.triggered:
#     #     return df.to_dict('records'),df_event.to_dict('records'),str(score1),str(score2)
#     # Extract the button information in JSON format
#     triggered_button = ctx.triggered[0]['prop_id']
#     button_info = eval(triggered_button.split('.')[0])  # Safely parse the button's JSON structure
#     button_type = button_info['type']
#     person_id = button_info['index']
#     variable=button_type.split('-button')[0]
#     # si un boutton est appuyé    (par defaut le xtx.triggered est long et le bouton "3pt-button" aurait été appuyé)
#     if not len(ctx.triggered)>1:
#         equipe=df.loc[person_id,'team']
#         id_team=df.loc[person_id,'id_team']
#         indice_idteam=df.loc[df.id_team==id_team].index.tolist()
#         indice_equipe=df.loc[df.id_team=='t1'].index.tolist()
#         nombre_joueurs=len(indice_equipe)
#         indice_autreequipe=df.loc[df.id_team=='t2'].index.tolist()
#         score1=df.loc[indice_equipe,set_actuel].unique().tolist()[0]
#         score2= df.loc[indice_autreequipe,set_actuel].unique().tolist()[0]
#         joueur=df.loc[person_id,'player']
#         if id_team=='t1':
#             score1,score2,event=score_to_update_click_libre(score1,score2)
#         elif id_team=='t2':
#             score2,score1,event=score_to_update_click_libre(score2,score1)
#         df.loc[indice_equipe,set_actuel]= score1
#         df.loc[indice_autreequipe,set_actuel]= score2

#         if event:
#             # df.loc[indice_equipe,set_actuel]=score1
#             # df.loc[indice_autreequipe,set_actuel]=score2
#             df.loc[indice_idteam,'nb_set_gagne']+= 1
#             df.loc[indice_equipe,set_actuel]= 0
#             df.loc[indice_autreequipe,set_actuel]= 0
#             set_actuel='set'+str(int(set_actuel[3])+1)
#         df_event=update_dataframe_libre(df_event,joueur,equipe,set_actuel,variable,score1,score2)
#     return  df.to_dict('records'),df_event.to_dict('records'),df_individual_data.to_dict('records'),set_actuel






# @callback(
#     Output('text-exportperf-libre', 'children',allow_duplicate=True),
#     Input('shared-data-ligue','data'),
#     Input('shared-data-store-footbasket','data'),
#     Input('validate-button-exportperf-libre', 'n_clicks'),
#     Input('output_table_team_render_libre-ligue', 'data'),
#     Input('output_table2_libre-ligue', 'data'),
#     Input('output_table_individuel_libre-ligue', 'data'),
#     prevent_initial_call=True
# )
# def export_perf_vollley(shared_data_ligue,share_data_match,n_clicks,df_stat,df_event,df_individual):
#     if n_clicks>=1:
#         ligue= shared_data_ligue['ligue_name']
#         date=datetime.date.today().strftime('%d/%m/%Y')
#         heure=datetime.datetime.now().strftime('%H:%M:%S')
#         joueurs1=share_data_match['donnees_team1-ligue']
#         joueurs2=share_data_match['donnees_team2-ligue']
#         post={'discipline':share_data_match['discipline_to_choose'],'date_enregistrement':date,'heure_enregistrement':heure,'saison':shared_data_ligue['saison'],'nom_equipe1':share_data_match['nomequipe1-ligue'],
#         'nom_equipe2':share_data_match['nomequipe2-ligue'],'statistiques':df_individual,'evenement':df_event,'stat_par_periode':df_stat,'joueurs_equipe1':joueurs1,'joueurs_equipe2':joueurs2}
#         print('export à venir')
#         print(donnees_finale)
#         db=cluster['Ligues']
#         collist = db.list_collection_names()
#         print(f"collist {collist}")
#         if ligue in collist:
#             print('exist')
#             db[ligue].insert_one(post)
#             return 'Données exportées'
#         else:
#             print('dont exist')
#             coll=db[ligue]
#             coll.insert_one(post)
#             return 'Données exportées'
#     else:
#         return dash.no_update

