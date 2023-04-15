

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

    od = pd.read_csv("pizza_sales/order_details.csv")
    o = pd.read_csv("pizza_sales/orders.csv")
    pt = pd.read_csv("pizza_sales/pizza_types.csv", encoding= 'unicode_escape') # codec decode error
    p = pd.read_csv("pizza_sales/pizzas.csv")


    ood = o.set_index('order_id').join(od.set_index('order_id')).reset_index()


    ppt = p.set_index('pizza_type_id').join(pt.set_index('pizza_type_id')).reset_index()



    df = ood.set_index('pizza_id').join(ppt.set_index('pizza_id')).reset_index().sort_values(by="order_details_id").reset_index(drop=True)



    groups = df.groupby("order_id").agg({"pizza_type_id":"count"}).reset_index()
    multiOrders = groups[groups.pizza_type_id>1].order_id.values


    # multi-order dataframe
    moDf = df[df.order_id.isin(multiOrders)].reset_index(drop=True)



    simple = moDf[["order_id", "quantity", "pizza_type_id"]]
    copyDf = simple.copy()
    copyDf = copyDf[copyDf.quantity==1]


    copyDf = copyDf.drop_duplicates().reset_index(drop=True)


    itemitem = copyDf.pivot(index='pizza_type_id', columns='order_id', values='quantity').fillna(0)


    # Given a cart, average cosine sim for each item and display the optimal n (5)

    # FINAL SYSTEM - USED LIVE AND INCLUDES ALL GIVEN DATA
    map_pizza = itemitem.index.to_list()

    knn = NearestNeighbors(metric='cosine', algorithm='brute')
    knn.fit(itemitem.values)
    distances, indices = knn.kneighbors(itemitem.values, n_neighbors=len(map_pizza)) #+1 for removal of self similarity


    plot_data = []
    #cart = ["bbq_ckn", "hawaiian", "five_cheese"]
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




