# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 17:47:22 2023

@author: leona
"""

import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import seaborn as sns
from dash import callback
import plotly.tools as tls
import seaborn as sns
import datetime
from PIL import Image



dash.register_page(__name__, path="/", name = "Home page")

df = pd.read_csv("final_dataset.csv", header = 0)

df.drop_duplicates(inplace = True)

df.drop(["Outcome code", "Person ID", "Location type", "Crime context", "Persistent ID", "Crime ID", "Location subtype", "Crime location (NA)"], axis = 1, inplace = True)

df['Outcome date'] = pd.to_datetime(df['Outcome date'], format='%Y-%m')


df['Crime month'] = pd.to_datetime(df['Crime month'], format='%Y-%m')



grouped_df = df.groupby([df["Crime month"].dt.year, 'Crime category']).size().reset_index(name='counts')

grouped_df['Crime year'] = grouped_df['Crime month'].astype(str)


df2 = df.copy()

df2['difference'] = df.apply(lambda row: (row['Outcome date'].year - row['Crime month'].year) * 12 + (row['Outcome date'].month - row['Crime month'].month), axis=1)

total_crimes = df2['Crime category'].count()
df_bubble = df2.groupby('Crime category').agg(
    num_crimes=('Crime month', 'count'),
    avg_duration=('difference', 'mean')
).reset_index()
df_bubble['crime_percentage'] = df_bubble['num_crimes'] / total_crimes * 100
df_bubble = df_bubble.sort_values(by='avg_duration')

image_path = Image.open("dataframe.png")

def bar_plot():
    fig = px.bar(grouped_df, x="Crime category", y="counts", 
                 color="Crime year", barmode="group", color_discrete_sequence=["yellow", "purple", "blue"])
    fig.update_layout(title= "Total number of crime per year and category", yaxis_title='Number of crimes', paper_bgcolor = "#282B30", font_color="white")
    fig.update_traces(marker_line_width=1, 
                  marker_line_color='black',
                  selector=dict(type='bar'))
    return fig

def bubble_plot():
    fig = px.scatter(
        data_frame=df_bubble,
        x='Crime category',
        y='avg_duration',
        size='crime_percentage',
        size_max=30,
        opacity=0.8,
        color_discrete_sequence=['purple'],
    )

    fig.update_traces(marker=dict(line=dict(width=0.5, color='white')))  
    fig.update_xaxes(title='Type of crime committed', tickangle=30, tickfont=dict(color='white'))
    fig.update_yaxes(title='Average investigation duration (in months)', tickfont=dict(color='white'))

    # Rimuovo la legenda originale
    fig.update_layout(showlegend=False)

    # Creo una legenda personalizzata per il crime_percentage
    size_legend = dict(title='Crime Percentage', yanchor='top', xanchor='right', x=1.2, y=0.5)
    fig.update_layout(legend=size_legend)

    # Set legend text color to white
    fig.update_layout(legend_font=dict(color='white'))

    # Set axis label colors to white
    fig.update_layout(xaxis_title_font_color='white', yaxis_title_font_color='white', paper_bgcolor = "#282B30")

    return fig
    


layout = html.Div([
    html.H1("Introduction", style={'textAlign': 'center', 'fontSize': 25, "color":"white"}),
    dbc.Row([
        html.H3("The aim of our study is to conduct an analysis of the dataset pertaining to crimes committed in London city recorded by the London Police from March 2020 to December 2022 (March 2020 being the earliest available data), with a focus on examining the temporal trends and patterns of crime types, their frequency and the associated case resolution times. This study is motivated by the need to gain a better understanding of the nature and evolution of criminal activity in London",
                style={'textAlign': 'justified', 'fontSize': 15, "color":"white"})
        ]),
    html.Br(),
    dbc.Row([
        dbc.Col([
            html.P("Among the variables present in our dataset, we choose to go into detail on:",
                    style={'textAlign': 'justified', 'fontSize': 15, "color":"white"}),

            html.H3("• Latitude and longitude to extrapolate the location of the crime",
                    style={'textAlign': 'justified', 'fontSize': 15, "color":"white"}),

            html.H3("• The crime categories: bicycle-theft, burglary, criminal-damage-arson, drugs, other-theft, possession-of-weapons, public-order, robbery, shoplifting, theft-from-the-person, vehicle crime, violent-crime, other-crime.",
                    style={'textAlign': 'justified', 'fontSize': 15, "color":"white"}),

            html.H3("• The output status of the investigation and its end date or update",
                    style={'textAlign': 'justified', 'fontSize': 15, "color":"white"})
            ], width = 5),
        dbc.Col([
            html.Img(src=image_path, style={'height': '70%', 'width': '100%'})
            ], width = 7)
        ]),
    html.Br(),
    html.Div([
        dbc.Row([
            html.H3("Grouped bar plot",
                    style={'textAlign': 'center', 'fontSize': 20, "color":"white"})
            ]),
        dbc.Row([
            html.H3("Compare the temporal patterns of multiple crime categories efficiently with a grouped bar plot. Each of the three bars corresponds to a year and displays the total number of crimes for a specific category. By grouping the bars by category, this visualization provides an informative way to see the evolution of multiple categories over time.", 
                    style={'textAlign': 'justified', 'fontSize': 15, "color":"white"})
            ]),
        dbc.Row([
            dcc.Graph(figure = bar_plot())
            ]),
        html.Br(),
        html.Hr(),
        html.Br(),
        dbc.Row([
            html.H3("Bubble Plot",
                    style={'textAlign': 'center', 'fontSize': 20, "color":"white"})
            ]),
        dbc.Row([
            html.H3("The bubble chart displays the relationship between crime categories, investigation duration, and occurrence percentages. Each bubble represents a specific crime category, with bubble size indicating the category's occurrence percentage, and the y-axis displaying the average investigation duration.",
                    style={'textAlign': 'justified', 'fontSize': 15, "color":"white"})
            ]),
        dbc.Row([
            dcc.Graph(figure = bubble_plot())
            ])
    ]),
    html.Div([
        dcc.Link("Next page", href="/line_plot", className="btn btn-outline-light mx-2 my-1", style={"float": "right", "borderColor": "white"}),
    ]),
    html.Br()
])
