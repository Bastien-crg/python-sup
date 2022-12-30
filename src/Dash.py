# filename = 'dash-01.py'

#
# Imports
#
import dash
from dash import dcc
from dash import html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc

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

def choose_year_file(date):
    match date:
        case 2021:
            return "../data/fr-esr-parcoursup-2021.csv"
        case 2020:
            return "../data/fr-esr-parcoursup-2020.csv"
        case 2019:
            return "../data/fr-esr-parcoursup-2019.csv"
        case 2018:
            return "../data/fr-esr-parcoursup-2018.csv"

def open_data(date):
    file_name = choose_year_file(date)
    file_manager = FileManager(file_name)
    file_list = file_manager.open_file()
    data = file_list[0]
    return data



def init_maps(data):
    coordTemp = data["Coordonnées GPS de la formation"]
    for i in range(len(coordTemp)):
        if (type(coordTemp[i]) != str):  # Certaines formations n'ont pas de coordonnées GPS
            data = data.drop(labels=i, axis=0)
    GestionCarte.createAllMap(data)

def init_dash(date):
    data = open_data(date)
    init_card(data)
    bar_chart = BarChart(data, column="Filière de formation très agrégée", selected_formations=[])
    fig = bar_chart.render_chart()
    return data, fig

def init_card(data):
    global card_nb_etablissement_content
    global card_nb_formations_content
    global card_nb_ecole_inge_content
    global card_nb_forma_commune_content
    global card_pourcentage_selectif_content
    global card_pourcentage_public_content
    
    card_nb_etablissement_content = [       
                            dbc.CardBody(
                                [
                                    html.H4("Nombre d'établissement", className="card_nb_etablissement",style={'textAlign' : 'center'}),
                                    html.P(
                                        data['Établissement'].nunique(),
                                        className="card-text",
                                        style={'textAlign' : 'center'},
                                    ),
                                ]
                            ),
                    ]
                    
    card_nb_formations_content = [       
                            dbc.CardBody(
                                [
                                    html.H4("Nombre de formations", className="card_nb_formations",style={'textAlign' : 'center'}),
                                    html.P(
                                        len(data.index),
                                        className="card-text",
                                        style={'textAlign' : 'center'},
                                    ),
                                ]
                            ),
                    ]
                
    card_nb_ecole_inge_content = [       
                            dbc.CardBody(
                                [
                                    html.H4("Nombre d'écoles d'ingénieur disponible", className="card_nb_ecole_inge",style={'textAlign' : 'center'}),
                                    html.P(
                                        data.loc[(data['Filière de formation très agrégée'] == "Ecole d'Ingénieur")]["Établissement"].nunique(),
                                        className="card-text",
                                        style={'textAlign' : 'center'},
                                    ),
                                ]
                            ),
                    ]
                
                
    card_nb_forma_commune_content = [       
                            dbc.CardBody(
                                [
                                    html.H4("Nombre de commune avec une formation", className="card_nb_forma_commune",style={'textAlign' : 'center'}),
                                    html.P(
                                        data['Commune de l’établissement'].nunique(),
                                        className="card-text",
                                        style={'textAlign' : 'center'},
                                    ),
                                ]
                            ),
                        ]
    
    card_pourcentage_selectif_content = [       
                                dbc.CardBody(
                                        [
                                            html.H4("Pourcentage des formations selectives ", className="card_pourcentage_selectif",style={'textAlign' : 'center'}),
                                            html.P(
                                                str(len(data.loc[(data['Sélectivité'] == "formation sélective")].index) / len(data.index) * 100) + " %",
                                                className="card-text",
                                                style={'textAlign' : 'center'},
                                            ),
                                        ]
                                    ),
                            ]
                   
    card_pourcentage_public_content = [       
                                dbc.CardBody(
                                         [
                                            html.H4("Pourcentage des formations public ", className="card_pourcentage_public",style={'textAlign' : 'center'}),
                                            html.P(
                                                str(len(data.loc[(data['Statut de l’établissement de la filière de formation (public, privé…)'] == "Public")].index) / len(data.index) * 100) + " %",
                                                className="card-text",
                                                style={'textAlign' : 'center'},
                                            ),
                                        ]
                                    ),
                            ]
    
        
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

    
    
    data , fig = init_dash(2021)
    app = dash.Dash(__name__)
    app.layout = html.Div(children=[

        html.H1(children=f'Titre de la page',
                style={'Position': 'relative', 'width': '100%', 'textAlign': 'center', 'color': '#7FDBFF'}),
        
        html.Div(
            id = "Left_column",
            style={'position': 'relative', 'width': '48%', 'float': 'left'},
            children = [
                html.Div(
                    id = "Cards_Div",
                    children = [
                        html.Div(
                            id = 'left_cards_div',
                            style={'position': 'relative', 'width': '49%', 'float': 'left'},
                            children = [
                                dbc.Card(card_nb_etablissement_content,color="#edc6a2"),
                                dbc.Card(card_nb_ecole_inge_content,color="#edc6a2"),
                                dbc.Card(card_pourcentage_public_content,color="#edc6a2"),
                            ]
                        ),
                        
                        html.Div(
                            id = "right_cards_div",
                            style={'position': 'relative', 'width': '49%', 'float': 'left'},
                            children = [
                                dbc.Card(card_nb_formations_content,color="#edc6a2"),
                                dbc.Card(card_nb_forma_commune_content,color="#edc6a2"),
                                dbc.Card(card_pourcentage_selectif_content,color="#edc6a2"),
                                
                            ]
                        ),
                        ]
                    ),
                ]
            ),
    
        
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
                                html.H4(children=f'Sélection des formations souhaitées',),
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
            return open("../templates/Carte_toute_formation.html", 'r').read()
        return open("../templates/Carte_par_formation_{}.html".format(name), 'r').read()

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
