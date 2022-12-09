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

import DebutCarte

from file_manager import FileManager

def read_file(filename):
    l = []
    with open(filename, newline='', encoding="UTF-8") as file:
        reader = csv.DictReader(file, delimiter=";")
        for row in reader:
            l.append(row)
    return l


def test():
    l = pd.read_csv("../data/fr-esr-parcoursup.csv", sep=";")

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
    c = pd.read_csv("../data/fr-esr-parcoursup.csv", sep = ";")
    coordTemp = c["Coordonnées GPS de la formation"]
    for i in range(len(coordTemp)):
        if(type(coordTemp[i]) != str):
            c = c.drop(labels=i,axis=0)
    DebutCarte.createAllMap(c)

    app.layout = html.Div(children=[

                            html.H1(children=f'Titre de la page',
                                    style={'Position' : 'relative','width' : '100%', 'textAlign': 'center', 'color': '#7FDBFF'}),
                            
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
                                    #style = { 'position' : 'relative','width' : '78%','padding' : 10 , 'float':'right'}
                                ), 
                            
                                html.Iframe(
                                    id = 'mapParFormation',
                                    srcDoc = open("../templates/Carte_toute_formation.html",'r').read(),
                                    height = '550',
                                    width = '60%'
                                    #style = { 'position' : 'relative','width' : '60%','padding' : 10 , 'float':'right'}
                                ),
                                
                            ]), 
                            
                            html.Button('hideTest', id='hideTest', n_clicks=0),
                            
                            html.Div(
                                id = 'Div_test',
                                hidden = False,
                                
                                children=f'''
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
    
    @app.callback(
    Output("mapParFormation", "srcDoc"), [Input("Change", "value")],
)
    def chooseFormation(name):
        if name == "All":
            return open("../templates/Carte_toute_formation.html",'r').read()
        return open("../templates/Carte_par_formation_{}.html".format(name),'r').read()
    
    
    @app.callback(
    Output("Div_test", "hidden"), [Input("hideTest", "n_clicks")],
)
    def chooseFormation(n_clicks):
        if n_clicks%2 == 0:
            return True
        return False
    
    
    #
    # RUN APP
    #

    app.run_server(debug=True) # (8)
    
