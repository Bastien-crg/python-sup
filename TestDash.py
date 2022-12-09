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
    
    print("AFFICHAGE")
    df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
    })

    fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
    
    app = dash.Dash(__name__) # (3)
    disableInter = False
    c = pd.read_csv("fr-esr-parcoursup.csv", sep = ";")
    coordTemp = c["Coordonnées GPS de la formation"]
    for i in range(len(coordTemp)):
        if(type(coordTemp[i]) != str):
            c = c.drop(labels=i,axis=0)
    DebutCarte.createAllMap(c)

    app.layout = html.Div(children=[

                            html.H1(children=f'Titre de la page',
                                        style={'textAlign': 'center', 'color': '#7FDBFF'}),
                            
                            html.Div(
                                id = "Map_Par_Formation",
                                hidden = False,
                                
                                children = [
                                
                                dcc.Dropdown(
                                    id = "Change",
                                    options = [
                                        {'label' : 'All','value':'All'},
                                        {'label' : 'BTS','value':'BTS'},
                                        {'label' : "Ecole d'Ingénieur",'value':"Ecole d'Ingénieur"},
                                        {'label' : 'Licence','value':'Licence'},
                                        {'label' : "Ecole de Commerce",'value':"Ecole de Commerce"},
                                        {'label' : 'CPGE','value':'CPGE'},
                                        {'label' : 'IFSI','value':'IFSI'},
                                        {'label' : 'EFTS','value':'EFTS'},
                                        {'label' : 'PASS','value':'PASS'},
                                        {'label' : 'Autre formation','value':'Autre formation'},
                                        {'label' : "License_Las",'value':"License_Las"}
                                    ],
                                    value='All'
                                ), 
                            
                                html.Iframe(
                                    id = 'mapParFormation',
                                    srcDoc = open("src\Carte_toute_formation.html",'r').read(),
                                    width = '60%',
                                    height = '600',
                                    margin = {
                                        'l': 90, 'b': 20, 't': 0, 'r': 0
                                    }
                                ),
                                
                            ]), 
                            
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
                            
                            
                            
                            html.Span(id="ChangeClick",style={"verticalAlign" : "middle"}),
    ]
    )

    # # Permet de changer la date; possible de faire la meme mais pour les cartes avec les départements
    # @app.callback(
    #     Output(component_id='graph1', component_property='figure'), # (1)
    #     [Input(component_id='year-slider', component_property='value')] # (2)
    # )
    # def update_figure(input_value): # (3)
    #     return px.scatter(data[input_value], x="gdpPercap", y="lifeExp",
    #                     color="continent",
    #                     size="pop",
    #                     hover_name="country") # (4)
    
#     @app.callback(
#     Output("interval", "disabled"), [Input("Play", "n_clicks")], State("interval","disabled"),
# )
#     def toogle(n,playing):
#         if n:
#             return not playing
#         else:
#             return playing
    
    
    # @app.callback(
    # Output("ChangeClick", "children"), [Input("Change", "n_clicks")]
    # )
    # def on_button_click(n):
    #     if n is None:
    #         return "Not clicked."
    #     else:
    #         return f"Clicked {n} times."
    
    @app.callback(
    Output("mapParFormation", "srcDoc"), [Input("Change", "value")],
)
    def chooseFormation(name):
        if name == "All":
            return open("src\Carte_toute_formation.html",'r').read()
        return open("src\Carte_par_formation_{}.html".format(name),'r').read()
    
    
    
    
    
    #
    # RUN APP
    #

    app.run_server(debug=True) # (8)
    
