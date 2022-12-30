from src.file_manager import FileManager
from src.chart import RankChart
from src.chart import Histogram
from src.chart import BarChart
from src.chart import PieChart
from src.chart import ScatterChart
from src.chart import EmptyChart
from src.Dash import main_Dash


def main():

    file_manager = FileManager("./data/fr-esr-parcoursup-2021.csv",
                               "./data/fr-esr-parcoursup-2020.csv",
                               "./data/fr-esr-parcoursup-2019.csv",
                               "./data/fr-esr-parcoursup-2018.csv")
    file_list = file_manager.open_file()

    data = file_list[0]

    """
    histo = Histogram(data, x="Capacité de l’établissement par formation", nbins=20, max_value=199)
    histo.render_chart()

    bar_chart = BarChart(data, column="Filière de formation très agrégée")
    bar_chart.render_chart()
    
    bar_chart = BarChart(data, column="Filière de formation")
    bar_chart.render_chart()

    pie_chart = PieChart(data, values="Effectif total des candidats pour une formation",names='Filière de formation très agrégée')
    pie_chart.render_chart(title="test")

    pie_chart = PieChart(data, values="Effectif total des candidats ayant accepté la proposition de l’établissement (admis)",names='Filière de formation très agrégée')
    pie_chart.render_chart(title="test")

    pie_chart = PieChart(data, values="Effectif total des candidats en phase principale",names='Filière de formation très agrégée')
    pie_chart.render_chart()

    rank_chart = RankChart(data)
    rank_chart.render_chart()
    
    scatter_chart = ScatterChart(data, abscisse="Capacité de l’établissement", ordonne="Nombre de formations par établissement",)
    scatter_chart.render_chart()
    
    empty = EmptyChart()
    empty.render_chart()
    """
    main_Dash()


if __name__ == '__main__':
    main()
