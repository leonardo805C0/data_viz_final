# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 12:01:00 2023

@author: leona
"""
#start the visualizations
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash import callback


dash.register_page(__name__, path="/map", name = "city of London map")

df = pd.read_csv("C:/Users/leona/LUISS/data_visualization/final_dataset.csv", header = 0)

df.drop_duplicates(inplace = True)

df.drop(["Outcome code", "Person ID", "Location type", "Crime context", "Persistent ID", "Crime ID", "Location subtype", "Crime location (NA)"], axis = 1, inplace = True)

df['Outcome date'] = pd.to_datetime(df['Outcome date'], format='%Y-%m')


df['Crime month'] = pd.to_datetime(df['Crime month'], format='%Y-%m')

df = df.drop(df[df['Latitude'] >= 51.55].index)

# define the app layout
layout = html.Div([
    html.H1("map of city of london", style={'textAlign': 'center', 'fontSize': 30, "color":"white"}),
    html.Div([
        dbc.Row([
            html.H3("The interactive density map-box displays crime density using a color gradient, allowing for filtering by year or crime category to track changes in the distribution of different types of crimes over time. This tool helps identify areas of high and low crime density, and enables deeper exploration of crime patterns and trends through interactive filtering.",
                    style={'textAlign': 'justified', 'fontSize': 20, "color":"white"})
            ])
        ]),
    html.Br(),
    html.Div([
        dbc.Row([
            dbc.Col(dcc.Dropdown(
                id='crime-dropdown1',
                options=[{'label': 'All crimes', 'value': 'all'}] + [{'label': crime, 'value': crime} for crime in df['Crime category'].unique()],
                value='all',
                clearable=False
            ), width=6),

            dbc.Col(dcc.Dropdown(
                id='year-dropdown1',
                options=[{'label': 'All years', 'value': 'all'}] + [{'label': year, 'value': year} for year in df['Crime month'].dt.year.unique()],
                value='all',
                clearable=False
            ), width=6)
        ]),
        
        dcc.Graph(id="crime-map-plot"
                    ),
        ]),
    html.Div(
                dcc.Link("Return to main page", href="/", className="btn btn-outline-light mx-2 my-1", style={"borderColor": "white"}, ),
                style={"float": "right"}  # add this style to move the link to the right
            ),
    html.Br()
])

@callback(
    Output('crime-map-plot', 'figure'),
    Input('year-dropdown1', 'value'),
    Input('crime-dropdown1', 'value'))


def update_map(year, crime):
    # Filter the data based on the selected year and crime type
    if year == 'all' and crime == 'all':
        filtered_df = df
    elif year == 'all':
        filtered_df = df[df['Crime category'] == crime]
    elif crime == 'all':
        filtered_df = df[df['Crime month'].dt.year == int(year)]
    else:
        filtered_df = df[(df['Crime month'].dt.year == int(year)) & (df['Crime category'] == crime)]
    
    # Group the data by latitude and longitude and count the number of crimes in each neighborhood
    crime_counts = filtered_df.groupby(['Latitude', 'Longitude'])['Outcome category'].count().reset_index()

    # Create the heatmap
    fig = px.density_mapbox(
        crime_counts, 
        lat='Latitude', 
        lon='Longitude', 
        z='Outcome category', 
        radius=10,
        center=dict(lat=51.516, lon=-0.092), 
        zoom=11, 
        mapbox_style='carto-positron',
        opacity=0.7,
        hover_data={'Latitude': False, 'Longitude': False, 'Outcome category': True},
        labels={'Outcome category': 'Number of Crimes'}
        )

    # Set the plot title and axis labels based on the selected filters
    if year == 'all' and crime == 'all':
        fig.update_layout(title='Number of crimes in London', mapbox={'style': 'carto-positron'}, plot_bgcolor = "#282B30", paper_bgcolor = "#282B30", font_color="white")
    elif year == 'all':
        fig.update_layout(title=f'Number of {crime} crimes across all years', mapbox={'style': 'carto-positron'}, plot_bgcolor = "#282B30", paper_bgcolor = "#282B30", font_color="white")
    elif crime == 'all':
        fig.update_layout(title=f'Number of crimes in London in {year}', mapbox={'style': 'carto-positron'}, plot_bgcolor = "#282B30", paper_bgcolor = "#282B30", font_color="white")
    else:
        fig.update_layout(title=f'Number of {crime} crimes in London in {year}', mapbox={'style': 'carto-positron'}, plot_bgcolor = "#282B30", paper_bgcolor = "#282B30", font_color="white")
    
    return fig