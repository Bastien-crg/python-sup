
import plotly.express as px
<<<<<<< HEAD
from .basic_chart import BasicChart
=======
from chart.basic_chart import BasicChart
>>>>>>> b4b9a9f473fc4581b1ede381570aa02ddd03dc25
import pandas as pd


class ScatterChart(BasicChart):

    def __init__(self, data, **parameters):
        super().__init__()
        self.abscisse = parameters["abscisse"]
        self.ordonne = parameters["ordonne"]
        self.set_data(data)

    def render_chart(self):
        self.data = self.backup_data["Établissement"].unique()
        self.data = pd.DataFrame(self.data)
        self.data = self.data.rename(columns={0: "Établissement"})
        self.data[self.abscisse] = 0
        self.data[self.ordonne] = 0
        self.backup_data["counting"] = 1
        for index, row in self.data.iterrows():
            self.data.at[index, self.abscisse] = self.backup_data.loc[
                self.backup_data["Établissement"] == row[0], "Capacité de l’établissement par formation"].sum()
            self.data.at[index, self.ordonne] = self.backup_data.loc[
                self.backup_data["Établissement"] == row[0], "counting"].sum()
        fig = px.scatter(self.data, x=self.abscisse, y=self.ordonne, hover_data=["Établissement"], log_x=True, log_y=True,title="Capacité des établissements en fonction de leur nombre de formations")
        # return fig
        fig.show()