# filename = 'dash-01.py'

#
# Imports
#
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output,Input

import csv
import plotly.express as px
import pandas as pd


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
    app = dash.Dash(__name__) # (3)

    fig = px.scatter(data[year], x="gdpPercap", y="lifeExp",
                        color="continent",
                        size="pop",
                        hover_name="country") # (4)

    # l = pd.read_csv("fr-esr-parcoursup.csv", sep=";")

    # fig = px.histogram(data_frame=l, x="Capacité de l’établissement par formation")

    app.layout = html.Div(children=[

                            html.H1(children=f'Capacité de l’établissement par formation ({year})',
                                        style={'textAlign': 'center', 'color': '#7FDBFF'}), # (5)
                            html.Label('Year'),
                            dcc.Slider(
                                id="year-slider",
                                min = 1952,
                                max = 2007,
                                step = 5,
                                marks={
                                    1952 :'1952',
                                    1957 :'1957',
                                    1962 :'1962',
                                    1967 :'1967',
                                    1972 :'1972',
                                    1977 :'1977',
                                    1982 :'1982',
                                    1987 :'1987',
                                    1992 :'1992',
                                    1997 :'1997',
                                    2002 :'2002',
                                    2007 :'2007',
                                },
                                value=2007,
                            ),
                            dcc.Graph(
                                id='graph1',
                                figure=fig
                            ), # (6)

                            html.Div(children=f'''
                                자유로운 기분, I like that
                                고민 따윈 already done, done (done, done)
                                색안경 끼고 보는 게 죄지
                                That's not my fault, woah
                                Told ya I don't care at all
                                내 멋대로 갈 거야 (oh-oh)
                                필요 없어 order
                                Don't need no guidance, I'm makin' my way
                            '''), # (7)
                            
                            dcc.Interval(   id='interval',
                                interval=1*1000, # in milliseconds
                                n_intervals=0),
                            
                            html.Button(
                                id = "Play"
                            ),

    ]
    )

    # Permet de changer la date; possible de faire la meme mais pour les cartes avec les départements
    @app.callback(
        Output(component_id='graph1', component_property='figure'), # (1)
        [Input(component_id='year-slider', component_property='value')] # (2)
    )
    def update_figure(input_value): # (3)
        return px.scatter(data[input_value], x="gdpPercap", y="lifeExp",
                        color="continent",
                        size="pop",
                        hover_name="country") # (4)

    @app.callback(  Output('year-slider', 'value'),
                [Input('interval', 'n_intervals')])
    def on_tick(n_intervals):
        if n_intervals is None: return 0
        return years[(n_intervals+1)%len(years)]
    
    
    
    
    #
    # RUN APP
    #

    app.run_server(debug=True) # (8)
    
