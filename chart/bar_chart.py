import plotly.express as px
import plotly.graph_objects as go
from chart.basic_chart import BasicChart


class BarChart(BasicChart):

    def __init__(self,data, **parameters):
        super().__init__()
        self.fille = list()
        self.garcon = list()
        self.formations = None
        self.column = parameters["column"]
        self.set_data(data)

    def render_chart(self):
        self.formations = self.data[self.column].unique()
        for i in self.formations:
            self.fille.append(self.data.loc[self.data[self.column] == i, 'Dont effectif des candidates admises'].sum())
            self.garcon.append(self.data.loc[self.data[self.column] == i, 'Effectif total des candidats ayant accepté la proposition de l’établissement (admis)'].sum())
            self.garcon[len(self.garcon) - 1] -= self.fille[len(self.fille) - 1]

        fig = go.Figure(data=[
            go.Bar(name='Garçon', x=self.formations, y=self.garcon),
            go.Bar(name='Fille', x=self.formations, y=self.fille)
        ])
        fig.update_layout(barmode='group')
        return fig
