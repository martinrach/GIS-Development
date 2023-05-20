
import numpy as np
from osgeo import gdal, ogr
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap



def plotting(dtm, viewshed, antennas):
    print("\nStart plotting...")
    
    # check for correct input formats
    if type(dtm) != gdal.Dataset:
        print("Format of the DTM must be a gdal.Dataset!")
        return None
    elif type(viewshed) != np.ndarray:
        print("Format of the viewshed must be an np.ndarray!")
        return None
    elif type(antennas) != list:
        print("Format of the antennas must be a list!")
        return None    
    

    # get dimensions of dtm
    xmin, xpixel, _, ymax, _, ypixel = dtm.GetGeoTransform()
    
    # split list of antennas
    x=[]
    y=[]
    for antenna in antennas:
        x.append(antenna[0]-int(xmin))
        y.append(abs(antenna[1]-int(ymax)))

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