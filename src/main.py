from file_manager import FileManager
from chart import RankChart
from chart import BarChart

def main():
    file_manager = FileManager("../data/fr-esr-parcoursup.csv")
    file_list = file_manager.open_file()

    data = file_list[0]
    """
    histo = Histogram(data, x="Capacité de l’établissement par formation", nbins=20, max_value=199)
    histo.render_chart()
    
    
    bar_chart = BarChart(data, column="Filière de formation très agrégée")
    bar_chart.render_chart()
    bar_chart = BarChart(data, column="Filière de formation")
    bar_chart.render_chart()
    pie_chart = PieChart(data, values="Effectif total des candidats en phase principale",
                         names='Filière de formation très agrégée')
    # pie_chart.render_chart()"""
    # rank_chart = RankChart(data)
    # rank_chart.render_chart()
    bar_chart = BarChart(data, column="Filière de formation très agrégée")
    bar_chart.render_chart()
    bar_chart.show()






if __name__ == '__main__':
    main()
