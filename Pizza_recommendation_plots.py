

import pandas as pd
from matplotlib.figure import Figure
from sklearn.neighbors import NearestNeighbors
import numpy as np
import matplotlib
from matplotlib.patches import Patch
from matplotlib.lines import Line2D



def plot_recs(cart):

    fig = Figure(figsize=[30,10])
    fig2 = Figure(figsize=[30,10])

    if(len(cart)>0):
        try:
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

            # Plot each distanceDf in plot_data and combine them and plot comment below
            # Plot bar chart of recommendation scores and highlight the top n


            # First plot individual plots for each

            # Get cart pizza indices and remove from indices of plot
            trueInd = [i for i in distanceDf.Indices if map_pizza[i] not in cart]

            dist = distanceDf.copy()
            dist.columns = ["Indices", "Dist"]




            font = {'size'   : 10}
            matplotlib.rc('font', **font)

            fig.subplots_adjust(left=-1,
                                bottom=0.1,
                                right=0.9,
                                top=0.9,
                                wspace=0.4,
                                hspace=0.4)

            # Mid point of left and right x-positions
            mid = (fig.subplotpars.right + fig.subplotpars.left)/2
            # fig.suptitle("Similarity between each pizza in the cart",x=mid, fontsize=40)


            axs = fig.subplots(1, len(cart))
            for i,plot in enumerate(plot_data):
                if(len(cart)>1):
                    ax = axs[i]
                else:
                    ax = axs
                
                # Get sorted values
                df = plot.merge(dist).sort_values("Dist")
                
                # Plot non-identical pizza scores
                df = df[df.Indices.isin(trueInd)].reset_index(drop=True)
                ax.barh(np.arange(len(df.Indices)), 1 - df.Distance, align='center')
                ax.set_yticks(np.arange(len(df.Indices)), labels=[map_pizza[i] for i in df.Indices])
                ax.invert_yaxis() # Flip y labels
                if(i==0):
                    ax.set_ylabel("Pizza Type")
                ax.set_xlabel("Cosine Similarity")
                ax.set_title(cart[i])
            
            fig.tight_layout(h_pad=20)


            # Plot combined graph

            font = {'size'   : 12}
            matplotlib.rc('font', **font)
            ax = fig2.gca()
            df = dist[dist.Indices.isin(trueInd)].reset_index(drop=True)
            df["Color"] = "LightBlue"
            df.Color.iloc[:n] = "Green"
            ax.barh(np.arange(len(df)),1-df.Dist, color=df.Color)
            ax.set_yticks(np.arange(len(df)), labels=[map_pizza[i] for i in df.Indices])
            ax.invert_yaxis() # Flip y labels
            ax.set_ylabel("Pizza Type")
            ax.set_xlabel("Cosine Similarity")
            ax.set_title("Average Cosine Similarity for all Pizzas in Cart")
            legend_elements = [Patch(facecolor='Green', edgecolor='k',
                                     label='Recommended'),
                               Patch(facecolor='LightBlue', edgecolor='k',
                                     label='Not Recommended')]
            ax.legend(handles=legend_elements, loc='lower right')
        except:
            print('continuing')


    return fig, fig2



