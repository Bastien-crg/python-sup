import plotly.graph_objects as go
import pandas as pd


def main():
    full_df = pd.read_csv("fr-esr-parcoursup.csv", sep=";")
    full_df["counting"] = 1
    cities = full_df["Commune de l’établissement"].unique()
    cities = pd.DataFrame(cities)
    cities["nb_of_form"] = 0
    for index, row in cities.iterrows():
        cities.at[index,"nb_of_form"] = full_df.loc[full_df['Commune de l’établissement'] == row[0], 'counting'].sum()
    cities = cities.sort_values(by=['nb_of_form'])
    filtered_cities = cities[cities["nb_of_form"]>150]
    """for i in cities:
        nb_of_form.append(full_df.loc[full_df['Commune de l’établissement'] == i, 'counting'].sum())"""
    fig = go.Figure(go.Bar(
        x=filtered_cities["nb_of_form"],
        y=filtered_cities[0],
        orientation='h'))

    fig.show()


if __name__ == '__main__':
    main()
