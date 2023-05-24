
import numpy as np
from osgeo import gdal, ogr
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap



def plotting(viewshed, antennas):
    print("\nStart plotting...")
    
    if type(viewshed) != np.ndarray:
        print("Format of the viewshed must be an np.ndarray!")
        return None
    elif type(antennas) != list:
        print("Format of the antennas must be a list!")
        return None    
    
    
    # split list of antennas
    x=[]
    y=[]
    for antenna in antennas:
        x.append(antenna[1])
        y.append(antenna[0])

    # Plotting
    plt.figure(figsize=(4,3))
    ax = plt.axes()

    ax.scatter(x,y, color='red', marker='x')
    ax.matshow(viewshed, cmap=ListedColormap(['k', 'w']))
    ax.set_yticks([])
    ax.set_xticks([])

    plt.title('Viewshed & Base-stations')
    plt.show()
    
    
    print("Plotting finished! \n")