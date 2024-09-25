
import pandas as pd
import dash
import dash_bootstrap_components as dbc
import numpy as np
from dash import dcc, html, Input, Output,dash_table,State, callback

dash.register_page(__name__, path="/parameters/about",name='A propos')




layout=  html.Div([html.P("Cette application a été concue par Samuel Ondo"),   
        html.Br(),
        html.P([
            'Contact:',
            html.Br(),
            html.Div([html.A('Linkedin', href='https://www.linkedin.com/in/samuel-ondo-0b7559177/', target="_blank")]),
                        html.Br(),
 html.P('Mail:ondosamuel10@gmail.com')])])
                
