import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
from dash import dcc, html, Input, Output,dash_table,State, callback
from dao.ligue_dao import get_data_by_filter
from pages.ligue.annotator_ligue.basket_ligue import get_nom_exhibition_ligue
from pages.ligue.annotator_ligue.foot_ligue import get_nom_exhibition_foot_ligue
from pages.ligue.annotator_ligue.tennis_ligue import get_nom_exhibition_tennis_ligue
from pages.ligue.annotator_ligue.volley_ligue import get_nom_exhibition_volley_individuel_ligue
from pages.ligue.annotator_ligue.libre_collectif_ligue import get_nom_exhibition_freemulti
from datetime import date
import io
from dao.ligue_dao import cluster
import base64
dash.register_page(__name__, path="/ligues/vos_ligues/ajouter_rencontre/annotation_posteriori",name='Paramètrage de la rencontre')
layout = html.Div(
    children=[
         html.Div(children="Quel action", className="menu-title"),
        dcc.Dropdown(
                    id='sys_ajout_resultat',
                    options=[{"label": x, "value": x} for x in ['Définir un match',"Ajouter le résultat d'un match"]],
                    clearable=False,
                    className="dropdown",
                    multi=False
                ),
        html.Div(id='view_choice_annotation'),
        html.Button('Cliquez 2 fois pour finir le processus', id='validate-button-posteriori', n_clicks=0)  # Use a button for validation
    ], className='wrapper'
)





# @callback(Output('view_choice_annotation','children'),
#         Input('shared-data-ligue','data'),
#         Input('sys_ajout_resultat','value')
#         )
# def upload_data(shared_data,choice,df):
#     discipline=shared_data
#     result=html.Div([
#         html.Div(children="Date du match", className="menu-title"),
#         dcc.DatePickerSingle(
#         id='my-date-picker-single',
#         display_format='D-M-Y',
#         min_date_allowed=date(2024, 1, 1),
#         max_date_allowed=date.today(),
#         initial_visible_month=date(2024, 1, 1),
#         date=date.today()
#     ),dmc.Group(id='heure_perf',
#     gap=50,
#     children=[
#         dmc.TimeInput(label="What time is it now?")]),
#         html.Div(children="Saison", className="menu-title"),
#         dcc.Input(id="saisoninput", type="number", value=4),
#         dcc.Upload(
#         id='upload-data',
#         children=html.Div([
#             'Drag and Drop or ',
#             html.A('Select Files')
#         ]),
#         style={
#             'width': '100%',
#             'height': '60px',
#             'lineHeight': '60px',
#             'borderWidth': '1px',
#             'borderStyle': 'dashed',
#             'borderRadius': '5px',
#             'textAlign': 'center',
#             'margin': '10px'
#         },
#         # Allow multiple files to be uploaded
#         multiple=True
#     )
#         ])
    











@callback(Output('view_choice_annotation','children'),
        Input('shared-data-ligue','data'),
        Input('sys_ajout_resultat','value')
        )
def get_view_choice(shared_data,choice):
    if choice=='Définir un match':
        result=html.Div([
        html.Div(children="Equipe 1", className="menu-title"),
        html.Div(id='dropdown_1_post'),
        html.P("Joueurs de l'équipe participants", className="lead"),
        html.Div(id='donnees_team1-ligue-dropdown_post'),
        html.Div(children="Joueurs de l'équipe participants", className="menu-title"),
        html.Div(id='dropdown_2_post'),
        html.Div(id='donnees_team2-ligue-dropdown_post'),
        html.Div(id='optional_view'),
        html.Button("Download CSV", id="btn_csv"),
        dcc.Download(id="download-dataframe-csv"),
        ])
    elif choice=="Ajouter le résultat d'un match":
        result=html.Div([
        html.Div(children="Date du match", className="menu-title"),
        dcc.DatePickerSingle(
        id='my-date',
        display_format='D-M-Y',
        min_date_allowed=date(2024, 1, 1),
        max_date_allowed=date.today(),
        initial_visible_month=date(2024, 1, 1),
        date=date.today()
            ),
        html.Div(children="Heure", className="menu-title"),
        dcc.Textarea(id="heure_perf",value="20:00" ), 
        html.Div(id='optional_view'),

        html.Div(children="Score de la première équipe", className="menu-title"),
        dcc.Input(id="score1_post", type="number", value=4),
        html.Div(children="Score de la deuxième équipe", className="menu-title"),
        dcc.Input(id="score2_post", type="number", value=4),
        dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=False
    ),
        html.Button('Cliquez 2 fois pour importer les données', id='validate-button-import', n_clicks=0) , # Use a button for validation
        html.Div(id='text_import')
        ])

    return result


def parse_contents(contents):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        # Assume that the user uploaded an excel file
        df = pd.read_excel(io.BytesIO(decoded),index_col=0)
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return df



@callback(
    Output('text_import', 'children'),
    Input('shared-data-ligue','data'),
    Input('validate-button-import', 'n_clicks'),
    Input('my-date','value'),
    Input('heure_perf','value'),
    Input('score1_post','value'),
    Input('score2_post','value'),
   Input('upload-data', 'contents'),
    State('optional_data', 'value'),
    State('optional_data2', 'value'),


    prevent_initial_call=True
)
def upload_in_df(shared_data,n_clicks,date,heure,score1,score2,data,opt1,opt2):
    print(date)
    print(heure)
    print(parse_contents(data))
    
    if n_clicks >=2 :
        df_stat=parse_contents(data)
        nom_equipe1=df_stat.loc[df_stat.id_team=='t1','team'].unique()[0]
        nom_equipe2=df_stat.loc[df_stat.id_team=='t2','team'].unique()[0]
        joueurs1=df_stat.loc[df_stat.id_team=='t1','player'].values.tolist()
        joueurs2=df_stat.loc[df_stat.id_team=='t2','player'].values.tolist()
        print(joueurs1)
        donnees_finale=pd.DataFrame({'equipe1':[nom_equipe1],
                                'equipe2':[nom_equipe2],
                                'score1':[score1],
                                'score2':[score2]                  })
        saison=shared_data['saison'][-1]
        ligue=shared_data['ligue_name']
        if discipline=='basket':
            post={'discipline':shared_data['discipline_ligue'],'date_enregistrement':date,'heure_enregistrement':heure,'saison':saison,'nom_equipe1':nom_equipe1,'sys_annot':opt1,'sys_match':opt2,
            'nom_equipe2':nom_equipe1,'statistiques':df_stat.to_dict('records'),'evenement':None,'stat_finale':donnees_finale.to_dict('records'),'joueurs_equipe1':joueurs1,'joueurs_equipe2':joueurs2}
        else:
            post={'discipline':shared_data['discipline_ligue'],'date_enregistrement':date,'heure_enregistrement':heure,'saison':saison,'nom_equipe1':nom_equipe1,
            'nom_equipe2':nom_equipe1,'statistiques':df_stat.to_dict('records'),'evenement':None,'stat_finale':donnees_finale.to_dict('records'),'joueurs_equipe1':joueurs1,'joueurs_equipe2':joueurs2}
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
    return dash.no_update



@callback(Output('optional_view','children',allow_duplicate=True),
        Input('shared-data-ligue','data'),prevent_initial_call=True
        )
def get_optional_view(shared_data):
    discipline=shared_data['discipline_ligue']
    if discipline=='tennis':
        return html.Div([html.P("Pour le tennis", className="lead"),
        html.Div(children="Nombre de set_gagnant", className="menu-title"),
        dcc.Input(id="optional_data", type="number", value=4),html.Div(id='optional_data2',children='0',style={"display": "none"})])
    elif discipline=='basket':
        return html.Div([html.Div(children="Type d'annotation", className="menu-title"),
        dcc.Dropdown(
            id="optional_data",
            options=[{"label": x, "value": y} for x, y in [['Simple', 'annot_simple'], ['Complet', 'annot_complet']]],
            clearable=False,
            value='annot_simple',
            className="dropdown"
        ),html.Div(children="Système de point ", className="menu-title"),
        dcc.Dropdown(
            id="optional_data2",
            options=[{"label": x, "value": y} for x, y in [['3PT=3,2PT=2', 'point_normal'], ['3PT=2,2PT=1', 'point_mini']]],
            clearable=False,
            value='point_normal',
            className="dropdown"
        ),])
    else:
        return html.Div([html.Div(id='optional_data',children='0',style={"display": "none"}),html.Div(id='optional_data2',children='0',style={"display": "none"})])


@callback(Output('dropdown_1_post','children'),
        Input('shared-data-ligue','data')
        )
def get_dropdown_equipe1(shared_data):
    all_team=[elem[0] for elem in shared_data['liste_equipe']]
    sys_ligue=shared_data['sys_ligue']
    if sys_ligue=='fix-teams':
        result_team1=dcc.Dropdown(
                    id='result_equipe1_post',
                    options=[{"label": x, "value": x} for x in all_team],
                    clearable=False,
                    className="dropdown",
                    multi=True
                )
    else:
        result_team1=dcc.Textarea(
        id='result_equipe1_post',
        value="t1" ,
        style={'width': '300px', 'height': '100px', 'resize': 'none', 'font-size': '14px'},
        )

    return result_team1


@callback(Output('dropdown_2_post','children'),
        Input('shared-data-ligue','data'),
        Input('result_equipe1_post','value')
        )
def get_dropdown_equipe2(shared_data,equipe1):
    print(f"equipe1 dropdown:{equipe1}")
    sys_ligue=shared_data['sys_ligue']
    if sys_ligue=='fix-teams':
        all_team=[elem[0] for elem in shared_data['liste_equipe']]
        team_restante=[elem for elem in all_team if elem not in equipe1]
        result_team2=dcc.Dropdown(
                    id='result_equipe2_post',
                    options=[{"label": x, "value": x} for x in team_restante],
                    clearable=False,
                    className="dropdown",
                    multi=True
                )
    else:
        result_team2=dcc.Textarea(
        id='result_equipe2_post',
        value="t2" ,
        style={'width': '300px', 'height': '100px', 'resize': 'none', 'font-size': '14px'},
        )
    return result_team2


@callback(Output('donnees_team1-ligue-dropdown_post','children'),
        Input('shared-data-ligue','data'),
        Input('result_equipe1_post','value')
        )
def get_data_equipe1(shared_data,equipe1):
    
    liste_equipe=shared_data['liste_equipe'] 
    sys_ligue=shared_data['sys_ligue']
    if sys_ligue=='fix-teams':
        liste_equipe1=[elem[1] for elem in liste_equipe if elem[0]==equipe1[0] ][0]
        div1=dcc.Dropdown(
                    id='donnees_team1-ligue_post',
                    options=[{"label": x, "value": x} for x in liste_equipe1],
                    clearable=False,
                    value=liste_equipe1,
                    className="dropdown",
                    multi=True)
        return div1
    else:
        all_team=[elem for elem in shared_data['liste_player']]
        div1=dcc.Dropdown(
                    id='donnees_team1-ligue_post',
                    options=[{"label": x, "value": x} for x in all_team],
                    clearable=False,
                    className="dropdown",
                    multi=True)
        return div1
    

@callback(Output('donnees_team2-ligue-dropdown_post','children'),
        Input('shared-data-ligue','data'),
        Input('result_equipe2_post','value'),
        Input('donnees_team1-ligue_post','value')
        )
def get_data_equipe2(shared_data,equipe2,donnees1):
    
    liste_equipe=shared_data['liste_equipe'] 
    sys_ligue=shared_data['sys_ligue']
    if sys_ligue=='fix-teams':
        liste_equipe2=[elem[1] for elem in liste_equipe if elem[0]==equipe2[0] ][0]
        
        div2=dcc.Dropdown(
                    id='donnees_team2-ligue_post',
                    options=[{"label": x, "value": x} for x in liste_equipe2],
                    clearable=False,
                    value=liste_equipe2,
                    className="dropdown",
                    multi=True)
        return div2
    else:
        all_team=[elem for elem in shared_data['liste_player']]
        joueurs_restant=[elem for elem in all_team if elem not in donnees1]
        div2=dcc.Dropdown(
                    id='donnees_team2-ligue_post',
                    options=[{"label": x, "value": x} for x in joueurs_restant],
                    clearable=False,
                    className="dropdown",
                    multi=True)
        return div2
    

@callback(
    Output("download-dataframe-csv", "data"),
    [Input('btn_csv', 'n_clicks')],
    [State('shared-data-ligue', 'data'),
    State('donnees_team1-ligue_post', 'value'),
    State('donnees_team2-ligue_post', 'value'),
    State('result_equipe1_post', 'value'),
    State('result_equipe2_post', 'value'),
    State('optional_data', 'value')
    ],
    prevent_initial_call=True,
)
def func(n_clicks,shared_data,input_value4,input_value5,input_value6,input_value7,val_optionnelle):
    discipline=shared_data['discipline_ligue']
    if n_clicks is None or n_clicks == 0:
        print("validate-button has not been clicked yet.")
        return dash.no_update
    print(f'donnees equipes:{input_value4},{input_value5}')
    dicto={'discipline_to_choose':discipline,'donnees_team1-ligue':input_value4,'donnees_team2-ligue':input_value5,
    'nomequipe1-ligue':input_value6[0] if type(input_value6)==list else input_value6,'nomequipe2-ligue':input_value7[0] if type(input_value7)==list else input_value7}
    if discipline=='foot':
        df=get_nom_exhibition_foot_ligue(dicto)
    elif discipline=='basket':
        df=get_nom_exhibition_ligue(dicto,val_optionnelle)
    elif discipline=='volley':
        df=get_nom_exhibition_volley_ligue(dicto)
    elif discipline=='tennis':
        df=get_nom_exhibition_tennis_ligue(dicto,val_optionnelle)
    elif discipline=='free-multi':
        df=get_nom_exhibition_freemulti(dicto)
    return dcc.send_data_frame(df.to_excel, "mydf.xlsx")









@callback(
    Output('url', 'pathname',allow_duplicate=True),
    Input('validate-button-posteriori', 'n_clicks'),
    prevent_initial_call=True
)
def navigate_ligue(n_clicks):
    if n_clicks >=2 :
        return '/ligues/vos_ligues'  # Navigate to the desired page
    return dash.no_update


