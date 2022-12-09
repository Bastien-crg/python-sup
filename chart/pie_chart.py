import plotly.express as px

from chart.basic_chart import BasicChart


class PieChart(BasicChart):

    def __init__(self, data, **parameters):
        super().__init__()
        self.values = parameters["values"]
        self.names = parameters["names"]
        self.set_data(data)

    def render_chart(self):
        fig = px.pie(self.data, values=self.values, names=self.names)
        fig.show()
        
    def returnPx(self):
        fig = px.pie(self.data, values=self.values, names=self.names)
        return fig
