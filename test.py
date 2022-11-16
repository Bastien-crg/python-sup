import csv
import plotly.express as px
import pandas as pd


def read_file(filename):
    l = []
    with open(filename, newline='', encoding="UTF-8") as file:
        reader = csv.DictReader(file, delimiter=";")
        for row in reader:
            l.append(row)
    return l


def main():
    l = pd.read_csv("fr-esr-parcoursup.csv", sep=";")

    fig = px.histogram(data_frame=l, x="Capacité de l’établissement par formation")
    # fig = px.histogram(data_frame=sorted(l, key=lambda d: int(d['Capacité de l’établissement par formation'])), x="Capacité de l’établissement par formation", nbins=10)
    fig.show()


if __name__ == '__main__':
    main()
