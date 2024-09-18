from dash import dcc, html
import dash_bootstrap_components as dbc




layout_parameters=html.Div([
            dbc.Nav(
            [dbc.NavLink("Mon compte", href="/parameters/account", active="exact"),
            dbc.NavLink("Deconnexion", href="/deconnextion", active="exact")
            ],
            vertical="md",
            pills=True
        )
            # html.Button('Mon compte', id='submit-val', n_clicks=0),
            # html.Button('Deconnexion', id='decconect_button', n_clicks=0),
            # html.Div(id='container-button-basic',
            #         children='Enter a value and press submit')
        ])