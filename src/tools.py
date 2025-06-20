import pandas as pd
from math import radians, sin, cos, sqrt, atan2



def haversine(lat1, lon1, lat2, lon2):
    # Radio de la Tierra en km
    R = 6371.0

    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c

def find_closest_municipio(latitude, longitude):
    ubicaciones = pd.read_csv('data/municipios.csv')

    ubicaciones['Distancia'] = ubicaciones.apply(
        lambda row: haversine(latitude, longitude, row['Latitud'], row['longitud']), axis=1
    )
    
    return ubicaciones[['Código Municipio','Nombre Municipio']].loc[ubicaciones['Distancia'].idxmin()]
    
    

def generate_recomendation(latitude, longitude,cycle):
    df = pd.read_csv('data/cultivos_con_ubicaciones.csv')
    
    closest_municipio = find_closest_municipio(latitude, longitude)
    
    print(f"Municipio más cercano: {closest_municipio['Nombre Municipio']} ({closest_municipio['Código Municipio']})")
    
    recomendados = df[
        (df['Código Municipio'] == closest_municipio['Código Municipio'])
    ]
    
    if cycle != "TODOS":
        recomendados = recomendados[recomendados['CICLO DE CULTIVO'] == cycle]
        
    recomendados = recomendados.drop_duplicates(subset=['GRUPO \nDE CULTIVO', 'CULTIVO'])
    
    return recomendados[['GRUPO \nDE CULTIVO', 'CULTIVO','Rendimiento\n(t/ha)']]

    
    
    