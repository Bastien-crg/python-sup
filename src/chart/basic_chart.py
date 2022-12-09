from abc import ABC, abstractmethod


class BasicChart(ABC):
    def __init__(self):
        self.backup_data = None
        self.data = None

    @abstractmethod
    def render_chart(self, **parameters):
        pass

    def set_data(self, data):
        self.data = data
        self.backup_data = data

    def reload_data(self):
        self.data = self.backup_data
