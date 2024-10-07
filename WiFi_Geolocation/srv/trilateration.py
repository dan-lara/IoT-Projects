# from __future__ import division
# import math
# import numpy as np

# http://en.wikipedia.org/wiki/Trilateration
# assuming elevation = 0
# length unit : km

# earthR = 6371

# class base_station(object):
#     def __init__(self, lat, lon, dist):
#         self.lat = lat
#         self.lon = lon
#         self.dist = dist

# #using authalic sphere
# #if using an ellipsoid this step is slightly different
# #Convert geodetic Lat/Long to ECEF xyz
# #   1. Convert Lat/Long to radians
# #   2. Convert Lat/Long(radians) to ECEF  (Earth-Centered,Earth-Fixed)
# def convert_geodetci_to_ecef(base_station):
#     x = earthR *(math.cos(math.radians(base_station.lat)) * math.cos(math.radians(base_station.lon)))
#     y = earthR *(math.cos(math.radians(base_station.lat)) * math.sin(math.radians(base_station.lon)))
#     z = earthR *(math.sin(math.radians(base_station.lat)))
#     print (x, y, z)
#     return np.array([x, y, z])

# def calculate_trilateration_point_ecef(base_station_list):
#     P1, P2, P3 = map(convert_geodetci_to_ecef, base_station_list)
#     DistA, DistB, DistC = map(lambda x: x.dist, base_station_list)

#     #vector transformation: circle 1 at origin, circle 2 on x axis
#     ex = (P2 - P1)/(np.linalg.norm(P2 - P1))
#     i = np.dot(ex, P3 - P1)
#     ey = (P3 - P1 - i*ex)/(np.linalg.norm(P3 - P1 - i*ex))
#     ez = np.cross(ex,ey)
#     d = np.linalg.norm(P2 - P1)
#     j = np.dot(ey, P3 - P1)

#     #plug and chug using above values
#     x = (pow(DistA,2) - pow(DistB,2) + pow(d,2))/(2*d)
#     y = ((pow(DistA,2) - pow(DistC,2) + pow(i,2) + pow(j,2))/(2*j)) - ((i/j)*x)

#     # only one case shown here
#     z = np.sqrt(pow(DistA,2) - pow(x,2) - pow(y,2))

#     #triPt is an array with ECEF x,y,z of trilateration point
#     triPt = P1 + x*ex + y*ey + z*ez

#     #convert back to lat/long from ECEF
#     #convert to degrees
#     lat = math.degrees(math.asin(triPt[2] / earthR))
#     lon = math.degrees(math.atan2(triPt[1],triPt[0]))



import numpy as np
import pandas as pd
from scipy.optimize import minimize

def trilateration_2D(df):
    # Fonction pour convertir le RSSI en distance (en mètres)
    def rssi_to_distance(rssi, A=-40, n=2):
        """
        Calcule la distance basée sur le RSSI.
        A : RSSI à 1 mètre
        n : Exposant de perte de propagation
        """
        return 10 ** ((A - rssi) / (10 * n))

    # Conversion du RSSI en distance
    df['Distance'] = df['RSSI'].apply(lambda rssi: rssi_to_distance(rssi))
    
    # Sélection des points d'accès pour la trilatération (il faut au moins 3 points)
    access_points = df[['Latitude', 'Longitude', 'Distance']]
    
    # Définition de la fonction d'erreur pour la trilatération
    def trilateration_error(x, points):
        """
        Calcule l'erreur de distance entre la position estimée x et les points d'accès.
        x : Position estimée [Latitude, Longitude]
        points : DataFrame avec les colonnes Latitude, Longitude, Distance
        """
        error = 0
        for _, row in points.iterrows():
            # Calcul de la distance entre la position estimée et chaque point d'accès
            distance_calculated = np.sqrt((x[0] - row['Latitude'])**2 + (x[1] - row['Longitude'])**2)
            # Somme des erreurs quadratiques
            error += (distance_calculated - row['Distance'])**2
        return error

    # Point initial (moyenne des coordonnées des points d'accès)
    initial_position = [access_points['Latitude'].mean(), access_points['Longitude'].mean()]

    # Optimisation de la position pour minimiser l'erreur
    result = minimize(trilateration_error, initial_position, args=(access_points,), method='BFGS')
    
    # Coordonnées estimées après optimisation
    estimated_position = result.x
    
    return estimated_position
