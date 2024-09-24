import dash
from dash import dcc, html, Input, Output, State, dash_table,callback
import pandas as pd
import dash_bootstrap_components as dbc
from dao.ligue_dao import insert_one_post,cluster
import datetime

from pages.ligue.annotator_ligue.basket_ligue import display_stat_by_id,get_nom_equipe_ligue
dash.register_page(__name__, path="/party_foot_ligue")

df_event_foot=pd.DataFrame(columns=['player','team','periode','time','event','score1','score2'])


def update_dataframe_foot(data_event,joueur,equipe,periode,temps,event,score1,score2):
    data_event.loc[len(data_event),['player','team','periode','time','event','score1','score2']]=[joueur,equipe,periode,temps,event,score1,score2]
    return data_event

# def update_dataframe_team(data_event,equipe,periode,temps,event,score1,score2):
#     data_event.loc[len(data_event),['team','periode','time','event','score1','score2']]=[equipe,periode,temps,event,score1,score2]
#     return data_event



def score_to_update_click_foot(variable,score,autre_score):
    if variable=='csc':
        autre_score+=1
    elif variable.split('-')[0]=='but':
        score+=1
    return score,autre_score


layout= html.Div([
    html.H1('Panel du match'),
     html.Div(children="Période actuelle", className="menu-title"),
        dcc.Input(id="current-periode-input-foot-ligue", type="number", value=1),
    
        html.Br(),
         html.Div([
        dcc.Input(id='duree-overtime-foot-ligue', type="number", value=5),
        html.Button('Cliquez pour ajouter un overtime', id='validate-overtime-foot-button', n_clicks=0),  # Use a button for validation
    ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}),
   html.Div([
        # html.Div(id='periode-output', style={'margin': '20px', 'fontSize': 20}),
        html.Div(id='nom_equipe1-ligue_foot',children='Team 1', style={'fontSize': 20, 'marginRight': '10px'}),
        # html.Div('Counter 1:', style={'fontSize': 20, 'marginRight': '10px'}),
        html.Div(id='scorecounter1_foot-ligue', children='0', style={'margin': '20px', 'fontSize': 20}),
        html.Div(' - ', style={'fontSize': 20, 'marginRight': '10px', 'marginLeft': '10px'}),
        html.Div(id='scorecounter2_foot-ligue', children='0', style={'margin': '20px', 'fontSize': 20}),
        html.Div(id='nom_equipe2-ligue-foot',children='Team 2', style={'fontSize': 20, 'marginLeft': '10px'})
        
    ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}),
   html.Div('Chrono:', style={'fontSize': 20, 'marginRight': '10px'}),
    html.Div(id='countdown-display_foot-ligue', style={'fontSize': 40, 'textAlign': 'center', 'marginTop': '20px'}),
    # Play/Pause Button
    html.Button('Play', id='play-pause-button_foot-ligue', n_clicks=0, style={'fontSize': 20, 'marginTop': '20px', 'textAlign': 'center', 'display': 'block', 'margin': '0 auto'}),

    # Interval component for ticking every second
    dcc.Interval(
        id='interval-component_foot-ligue',
        interval=1000,  # 1 second
        n_intervals=0,
        disabled=True  # Initially disabled until Play is clicked
    ),
    # Create a table-like structure with rows of buttons per person
    html.Div(id='buttons-container-foot-ligue', style={'padding': '20px'}),
     html.Br(),
    html.H1("Statistiques du match"),
    html.Div(id='stat-container-foot-ligue', style={'padding': '20px'}),
    html.Div(id='stat-container-foot2-ligue', style={"display": "none"}),

    html.H1("Données d'évènements"),
    # Dash DataTable to display the updated dataframe
    dash_table.DataTable(
        id="output_table2_foot-ligue",
            export_format="csv",
        columns=[{"name": i, "id": i} for i in df_event_foot.columns],  # Display dataframe columns
        data=df_event_foot.to_dict('records'),  # Initialize the table with dataframe data
        # filter_action='native',  # Enable filtering
        style_header={
            'backgroundColor': 'rgb(30, 30, 30)',
            'color': 'white'
        },
        style_data={
            'backgroundColor': 'rgb(50, 50, 50)',
            'color': 'white'
        }
    ),
    html.Button('Cliquez 1 fois pour sauvegarder', id='validate-button-exportperf-foot', n_clicks=0) ,
    html.Div(id='text-exportperf-foot',style={'fontSize': 40, 'textAlign': 'center', 'marginTop': '20px'})
])



def display_stat_foot(df):
    layout_stat=dash_table.DataTable(
            id="output_table_foot_render-ligue",
                export_format="csv",
            columns=[{"name": i, "id": i} for i in df.columns],  # Display dataframe columns
            data=df.to_dict('records'),  # Initialize the table with dataframe data
            # filter_action='native',  # Enable filtering
            style_header={
                'backgroundColor': 'rgb(30, 30, 30)',
                'color': 'white'
            },
            style_data={
                'backgroundColor': 'rgb(50, 50, 50)',
                'color': 'white'
            }
        )
    return layout_stat

def display_stat_foot2(df):
    layout_stat=dash_table.DataTable(
            id="gametime_table-ligue",
                export_format="csv",
            columns=[{"name": i, "id": i} for i in df.columns],  # Display dataframe columns
            data=df.to_dict('records'),  # Initialize the table with dataframe data
            # filter_action='native',  # Enable filtering
            style_header={
                'backgroundColor': 'rgb(30, 30, 30)',
                'color': 'white'
            },
            style_data={
                'backgroundColor': 'rgb(50, 50, 50)',
                'color': 'white'
            }
        )
    return layout_stat

def display_buttons_foot(df):
    layout_button=html.Div(
    [html.Div([#df=df_mattch_team
    html.Div(df.loc[i, 'player'], style={'display': 'inline-block', 'width': '100px'}),
        html.Div(df.loc[i, 'team'], style={'display': 'inline-block', 'width': '100px'}),
        html.Button('But normal', id={'type': 'but-normal-button', 'index': i}, n_clicks=0),
        html.Button('But sur penalty', id={'type': 'but-penalty-button', 'index': i}, n_clicks=0),
        html.Button('But sur coup franc', id={'type': 'but-coupfranc-button', 'index': i}, n_clicks=0),
        html.Button('AST', id={'type': 'passe-decisive-button', 'index': i}, n_clicks=0),
        html.Button('CSC', id={'type': 'csc-button', 'index': i}, n_clicks=0),
        html.Button('Carton Jaune', id={'type': 'carton-rouge-button', 'index': i}, n_clicks=0),
        html.Button('Carton rouge', id={'type': 'carton-jaune-button', 'index': i}, n_clicks=0),
        html.Button('Pause jeu', id={'type': 'gametime-button', 'index': i}, n_clicks=0)

    ], style={'padding': '10px'}) for i in df.index])
    return layout_button




def get_nom_exhibition_foot_ligue(shared_data):
    """ Retourne les données des équipes (initialisation du df) 
    df_result à utiliser pour le layout des boutons et des stats"""
    joueurs1=shared_data['donnees_team1-ligue']
    joueurs2=shared_data['donnees_team2-ligue']
    nom_equipe1=shared_data['nomequipe1-ligue']
    nom_equipe2=shared_data['nomequipe2-ligue']
    
    data = {
    'player':joueurs1+joueurs2 ,
    'team':[nom_equipe1]*len(joueurs1)+ [nom_equipe2]*len(joueurs2),
    'id_team':['t1']*len(joueurs1)+['t2']*len(joueurs2),
    'pause':[False]*(len(joueurs1+joueurs2))}
    df_result = pd.DataFrame(data)
    for i in ['but-normal','but-penalty','but-coupfranc','passe-decisive','csc','carton-jaune','carton-rouge','gametime']:
       df_result[i]=0
    print(f"voici les data apres application de get_exhibition{df_result}")

    return df_result




@callback(
    Output('shared-data-store-footbasket', 'data',allow_duplicate=True),
    Input('validate-overtime-foot-button', 'n_clicks'),
    Input('duree-overtime-foot-ligue', 'value'),
    State('shared-data-store-footbasket', 'data'),
    prevent_initial_call=True
)
def add_overtime_foot(n_clicks,duree,shared_data):
    # premier click va permettre d'avoir la valeur de shared_data, deuxième permet d'obtenir discipline
    if n_clicks>=1: 
        shared_data['periode-input']+=1
        shared_data['start-time-input']=duree
    return shared_data

@callback(
    Output('nom_equipe1-ligue-foot', 'children'),Output('nom_equipe2-ligue-foot', 'children',allow_duplicate=True),  # To dynamically update the buttons
    [
    # State({'type': 'output_table_team', 'index': dash.dependencies.ALL}, 'data'),
    Input('shared-data-store-footbasket', 'data')],
    prevent_initial_call=True  #,# Dropdown to choose the annotation system
)
def get_nom_equipes(shared_data):
    """ Retourne le layout des boutons"""
    return get_nom_equipe_ligue(shared_data)



# Useful for layout
@callback(
    Output('buttons-container-foot-ligue', 'children'),Output('stat-container-foot-ligue', 'children'),Output('stat-container-foot2-ligue', 'children'), # To dynamically update the buttons
    [
    # State({'type': 'output_table_team', 'index': dash.dependencies.ALL}, 'data'),
    Input('shared-data-store-footbasket', 'data')]  #,# Dropdown to choose the annotation system
)
def update_display_foot(shared_data):
    """ Retourne le layout des boutons"""
    # Recreate the DataFrame from the stored data
    # Call the display_annot_buttons function with the current DataFrame and annotation system
    # print('on est a update_buttons_display')
    print('not yet, transforation des données partagés pour display boutons et stat')
    df=get_nom_exhibition_foot_ligue(shared_data)
    print('yes')
    donnees_button=display_buttons_foot(df)
    donnees_stat=display_stat_by_id(df,'output_table_foot_render-ligue')
    donnees_stat2=display_stat_by_id(df,'gametime_table-ligue')
    return donnees_button,donnees_stat,donnees_stat2


# Callback to handle play/pause button and the countdown
@callback(
    [Output('interval-component_foot-ligue', 'disabled'),
     Output('play-pause-button_foot-ligue', 'children')],
    [Input('play-pause-button_foot-ligue', 'n_clicks')],
    [State('interval-component_foot-ligue', 'disabled')],
    allow_duplicate=True
)
def toggle_timer_foot(n_clicks, is_disabled):
    if n_clicks % 2 == 1:
        # If odd clicks (Play), enable the interval (timer starts)
        return False, "Pause"
    else:
        # If even clicks (Pause), disable the interval (timer pauses)
        return True, "Play"

@callback(
    Output('countdown-display_foot-ligue', 'children'), 
    Output('interval-component_foot-ligue', 'n_intervals'),
    Output('gametime_table-ligue','data'),
    
    [Input('interval-component_foot-ligue', 'n_intervals'),
     Input('play-pause-button_foot-ligue', 'n_clicks')],
    [State('interval-component_foot-ligue', 'disabled'),
     State('shared-data-store-footbasket', 'data'),
     State('current-periode-input-foot-ligue', 'value'),
     State('countdown-display_foot-ligue','children'),
     Input({'type': 'gametime-button', 'index': dash.dependencies.ALL}, 'n_clicks'),
    State('gametime_table-ligue','data')
     ]
)
def update_timer_foot(n_intervals, play_pause_clicks, is_disabled, shared_data,periode,temps_actuel,game_click,gametable):

    # données pour update gametie et les autres stat
    gametable=pd.DataFrame(gametable) if gametable else get_nom_exhibition_foot_ligue(shared_data)
    temps_total_periode=shared_data['start-time-input-ligue']
    total_periods = int(shared_data.get('periode-input-ligue', 4))
    event=False

    # formatge du temps actuel
    temps_actuel=0 if not temps_actuel else temps_actuel
    if temps_actuel!=0:
        temps_actuel=int(temps_actuel[:2])*60+int(temps_actuel[3:])
    ctx = dash.callback_context
    # Default values if shared_data is None
    if int(temps_actuel) >= temps_total_periode :
        temps_actuel=temps_total_periode
        # print( ctx.triggered[0]['prop_id'])
        # print(f"periode:{periode} vs max periode {total_periods}")

        if str(ctx.triggered[0]['prop_id'])=='play-pause-button_foot-ligue.n_clicks' and periode<total_periods:
            if not play_pause_clicks % 2 == 1:  # Odd number of clicks means play  (complementaire=pause)
                temps_actuel=0  # Reset time for the new period
                n_intervals=0
                event=True
    if not is_disabled and not str(ctx.triggered[0]['prop_id'])=='play-pause-button_foot-ligue.n_clicks' :
        if int(temps_actuel) <temps_total_periode and not event:
            temps_actuel+=1
    
    long_table=len(gametable)
    print(ctx.triggered[0]['prop_id'])
    if not is_disabled:
        # soit dictionnaire.n_click soit un nom de bouton
        dicto=ctx.triggered[0]['prop_id']
        # on veut etudier les dictionnaires
        if dicto not in ['interval-component_foot-ligue.n_intervals','play-pause-button_foot-ligue.n_clicks','gametime_table-ligue.data']:
            # dictionnaire d'interet
            dicto_eval=eval(dicto.split('.')[0])
            if isinstance(dicto_eval,dict):
                #indice du joueur, nombre de click  et nom du bouton
                index_to_change=dicto_eval['index']
                true_gameclick=game_click[index_to_change]
                type_button=dicto_eval['type']

                for i in range(long_table):
                    #individu pas en pause et n'est pas concerné par le changement de statut
                    if not gametable.loc[i,'pause'] and i!=index_to_change:
                        gametable.loc[i,'gametime']+=1
                    #individu en pause revient sur le terrain
                    elif gametable.loc[i,'pause'] and i==index_to_change and true_gameclick % 2 == 1 and type_button=='gametime-button':
                        gametable.loc[i,'pause']=False
                    #individu pas en pause va en pause
                    elif not gametable.loc[i,'pause'] and i==index_to_change and true_gameclick % 2 != 1 and type_button=='gametime-button':
                        gametable.loc[i,'pause']=True
        elif dicto=='play-pause-button_foot-ligue.n_clicks':
            pass
        else:
            #on ajoute une seconde au temps de jeu de ceux pas en pause
            for i in range(long_table):
                if gametable.loc[i,'pause']!=True:
                    gametable.loc[i,'gametime']+=1
    # Format the time in MM:SS format
    minutes, seconds = divmod(temps_actuel, 60)
    time = f"{minutes:02}:{seconds:02}"

    # Format the period based on discipline
    # periode = f"{current_period}MT" if discipline.split('-')[0] == 'football' else f"QT{current_period}"
    return time,n_intervals,gametable.to_dict('records')







# Callback to update each team information and update the table
@callback(
    [Output("output_table_foot_render-ligue", "data"),
    Output("output_table2_foot-ligue", "data"),
    Output("scorecounter1_foot-ligue", "children"),
    Output("scorecounter2_foot-ligue", "children")],
    # Output("periode-output", "children")],
    [Input({'type': 'but-normal-button', 'index': dash.dependencies.ALL}, 'n_clicks'),
    Input({'type': 'but-penalty-button', 'index': dash.dependencies.ALL}, 'n_clicks'),
    Input({'type': 'but-coupfranc-button', 'index': dash.dependencies.ALL}, 'n_clicks'),
    Input({'type': 'passse-decisive-button', 'index': dash.dependencies.ALL}, 'n_clicks'),
    Input({'type': 'csc-button', 'index': dash.dependencies.ALL}, 'n_clicks'),
    Input({'type': 'carton-jaune-button', 'index': dash.dependencies.ALL}, 'n_clicks'),
    Input({'type': 'carton-rouge-button', 'index': dash.dependencies.ALL}, 'n_clicks'),
    State('scorecounter1_foot-ligue', 'children'),
    State('scorecounter2_foot-ligue', 'children'),
    State('output_table_foot_render-ligue', 'data'),
    State('output_table2_foot-ligue', 'data'),
    State('countdown-display_foot-ligue','children'),
    Input('current-periode-input-foot-ligue','value'),
    State('shared-data-store-footbasket', 'data'),
    Input('gametime_table-ligue','data')
    ]
)
def update_person_info_foot(but_normal_clicks,but_pen_clicks,but_cf_clicks,
                        ast_clicks,csc_clicks,jaune_clicks,
                        rouge_clicks,
                        score1,score2,table_data,event_data,time,periode,shared_data,gametime_table):
    score1=int(score1)
    score2=int(score2)
    gametime_table=pd.DataFrame(gametime_table)

    # print(f"input update_person_info_team: {table_data}")
    df_event = pd.DataFrame(event_data)
    df = pd.DataFrame(table_data) if table_data else get_nom_exhibition_foot_ligue(shared_data)
    # df = pd.DataFrame(df_table)
    # print('voila les données pour mise à jour team')
    # print(df)
    # Determine which button was clicked
    ctx = dash.callback_context
    if not ctx.triggered:
        print('no trigger')
        return df.to_dict('records'),df_event.to_dict('records'),str(score1),str(score2)
    print(str(ctx.triggered[0]['prop_id']))
    if str(ctx.triggered[0]['prop_id']) not in ['shared-data-store-footbasket.data','current-periode-input-foot-ligue.value','gametime_table-ligue.data']:
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
                score1,score2=score_to_update_click_foot(variable,score1,score2)
            elif id_team=='t2':
                score2,score1=score_to_update_click_foot(variable,score2,score1)
            
            df_event=update_dataframe_foot(df_event,joueur,equipe,periode,time,variable,score1,score2)
            # Return the updated messages and the updated table data
    
    df.pause=gametime_table.pause.values.tolist()
    df.gametime=gametime_table.gametime.values.tolist()
    return  df.to_dict('records'),df_event.to_dict('records'),str(score1),str(score2)




@callback(
    Output('text-exportperf-foot', 'children',allow_duplicate=True),
    Input('shared-data-ligue','data'),
    Input('shared-data-store-footbasket','data'),
    Input('validate-button-exportperf-foot', 'n_clicks'),
    Input('output_table_foot_render-ligue', 'data'),
    Input('output_table2_foot-ligue', 'data'),
    prevent_initial_call=True
)
def export_perf(shared_data_ligue,share_data_match,n_clicks,df_stat,df_event):
    if n_clicks>=1:
        dff_event=pd.DataFrame(df_event)
        print('dff_event')
        print(dff_event)
        print(dff_event.columns)
        print(dff_event.tail(1))
        donnees_finale=dff_event.tail(1).loc[:,['score1','score2']]
        donnees_finale['equipe1']=share_data_match['nomequipe1-ligue']
        donnees_finale['equipe2']=share_data_match['nomequipe2-ligue']
        joueurs1=share_data_match['donnees_team1-ligue']
        joueurs2=share_data_match['donnees_team2-ligue']
        ligue= shared_data_ligue['ligue_name']
        date=datetime.date.today().strftime('%d/%m/%Y')
        heure=datetime.datetime.now().strftime('%H:%M:%S')
        post={'discipline':share_data_match['discipline_to_choose'],'date_enregistrement':date,'heure_enregistrement':heure,'saison':shared_data_ligue['saison'],'nom_equipe1':share_data_match['nomequipe1-ligue'],
        'nom_equipe2':share_data_match['nomequipe2-ligue'],'statistiques':df_stat,'evenement':df_event,'stat_finale':donnees_finale.to_dict('records'),'joueurs_equipe1':joueurs1,'joueurs_equipe2':joueurs2}
        print('export à venir')
        print(donnees_finale)
        db=cluster['Ligues']
        collist = db.list_collection_names()
        print(f"collist {collist}")
        if ligue in collist:
            print('exist')
            db[ligue].insert_one(post)
            return 'Données exportées'
        else:
            print('dont exist')
            coll=db[ligue]
            coll.insert_one(post)
            return 'Données exportées'
    else:
        return dash.no_update