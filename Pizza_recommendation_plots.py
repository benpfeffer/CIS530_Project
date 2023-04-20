# Pizza_recommendation_plots.py file for Cart-Based Pizza Recommendation System
# Ben Pfeffer, Andrew Anctil, Bradon Wetzel
# CIS 530 - Advanced Data Mining - Professor Thomas Gyeera

# Import libraries
import pandas as pd
from matplotlib.figure import Figure
from sklearn.neighbors import NearestNeighbors
import numpy as np
import matplotlib
from matplotlib.patches import Patch



def plot_recs(cart):
    """
    Function to plot the breakdown of the calculation for the top 5 recommendations based on the current cart.
    Input: cart: list of pizza types
    Ouput: 2 matplotlib figures: horizontal bar charts of the cosine similarities for each item in the cart, and the average
    """

    # Initialize the figures to be returned
    fig = Figure(figsize=[30,10])
    fig2 = Figure(figsize=[30,10])

    # Detect if there are items in the cart
    if(len(cart)>0):
        try:
            # Load the distances and indices from the Nearest Neighbors model from pizza_rec_model.py
            distances = np.loadtxt('distances.txt')
            indices = np.loadtxt('indices.txt').astype(int)

            # Open the map file and extract pizza mapped to indices (needed because not numbers)
            mp = open("map.txt", "r")
            mpd = mp.read()
            map_pizza = mpd.split('\n')
            mp.close()

            # Initialize the plot data list
            plot_data = []
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

                # Add each dataframe of cosine similarities to the items in the cart to the plot data list
                plot_data.append(currDf)

            # Group the output dataframe by the indices(which map to pizza types) and get the mean distance, then sort by distance ascending
            distanceDf = totalDf.groupby("Indices").agg({"Distance":"mean"}).sort_values(by="Distance").reset_index()

            # Plot each dataframe in plot_data and combine them to plot bar chart of recommendation scores and highlight the top n

            # First plot individual plots for each pizza in the cart

            # Get cart pizza indices and remove from indices of plot
            trueInd = [i for i in distanceDf.Indices if map_pizza[i] not in cart]

            # Duplicate and simplify the dataframe
            dist = distanceDf.copy()
            dist.columns = ["Indices", "Dist"]

            # Set matplotlib font
            font = {'size'   : 10}
            matplotlib.rc('font', **font)

            # Set subplot locational parameters for the figure
            fig.subplots_adjust(left=-1,
                                bottom=0.1,
                                right=0.9,
                                top=0.9,
                                wspace=0.4,
                                hspace=0.4)

            # Get the midpoint of the left and right x positions
            mid = (fig.subplotpars.right + fig.subplotpars.left)/2

            # Create subplots
            axs = fig.subplots(1, len(cart))

            # Iterate through plot data
            for i,plot in enumerate(plot_data):
                # Set current axis to plot based on the number of items in the cart
                if(len(cart)>1):
                    ax = axs[i]
                else:
                    ax = axs
                
                # Get sorted values of the plot data
                df = plot.merge(dist).sort_values("Dist")
                
                # Plot non-identical pizza scores (and not in cart)
                df = df[df.Indices.isin(trueInd)].reset_index(drop=True)
                # Use a horizontal bar chart and format properly
                ax.barh(np.arange(len(df.Indices)), 1 - df.Distance, align='center')
                ax.set_yticks(np.arange(len(df.Indices)), labels=[map_pizza[i] for i in df.Indices])
                ax.invert_yaxis() # Flip y labels
                # Set the ylabel for the first plot only
                if(i==0):
                    ax.set_ylabel("Pizza Type")
                ax.set_xlabel("Cosine Similarity")
                ax.set_title(cart[i])
            
            # Use tight layout to allow subplots to show properly in web page
            fig.tight_layout(h_pad=20)


            # Plot combined graph

            # Set matplotlib font
            font = {'size'   : 12}
            matplotlib.rc('font', **font)

            # Get the axis of figure 2
            ax = fig2.gca()

            # Plot non-identical pizza scores (and not in cart)
            df = dist[dist.Indices.isin(trueInd)].reset_index(drop=True)

            # Set the color based on whether or not they are in the top n
            df["Color"] = "LightBlue"
            df.Color.iloc[:n] = "Green"
            # Plot the averaged horizontal bar chart, coloring by the top n, formatting properly
            ax.barh(np.arange(len(df)),1-df.Dist, color=df.Color)
            ax.set_yticks(np.arange(len(df)), labels=[map_pizza[i] for i in df.Indices])
            ax.invert_yaxis() # Flip y labels
            ax.set_ylabel("Pizza Type")
            ax.set_xlabel("Cosine Similarity")
            ax.set_title("Average Cosine Similarity for all Pizzas in Cart")
            # Add a custom legend
            legend_elements = [Patch(facecolor='Green', edgecolor='k',
                                     label='Recommended'),
                               Patch(facecolor='LightBlue', edgecolor='k',
                                     label='Not Recommended')]
            ax.legend(handles=legend_elements, loc='lower right')
        except:
            print('continuing')

    # Return the 2 figures
    return fig, fig2



