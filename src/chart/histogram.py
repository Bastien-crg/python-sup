import plotly.express as px

from src.chart.basic_chart import BasicChart


class Histogram(BasicChart):

    def __init__(self, data, **parameters):
        super().__init__()
        self.x = parameters["x"]
        self.nbins = parameters["nbins"]
        self.max_value = parameters["max_value"]
        self.set_data(data)

    def render_chart(self):
        self.data = self.data.loc[self.data[self.x] <= self.max_value]
        fig = px.histogram(data_frame=self.data, x=self.x, nbins=self.nbins)
        return fig
        # fig.show()


