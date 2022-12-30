import pandas as pd
import plotly.graph_objects as go
from chart.basic_chart import BasicChart


class RankChart(BasicChart):

    def __init__(self, data):
        super().__init__()
        self.set_data(data)

    # x : Capacité de l’établissement par formation, nbins : 20
    def render_chart(self, **parameters):
        self.data = self.backup_data["Commune de l’établissement"].unique()
        self.data = pd.DataFrame(self.data)
        self.data["nb_of_form"] = 0
        self.backup_data["counting"] = 1
        for index, row in self.data.iterrows():
            self.data.at[index, "nb_of_form"] = self.backup_data.loc[
                self.backup_data['Commune de l’établissement'] == row[0], 'counting'].sum()
        self.data = self.data.sort_values(by=['nb_of_form'])
        cities = self.data[self.data["nb_of_form"] > 150]
        fig = go.Figure(go.Bar(x=cities["nb_of_form"], y=cities[0], orientation='h'))
        fig.update_layout(title_text='Classement des villes avec le plus de formation')
        return fig
