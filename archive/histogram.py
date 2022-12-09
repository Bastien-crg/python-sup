import plotly.express as px
import pandas as pd


def main():
    full_df = pd.read_csv("../data/fr-esr-parcoursup.csv", sep=";")
    filtered_df = full_df.loc[full_df["Capacité de l’établissement par formation"] <= 199]
    fig = px.histogram(data_frame=filtered_df, x="Capacité de l’établissement par formation", nbins=20)
    fig.show()


if __name__ == '__main__':
    main()
