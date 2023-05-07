# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 17:24:35 2023

@author: leona
"""

import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# For this dash we start creating the app. It is useful to remark
# that the disposition of the folders is important to get the right 
# result on the dash

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.SLATE])
server = app.server

app.layout = html.Div(
    [
         html.H1("London Crimes Analysis", style={'textAlign': 'center', 'fontSize': 40, "color":"white"}),
         html.Div([
             dcc.Link(page["name"], href = page["path"], className="btn btn-outline-light mx-2 my-1", style={"borderColor": "white"}, )
             for page in dash.page_registry.values()
             ],
             className="text-center"),
         html.Hr(),
         
         dbc.Container(dash.page_container, fluid=True),
        
     ],
    )

if __name__ == "__main__":
    app.run(debug=False, port = "8080")