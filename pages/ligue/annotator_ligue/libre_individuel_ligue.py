import pandas as pd
import dash
import dash_bootstrap_components as dbc
import numpy as np
from dash import dcc, html, Input, Output,dash_table,State, callback
import datetime

from pages.ligue.annotator_ligue.basket_ligue import display_stat_by_id,get_nom_equipe_ligue


dash.register_page(__name__, path="/party_free_solo_ligue")



df_event_freesolo=pd.DataFrame(columns=['player','time','event'])

def update_dataframe_general(data_event,joueur,temps,event):
    data_event.loc[len(data_event),['player','time','event']]=[joueur,temps,event]
    return data_event

# def update_dataframe_team(data_event,equipe,periode,temps,event,score1,score2):
#     data_event.loc[len(data_event),['team','periode','time','event','score1','score2']]=[equipe,periode,temps,event,score1,score2]
#     return data_event


def score_to_update_click(df,id,variable):
    if variable=='ajout-point':
        df.loc[id,'score']+=1
    elif variable=='retrait-point':
        df.loc[id,'score']-=1
    return df



layout= html.Div([
    html.H1('Panel du match'),
   html.Div('Chrono:', style={'fontSize': 20, 'marginRight': '10px'}),
    html.Div(id='countdown-display_team-ligue-freesolo', style={'fontSize': 40, 'textAlign': 'center', 'marginTop': '20px'}),
    # Play/Pause Button
    html.Button('Play', id='play-pause-button_team-ligue-freesolo', n_clicks=0, style={'fontSize': 20, 'marginTop': '20px', 'textAlign': 'center', 'display': 'block', 'margin': '0 auto'}),

    # Interval component for ticking every second
    dcc.Interval(
        id='interval-component_team-ligue-freesolo',
        interval=1000,  # 1 second
        n_intervals=0,
        disabled=True  # Initially disabled until Play is clicked
    ),
    dcc.Store(id='countdown-value_team-ligue-freesolo',data=60),
    # Create a table-like structure with rows of buttons per person
    html.Div(id='buttons-container-ligue-freesolo', style={'padding': '20px'}),
     html.Br(),
    html.H1("Statistiques du match"),
    html.Div(id='stat-container-ligue-freesolo', style={'padding': '20px'}),
    html.Div(id='stat-container2-ligue-freesolo', style={"display": "none"}),

     html.Br(),

    html.H1("Données d'évènements"),
    # Dash DataTable to display the updated dataframe
    dash_table.DataTable(
        id="output_table2_team-ligue-freesolo",
            export_format="csv",
        columns=[{"name": i, "id": i} for i in df_event_freesolo.columns],  # Display dataframe columns
        data=df_event_freesolo.to_dict('records'),  # Initialize the table with dataframe data
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

     html.Button('Cliquez 1 fois pour sauvegarder', id='validate-button-exportperf-freesolo', n_clicks=0) ,
    html.Div(id='text-exportperf-freesolo',style={'fontSize': 40, 'textAlign': 'center', 'marginTop': '20px'})
 # Use a button for validation

])


def display_stat_by_id(df,id_input):
    layout_stat=dash_table.DataTable(
            id=id_input,
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

def display_buttons(df):
    
    layout_button=html.Div(
    [html.Div([#df=df_mattch
        html.Div(df.loc[i, 'player'], style={'display': 'inline-block', 'width': '100px'}),
        html.Div([
        html.Button('Ajout', id={'type': 'ajout-point-button', 'index': i}, n_clicks=0),
        html.Button('Retrait', id={'type': 'retrait-point-button', 'index': i}, n_clicks=0)], style={'display': 'flex', 'flex-wrap': 'wrap', 'gap': '5px'})
    ], style={'padding': '10px'}) for i in df.index]
) 
    return layout_button




def get_nom_exhibition_freesolo(shared_data):
    """ Retourne les données des équipes (initialisation du df) 
    df_result à utiliser pour le layout des boutons et des stats"""
    joueurs=shared_data['donnees-ligue']
    data = {
    'player':joueurs}
    df_result = pd.DataFrame(data)
    variables=['ajout-point','retrait-point','score']
    for i in variables:
       df_result[i]=0
    print(f"voici les data apres application de get_exhibition{df_result}")
    return df_result


# Useful for layout
@callback(
    Output('buttons-container-ligue-freesolo', 'children'),Output('stat-container-ligue-freesolo', 'children'),
    [
    # State({'type': 'output_table_team', 'index': dash.dependencies.ALL}, 'data'),
    Input('shared-data-store-ligue-freesolo', 'data')]  #,# Dropdown to choose the annotation system
)
def update_display(shared_data):
    """ Retourne le layout des boutons"""
    # Recreate the DataFrame from the stored data
    # Call the display_annot_buttons function with the current DataFrame and annotation system
    # print('on est a update_buttons_display')
    print(f"shared data for display button and stat: {shared_data}")
    df=get_nom_exhibition_freesolo(shared_data)
    donnees_button=display_buttons(df)
    donnees_stat=display_stat_by_id(df,'output_table_team_render-ligue-freesolo')
    return donnees_button,donnees_stat


# Callback to handle play/pause button and the countdown
@callback(
    [Output('interval-component_team-ligue-freesolo', 'disabled'),
     Output('play-pause-button_team-ligue-freesolo', 'children')],
    [Input('play-pause-button_team-ligue-freesolo', 'n_clicks')],
    [State('interval-component_team-ligue-freesolo', 'disabled')],
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
    Output('countdown-display_team-ligue-freesolo', 'children'), 
    Output('interval-component_team-ligue-freesolo', 'n_intervals'),

    [Input('interval-component_team-ligue-freesolo', 'n_intervals'),
     Input('play-pause-button_team-ligue-freesolo', 'n_clicks')],
    [State('interval-component_team-ligue-freesolo', 'disabled'),
     State('shared-data-store-ligue-freesolo', 'data'),
          State('countdown-display_team-ligue-freesolo','children')

   
]
)
def update_timer_team(n_intervals, play_pause_clicks, is_disabled, shared_data,temps_actuel):
    # formatge du temps actuel
    temps_actuel=0 if not temps_actuel else temps_actuel
    if temps_actuel!=0:
        temps_actuel=int(temps_actuel[:2])*60+int(temps_actuel[3:])
     # données pour update gametie et les autres stat
    ctx = dash.callback_context
    # Default values if shared_data is None
    # print([countdown_start,n_intervals])
    # if is_disabled:
    #     return dash.no_update, dash.no_update, gametable.to_dict('records')
    if not is_disabled and not str(ctx.triggered[0]['prop_id'])=='play-pause-button_team-ligue-freesolo.n_clicks' :
        temps_actuel+=1
   
    # Format the time in MM:SS format
    minutes, seconds = divmod(temps_actuel, 60)
    time = f"{minutes:02}:{seconds:02}"

    # Format the period based on discipline
    # periode = f"{current_period}MT" if discipline.split('-')[0] == 'football' else f"QT{current_period}"
    return time,n_intervals



# Callback to update each team information and update the table
@callback(
    [Output("output_table_team_render-ligue-freesolo", "data"),
    Output("output_table2_team-ligue-freesolo", "data")],
    # Output("periode-output", "children")],
    [Input({'type': 'ajout-point-button', 'index': dash.dependencies.ALL}, 'n_clicks'),
    Input({'type': 'retrait-point-button', 'index': dash.dependencies.ALL}, 'n_clicks'),
    State('output_table_team_render-ligue-freesolo', 'data'),
    State('output_table2_team-ligue-freesolo', 'data'),
    State('countdown-display_team-ligue-freesolo','children'),
    State('shared-data-store-ligue-freesolo', 'data')
    ]
)
def update_person_info_team(ajout_click,retrait_click,table_data,event_data,time,shared_data):

    
    # print(f"input update_person_info_team: {table_data}")
    df_event = pd.DataFrame(event_data,columns=['player','time','event'])
    df = pd.DataFrame(table_data) if table_data else get_nom_exhibition_freesolo(shared_data)

    # Determine which button was clicked
    ctx = dash.callback_context
    print( {trigger['prop_id'].split('.')[0]: trigger['value'] for trigger in ctx.triggered})
    if not ctx.triggered:
        print('no trigger')
        return df.to_dict('records'),df_event.to_dict('records')
    # Extract the button information in JSON format
    print(str(ctx.triggered))

    if str(ctx.triggered[0]['prop_id']) not in ['shared-data-store-ligue-freesolo.data']:
        triggered_button = ctx.triggered[0]['prop_id']
        button_info = eval(triggered_button.split('.')[0])  # Safely parse the button's JSON structure
        button_type = button_info['type']
        person_id = button_info['index']
        joueur=df.loc[person_id,'player']
        variable=button_type.split('-button')[0]

        # si un boutton est appuyé    (par defaut le xtx.triggered est long et le bouton "3pt-button" aurait été appuyé)
        if not len(ctx.triggered)>1:
            df.at[person_id,variable] += 1
            df=score_to_update_click(df,person_id,variable)
            df_event=update_dataframe_general(df_event,joueur,time,variable)
            # Return the updated messages and the updated table data
    return  df.to_dict('records'),df_event.to_dict('records')




@callback(
    Output('text-exportperf-freesolo', 'children',allow_duplicate=True),
    Input('shared-data-ligue','data'),
    Input('shared-data-store-ligue-freesolo','data'),
    Input('validate-button-exportperf-freesolo', 'n_clicks'),
    Input('output_table_team_render-ligue-freesolo', 'data'),
    Input('output_table2_team-ligue-freesolo', 'data'),
    prevent_initial_call=True
)
def export_perf(shared_data_ligue,share_data_match,n_clicks,df_stat,df_event):
    if n_clicks>=1:
        joueurs=share_data_match['donnees-ligue']
        ligue= shared_data_ligue['ligue_name']
        date=datetime.date.today().strftime('%d/%m/%Y')
        heure=datetime.datetime.now().strftime('%H:%M:%S')
        post={'discipline':share_data_match['discipline_to_choose'],'date_enregistrement':date,'heure_enregistrement':heure,'saison':shared_data_ligue['saison'],
        'statistiques':df_stat,'evenement':df_event,'joueurs':joueurs}
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