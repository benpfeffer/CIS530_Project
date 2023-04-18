import pandas as pd
from sklearn.neighbors import NearestNeighbors
import numpy as np


def store_model():
	"""
	Store the distances, indices, and map using nearest neighbors (brute, cosine) of the pizzas
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


	# ### From class notes, best recommendation type is item to item
	# ### In our case, this means pizzas that go with pizzas, not order

	# ### Need co-occurence of pizza type using cosine similarity


	simple = moDf[["order_id", "quantity", "pizza_type_id"]]
	copyDf = simple.copy()
	copyDf['quantity'] = 1


	copyDf = copyDf.drop_duplicates().reset_index(drop=True)


	itemitem = copyDf.pivot(index='pizza_type_id', columns='order_id', values='quantity').fillna(0)


	# ### Given a cart, average cosine sim for each item and display the optimal n (5)

	# FINAL SYSTEM - USED LIVE AND INCLUDES ALL GIVEN DATA
	map_pizza = itemitem.index.to_list()

	knn = NearestNeighbors(metric='cosine', algorithm='brute')
	knn.fit(itemitem.values)
	distances, indices = knn.kneighbors(itemitem.values, n_neighbors=len(map_pizza)) #+1 for removal of self similarity


	# Store model results and the map to indices
	np.savetxt("distances.txt", distances)
	np.savetxt("indices.txt", indices)
	np.savetxt("map.txt", map_pizza,fmt='%s')





