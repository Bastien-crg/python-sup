# filename = 'dash-01.py'

#
# Imports
#
import dash
from dash import dcc
from dash import html
from dash import ctx
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc

import src.GestionCarte as GestionCarte

from src.file_manager import FileManager
from src.chart import RankChart
from src.chart import BarChart
from src.chart import PieChart
from src.chart import Histogram
from src.chart import ScatterChart
from src.chart import EmptyChart

from time import sleep

def create_Bar_chart(data, column_Name, selected_formation=[]):
    bar_chart = BarChart(data, column=column_Name, selected_formations=selected_formation)  
    fig = bar_chart.render_chart()
    return fig

def create_scatter_chart(data,abscisse,ordonee):
    scatter_chart = ScatterChart(data, abscisse=abscisse, ordonne=ordonee)
    fig = scatter_chart.render_chart()
    return fig


def create_Histogram(data, x_name, nbins=20, max_value=199):
    histogram = Histogram(data, x=x_name, nbins=nbins, max_value=max_value)
    fig = histogram.render_chart()
    return fig


def create_Pie_chart(data, values_name, names):
    pie_chart = PieChart(data, values=values_name,
                         names=names)
    fig = pie_chart.render_chart(title=values_name)
    return fig


def create_Rank_chart(data):
    if date != 2021:
        return create_Empty_chart()
    rank_chart = RankChart(data)
    fig = rank_chart.render_chart()
    return fig

def create_Empty_chart():
    empty_chart = EmptyChart()
    fig = empty_chart.render_chart()
    return fig

def choose_year_file(date):
    match date:
        case 2021:
            return "data/fr-esr-parcoursup-2021.csv"
        case 2020:
            return "data/fr-esr-parcoursup-2020.csv"
        case 2019:
            return "data/fr-esr-parcoursup-2019.csv"
        case 2018:
            return "data/fr-esr-parcoursup-2018.csv"


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


def init_pie_chart(data):
    global pie_chart_choix
    global pie_chart_admis

    pie_chart_choix = create_Pie_chart(data, "Effectif total des candidats pour une formation",
                                       'Filière de formation très agrégée')
    pie_chart_admis = create_Pie_chart(data,
                                       "Effectif total des candidats ayant accepté la proposition de l’établissement (admis)",
                                       'Filière de formation très agrégée')
    
def pie_chart_div(data):
    init_pie_chart(data)
    div = [
        dcc.Tab(label="Repartitions des choix des élèves",
        children=[dcc.Graph(figure=pie_chart_choix)]),
        dcc.Tab(
            label="Effectif total des candidats ayant accepté la proposition de l’établissement",
            children=[dcc.Graph(figure=pie_chart_admis)])
    ]
    return div

def init_dash(date):
    data = open_data(date)
    init_card(data,date)
    init_pie_chart(data)
    fig = create_Empty_chart()
    return data, fig


def init_card(data,date):
    global card_nb_etablissement_content
    global card_nb_formations_content
    global card_nb_ecole_inge_content
    global card_nb_forma_commune_content
    global card_pourcentage_selectif_content
    global card_pourcentage_public_content
    if date > 2020:
        nb_commune = str(data['Commune de l’établissement'].nunique()) 
    else:
        nb_commune = "NON DISPONIBLE"

    if date > 2019:
        selectivite = str(len(data.loc[(data['Sélectivité'] == "formation sélective")].index) / len(data.index) * 100) + " %"
    else:
        selectivite = "NON DISPONIBLE"
    
    if date > 2018:
        prct_forma_public = str(len(data.loc[(data['Statut de l’établissement de la filière de formation (public, privé…)'] == "Public")].index) / len(data.index) * 100) + " %"
    else: 
        prct_forma_public = "NON DISPONIBLE"
        
    card_nb_etablissement_content = [       
                            dbc.CardBody(
                                [
                                    html.H4("Nombre d'établissement", className="card_nb_etablissement",style={'textAlign' : 'center'}),
                                    html.H2(
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
                                    html.H2(
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
                                    html.H2(
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
                                    html.H2(
                                        nb_commune,
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
                                            html.H2(
                                                selectivite,
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
                                            html.H2(
                                                prct_forma_public,
                                                className="card-text",
                                                style={'textAlign' : 'center'},
                                            ),
                                        ]
                                    ),
                            ]
    

def card_div(data):
    init_card(data,date)
    div = [
        html.Div(
            id='left_cards_div',
            style={'position': 'relative', 'width': '49%', 'float': 'left'},
            children=[
                        dbc.Card(card_nb_etablissement_content, color="#edc6a2"),
                        dbc.Card(card_nb_ecole_inge_content, color="#edc6a2"),
                        dbc.Card(card_pourcentage_public_content, color="#edc6a2"),
                    ]
            ),

            html.Div(
                    id="right_cards_div",
                    style={'position': 'relative', 'width': '49%', 'float': 'left'},
                    children=[
                                dbc.Card(card_nb_formations_content, color="#edc6a2"),
                                dbc.Card(card_nb_forma_commune_content, color="#edc6a2"),
                                dbc.Card(card_pourcentage_selectif_content, color="#edc6a2"),
                            ]
                    ),
    ]
    return div
    
def manage_dash(FORMATIONS_OPTIONS):
    global fig
    global change_date
    global data
    data , fig = init_dash(date)
    app = dash.Dash(__name__)
    app.layout = html.Div(
        children=[
            dcc.Location(id='url', refresh=False),
            html.H1(children=f'Titre de la page',
                    style={'Position': 'relative', 'width': '100%', 'textAlign': 'center', 'color': '#7FDBFF'}),
            html.A(
                id = "change_year",
                children=[
                    html.Button('2021', id='btn-2021', n_clicks=0),
                    html.Button('2020', id='btn-2020', n_clicks=0),
                    html.Button('2019', id='btn-2019', n_clicks=0),
                    html.Button('2018', id='btn-2018', n_clicks=0),
                    html.Div(id='container-button')
                ]),
            html.Div(
                id = "main_body",
                children = [
                    html.Div(
                        id="Left_column",
                        style={'position': 'relative', 'width': '48%', 'float': 'left'},
                        children=[
                            html.Div(
                                id="Cards_Div",
                                children=[
                                    html.Div(
                                        id='left_cards_div',
                                        style={'position': 'relative', 'width': '49%', 'float': 'left'},
                                        children=[
                                            dbc.Card(card_nb_etablissement_content, color="#edc6a2"),
                                            dbc.Card(card_nb_ecole_inge_content, color="#edc6a2"),
                                            dbc.Card(card_pourcentage_public_content, color="#edc6a2"),
                                        ]
                                    ),

                                    html.Div(
                                        id="right_cards_div",
                                        style={'position': 'relative', 'width': '49%', 'float': 'left'},
                                        children=[
                                            dbc.Card(card_nb_formations_content, color="#edc6a2"),
                                            dbc.Card(card_nb_forma_commune_content, color="#edc6a2"),
                                            dbc.Card(card_pourcentage_selectif_content, color="#edc6a2"),

                                        ]
                                    ),
                                ]
                            ),

                            html.Div(
                                id="pie_chart",
                                style={'position': 'relative', 'width': '96%', 'float': 'left'},
                                children=[
                                    dcc.Tabs(
                                        id="tabs_pie_chart",
                                    ),
                                ]
                            )
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
                                srcDoc=open("templates/Carte_toute_formation.html", 'r').read(),
                                width='100%',
                                height='650',
                            ),

                        ]
                    ),

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
                                            4: 'scatter',
                                        },
                                        value=1,
                                    ),
                                    html.Div(
                                        id='Dropdown-bar_chart-holder',
                                        hidden=False,
                                        children=[
                                            html.H4(children=f'Sélection des formations souhaitées', ),
                                            dcc.Dropdown(

                                                options=FORMATIONS_OPTIONS,
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
                    )
                ]
            ),

            html.Span(id="ChangeClick", style={"verticalAlign": "middle"}),
        ]
    )

    @app.callback(
        Output("mapParFormation", "srcDoc"), [Input("Change", "value")],
    )
    def choose_map_Formation(name):
        if name == "All":
            return open("templates/Carte_toute_formation.html", 'r').read()
        return open("templates/Carte_par_formation_{}.html".format(name), 'r').read()

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
        global data
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
                fig = create_scatter_chart(data, "Capacité de l’établissement",'Nombre de formations par établissement')
                return fig, True

    @app.callback(
    Output('container-button', 'children'),
    Output('Cards_Div','children'),
    Output('pie_chart','children'),
    Input('btn-2021', 'n_clicks'),
    Input('btn-2020', 'n_clicks'),
    Input('btn-2019', 'n_clicks'),
    Input('btn-2018', 'n_clicks')
)
    def displayClick(btn1, btn2, btn3, btn4):
        global date
        global fig
        global data
        global change_date
        msg = "Année choisie = 2021"
        if "btn-2021" == ctx.triggered_id:
            date = 2021
            msg = "Année choisie = 2021"
        elif "btn-2020" == ctx.triggered_id:
            date = 2020
            msg = "Année choisie = 2020"
        elif "btn-2019" == ctx.triggered_id:
            date = 2019
            msg = "Année choisie = 2019"
        elif "btn-2018" == ctx.triggered_id: 
            date = 2018
            msg = "Année choisie = 2018"
        data = open_data(date)
        div_card = card_div(data)
        init_pie_chart(data)
        div_pie_chart = pie_chart_div(data)
        return html.Div(msg),div_card,[dcc.Tabs(id="tabs_pie_chart",children=div_pie_chart),]

    
    #
    # RUN APP
    #

    app.run_server(debug=True)

def main_Dash(is_date_selected = False):
    # Dictionnaire des formations possibles
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
    FORMATIONS_OPTIONS = [
        {"label": str(FORMATIONS[formations]), "value": str(FORMATIONS[formations])}
        for formations in FORMATIONS
    ]
    global date
    global fig
    global data
    global change_date
    change_date = False
    date = 2021
    data , fig = init_dash(date)
    
    manage_dash(FORMATIONS_OPTIONS)
    
