# Pizza_recommendation_plots.py file for Cart-Based Pizza Recommendation System
# Ben Pfeffer, Andrew Anctil, Bradon Wetzel
# CIS 530 - Advanced Data Mining - Professor Thomas Gyeera

# Import libraries
import matplotlib
from matplotlib.figure import Figure
import pandas as pd
import numpy as np

def plot_metrics():
    """
    Function to plot the metrics of the validation and test set
    Output: matplotlib figure of the metrics
    """

    # Read the metrics from csv files obtained through Pizza_recommendation_simple.ipynb
    val = pd.read_csv('valMetrics.csv').drop("Unnamed: 0", axis=1)
    df = pd.read_csv('metrics.csv').drop("Unnamed: 0", axis=1)
    
    # Set matplotlib font
    font = {'size'   : 22}
    matplotlib.rc('font', **font)

    # Create and initialize a figure, adjusting the subplot location
    fig = Figure(figsize=[35,12])
    fig.subplots_adjust(left=-1,
                        bottom=0.1,
                        right=0.9,
                        top=0.9,
                        wspace=0.4,
                        hspace=0.4)

    # Get the midpoint of the left and right x positions
    mid = (fig.subplotpars.right + fig.subplotpars.left)/2

    # Create subplots for every column besides the number of recommendations
    axs = fig.subplots(1,len(df.columns[:-1]))

    # Iterate through these columns
    for i,metric in enumerate(df.columns[:-1]):
        # Set the current axis
        ax = axs[i]

        # Plot the validation metric and test metric as a line plot
        l1, = ax.plot(val[metric], linewidth=7.0)
        l2, = ax.plot(df[metric], linewidth=7.0)
        # Format the plot
        # Set y axis label for the first plot
        if(i==0):
            ax.set_ylabel("Score")
        ax.set_xlabel("Number of Recs")
        # Set the x axis ticks to the number of recommendations column
        ax.set_xticks(np.arange(len(df)),df["NumRec"])
        # Set the title as the metric
        ax.set_title(metric)
        # Create a vertical line at x=4 (recs=5) to view the optimal recommendation metrics
        ax.axvline(4, linestyle="--")

    # Create a legend
    fig.legend((l1, l2), ("Val", "Test"), loc='upper right')

    # Use tight layout to perfect webpage view
    fig.tight_layout()

    # Return the figure of the metrics
    return fig