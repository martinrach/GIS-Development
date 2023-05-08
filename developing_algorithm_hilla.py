# -*- coding: utf-8 -*-
"""
Created on Sun May  7 10:48:26 2023

@author: Hilla
"""


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
import fiona
from fiona.crs import CRS

gdal.UseExceptions()



####### folder structure #######
# input
folder = '/Users/Hilla/Documents/Aalto-yliopisto/GIS Development/'
file_name = 'L3432D_clipped_5x5.tif'
input_file = folder+file_name

# output
output_file = 'viewshed_result.tif'
output_file = folder+output_file

# remove output file if it already exists
if os.path.exists(output_file):
    os.remove(output_file)


####### define parameters #######
# antenna
antenna_height = int(50)
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



####### ITERATION #######

max_number_of_stations = 2
antenna_list = []
coverage = 0

# turn band into array (possible antenna stations)
possible_antenna = band.ReadAsArray()
print(possible_antenna)

print('{:.0f} % of the area is covered by the base stations.'.format(coverage))
iteration_count = 0
while coverage < 98 and len(antenna_list) <= max_number_of_stations:

    # find highest point (index)
    index = np.unravel_index(np.argmax(possible_antenna, axis=None), 
                             possible_antenna.shape)

    # position of highest point
    obsX = int(xmin) + int(index[0])
    obsY = int(ymax) - int(index[1])
    
    # add the coordinates of the highest point to list (station locations)
    antenna_list.append((obsX, obsY, index))

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

    # combine viewsheds
    viewshed = np.dstack([viewshed, new_viewshed]).max(axis=2)
    #print(viewshed)
    
    # calculate coverage
    non_zeros = np.count_nonzero(viewshed)
    zeros = viewshed.size - non_zeros
    coverage = non_zeros / viewshed.size * 100
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


print(antenna_list)
print(viewshed)

'''
# create output raster file from the final viewshed
fileformat = "GTiff"
driver = gdal.GetDriverByName(fileformat)
metadata = driver.GetMetadata()

dst_filename = 'final_viewshed.tif'

dst_ds = driver.CreateCopy(dst_filename, dtm, strict=0)

dst_ds.GetRasterBand(1).WriteArray(viewshed)

dst_ds = None
src_ds = None

# create output vector file from the antenna placement
base_stations = []
for station in antenna_list:
    print(station)
    base_st = {'geometry': {'type': 'Point', 'coordinates': station}, 
           'properties': dict([('name', 'base_station')])}
    base_stations.append(base_st)
schema = {'geometry': 'Point', 'properties': dict([('name', 'str')])}

with fiona.open('base_stations.gpkg', 'w', driver='GPKG', crs=CRS.from_epsg(3067), schema=schema) as file:
    file.writerecords(base_stations)
    
'''