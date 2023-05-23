
import os
import numpy as np
from matplotlib import pyplot as plt
from osgeo import gdal

gdal.UseExceptions()




def base_station_placement(output_path, input_path, no_stations=None, antenna_height=100, max_stationss=10, coverage_treshold = 95, station_buffer = 500):
    
    
    ###############################################################
    ####### preparation for actual method #######
    ###############################################################
    # read input
    height_model = gdal.Open(input_path, gdal.GA_ReadOnly)
    
    
    # remove output file if it already exists
    if os.path.exists(output_path):
        os.remove(output_path)
        
    
    ####### size of height_model #######
    xmin, xpixel, _, ymax, _, ypixel = height_model.GetGeoTransform()
    
    
    ####### define some of the outputs #######
    viewshed = np.zeros((height_model.RasterXSize, height_model.RasterYSize), dtype=np.int8)
    stations_list = []
    coverage_list = []
    indices = []
    coverage = 0
    iteration_count = 0
    
    
    ####### create band #######
    band = height_model.GetRasterBand(1)
    print("Band successfully imported!")


    # turn band into array (possible antenna stations)
    possible_antenna = band.ReadAsArray()
    
    
    # areas where no stations can be
    if no_stations == None:
        no_stations = np.zeros((height_model.RasterXSize, height_model.RasterYSize), dtype=np.int8)
    else:
        if no_stations.shape != possible_antenna.shape:
            print("File for no stations not compatible with the height_model (dimensions)")
            return None
    
    
    # filter not possible positions
    possible_antenna = np.where(no_stations==1, 0, possible_antenna)
    


    ###############################################################
    ####### actual method #######
    ###############################################################
    while coverage < coverage_treshold and len(stations_list) < max_stationss:
        # function for this loop
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
                                            targetRasterName=output_path, 
                                            creationOptions=['COMPRESS=NONE'], 
                                            observerX=obsX, 
                                            observerY=obsY, 
                                            observerHeight=antenna_height, 
                                            targetHeight=0, 
                                            maxDistance=int(50000000), 
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
                new_no_stations = 1*create_circular_mask(possible_antenna.shape[0], possible_antenna.shape[1], center=(stationY, stationX), radius=station_buffer).T 
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
                stations_list.append([obsX, obsY])
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


    return stations_list, coverage_list, indices, coverage, iteration_count, viewshed










