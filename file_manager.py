import pandas


class FileManager:
    def __init__(self, *filenames):
        self.filenames = filenames

    def open_file(self):
        res = []
        for file in self.filenames:
            res.append(pandas.read_csv(file, sep=";"))
        return res
