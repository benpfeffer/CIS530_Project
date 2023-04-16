import matplotlib
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import pandas as pd

def plot_metrics():
    df = pd.read_csv('metrics.csv').drop("Unnamed: 0", axis=1)
    
    font = {'size'   : 22}
    matplotlib.rc('font', **font)

    fig = plt.figure(figsize=[35,12])
    plt.subplots_adjust(left=-1,
                        bottom=0.1,
                        right=0.9,
                        top=0.9,
                        wspace=0.4,
                        hspace=0.4)

    # Mid point of left and right x-positions
    mid = (fig.subplotpars.right + fig.subplotpars.left)/2

    # reading the image
    image = plt.imread('pizza.png')

    # OffsetBox
    image_box = OffsetImage(image, zoom=0.05)

    for i,metric in enumerate(df.columns[:-1]):
        ax = plt.subplot(1, len(df), i + 1)    
        for x0, y0 in zip(df.index, df[metric]):
            ab = AnnotationBbox(image_box, (x0, y0), frameon=False)
            ax.add_artist(ab)

        ax.plot(df[metric], linewidth=7.0)
        if(i==0):
            ax.set_ylabel("Score")
        ax.set_xlabel(metric)
        ax.axvline(5, linestyle="--")
    return fig