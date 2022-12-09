from file_manager import FileManager
from chart.histogram import Histogram
from chart.bar_chart import BarChart
from chart.pie_chart import PieChart
from dash import dcc


def main():
    file_manager = FileManager("fr-esr-parcoursup.csv")
    file_list = file_manager.open_file()

    data = file_list[0]
    """
    histo = Histogram(data, x="Capacité de l’établissement par formation", nbins=20, max_value=199)
    histo.render_chart()
    
    
    bar_chart = BarChart(data, column="Filière de formation très agrégée")
    bar_chart.render_chart()
    bar_chart = BarChart(data, column="Filière de formation")
    bar_chart.render_chart()"""
    pie_chart = PieChart(data, values="Effectif total des candidats en phase principale",
                         names='Filière de formation très agrégée')
    # pie_chart.render_chart()
    dcc.Graph(figure=pie_chart)

    app.layout = html.Div(children=[

        html.H1(children=f'Capacité de l’établissement par formation ({year})',
                style={'textAlign': 'center', 'color': '#7FDBFF'}),  # (5)
        html.Label('Year'),
        dcc.Slider(
            id="year-slider",
            min=1952,
            max=2007,
            step=5,
            marks={
                1952: '1952',
                1957: '1957',
                1962: '1962',
                1967: '1967',
                1972: '1972',
                1977: '1977',
                1982: '1982',
                1987: '1987',
                1992: '1992',
                1997: '1997',
                2002: '2002',
                2007: '2007',
            },
            value=2007,
        ),
        dcc.Graph(
            id='graph1',
            figure=fig
        ),  # (6)

        html.Div(
            id="graph2-container",
            children=[
                dcc.Graph(
                    id="graph2",
                    figure=fig2
                ),
            ],
            style={"display": "none"}
        ),

        html.Div(children=f'''
                                    자유로운 기분, I like that
                                    고민 따윈 already done, done (done, done)
                                    색안경 끼고 보는 게 죄지
                                    That's not my fault, woah
                                    Told ya I don't care at all
                                    내 멋대로 갈 거야 (oh-oh)
                                    필요 없어 order
                                    Don't need no guidance, I'm makin' my way
                                '''),  # (7)

        dcc.Interval(id='interval',
                     interval=1 * 1000,  # in milliseconds
                     n_intervals=0,
                     ),

        dbc.Button(
            "Play",
            color="Play",
            id="Play",
            title="Play",
            n_clicks=0
        ),
        html.Span(id="PlayClick", style={"verticalAlign": "middle"}),

        dcc.Dropdown(
            id="Change",
            options=[
                {'label': 'Yes', 'value': True},
                {'label': 'No', 'value': False}
            ],
            value=True
        ),
        html.Span(id="ChangeClick", style={"verticalAlign": "middle"}),
    ]
    )


if __name__ == '__main__':
    main()
