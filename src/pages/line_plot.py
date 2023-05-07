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


dash.register_page(__name__, path="/line_plot", name = "Discover city of London crimes")

df = pd.read_csv("final_dataset.csv", header = 0)

df.drop_duplicates(inplace = True)

df.drop(["Outcome code", "Person ID", "Location type", "Crime context", "Persistent ID", "Crime ID", "Location subtype", "Crime location (NA)"], axis = 1, inplace = True)

df['Outcome date'] = pd.to_datetime(df['Outcome date'], format='%Y-%m')


df['Crime month'] = pd.to_datetime(df['Crime month'], format='%Y-%m')

layout = html.Div([
    html.H1("Line plot for the number of crimes", style={'textAlign': 'center', 'fontSize': 30, "color":"white"}),
    html.Div([
        dbc.Row([
            html.H3("Line plots show the temporal trend of crimes committed over time, divided by category. Through these plots, it is possible to identify trends or seasonal patterns in the commission of individual categories of crimes, in order to identify in which months more crimes are committed or which type of crime increases or decreases in a certain period of the year. Due to their interactive nature, it is possible to select the crime category to display or the specific year.",
                    style={'textAlign': 'justified', 'fontSize': 20, "color":"white"})
            ])
        ]),
    html.Br(),
    html.Div([
        dbc.Row([
            dbc.Col(dcc.Dropdown(
                id='crime-dropdown',
                options=[{'label': 'All crimes', 'value': 'all'}] + [{'label': crime, 'value': crime} for crime in df['Crime category'].unique()],
                value='all',
                clearable=False
            ), width=6),

            dbc.Col(dcc.Dropdown(
                id='year-dropdown',
                options=[{'label': 'All years', 'value': 'all'}] + [{'label': year, 'value': year} for year in df['Crime month'].dt.year.unique()],
                value='all',
                clearable=False
            ), width=6)
        ]),
        
        dcc.Graph(id="crime-line-plot")
    ]),
    html.Div(
                dcc.Link("Next page", href="/map", className="btn btn-outline-light mx-2 my-1", style={"borderColor": "white"}, ),
                style={"float": "right"}  # add this style to move the link to the right
            ),
html.Br()
])

@callback(
    Output('crime-line-plot', 'figure'),
    Input('year-dropdown', 'value'),
    Input('crime-dropdown', 'value'))


def update_line_plot(year, crime):
    # Filter the data based on the selected year and crime type
    if year == 'all' and crime == 'all':
        filtered_df = df
    elif year == 'all':
        filtered_df = df[df['Crime category'] == crime]
    elif crime == 'all':
        filtered_df = df[df['Crime month'].dt.year == int(year)]
    else:
        filtered_df = df[(df['Crime month'].dt.year == int(year)) & (df['Crime category'] == crime)]
    
    # Group the data by month and count the number of crimes
    crime_counts = filtered_df.groupby(filtered_df['Crime month'])['Crime month'].count()
    # Create the line plot
    fig = px.line(crime_counts, x=crime_counts.index, y=crime_counts.values)
    fig.update_traces(line_color='purple', line_width=3)
    plt.xticks(crime_counts.index)
    
    # Set the plot title and axis labels based on the selected filters
    if year == 'all' and crime == 'all':
        fig.update_layout(title='Number of crimes', xaxis_title='Month', yaxis_title='Number of crimes', paper_bgcolor = "#282B30", font_color="white")
    elif year == 'all':
        fig.update_layout(title=f'Number of {crime} crimes across all years', xaxis_title='Month', yaxis_title='Number of crimes', paper_bgcolor = "#282B30", font_color="white")
    elif crime == 'all':
        fig.update_layout(title=f'Number of crimes in {year}', xaxis_title='Month', yaxis_title='Number of crimes', paper_bgcolor = "#282B30", font_color="white")
    else:
        fig.update_layout(title=f'Number of {crime} crimes in {year}', xaxis_title='Month', yaxis_title='Number of crimes', paper_bgcolor = "#282B30", font_color="white")
    
    return fig




