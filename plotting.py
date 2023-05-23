
import numpy as np
from osgeo import gdal, ogr
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap



def plotting(input_path, viewshed, antennas):
    print("\nStart plotting...")
    
    # read input
    height_model = gdal.Open(input_path, gdal.GA_ReadOnly)
    
    # check for correct input formats
    if type(height_model) != gdal.Dataset:
        print("Format of the height_model must be a gdal.Dataset!")
        return None
    elif type(viewshed) != np.ndarray:
        print("Format of the viewshed must be an np.ndarray!")
        return None
    elif type(antennas) != list:
        print("Format of the antennas must be a list!")
        return None    
    

    # get dimensions of height_model
    xmin, xpixel, _, ymax, _, ypixel = height_model.GetGeoTransform()
    
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