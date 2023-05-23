import numpy as np

#rasterizing the point cloud date row by row

def rasterize(pcd, X):

    buildings = np.zeros(shape=(1500)).astype(np.float64)
    end_X = X + 2000
    i = 0
    while i < 1500:
        points_in_pixel = []
        for point in pcd:
            if X < point[0] < end_X:
                points_in_pixel.append(point[2])
                if len(points_in_pixel) > 1:
                    sum = 0
                    count = 0
                    for p in points_in_pixel:
                        sum += p
                        count += 1
                    h = (sum / count) / 1000
                    buildings[i] = h
                elif len(points_in_pixel) == 1:
                    h = points_in_pixel[0] / 1000
                    buildings[i] = h
        i = i + 1
        X = X + 2000
        end_X = end_X + 2000

    return buildings

 #Slicing pointcloud in n smaller point clouds, "n" must be a number a square root is able to take out of, i.e. 4, 9, 16, 25

def slicePointcloud(n, pcd):

    Y = 0
    Xmax = 3000000
    Ymax = 3000000

    point_data_og = np.stack([pcd.X, pcd.Y, pcd.Z], axis=0).transpose((1, 0))
    point_data = point_data_og
    rasters = []
    while Y < Ymax:
        Y_end = Y + n
        X = 0
        points_in_area = []
        for point in point_data:
            if X < point[0] < Xmax and Y < point[1] < Y_end:
                points_in_area.append(point)
        raster = rasterize(points_in_area, 0)
        rasters.insert(0, raster)
        Y = Y + n
        print(Y / 2000)

    buildings = np.array([np.array(xi) for xi in rasters])
    print(buildings)
    print(buildings.shape)
    return buildings

"""
def rasterize_pixel(pcd, X, Y):

    #buildings = np.zeros(shape=(1500, 1)).astype(np.float64)

    end_X = X + 2000

    end_Y = Y + 2000
    #print(pcd)
    i = 0
    #print(X, Y)
    h = 0
    points_in_pixel = []
    for point in pcd:
            #print(point[0], point[1], point[2])
        if X < point[0] < end_X and Y < point[1] < end_Y:
            #print(point[2])
            points_in_pixel.append(point[2])

    if len(points_in_pixel) > 1:
        sum = 0
        count = 0
        for p in points_in_pixel:
            sum += p
            count += 1
        h = (sum / count) / 1000
    elif len(points_in_pixel) == 1:
        h = points_in_pixel[0] / 1000

    return h
"""