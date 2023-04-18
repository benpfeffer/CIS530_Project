import matplotlib
from matplotlib.figure import Figure
import pandas as pd
import numpy as np

def plot_metrics():
    val = pd.read_csv('valMetrics.csv').drop("Unnamed: 0", axis=1)
    df = pd.read_csv('metrics.csv').drop("Unnamed: 0", axis=1)
    
    font = {'size'   : 22}
    matplotlib.rc('font', **font)

    fig = Figure(figsize=[35,12])
    fig.subplots_adjust(left=-1,
                        bottom=0.1,
                        right=0.9,
                        top=0.9,
                        wspace=0.4,
                        hspace=0.4)

    # Mid point of left and right x-positions
    mid = (fig.subplotpars.right + fig.subplotpars.left)/2


    axs = fig.subplots(1,len(df.columns[:-1]))
    for i,metric in enumerate(df.columns[:-1]):
        ax = axs[i]

        l1, = ax.plot(val[metric], linewidth=7.0)
        l2, = ax.plot(df[metric], linewidth=7.0)
        if(i==0):
            ax.set_ylabel("Score")
        ax.set_xlabel("Number of Recs")
        ax.set_xticks(np.arange(len(df)),df["NumRec"])
        ax.set_title(metric)
        ax.axvline(4, linestyle="--")

    fig.legend((l1, l2), ("Val", "Test"), loc='upper right')
    fig.tight_layout()

    return fig