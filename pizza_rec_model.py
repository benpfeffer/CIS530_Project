# pizza_rec_model.py file for Cart-Based Pizza Recommendation System
# Ben Pfeffer, Andrew Anctil, Bradon Wetzel
# CIS 530 - Advanced Data Mining - Professor Thomas Gyeera

# Import libraries
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import numpy as np


def store_model():
	"""
	Store the distances, indices, and map into text files using nearest neighbors (brute, cosine) of the pizzas ordered together
	"""

	# Load the data
	od = pd.read_csv("pizza_sales/order_details.csv")
	o = pd.read_csv("pizza_sales/orders.csv")
	pt = pd.read_csv("pizza_sales/pizza_types.csv", encoding= 'unicode_escape') # codec decode error
	p = pd.read_csv("pizza_sales/pizzas.csv")

	# Join the data on the id columns into one dataframe
	ood = o.set_index('order_id').join(od.set_index('order_id')).reset_index()
	ppt = p.set_index('pizza_type_id').join(pt.set_index('pizza_type_id')).reset_index()
	df = ood.set_index('pizza_id').join(ppt.set_index('pizza_id')).reset_index().sort_values(by="order_details_id").reset_index(drop=True)

	# Group by order and get the count
	groups = df.groupby("order_id").agg({"pizza_type_id":"count"}).reset_index()

	# Select orders with more than one pizza
	multiOrders = groups[groups.pizza_type_id>1].order_id.values

	# Create the multi-order dataframe
	moDf = df[df.order_id.isin(multiOrders)].reset_index(drop=True)


	# ### From class notes, best recommendation type is item to item
	# ### In our case, this means pizzas that go with pizzas, not order

	# ### Need co-occurence of pizza type using cosine similarity

	# Simplify data
	simple = moDf[["order_id", "quantity", "pizza_type_id"]]
	copyDf = simple.copy()

	# Set all quantities to 1 because we don't want to recommend the same pizza again
	copyDf['quantity'] = 1

	# Drop duplicates, as it causes an error in the pivot due to duplicate order_ids
	copyDf = copyDf.drop_duplicates().reset_index(drop=True)

	# Pivot the dataframe to have the rows as pizzas and the columns as orders, with a binary value of whether or not a pizza type was ordered
	itemitem = copyDf.pivot(index='pizza_type_id', columns='order_id', values='quantity').fillna(0)


	# ### Given a cart, average cosine sim for each item and display the optimal n (5)

	# Get the names of the pizzas in order
	map_pizza = itemitem.index.to_list()

	# FINAL MODEL - USED LIVE AND INCLUDES ALL GIVEN DATA
	# Initialize and fit NearestNeighbors using cosine metric and brute algorithm
	knn = NearestNeighbors(metric='cosine', algorithm='brute')
	knn.fit(itemitem.values)

	# Calculate and store the distances and indices between all pizza types
	distances, indices = knn.kneighbors(itemitem.values, n_neighbors=len(map_pizza))


	# Store model results and the map to indices
	np.savetxt("distances.txt", distances)
	np.savetxt("indices.txt", indices)
	np.savetxt("map.txt", map_pizza,fmt='%s')





