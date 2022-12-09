# filename = 'dash-01.py'

#
# Imports
#
import dis
from faulthandler import disable
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output,Input,State

import csv
from matplotlib.widgets import Slider
import plotly.express as px
import pandas as pd
from sqlalchemy import false

from file_manager import FileManager
from chart.histogram import Histogram
from chart.bar_chart import BarChart
from chart.pie_chart import PieChart

import DebutCarte 

def read_file(filename):
    l = []
    with open(filename, newline='', encoding="UTF-8") as file:
        reader = csv.DictReader(file, delimiter=";")
        for row in reader:
            l.append(row)
    return l


def test():
    l = pd.read_csv("fr-esr-parcoursup.csv", sep=";")

    fig = px.histogram(data_frame=l, x="Capacité de l’établissement par formation")
    # fig = px.histogram(data_frame=sorted(l, key=lambda d: int(d['Capacité de l’établissement par formation'])), x="Capacité de l’établissement par formation", nbins=10)
    fig.show()

#
# Data
#

year = 2007

gapminder = px.data.gapminder() # (1)
years = gapminder["year"].unique()
data = { year:gapminder.query("year == @year") for year in years} # (2)

#
# Main
#

if __name__ == '__main__':
    
    df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
    })

    fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
    
    print(type(fig))
    
    file_manager = FileManager("fr-esr-parcoursup.csv")
    file_list = file_manager.open_file()

    data = file_list[0]
    pie_chart = PieChart(data, values="Effectif total des candidats en phase principale",
                         names='Filière de formation très agrégée')
    
    fig2 = pie_chart.returnPx()
    
    print(type(pie_chart))
    print(type(fig2))
    
    app = dash.Dash(__name__) # (3)

    app.layout = html.Div(children=[

                            html.H1(children=f'Titre de la page',
                                        style={'textAlign': 'center', 'color': '#7FDBFF'}),
                            html.Div(children='''
                                Dash: A web application framework for your data.
                            '''),
                            dcc.Graph(
                                id='example-graph',
                                figure=fig2
                            )
    ]
    )
    
    
    
    
    
    #
    # RUN APP
    #

    app.run_server(debug=True) # (8)
    
