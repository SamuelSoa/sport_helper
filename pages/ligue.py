import dash
from dash import dcc, html, Input, Output,dash_table
import dash_bootstrap_components as dbc
from function_for_app import plot_team_basket
import pandas as pd







# @app.callback(
#     Output('url', 'pathname'),
#     Input('validate_creation_ligue', 'n_clicks'),
#     State('shared-data-store2', 'data'),
#     prevent_initial_call=True
# )
# def navigate(n_clicks,shared_data):
#     # premier click va permettre d'avoir la valeur de shared_data, deuxième permet d'obtenir discipline
#     sys_ligue=shared_data['sys_ligue']
#     if n_clicks ==1:
#         if sys_ligue=='variable-teams':
        
#         elif sys_ligue=='fixed-teams':
#             return '/exhibition/party_basket'  # Navigate to the desired page
#     elif n_clicks >=2 and discipline =='tennis':
#         return '/exhibition/party_tennis'  # Navigate to the desired page
#     elif n_clicks >=2 and discipline =='volley':
#         return '/exhibition/party_volley'  # Navigate to the desired page
#     elif n_clicks >=2 and discipline =='football':
#         return '/exhibition/party_foot'  # Navigate to the desired page
#     return dash.no_update
