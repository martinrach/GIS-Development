# -*- coding: utf-8 -*-
"""
Created on Sat May  6 10:29:16 2023

@author: rachb
"""
####### modules and stuff #######
import os
import numpy as np
import numpy.ma as ma
from matplotlib import pyplot as plt
from osgeo import gdal, ogr
from PIL import Image 
from matplotlib.colors import ListedColormap

gdal.UseExceptions()



####### folder structure #######
# input
folder = '/Users/rachb/Desktop/GIS/'
file_name = 'L4131H.tif'
input_file = folder+file_name

# output
output_file = 'viewshed_result.tif'
output_file = folder+output_file

# remove output file if it already exists
if os.path.exists(output_file):
    os.remove(output_file)


####### define parameters #######
# antenna
antenna_height = int(100)
antenna_distance = int(50000000)



####### load band #######
dtm = gdal.Open(input_file, gdal.GA_ReadOnly)
print("Driver: {}/{}".format(dtm.GetDriver().ShortName,
                             dtm.GetDriver().LongName))
print("Size is {} x {} x {}".format(dtm.RasterXSize,
                                    dtm.RasterYSize,
                                    dtm.RasterCount))



####### size of dtm #######
xmin, xpixel, _, ymax, _, ypixel = dtm.GetGeoTransform()


####### viewshed matrix #######
width, height = dtm.RasterXSize, dtm.RasterYSize
viewshed = np.zeros((width, height), dtype=np.int8)


####### create band #######
band = dtm.GetRasterBand(1)
print("Band successfully imported!")








###############################################################
###############################################################
####### start method #######
###############################################################
###############################################################
# turn band into array (possible antenna stations)
possible_antenna = band.ReadAsArray()

# areas where no stations can be
no_stations = np.zeros((width, height), dtype=np.int8)

# filter not possible positions
possible_antenna = np.where(no_stations==1, 0, possible_antenna)


####### stuff for iteration #######
max_number_of_stations = 10
antenna_list = []
coverage_list = []
coverage = 0
iteration_count = 0
coverage_treshold = 95
indices = []


####### start iteration #######
while coverage < coverage_treshold and len(antenna_list) < max_number_of_stations:
    # function
    def create_circular_mask(h, w, center=None, radius=None):

        if center is None: # use the middle of the image
            center = (int(w/2), int(h/2))
        if radius is None: # use the smallest distance between the center and image walls
            radius = min(center[0], center[1], w-center[0], h-center[1])
    
        Y, X = np.ogrid[:h, :w]
        dist_from_center = np.sqrt((X - center[0])**2 + (Y-center[1])**2)
    
        mask = dist_from_center <= radius
        return mask

    
    
    
    
    # find highest point (new station)
    station = np.unravel_index(np.argmax(possible_antenna, axis=None), possible_antenna.shape, order='C') 
    stationX = station[1]
    stationY = station[0]
    
    
    
    
    
    
    # case for no valid position
    if no_stations[stationY, stationX] == 1:
        possible_antenna[stationY, stationX] = 0
        #print("Station position not possible:", (stationY, stationX))
        continue
    
    
    # case for valid positions
    elif no_stations[stationY, stationX] == 0:
        # position of highest point
        obsX = int(xmin) + int(stationX)
        obsY = int(ymax) - int(stationY)  
    
        # calculate viewshed
        dataset = gdal.ViewshedGenerate(srcBand = band, 
                                        driverName='GTiff', 
                                        targetRasterName=output_file, 
                                        creationOptions=['COMPRESS=NONE'], 
                                        observerX=obsX, 
                                        observerY=obsY, 
                                        observerHeight=antenna_height, 
                                        targetHeight=0, 
                                        maxDistance=antenna_distance, 
                                        visibleVal=1, 
                                        invisibleVal=0, 
                                        outOfRangeVal=0, 
                                        noDataVal=2, 
                                        dfCurvCoeff=1 - 1/7, 
                                        mode=1)

        # turn viewshed into array and delete it
        new_viewshed = dataset.ReadAsArray()
        del dataset   
        
        
        
        
        
        # evaluate impact of new viewshed
        changes = np.count_nonzero(np.abs(new_viewshed-viewshed))
        max_change = np.count_nonzero(viewshed == 0)
        
        # Impact of new viewshed is very low
        if changes < 0.05*max_change:
            print("Too little impact: ", (stationY, stationX))
            possible_antenna[stationY, stationX] = 0
            continue




        # Impact of viewshed is high
        else: 
            # combine viewshed
            viewshed = np.dstack([viewshed, new_viewshed]).max(axis=2)
            viewshed[stationY, stationX] = 1
        
            # no stations around the old station
            new_no_stations = 1*create_circular_mask(possible_antenna.shape[0], possible_antenna.shape[1], center=(stationY, stationX), radius=500).T 
            new_no_stations = np.where(new_no_stations == 1, 1, no_stations)   #new_no_station = ...
                        

            #no_stations = np.dstack([no_stations, new_no_stations]).max(axis=2)
            np.maximum(no_stations, new_no_stations, out=no_stations)

            
            
            # filter not possible positions
            possible_antenna = np.where(no_stations==1, 0, possible_antenna)
            
            # no stations at the same place
            possible_antenna[stationY, stationX] = 0
            
            # calculate coverage
            coverage = np.count_nonzero(viewshed) / viewshed.size * 100
            
            # append data to the lists
            antenna_list.append([obsX, obsY])
            indices.append([stationY, stationX])
            coverage_list.append(coverage)
    
            # some output
            print('{:.0f} % of the area is covered by the base stations.'.format(coverage))
    
            # some plotting
            #plt.matshow(viewshed)
            plt.matshow(no_stations)
            #plt.matshow(possible_antenna)



    
    iteration_count += 1
    
    # see every 10th iteration
    if iteration_count%10 == 0:
        print("Number of Iteration: ", iteration_count)        
        
    if np.count_nonzero(possible_antenna) == 0:
        print("No more possible station positions!")        
        break


    













"""
    # check if new antenna is too close to existing antenna   
    if np.isin(indices, [np.arange(index[0]-25, index[0]+25), np.arange(index[1]-25,index[1]+25)]).any():
        # if too close, mark it as not possible antenna position
        possible_antenna[index[0], index[1]] = 0
        continue
    
    
    
        #before = np.count_nonzero(viewshed == 1)
        #after = np.count_nonzero(np.dstack([viewshed, new_viewshed]).max(axis=2) == 1)
        #changes = after-before
"""






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




def goodness(viewshed, antennas):
    # check for correct input formats
    if type(viewshed) != np.ndarray:
        print("Format of the viewshed must be an np.ndarray!")
        return None
    elif type(antennas) != list:
        print("Format of the antennas must be a list!")
        return None    
    
    # calculate coverage of the viewshed in [%]
    coverage = np.count_nonzero(viewshed) / viewshed.size * 100
    
    # avergae coverage per antenna
    avg_coverage = coverage / len(antennas)
    
    # print result
    print('{:.0f} % of the area is covered by the base stations.'.format(coverage))
    print('Average coverage per base-station: {:.2f}%'.format(avg_coverage))





plotting(dtm, viewshed, antenna_list)
goodness(viewshed, antenna_list)



