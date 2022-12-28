# filename = 'dash-01.py'

#
# Imports
#
import dash
from dash import dcc
from dash import html
from dash.dependencies import Output, Input
import plotly.express as px
import pandas as pd

import DebutCarte

from file_manager import FileManager
from chart import RankChart
from chart import BarChart
from chart import PieChart
from chart import Histogram

#
# Data
#

year = 2007

gapminder = px.data.gapminder()  # (1)
years = gapminder["year"].unique()
data = {year: gapminder.query("year == @year") for year in years}  # (2)


def create_Bar_chart(data, column_Name):
    bar_chart = BarChart(data, column=column_Name)
    fig = bar_chart.render_chart()
    return fig


def create_Basic_chart(data):
    return


def create_Histogram(data, x_name, nbins=20, max_value=199):
    histo = Histogram(data, x=x_name, nbins=nbins, max_value=max_value)
    fig = histo.render_chart()
    return fig


def create_Pie_chart(data, values_name, names):
    pie_chart = PieChart(data, values=values_name,
                         names=names)
    fig = pie_chart.render_chart()
    return fig


def create_Rank_chart(data):
    rank_chart = RankChart(data)
    fig = rank_chart.render_chart()
    return fig


#
# Main
#

if __name__ == '__main__':

    file_manager = FileManager("../data/fr-esr-parcoursup-2021.csv")
    file_list = file_manager.open_file()

    data = file_list[0]

    bar_chart = BarChart(data, column="Filière de formation très agrégée")
    fig = bar_chart.render_chart()
    print("AFFICHAGE")

    app = dash.Dash(__name__)  # (3)
    disableInter = False
    c = pd.read_csv("../data/fr-esr-parcoursup-2021.csv", sep=";")
    coordTemp = c["Coordonnées GPS de la formation"]
    for i in range(len(coordTemp)):
        if type(coordTemp[i]) != str:
            c = c.drop(labels=i, axis=0)
    DebutCarte.createAllMap(c)

    app.layout = html.Div(children=[

        html.H1(children='Titre de la page',
                style={'Position': 'relative', 'width': '100%', 'textAlign': 'center', 'color': '#7FDBFF'}),

        html.Div(
            id="Map_Par_Formation",
            hidden=False,
            style={'position': 'relative', 'width': '50%', 'padding': 10, 'float': 'right'},
            children=[

                dcc.Dropdown(
                    id="Change",
                    options=[
                        {'label': 'All', 'value': 'All'},
                        {'label': 'BTS', 'value': 'BTS'},
                        {'label': "Ecole d'Ingénieur", 'value': "Ecole d'Ingénieur"},
                        {'label': 'Licence', 'value': 'Licence'},
                        {'label': "Ecole de Commerce", 'value': "Ecole de Commerce"},
                        {'label': 'CPGE', 'value': 'CPGE'},
                        {'label': 'IFSI', 'value': 'IFSI'},
                        {'label': 'EFTS', 'value': 'EFTS'},
                        {'label': 'PASS', 'value': 'PASS'},
                        {'label': 'Autre formation', 'value': 'Autre formation'},
                        {'label': "License_Las", 'value': "License_Las"}
                    ],
                    value='All'
                ),

                html.Iframe(
                    id='mapParFormation',
                    srcDoc=open("../templates/Carte_toute_formation.html", 'r').read(),
                    width='100%',
                    height='650',
                ),

            ]),

        html.Div(
            id='Div_test',
            hidden=False,
            style={'position': 'relative', 'width': '100%', 'padding': 10, 'float': 'left'},
            children=[
                html.Button('hideTest', id='hideTest', n_clicks=0),
                html.Button('showFig', id='showFig', n_clicks=0),
                html.Span(id="PlayFig", hidden=True),
                dcc.Slider(
                    id="graph-slider",
                    min=1,
                    max=4,
                    step=1,
                    marks={
                        1: 'bar_chart',
                        2: 'rank_chart',
                        3: 'histogram',
                        4: 'pie_chart',
                    },
                    value=1,
                ),
                dcc.Graph(
                    id="graph",
                    figure=fig
                ),
            ]
        ),  # (7)

        html.Span(id="ChangeClick", style={"verticalAlign": "middle"}),
    ]
    )


    @app.callback(
        Output("mapParFormation", "srcDoc"), [Input("Change", "value")],
    )
    def chooseFormation(name):
        if name == "All":
            return open("../templates/Carte_toute_formation.html", 'r').read()
        return open("../templates/Carte_par_formation_{}.html".format(name), 'r').read()


    @app.callback(
        Output("Div_test", "hidden"), [Input("hideTest", "n_clicks")],
    )
    def chooseFormation(n_clicks):
        if n_clicks % 2 == 0:
            return False
        return True


    @app.callback(
        Output("PlayFig", "hidden"), [Input("showFig", "n_clicks")]
    )
    def chooseFormation(n_clicks):
        if n_clicks:
            print(n_clicks)
            fig.show()
        n_clicks = 0
        return True


    @app.callback(
        Output(component_id='graph', component_property='figure'),  # (1)
        [Input(component_id='graph-slider', component_property='value')]  # (2)
    )
    def update_figure(input_value):
        global fig
        match input_value:
            case 1:
                fig = create_Bar_chart(data, "Filière de formation très agrégée")
                return fig
            case 2:
                fig = create_Rank_chart(data)
                return fig
            case 3:
                fig = create_Histogram(data, "Capacité de l’établissement par formation")
                return fig
            case 4:
                fig = create_Pie_chart(data, "Effectif total des candidats en phase principale",
                                       'Filière de formation très agrégée')
                return fig


    #
    # RUN APP
    #

    app.run_server(debug=True)  # (8)
