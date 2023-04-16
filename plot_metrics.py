import matplotlib
from matplotlib.figure import Figure
import pandas as pd

def plot_metrics():
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

        ax.plot(df[metric], linewidth=7.0)
        if(i==0):
            ax.set_ylabel("Score")
        ax.set_xlabel(metric)
        ax.axvline(5, linestyle="--")

    fig.tight_layout()

    return fig