# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 14:03:33 2023

@author: Hilla
"""

from osgeo import gdal, ogr

gdal.UseExceptions()

dtm = gdal.Open('L3432D.tif', gdal.GA_ReadOnly)

print("Driver: {}/{}".format(dtm.GetDriver().ShortName,
                            dtm.GetDriver().LongName))
print("Size is {} x {} x {}".format(dtm.RasterXSize,
                                    dtm.RasterYSize,
                                    dtm.RasterCount))

band = dtm.GetRasterBand(1)
print(band)



dataset = gdal.ViewshedGenerate(band, 
                                driverName='GeoTIFF', 
                                targetRasterName='viewshed_with_script.tif', 
                                creationOptions='COMPRESS=NONE', 
                                observerX='266000', 
                                observerY='6738000', 
                                observerHeight='2', 
                                targetHeight='0', 
                                maxDistance='500', 
                                visibleVal='1', 
                                invisibleVal='0', 
                                outOfRangeVal='0', 
                                noDataVal='2', 
                                dfCurvCoeff='1', 
                                mode='NORMAL')



print('code completed')