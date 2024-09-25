import pandas as pd
import dash
import dash_bootstrap_components as dbc
import numpy as np
from dash import dcc, html, Input, Output,dash_table,State, callback


dash.register_page(__name__, path="/exhibition/party_basket")


df_event_team=pd.DataFrame(columns=['player','team','periode','time','event','score1','score2'])


def update_dataframe_general(data_event,joueur,equipe,periode,temps,event,score1,score2):
    data_event.loc[len(data_event),['player','team','periode','time','event','score1','score2']]=[joueur,equipe,periode,temps,event,score1,score2]
    return data_event

# def update_dataframe_team(data_event,equipe,periode,temps,event,score1,score2):
#     data_event.loc[len(data_event),['team','periode','time','event','score1','score2']]=[equipe,periode,temps,event,score1,score2]
#     return data_event


def score_to_update_click(variable,score,sys_point):
    if sys_point=='point_normal':
        if variable=='3pt-reussi':
            score+=3
        elif variable=='2pt-reussi':
            score+=2
        elif variable=='lf-reussi':
            score+=1
    elif sys_point=='point_mini':
        if variable=='3pt-reussi':
            score+=2
        elif variable=='2pt-reussi':
            score+=1
        elif variable=='lf-reussi':
            score+=1
    return score


layout= html.Div([
    html.H1('Panel du match'),
     html.Div(children="Période actuelle", className="menu-title"),
        dcc.Input(id="current-periode-input", type="number", value=1),
     html.Div(children="Système de point", className="menu-title"),
        dcc.Dropdown(
            id="sys_pt_basket_team",
            options=[{"label": x, "value": y} for x, y in [['3PT=3,2PT=2', 'point_normal'], ['3PT=2,2PT=1', 'point_mini']]],
            clearable=False,
            value='point_normal',
            className="dropdown"
        ),
    html.Div(children="Type d'annotation", className="menu-title"),
    dcc.Dropdown(
        id="sys_annot",
        options=[{"label": x, "value": y} for x, y in [['Simple', 'annot_simple'], ['Complet', 'annot_complet']]],
        clearable=False,
        value='annot_simple',
        className="dropdown"
    ),
        html.Br(),
         html.Div([
                    html.Div(children="Durée de l'overtime (s) "),

        dcc.Input(id='duree-overtime', type="number", value=5),
        html.Button('Cliquez pour ajouter un overtime', id='validate-overtime-button', n_clicks=0),  # Use a button for validation
    ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}),
   html.Div([
        # html.Div(id='periode-output', style={'margin': '20px', 'fontSize': 20}),
        html.Div(id='nom_equipe1',children='Team 1', style={'fontSize': 20, 'marginRight': '10px'}),
        # html.Div('Counter 1:', style={'fontSize': 20, 'marginRight': '10px'}),
        html.Div(id='scorecounter1_team', children='0', style={'margin': '20px', 'fontSize': 20}),
        html.Div(' - ', style={'fontSize': 20, 'marginRight': '10px', 'marginLeft': '10px'}),
        html.Div(id='scorecounter2_team', children='0', style={'margin': '20px', 'fontSize': 20}),
        html.Div(id='nom_equipe2',children='Team 2', style={'fontSize': 20, 'marginLeft': '10px'})
        
    ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}),
   html.Div('Chrono:', style={'fontSize': 20, 'marginRight': '10px'}),
    html.Div(id='countdown-display_team', style={'fontSize': 40, 'textAlign': 'center', 'marginTop': '20px'}),
    # Play/Pause Button
    html.Button('Play', id='play-pause-button_team', n_clicks=0, style={'fontSize': 20, 'marginTop': '20px', 'textAlign': 'center', 'display': 'block', 'margin': '0 auto'}),

    # Interval component for ticking every second
    dcc.Interval(
        id='interval-component_team',
        interval=1000,  # 1 second
        n_intervals=0,
        disabled=True  # Initially disabled until Play is clicked
    ),
    dcc.Store(id='countdown-value_team',data=60),
    # Create a table-like structure with rows of buttons per person
    html.Div(id='buttons-container', style={'padding': '20px'}),
     html.Br(),
    html.H1("Statistiques du match"),
    html.Div(id='stat-container', style={'padding': '20px'}),
    html.Div(id='stat-container2', style={"display": "none"}),

     html.Br(),

    html.H1("Données d'évènements"),
    # Dash DataTable to display the updated dataframe
    dash_table.DataTable(
        id="output_table2_team",
            export_format="csv",
        columns=[{"name": i, "id": i} for i in df_event_team.columns],  # Display dataframe columns
        data=df_event_team.to_dict('records'),  # Initialize the table with dataframe data
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
         html.Br(),

    html.H1("Données par période"),
    html.Div(id='table_qt_container', style={'padding': '20px'})
])


def display_stat(df):
    layout_stat=dash_table.DataTable(
            id="output_table_team_render",
                export_format="csv",
            columns=[{"name": i, "id": i} for i in df.columns],  # Display dataframe columns
            data=df.to_dict('records'),  # Initialize the table with dataframe data
            filter_action='native',  # Enable filtering
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

def display_statqt(df):
    print(f"df period:{df}")
    layout_stat2=dash_table.DataTable(
            id="table_qt",
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
    return layout_stat2

def display_stat_timebasket(df):
    layout_stat=dash_table.DataTable(
            id="gametime_table_bsk",
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


def display_buttons(df,sys_annot):
    if sys_annot=='annot_simple':
        layout_button=html.Div(
        [html.Div([#df=df_mattch_team
        html.Div(df.loc[i, 'player'], style={'display': 'inline-block', 'width': '100px'}),
            html.Div(df.loc[i, 'team'], style={'display': 'inline-block', 'width': '100px'}),
            html.Button('3pt tentative', id={'type': '3pt-button', 'index': i}, n_clicks=0),
            html.Button('3pt reussi', id={'type': '3pt-reussi-button', 'index': i}, n_clicks=0),
            html.Button('3pt loupé', id={'type': '3pt-echoue-button', 'index': i}, n_clicks=0),

            html.Button('2pt tentative', id={'type': '2pt-button', 'index': i}, n_clicks=0),
            html.Button('2pt reussi', id={'type': '2pt-reussi-button', 'index': i}, n_clicks=0),
            html.Button('2pt loupé', id={'type': '2pt-echoue-button', 'index': i}, n_clicks=0),

            html.Button('LF tentative', id={'type': 'lf-button', 'index': i}, n_clicks=0),
            html.Button('LF reussi', id={'type': 'lf-reussi-button', 'index': i}, n_clicks=0),
            html.Button('LF loupé', id={'type': 'lf-echoue-button', 'index': i}, n_clicks=0),
            html.Button('Faute', id={'type': 'faute-button', 'index': i}, n_clicks=0),
        html.Button('Pause jeu', id={'type': 'gametime-button', 'index': i}, n_clicks=0)

        ], style={'padding': '10px'}) for i in df.index])
       
    elif sys_annot=='annot_complet':
        layout_button=html.Div(
        [html.Div([#df=df_mattch
            html.Div(df.loc[i, 'player'], style={'display': 'inline-block', 'width': '100px'}),
            html.Div(df.loc[i, 'team'], style={'display': 'inline-block', 'width': '100px'}),
            html.Div([
            html.Button('3pt', id={'type': '3pt-button', 'index': i}, n_clicks=0),
            html.Button('3pt reussi', id={'type': '3pt-reussi-button', 'index': i}, n_clicks=0),
            html.Button('3pt loupé', id={'type': '3pt-echoue-button', 'index': i}, n_clicks=0),

            html.Button('2pt', id={'type': '2pt-button', 'index': i}, n_clicks=0),
            html.Button('2pt reussi', id={'type': '2pt-reussi-button', 'index': i}, n_clicks=0),
            html.Button('2pt loupé', id={'type': '2pt-echoue-button', 'index': i}, n_clicks=0),

            html.Button('LF', id={'type': 'lf-button', 'index': i}, n_clicks=0),
            html.Button('LF reussi', id={'type': 'lf-reussi-button', 'index': i}, n_clicks=0),
            html.Button('LF loupé', id={'type': 'lf-echoue-button', 'index': i}, n_clicks=0),

            html.Button('Faute', id={'type': 'faute-button', 'index': i}, n_clicks=0),
            html.Button('Reb', id={'type': 'reb-button', 'index': i}, n_clicks=0),
            html.Button('AST', id={'type': 'ast-button', 'index': i}, n_clicks=0),
            html.Button('STL', id={'type': 'stl-button', 'index': i}, n_clicks=0),
            html.Button('BLK', id={'type': 'blk-button', 'index': i}, n_clicks=0),
            html.Button('TO', id={'type': 'to-button', 'index': i}, n_clicks=0),
        html.Button('Pause jeu', id={'type': 'gametime-button', 'index': i}, n_clicks=0)], style={'display': 'flex', 'flex-wrap': 'wrap', 'gap': '5px'})
        ], style={'padding': '10px'}) for i in df.index]
    )
    
    return layout_button




def get_nom_exhibition(shared_data,sys_annot):
    """ Retourne les données des équipes (initialisation du df) 
    df_result à utiliser pour le layout des boutons et des stats"""
    donnees_equipes1=shared_data['donnees_team1'].split(',')
    donnees_equipes2=shared_data['donnees_team2'].split(',')
    nom_equipe1=shared_data['nomequipe1']
    nom_equipe2=shared_data['nomequipe2']
    joueurs1=donnees_equipes1
    joueurs2=donnees_equipes2
    data = {
    'player':joueurs1+joueurs2 ,
    'team':[nom_equipe1]*len(joueurs1)+ [nom_equipe2]*len(joueurs2),
    'id_team':['t1']*len(joueurs1)+['t2']*len(joueurs2),
    'pause':[False]*len(joueurs1+joueurs2)}
    df_result = pd.DataFrame(data)
    if sys_annot=='annot_simple':
        variables=['3pt','3pt-reussi','3pt-echoue','2pt','2pt-reussi','2pt-echoue','lf','lf-reussi','lf-echoue','faute','gametime']
    else:
        variables=['3pt','3pt-reussi','3pt-echoue','2pt','2pt-reussi','2pt-echoue','lf','lf-reussi','lf-echoue','faute','reb','ast','stl','blk','to','gametime']
    for i in variables:
       df_result[i]=0
    print(f"voici les data apres application de get_exhibition{df_result}")

    return df_result



def get_initqt(shared_data):
    """ Retourne les données des équipes (initialisation du df) 
    df_result à utiliser pour le layout des boutons et des stats"""
    print(f'share data for initqt:{shared_data}')
    nom_equipe1=shared_data['nomequipe1']
    nom_equipe2=shared_data['nomequipe2']
    nombre_periode=shared_data['periode-input']
    liste_periode=range(1,nombre_periode+1)

    data = {
    'team':[nom_equipe1,nom_equipe2]}
    df_result = pd.DataFrame(data)
    for i in liste_periode:
       df_result[str(i)]=0
    str_liste_periode=[str(i) for i in range (1,nombre_periode+1)]
    df_result['total']=df_result[str_liste_periode].sum(axis=1).values.tolist()
    print(f"voici les data apres application de get_initqt{df_result}")
    return df_result

def get_donnees_per_period(data_stat,data_event,shared_data):
    df_vierge=pd.DataFrame()
    df_vierge['team']=data_stat['team'].unique()
    nombre_periode=shared_data['periode-input']
    liste_periode=range(1,nombre_periode+1)
    liste=[]
    for periode in liste_periode:
        sous_df=data_event.loc[data_event['periode']==periode,['score1','score2']].values.tolist()
        # print(f'df interet:{sous_df}')

        if len(sous_df)>=1:
            result=sous_df[-1]
            if periode>1:
                dernier_results=data_event.loc[data_event['periode']==periode-1,['score1','score2']].values.tolist()
                if len(dernier_results)>=1:
                    dernier_result=dernier_results[-1]
                else:
                    dernier_result=[0,0]
                result=np.subtract(result,dernier_result)
        else:
            result=[0,0]
        
        df_vierge[str(periode)]=result
    str_liste_periode=[str(i) for i in range (1,nombre_periode+1)]
    df_vierge['total']=df_vierge[str_liste_periode].sum(axis=1).values.tolist()
    return df_vierge



# import pandas as pd;shared_data={'discipline_to_choose': 'basket', 'periode-input': 4, 'start-time-input': 900, 'donnees_team1': 'at,ag', 'donnees_team2': 'bv,bd', 'nomequipe1': 't1', 'nomequipe2': 't2'};get_initqt(shared_data)



### Basket ###


@callback(
    Output('shared-data-store', 'data',allow_duplicate=True),
    Input('validate-overtime-button', 'n_clicks'),
    Input('duree-overtime', 'value'),
    State('shared-data-store', 'data'),
    prevent_initial_call=True
)
def add_overtime(n_clicks,duree,shared_data):
    # premier click va permettre d'avoir la valeur de shared_data, deuxième permet d'obtenir discipline
    if n_clicks>=1: 
        shared_data['periode-input']+=1
        shared_data['start-time-input']=duree
    return shared_data
# Useful for layout
@callback(
    Output('buttons-container', 'children'),Output('stat-container', 'children'),Output('table_qt_container', 'children'),Output('stat-container2', 'children'),  # To dynamically update the buttons
    [
    # State({'type': 'output_table_team', 'index': dash.dependencies.ALL}, 'data'),
    Input('shared-data-store', 'data'),
    Input('sys_annot', 'value')]  #,# Dropdown to choose the annotation system
)
def update_display(shared_data,annot_system):
    """ Retourne le layout des boutons"""
    # Recreate the DataFrame from the stored data
    # Call the display_annot_buttons function with the current DataFrame and annotation system
    # print('on est a update_buttons_display')
    print(f"shared data for display button and stat: {shared_data}")
    df=get_nom_exhibition(shared_data,annot_system)
    donnees_button=display_buttons(df,annot_system)
    donnees_stat=display_stat(df)
    donnees_stat2=display_stat_timebasket(df)
    df_temp=get_initqt(shared_data)
    donnees_qt=display_statqt(df_temp)
    print(f"df_period update display:{donnees_qt}")
    return donnees_button,donnees_stat,donnees_qt,donnees_stat2


# Callback to handle play/pause button and the countdown
@callback(
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

@callback(
    Output('countdown-display_team', 'children'), 
    Output('interval-component_team', 'n_intervals'),
    Output('gametime_table_bsk','data'),

    [Input('interval-component_team', 'n_intervals'),
     Input('play-pause-button_team', 'n_clicks')],
    [State('interval-component_team', 'disabled'),
     State('shared-data-store', 'data'),
     State('current-periode-input', 'value'),
     Input({'type': 'gametime-button', 'index': dash.dependencies.ALL}, 'n_clicks'),
    State('gametime_table_bsk','data'),
        Input('sys_annot','value')
]
)
def update_timer_team(n_intervals, play_pause_clicks, is_disabled, shared_data,periode,game_click,gametable,annot_sys):
     # données pour update gametie et les autres stat
    gametable=pd.DataFrame(gametable) if gametable else get_nom_exhibition(shared_data,annot_sys)
    ctx = dash.callback_context
    # Default values if shared_data is None
    countdown_start = shared_data.get('start-time-input', 900)
    # print([countdown_start,n_intervals])

    discipline = shared_data['discipline_to_choose']
    total_periods = shared_data['periode-input']
    # if is_disabled:
    #     return dash.no_update, dash.no_update, gametable.to_dict('records')

    remaining_time = int(countdown_start) - n_intervals
    if remaining_time <= 0 :
        remaining_time=0
        if 'play-pause-button_team' in ctx.triggered[0]['prop_id'] and periode<total_periods:
            if not play_pause_clicks % 2 == 1:  # Odd number of clicks means play  (complementaire=pause)
                remaining_time = int(shared_data.get('start-time-input', 900))  # Reset time for the new period
                n_intervals=0
    
    long_table=len(gametable)
    
    print(ctx.triggered[0]['prop_id'])
    if not is_disabled:
        # soit dictionnaire.n_click soit un nom de bouton
        dicto=ctx.triggered[0]['prop_id']
        # on veut etudier les dictionnaires
        if dicto not in ['interval-component_team.n_intervals','play-pause-button_team.n_clicks','gametime_table.data']:
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
        elif dicto in 'play-pause-button_team.n_clicks':
            pass
        else:
            #on ajoute une seconde au temps de jeu de ceux pas en pause
            for i in range(long_table):
                if gametable.loc[i,'pause']!=True:
                    gametable.loc[i,'gametime']+=1
    # Format the time in MM:SS format
    minutes, seconds = divmod(remaining_time, 60)
    time = f"{minutes:02}:{seconds:02}"

    # Format the period based on discipline
    # periode = f"{current_period}MT" if discipline.split('-')[0] == 'football' else f"QT{current_period}"
    return time,n_intervals,gametable.to_dict('records')



# Callback to update each team information and update the table
@callback(
    [Output("output_table_team_render", "data"),
    Output("output_table2_team", "data"),
    Output("table_qt", "data"),
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
    Input({'type': 'faute-button', 'index': dash.dependencies.ALL}, 'n_clicks'),
    Input({'type': 'reb-button', 'index': dash.dependencies.ALL}, 'n_clicks'),
    Input({'type': 'ast-button', 'index': dash.dependencies.ALL}, 'n_clicks'),
    Input({'type': 'stl-button', 'index': dash.dependencies.ALL}, 'n_clicks'),
    Input({'type': 'blk-button', 'index': dash.dependencies.ALL}, 'n_clicks'),
    Input({'type': 'to-button', 'index': dash.dependencies.ALL}, 'n_clicks'),
    State('scorecounter1_team', 'children'),
    State('scorecounter2_team', 'children'),
    State('output_table_team_render', 'data'),
    State('output_table2_team', 'data'),
    State('table_qt', 'data'),
    State('countdown-display_team','children'),
    Input('current-periode-input','value'),
    Input('sys_pt_basket_team','value'),
    Input('sys_annot','value'),
    State('shared-data-store', 'data'),
    Input('gametime_table_bsk','data')
    ]
)
def update_person_info_team(trois_pt_clicks,trois_pt_reussi_clicks,trois_pt_echoue_clicks,
                        deux_pt_clicks,deux_pt_reussi_clicks,deux_pt_echoue_clicks,
                        lf_clicks,lf_reussi_clicks,lf_echoue_clicks,faute_click,
                        reb_clicks,ast_clicks,stl_clicks,blk_clicks,to_clicks,
                        score1,score2,table_data,event_data,period_data,time,periode,sys_point,sys_annot,shared_data,gametime_table):

    gametime_table=pd.DataFrame(gametime_table)  if gametime_table else get_nom_exhibition(shared_data,sys_annot) 
    score1=int(score1)
    score2=int(score2)
    # print(f"input update_person_info_team: {table_data}")
    df_event = pd.DataFrame(event_data,columns=['player','team','periode','time','event','score1','score2'])
    df = pd.DataFrame(table_data) if table_data else get_nom_exhibition(shared_data,sys_annot)
    df_periode= pd.DataFrame(period_data) if period_data else get_initqt(shared_data)

    # Determine which button was clicked
    ctx = dash.callback_context
    print( {trigger['prop_id'].split('.')[0]: trigger['value'] for trigger in ctx.triggered})
    if not ctx.triggered:
        print('no trigger')
        return df.to_dict('records'),df_event.to_dict('records'),df_periode.to_dict('records'),str(score1),str(score2)
    # Extract the button information in JSON format
    print(str(ctx.triggered))

    if str(ctx.triggered[0]['prop_id']) not in ['shared-data-store.data','current-periode-input.value','gametime_table_bsk.data']:
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
            df_event=update_dataframe_general(df_event,joueur,equipe,int(periode),time,variable,score1,score2)
            # Return the updated messages and the updated table data
    df_periode=get_donnees_per_period(df.copy(),df_event.copy(),shared_data.copy())
    print(f"periode:{df_periode}")
    df.pause=gametime_table.pause.values.tolist()
    df.gametime=gametime_table.gametime.values.tolist()
    return  df.to_dict('records'),df_event.to_dict('records'),df_periode.to_dict('records'),str(score1),str(score2)

