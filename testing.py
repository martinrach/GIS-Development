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
antenna_distance = int(50000)



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


####### stuff for iteration #######
max_number_of_stations = 20
antenna_list = []
coverage = 0
iteration_count = 0
coverage_treshold = 98
indices = []


####### start iteration #######
while coverage < coverage_treshold and len(antenna_list) < max_number_of_stations:
    # find highest point (index)
    index = np.unravel_index(np.argmax(possible_antenna, axis=None), 
                             possible_antenna.shape)
        
    # check if new antenna is too close to existing antenna   
    if np.isin(indices, [np.arange(index[0]-25, index[0]+25), np.arange(index[1]-25,index[1]+25)]).any():
        # if too close, mark it as not possible antenna position
        possible_antenna[index[0], index[1]] = 0
        continue

    # position of highest point
    obsX = int(xmin) + int(index[0])
    obsY = int(ymax) - int(index[1])

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
    
    # check if the new viewshed contributes much to the result
    if len(antenna_list) > 1:
        changes = abs(np.count_nonzero(viewshed == 1) - np.count_nonzero(np.dstack([viewshed, new_viewshed]).max(axis=2) == 1))
        if changes < 0.03*np.count_nonzero(viewshed == 0):
            possible_antenna[index[0], index[1]] = 0
            continue

    # add the coordinates of the highest point to list (station locations)
    antenna_list.append([obsX, obsY])
    indices.append([index[0], index[1]])

    # combine viewsheds
    viewshed = np.dstack([viewshed, new_viewshed]).max(axis=2)
    
    # calculate coverage
    coverage = np.count_nonzero(viewshed) / viewshed.size * 100
    print('{:.0f} % of the area is covered by the base stations.'.format(coverage))

    
    # get new possible antenna positions
    possible_antenna = ma.array(possible_antenna, mask=viewshed)
    #print(possible_antenna)

    # plot results (viewshed, mask and possible antenna position)
    plt.matshow(viewshed)
    #plt.matshow(mask)
    plt.matshow(possible_antenna)

    iteration_count += 1

    #print(iteration_count)

















######## TESTING ########


#a = (np.arange(index[0]-50,index[0]+50), np.arange(index[1]-50,index[1]+50))
#print(a)


#mask[a] = 0


#print(possible_antenna[index[0], index[1]])
#print(mask[index[0], index[1]])














print('code completed')























# width_small, height_small = new_viewshed_small.shape

# diff_width = abs(width-width_small)
# diff_height = abs(height-height_small)

#new_viewshed = np.pad(new_viewshed_small, (()))


# print(new_viewshed.size)
# print(viewshed.size)