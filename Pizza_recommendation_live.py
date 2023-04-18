

import pandas as pd
from sklearn.neighbors import NearestNeighbors
import numpy as np


def get_recs(cart):
    """
    Input: cart: list of pizza types
    Ouput: top 5 recommended pizzas based on the cart

    Potential fixes: Save the model distances, since new orders cannot be saved, and shorten this code to only make recs in the loop at the end
    - not needed because recs are made instantly, but if the data were to increase in size dramatically, then this fix should be implemented
    """

    distances = np.loadtxt('distances.txt')
    indices = np.loadtxt('indices.txt').astype(int)
    # opening the file and extract pizza mapped to indices
    mp = open("map.txt", "r")
    mpd = mp.read()
    map_pizza = mpd.split('\n')
    mp.close()

    plot_data = []
    n = 5 # 5 pizza recommendations
    for i,item in enumerate(cart):
        idx = map_pizza.index(item)
        currDf = pd.DataFrame()
        currDf["Distance"] = distances[idx]
        currDf["Indices"] = indices[idx]
        currDf = currDf.sort_values(by="Indices")
        if(i==0):
            totalDf = currDf
        else:
            totalDf = totalDf.append(currDf)
        plot_data.append(currDf)

    distanceDf = totalDf.groupby("Indices").agg({"Distance":"mean"}).sort_values(by="Distance").reset_index() 
    all_recs = [(map_pizza[i], 1-d) for i,d in zip(distanceDf.Indices,distanceDf.Distance) if map_pizza[i] not in cart]

    return [i[0] for i in all_recs[:n]] # return top n recommended pizzas (not distance values here)




