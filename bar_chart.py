import plotly.graph_objects as go
import pandas as pd


def main():
    full_df = pd.read_csv("fr-esr-parcoursup.csv", sep=";")
    formations = full_df["Filière de formation très agrégée"].unique()
    fille = list()
    garcon = list()
    for i in formations:
        fille.append(full_df.loc[full_df[
                                     'Filière de formation très agrégée'] == i, 'Dont effectif des candidates admises'].sum())
        garcon.append(full_df.loc[full_df[
                                      'Filière de formation très agrégée'] == i, 'Effectif total des candidats ayant accepté la proposition de l’établissement (admis)'].sum())
        garcon[len(garcon) - 1] -= fille[len(fille) - 1]
    print(formations)
    fig = go.Figure(data=[
        go.Bar(name='Garçon', x=formations, y=garcon),
        go.Bar(name='Fille', x=formations, y=fille)
    ])
    # Change the bar mode
    fig.update_layout(barmode='group')
    fig.show()


    # detailed
    formations = full_df["Filière de formation"].unique()
    fille = list()
    garcon = list()
    for i in formations:
        fille.append(full_df.loc[full_df[
                                     'Filière de formation'] == i, 'Dont effectif des candidates admises'].sum())
        garcon.append(full_df.loc[full_df[
                                      'Filière de formation'] == i, 'Effectif total des candidats ayant accepté la proposition de l’établissement (admis)'].sum())
        garcon[len(garcon) - 1] -= fille[len(fille) - 1]
    print(formations)
    fig = go.Figure(data=[
        go.Bar(name='Garçon', x=formations, y=garcon),
        go.Bar(name='Fille', x=formations, y=fille)
    ])
    # Change the bar mode
    fig.update_layout(barmode='group')
    fig.show()


if __name__ == '__main__':
    main()
