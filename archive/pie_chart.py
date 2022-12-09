import plotly.express as px
import pandas as pd


def main():
    full_df = pd.read_csv("../data/fr-esr-parcoursup.csv", sep=";")
    fig = px.pie(full_df, values="Effectif total des candidats en phase principale",
                 names='Filière de formation très agrégée')
    fig.show()
    fig = px.pie(full_df, values="Effectif total des candidats ayant accepté la proposition de l’établissement (admis)",
                 names='Filière de formation très agrégée')
    fig.show()


if __name__ == '__main__':
    main()
