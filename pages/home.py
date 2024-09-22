
import pandas as pd
import dash
import dash_bootstrap_components as dbc
import numpy as np
from dash import dcc, html, Input, Output,dash_table,State, callback

dash.register_page(__name__, path="/",name='Home')



layout=  html.Div([html.P("Bienvenue sur l'application SportHelper!"),
                    html.Br(),
                    html.P("Avec le mode exhibition, vous pourrez enregistrer les moments forts et obtenir les statistiques d'une partie donnée en live. Leur telechargement est possible "),
                    
                    html.Br(),
                    html.P("Les ligues permettent de créer un championnat et garder une trace des compétitions avec vos partenaires"),
                    html.Br(),
                    html.P("Les perspectives sont enormes: "),
                    html.Br(),
                    html.P("- Création d'un championnat de foot se déroulant dans vos stades municipaux, les city, les five, etc..."),
                    html.Br(),
                    html.P("- Archivage des matchs de votre playground de basket"),
                    html.Br(),
                    html.P("- Sauvegarde de vos parties périodiques de Beach volley lors des vacances d'été"),
                    html.Br(),
                    html.P("- Organisation de tounois ponctuels"),
                    html.Br(),
                    html.P("Pofitez de cette application! Sportivement votre")
                    ])
