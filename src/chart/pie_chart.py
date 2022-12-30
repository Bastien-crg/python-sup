import plotly.express as px
from .basic_chart import BasicChart


class PieChart(BasicChart):

    def __init__(self, data, **parameters):
        super().__init__()
        self.values = parameters["values"]
        self.names = parameters["names"]
        self.set_data(data)

    def render_chart(self, **parameters):
        fig = px.pie(self.data, values=self.values, names=self.names, title=parameters["title"],
                     color_discrete_map={'Licence': 'blue',
                                         'BTS': 'red',
                                         'IFSI': 'lime',
                                         'BUT': 'violet',
                                         'CPGE': 'orange',
                                         'PASS': 'cyan',
                                         'Autre formation': 'pink',
                                         'Ecole d\'ingénieur': 'green',
                                         'Licence_Las': 'cyan',
                                         'Ecole de commerce': 'yellow',
                                         'EFTS': 'white'
                                         })
        return fig
