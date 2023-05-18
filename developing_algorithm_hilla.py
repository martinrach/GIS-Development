# -*- coding: utf-8 -*-
"""
Created on Tue May  9 14:26:00 2023

@author: Hilla
"""


####### modules and stuff #######
import os
import numpy as np
import numpy.ma as ma
from matplotlib import pyplot as plt
from osgeo import gdal, ogr
import fiona
#from fiona.crs import CRS
gdal.UseExceptions()



####### folder structure #######
# input
folder = '/Users/Hilla/Documents/Aalto-yliopisto/GIS Development/'
file_name = 'L3432D.tif'
input_file = file_name

# output
output_file = 'viewshed_result1.tif'
output_file = output_file

# output
output_viewshed = 'viewshed.tif'
output_viewshed = output_file

# remove output file if it already exists
if os.path.exists(output_file):
    os.remove(output_file)


####### define parameters #######
# antenna
antenna_height = int(20)
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
max_number_of_stations = 5
antenna_list = []
coverage = 0
iteration_count = 0
coverage_treshold = 88
indices = []
passed = True
tries = []


####### start iteration #######
while coverage < coverage_treshold and len(antenna_list) < max_number_of_stations:
    # find highest point (index)
    index = np.unravel_index(np.argmax(possible_antenna, axis=None), 
                             possible_antenna.shape)
    '''
    # check if new antenna is too close to existing antenna   
    if np.isin(indices, [np.arange(index[0]-25, index[0]+25), np.arange(index[1]-25,index[1]+25)]).any():
        # if too close, mark it as not possible antenna position
        possible_antenna[index[0], index[1]] = 0
        continue
    '''
    # position of highest point
    obsX = int(xmin) + int(index[1])*2+1
    obsY = int(ymax) - int(index[0])*2-1
    #print(obsX, obsY)
    #print(index[1], index[0], possible_antenna[index[1], index[0]])
    #print(possible_antenna)
    
    if possible_antenna[index[0], index[1]] == 0.0:
        break
    '''
    # check if the highest point is too close to the latest antenna
    if antenna_list != []:
        dif_x = abs(obsX - antenna_list[-1][0])
        dif_y = abs(obsY - antenna_list[-1][1])
        
        #print('difs', dif_x, dif_y)
        if dif_x < 500 or dif_y < 500:
            possible_antenna[index[0], index[1]] = 0
            coverage = np.count_nonzero(viewshed) / viewshed.size * 100
            #print(coverage)
            #print(viewshed)
            continue
    '''
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
    '''
    # check if the new viewshed contributes much to the result
    if len(antenna_list) > 1:
        changes = abs(np.count_nonzero(viewshed == 1) - np.count_nonzero(np.dstack([viewshed, new_viewshed]).max(axis=2) == 1))
        print(changes)
        print('evaluation', changes/viewshed.size*100)
        if changes/viewshed.size*100 < 1:
            passed = False
            possible_antenna[index[0], index[1]] = 0
            print(possible_antenna[index[0], index[1]])
            print('False')
            print(possible_antenna)
            tries.append([obsX, obsY])
            continue
        
        else:
            passed = True
        #if changes < 0.03*np.count_nonzero(viewshed == 0):
            #possible_antenna[index[1], index[0]] = 0
            #continue
    '''
    
    # check if the new viewshed contributes much to the result
    if len(antenna_list) >= 1:
        changes = abs(np.count_nonzero(viewshed == 1) - np.count_nonzero(np.dstack([viewshed, new_viewshed]).max(axis=2) == 1))
        if changes < 0.03*np.count_nonzero(viewshed == 0):
            possible_antenna[index[0], index[1]] = 0
            continue
    
    # add the coordinates of the highest point to list (station locations)
    #if possible_antenna[index[1], index[0]] != 0:
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
    #plt.matshow(possible_antenna)

    iteration_count += 1

    #print(iteration_count)


# remove output file if it already exists
if os.path.exists(output_viewshed):
    os.remove(output_viewshed)

# create a raster file for the final viewshed
driver = gdal.GetDriverByName("GTiff")
out_ds = driver.Create('viewshed.tif', viewshed.shape[1], viewshed.shape[0], 1, gdal.GDT_Float32)
out_ds.SetProjection(dtm.GetProjection())
out_ds.SetGeoTransform(dtm.GetGeoTransform())
band = out_ds.GetRasterBand(1)
band.WriteArray(viewshed)
band.FlushCache()
band.ComputeStatistics(False)
del out_ds
'''
# create a vector file with antenna locations  
b_stations = []
for location in antenna_list:
    station = {'geometry': {
        'type': 'Point', 'coordinates': location},
        'properties': dict([('name', 'base_station')])}
    b_stations.append(station)
    
schema = {'geometry': 'Point',
          'properties': dict([('name', 'str')])}

with fiona.open('base_station.gpkg', 'w', driver='GPKG', crs=CRS.from_epsg('3067'), schema=schema) as file:
    file.writerecords(b_stations)

tries1 = []
for location in tries:
    station = {'geometry': {
        'type': 'Point', 'coordinates': location},
        'properties': dict([('name', 'base_station')])}
    tries1.append(station)
    
schema = {'geometry': 'Point',
          'properties': dict([('name', 'str')])}

with fiona.open('base_station_tries.gpkg', 'w', driver='GPKG', crs=CRS.from_epsg('3067'), schema=schema) as file:
    file.writerecords(tries1)
'''









######## TESTING ########


#a = (np.arange(index[0]-50,index[0]+50), np.arange(index[1]-50,index[1]+50))
#print(a)


#mask[a] = 0


#print(possible_antenna[index[0], index[1]])
#print(mask[index[0], index[1]])












print(antenna_list)

print('code completed')























# width_small, height_small = new_viewshed_small.shape

# diff_width = abs(width-width_small)
# diff_height = abs(height-height_small)

#new_viewshed = np.pad(new_viewshed_small, (()))


# print(new_viewshed.size)
# print(viewshed.size)