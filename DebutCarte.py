import geojson, geopandas, folium
import pandas as pd
import math

def functionTransform(data):
    return math.log(data)

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
        case "License_Las":
            return 'white'
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
    
    map.save(outfile='Toute les Formation.html')    

def mapParFilièreTresAgrégée(dataframe,name):
    coordsFrance = (46.539758, 2.430331)
    lstName = dataframe[(dataframe["Filière de formation très agrégée"] == name)]
    map2 = folium.Map(location=coordsFrance, tiles='OpenStreetMap', zoom_start=6)
    for i in lstName.index:
        folium.CircleMarker(
            location = (float((lstName["Coordonnées GPS de la formation"][i].split(","))[0]), float((lstName["Coordonnées GPS de la formation"][i].split(","))[1])),
            radius = functionTransform( lstName["Capacité de l’établissement par formation"][i] ),
            color = mapFromationColor(dataframe["Filière de formation très agrégée"][i]),
            fill = True,
            fill_color = mapFromationColor(dataframe["Filière de formation très agrégée"][i])
        ).add_to(map2)      
    map2.save(outfile='map2.html')

def main():
    c = pd.read_csv("fr-esr-parcoursup.csv", sep = ";")
    coordTemp = c["Coordonnées GPS de la formation"]
    for i in range(len(coordTemp)):
        if(type(coordTemp[i]) != str):
            c = c.drop(labels=i,axis=0)
    mapParFilièreTresAgrégée(c,"BTS")
    mapTouteFormation(c)
    
    
if __name__ == '__main__':
    main()
    

