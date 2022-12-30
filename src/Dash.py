# filename = 'dash-01.py'

#
# Imports
#
import dash
from dash import dcc
from dash import html
from dash.dependencies import Output, Input

import GestionCarte

from file_manager import FileManager
from chart import RankChart
from chart import BarChart
from chart import PieChart
from chart import Histogram


def create_Bar_chart(data, column_Name, selected_formation=[]):
    bar_chart = BarChart(data, column=column_Name, selected_formations=selected_formation)
    fig = bar_chart.render_chart()
    return fig


def create_Basic_chart(data):
    return


def create_Histogram(data, x_name, nbins=20, max_value=199):
    histogram = Histogram(data, x=x_name, nbins=nbins, max_value=max_value)
    fig = histogram.render_chart()
    return fig


def create_Pie_chart(data, values_name, names):
    pie_chart = PieChart(data, values=values_name,
                         names=names)
    fig = pie_chart.render_chart(title="Choix des élèves")
    return fig


def create_Rank_chart(data):
    rank_chart = RankChart(data)
    fig = rank_chart.render_chart()
    return fig


def main_Dash():
    #Dictionnaire des formations possibles
    FORMATIONS = dict(
        BTS="BTS",
        LICENCE="Licence",
        ECOLE_INGENIEUR="Ecole d'Ingénieur",
        ECOLE_COMMERCE="Ecole de Commerce",
        CPGE="CPGE",
        BUT="BUT",
        AUTRE_FORMATIONS="Autre formation",
        IFSI="IFSI",
        EFTS="EFTS",
        PASS="PASS",
        LICENCE_LAS="Licence_Las",
    )


    FORMATIONS_options = [
        {"label": str(FORMATIONS[formations]), "value": str(FORMATIONS[formations])}
        for formations in FORMATIONS
    ]

    file_manager = FileManager("./data/fr-esr-parcoursup-2021.csv")
    file_list = file_manager.open_file()
    data = file_list[0]
    bar_chart = BarChart(data, column="Filière de formation très agrégée", selected_formations=[])
    fig = bar_chart.render_chart()

    app = dash.Dash(__name__)  # (3)
    disableInter = False
    coordTemp = data["Coordonnées GPS de la formation"]
    for i in range(len(coordTemp)):
        if (type(coordTemp[i]) != str):  # Certaines formations n'ont pas de coordonnées GPS
            data = data.drop(labels=i, axis=0)
    GestionCarte.createAllMap(data)

    app.layout = html.Div(children=[

        html.H1(children=f'Titre de la page',
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
                    srcDoc=open("./templates/Carte_toute_formation.html", 'r').read(),
                    width='100%',
                    height='650',
                ),

            ]),

        html.Div(
            id='Holder_Div_Graph',
            hidden=False,
            style={'position': 'relative', 'width': '100%', 'padding': 10, 'float': 'left'},
            children=[
                html.Button('Hide/Show Graph', id='hideGraph', n_clicks=0),
                html.Div(
                    id='Div_Graph',
                    hidden=False,
                    children=[
                        html.Button('Open Graph', id='showFig', n_clicks=0),
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
                        html.Div(
                            id='Dropdown-bar_chart-holder',
                            hidden=False,
                            children=[
                                html.Label('Sélection des formations souhaitées.'),
                                dcc.Dropdown(

                                    options=FORMATIONS_options,
                                    value=list(),
                                    id="Dropdown-bar_chart",
                                    multi=True),
                                html.Br()
                            ]
                        ),
                        dcc.Graph(
                            id="graph",
                            figure=fig
                        ),
                    ]
                )
            ]
        ),  # (7)

        html.Span(id="ChangeClick", style={"verticalAlign": "middle"}),
    ]
    )

    @app.callback(
        Output("mapParFormation", "srcDoc"), [Input("Change", "value")],
    )
    def choose_map_Formation(name):
        if name == "All":
            return open("./templates/Carte_toute_formation.html", 'r').read()
        return open("./templates/Carte_par_formation_{}.html".format(name), 'r').read()

    @app.callback(
        Output("Div_Graph", "hidden"), [Input("hideGraph", "n_clicks")],
    )
    def hide_graph(n_clicks):
        if n_clicks % 2 == 0:
            return False
        return True

    @app.callback(
        Output("PlayFig", "hidden"), [Input("showFig", "n_clicks")]
    )
    def showFig_in_open_window(n_clicks):
        if n_clicks:
            fig.show()
        n_clicks = 0
        return True

    @app.callback(
        Output(component_id='graph', component_property='figure'),  # (1)
        Output(component_id='Dropdown-bar_chart-holder', component_property='hidden'),
        [Input(component_id='graph-slider', component_property='value'), Input('Dropdown-bar_chart', 'value')]  # (2)
    )
    def update_figure(input_value, formation):
        global fig
        match input_value:
            case 1:
                fig = create_Bar_chart(data, "Filière de formation très agrégée", formation)
                return fig, False
            case 2:
                fig = create_Rank_chart(data)
                return fig, True
            case 3:
                fig = create_Histogram(data, "Capacité de l’établissement par formation")
                return fig, True
            case 4:
                fig = create_Pie_chart(data, "Effectif total des candidats en phase principale",
                                       'Filière de formation très agrégée')
                return fig, True

    #
    # RUN APP
    #

    app.run_server(debug=True)  # (8)
