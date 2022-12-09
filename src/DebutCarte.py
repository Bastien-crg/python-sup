import geojson, geopandas, folium
import pandas as pd
import math

def functionTransform(data):
    return ((math.log(data))**2)/5

def mapFromationColor(name):
    match name:         
        case "BTS":
            return 'blue'
        case "Ecole d'Ingénieur":
            return 'gold'
        case "Licence":
            return 'green'
        case "Ecole de Commerce":
            return 'purple'
        case "CPGE":
            return 'darkred'
        case "BUT":
            return 'brown'
        case "IFSI":
            return 'gray'
        case "EFTS":
            return 'orange'
        case "PASS":
            return 'black'
        case _:
            return 'crimson'

def mapTouteFormation(dataframe):
    coordsFrance = (46.539758, 2.430331)
    map = folium.Map(location=coordsFrance, tiles='OpenStreetMap', zoom_start=6)

    for i in dataframe.index:
        folium.CircleMarker(
            location = (float((dataframe["Coordonnées GPS de la formation"][i].split(","))[0]), float((dataframe["Coordonnées GPS de la formation"][i].split(","))[1])),
            radius = 2,
            color = mapFromationColor(dataframe["Filière de formation très agrégée"][i]),
            fill = True,
            fill_color = mapFromationColor(dataframe["Filière de formation très agrégée"][i])
        ).add_to(map)
    return map   

def mapParFilièreTresAgrégée(dataframe,name):
    coordsFrance = (46.539758, 2.430331)
    lstName = dataframe[(dataframe["Filière de formation très agrégée"] == name)]
    map2 = folium.Map(location=coordsFrance, tiles='OpenStreetMap', zoom_start=6)
    for i in lstName.index:
        folium.CircleMarker(
            location = (float((lstName["Coordonnées GPS de la formation"][i].split(","))[0]), float((lstName["Coordonnées GPS de la formation"][i].split(","))[1])),
            radius = functionTransform(lstName["Capacité de l’établissement par formation"][i] ),
            color = mapFromationColor(dataframe["Filière de formation très agrégée"][i]),
            fill = True,
            fill_color = mapFromationColor(dataframe["Filière de formation très agrégée"][i])
        ).add_to(map2)  
    return map2

def createAllMap(dataframe):
    lstNameFormation = ["BTS","Ecole d'Ingénieur","Licence","Ecole de Commerce","CPGE","BUT","IFSI","EFTS","PASS",]
    for name in lstNameFormation :
        map = mapParFilièreTresAgrégée(dataframe,name)
        map.save("../templates/Carte_par_formation_{}.html".format(name))
    map = mapTouteFormation(dataframe)
    map.save("../templates/Carte_toute_formation.html")

def main():
    c = pd.read_csv("../data/fr-esr-parcoursup.csv", sep =";")
    coordTemp = c["Coordonnées GPS de la formation"]
    for i in range(len(coordTemp)):
        if(type(coordTemp[i]) != str):
            c = c.drop(labels=i,axis=0)
    createAllMap(c)
    
    
if __name__ == '__main__':
    main()
    

