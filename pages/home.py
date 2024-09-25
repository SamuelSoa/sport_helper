
import pandas as pd
import dash
import dash_bootstrap_components as dbc
import numpy as np
from dash import dcc, html, Input, Output,dash_table,State, callback

dash.register_page(__name__, path="/",name='Home')



layout=  html.Div([html.P("Bienvenue sur l'application SportHelper!"),
                    html.P("Deux moyens d'enregistrer vos performances:"),
                    html.P("- Avec le mode exhibition, vous pourrez enregistrer les moments forts et obtenir les statistiques d'une partie donnée en live. Leur telechargement est possible "),
                    html.P("- Les ligues permettent de créer un championnat et de garder une trace des compétitions avec vos partenaires"),
                    html.P("Les perspectives sont enormes: "),
                    html.P(["- Création d'un championnat de foot se déroulant dans un stade municipal, un city, un five, etc...",
                     html.Br(),
                      "- Archivage des matchs de votre playground de basket",
                    html.Br(),
                    "- Sauvegarde de vos parties périodiques de Beach volley lors des vacances d'été",
                    html.Br(),
                   "- Organisation de tournois ponctuels"]),
                    html.Br(),
                    html.P("Profitez de cette application! Sportivement votre")
                    ])
