#rasterizing classified_points -pointcloud and combining it with elevation model
import numpy as np
import rasterio
import laspy
from rasterio.transform import from_origin
from matplotlib import pyplot
from skimage import morphology
from rasterio.windows import Window
import pyproj
import SlicePointcloud
import WaterAreas

# Rivi = int(index / 30))
#print(int(1 / 30))

arr = np.zeros(shape=(1500,1500)).astype(np.float64)
#print(arr.data)

sign = "L4131H"
dem = sign + ".tif"
with rasterio.open('Elevation model/'+ dem) as src:

    array = src.read(1)
    print(src.transform[2])
    print(src.transform[5])
    #pyplot.imshow(array, cmap='pink')
    pyplot.show()
    # The size in pixels of your desired window
    xsize, ysize = 1500, 1500

    # Generate a random window origin (upper left) that ensures the window
    # doesn't go outside the image. i.e. origin can only be between
    # 0 and image width or height less the window width or height
    xmin1, xmax1 = 0, xsize
    ymin1, ymax1 = 0, ysize
    print(xmin1, xmax1, ymin1, ymax1, "image position")
    # Create a Window and calculate the transform from the source dataset
    window1 = Window(xmin1, ymin1, xsize, ysize)
    transform = src.window_transform(window1)

    # Create a new cropped raster to write to
    profile = src.profile
    profile.update({
        'height': xsize,
        'width': ysize,
        'transform': transform})

    with rasterio.open('Elevation model/' + dem + 'output_2.tif', 'w', **profile) as dst1:
        # Read the data from the window and write it to the output raster
        dst1.write(src.read(window=window1))

    # Generate a random window origin (upper left) that ensures the window
    # doesn't go outside the image. i.e. origin can only be between
    # 0 and image width or height less the window width or height
    xmin2, xmax2 = 1500, xsize + 1500
    ymin2, ymax2 = 0, ysize
    print(xmin1, xmax2, ymin2, ymax2, "image position")
    # Create a Window and calculate the transform from the source dataset
    window2 = Window(xmin2, ymin2, xsize, ysize)
    transform = src.window_transform(window2)

    # Create a new cropped raster to write to
    profile = src.profile
    profile.update({
        'height': xsize,
        'width': ysize,
        'transform': transform})

    with rasterio.open('Elevation model/' + dem + 'output_4.tif', 'w', **profile) as dst2:
        # Read the data from the window and write it to the output raster
        dst2.write(src.read(window=window2))

    # Generate a random window origin (upper left) that ensures the window
    # doesn't go outside the image. i.e. origin can only be between
    # 0 and image width or height less the window width or height
    xmin3, xmax3 = 0, xsize
    ymin3, ymax3 = 1500, ysize + 1500
    print(xmin3, xmax3, ymin3, ymax3, "image position")
    # Create a Window and calculate the transform from the source dataset
    window3 = Window(xmin3, ymin3, xsize, ysize)
    transform = src.window_transform(window3)

    # Create a new cropped raster to write to
    profile = src.profile
    profile.update({
        'height': xsize,
        'width': ysize,
        'transform': transform})

    with rasterio.open('Elevation model/' + dem +'output_1.tif', 'w', **profile) as dst3:
        # Read the data from the window and write it to the output raster
        dst3.write(src.read(window=window3))


    # Generate a random window origin (upper left) that ensures the window
    # doesn't go outside the image. i.e. origin can only be between
    # 0 and image width or height less the window width or height
    xmin4, xmax4 = 1500, xsize + 1500
    ymin4, ymax4 = 1500, ysize + 1500
    print(xmin4, xmax4, ymin4, ymax4, "image position")
    # Create a Window and calculate the transform from the source dataset
    window4 = Window(xmin4, ymin4, xsize, ysize)
    transform = src.window_transform(window1)

    # Create a new cropped raster to write to
    profile = src.profile
    profile.update({
        'height': xsize,
        'width': ysize,
        'transform': transform})

    with rasterio.open('Elevation model/' + dem + 'output_3.tif', 'w', **profile) as dst4:
        # Read the data from the window and write it to the output raster
        dst4.write(src.read(window=window4))


with rasterio.open('Elevation model/' + dem + 'output_1.tif') as cropped1:
    array2 = cropped1.read(1)
    pyplot.imshow(array2, cmap='pink')
    pyplot.show()

with rasterio.open('Elevation model/' + dem + 'output_2.tif') as cropped2:
    array3 = cropped2.read(1)
    pyplot.imshow(array3, cmap='pink')
    pyplot.show()

with rasterio.open('Elevation model/' + dem + 'output_3.tif') as cropped3:
    array4 = cropped3.read(1)
    pyplot.imshow(array4, cmap='pink')
    pyplot.show()

with rasterio.open('Elevation model/' + dem + 'output_4.tif') as cropped4:
    array5 = cropped4.read(1)
    pyplot.imshow(array5, cmap='pink')
    pyplot.show()


count = 2 # number of existing height models with same sign like L4131E
while count < 3:
    count = count + 1
    print(count)
    pcd = sign + str(count) + '.laz_classified.las'
    Dem = 'Elevation model/' + dem + 'output_' + str(count) + '.tif'
    print(Dem)

    size = 10000 # the size of each point cloud side

    with rasterio.open(Dem) as src:
        #print(src.crs)
        input_tif_h = src.read(1)
        #print(input_tif_h[1499])
        #print(src.transform)

    #X = src.transform[2]
    #Y = src.transform[5]
    X = 377000
    Y = 6675000
    height_raster = np.zeros(shape=(1500, 1500)).astype(np.float64)
    zero_raster = np.zeros(shape=(1500, 1500)).astype(np.float64)
    pyplot.imshow(input_tif_h, cmap='Reds')
    pyplot.show()
    """
    row_b = 0
    row_d = 1499
    while row_d >= 0:
        row_bldg = zero_raster[row_b]
        row_dem = input_tif_h[row_d]
        height_raster[row_d] = row_dem + row_bldg
        row_d = row_d - 1
        row_b = row_b + 1
    print(height_raster)
    """

    with laspy.open("C:/Users/Janne Niskanen/Documents/opiskelu/GIS-project/Input data/" + pcd) as temp:
        print(temp)
        input_las = temp.read()
        print(input_las)
        print('Points from data:', len(input_las.points))
        header = input_las.header
        header.add_crs(crs=pyproj.CRS(proj='utm', zone=35, ellps='WGS84') ,keep_compatibility=True)
        #print(input_las.X)
        buildings = SlicePointcloud.slicePointcloud(2000, input_las)

    pyplot.imshow(buildings, cmap='Paired')
    pyplot.show()

    # performing opening and closing to the raster to fill the gaps and remove outliers
    opened_raster = morphology.area_opening(buildings, area_threshold=9, connectivity=2)
    result_raster = morphology.dilation(opened_raster)

    #with rasterio.open('test_sea_raster.tiff') as src:

    pyplot.imshow(result_raster, cmap='pink')
    pyplot.show()



    WaterAreas.slice_water_shp(X, Y, Dem)
    print(Dem)
    with rasterio.open(Dem + 'test_sea_raster.tif') as src:
        sea_raster = src.read(1)
        pyplot.imshow(sea_raster)
        pyplot.show()
    with rasterio.open(Dem + 'test_lake_raster.tif') as src:
        lake_raster = src.read(1)
        pyplot.imshow(lake_raster)
        pyplot.show()
    # Combining elevation model and building height model by selecting the highest value of each pixel between them
    i = 0
    while i < 1500:
        row_dem = input_tif_h[i]
        row_buildings = result_raster[i]
        row_sea = sea_raster[i]
        row_lake = lake_raster[i]
        j = 0
        while j < 1500:
            h_dem = row_dem[j]
            h_buildings = row_buildings[j]
            h_sea = row_sea[j]
            h_lake = row_lake[j]
            if h_dem > h_buildings:
                row_buildings[j] = h_dem
            if h_sea > 100000 or h_lake > 100000:
                row_buildings[j] = -1
            j = j + 1
        i = i + 1

    pyplot.imshow(result_raster, cmap='jet')
    pyplot.show()
    transform = from_origin(src.transform[2], src.transform[5], 2, 2)
    new_dataset = rasterio.open(sign + str(count) + '_height_raster.tif', 'w', driver='GTiff',
                                height = result_raster.shape[0], width = height_raster.shape[1],
                                count=1, dtype=str(result_raster.dtype),
                                transform=transform)

    new_dataset.write(result_raster, 1)
    new_dataset.close()
