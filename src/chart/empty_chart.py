import plotly.graph_objects as go
from .basic_chart import BasicChart


class EmptyChart(BasicChart):

    def __init__(self):
        super().__init__()

    def render_chart(self):
        fig = go.Figure()
        fig.update_layout(
            xaxis={"visible": False},
            yaxis={"visible": False},
            annotations=[
                {
                    "text": "Ce graphique n'est pas disponible pour cette année",
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "font": {
                        "size": 28
                    }
                }
            ]
        )
        return fig
