# Pizza_recommendation_live.py file for Cart-Based Pizza Recommendation System
# Ben Pfeffer, Andrew Anctil, Bradon Wetzel
# CIS 530 - Advanced Data Mining - Professor Thomas Gyeera

# Import libraries
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import numpy as np


def get_recs(cart):
    """
    Function to get the top 5 recommendations based on the current cart.
    Input: cart: list of pizza types
    Ouput: list: top 5 recommended pizzas based on the cart
    """

    # Load the distances and indices from the Nearest Neighbors model from pizza_rec_model.py
    distances = np.loadtxt('distances.txt')
    indices = np.loadtxt('indices.txt').astype(int)

    # Open the map file and extract pizza mapped to indices (needed because not numbers)
    mp = open("map.txt", "r")
    mpd = mp.read()
    map_pizza = mpd.split('\n')
    mp.close()

    n = 5 # 5 pizza recommendations
    # Iterate through items in the cart
    for i,item in enumerate(cart):
        # Get the index of the current cart item
        idx = map_pizza.index(item)

        # Create a dataframe of the distances and indices, and sort by indices
        currDf = pd.DataFrame()
        currDf["Distance"] = distances[idx]
        currDf["Indices"] = indices[idx]
        currDf = currDf.sort_values(by="Indices")

        # Create an output dataframe for all pizzas, storing all indices and distances
        if(i==0):
            totalDf = currDf
        else:
            totalDf = totalDf.append(currDf)

    # Group the output dataframe by the indices(which map to pizza types) and get the mean distance, then sort by distance ascending
    distanceDf = totalDf.groupby("Indices").agg({"Distance":"mean"}).sort_values(by="Distance").reset_index() 

    # Get the top pizza type recommendations if they are not in the cart, which is sorted in order of distance ascending
    all_recs = [(map_pizza[i], 1-d) for i,d in zip(distanceDf.Indices,distanceDf.Distance) if map_pizza[i] not in cart]

    # Return the top n (5) recommended pizza types
    return [i[0] for i in all_recs[:n]]




