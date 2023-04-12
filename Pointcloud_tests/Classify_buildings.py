import numpy as np
from math import sqrt
import open3d as o3d
import Visualize_data


# Dividing data to smaller sets to make calculatios faster

def Classify(data, n):
    if len(data) < 400:
        geom = o3d.geometry.PointCloud()
        geom.points = o3d.utility.Vector3dVector(data)
        list_of_points = select_building_points(geom, n)
        return list_of_points

    else:
        # print(data[199])
        c = int(len(data) / 2)
        # print(c)
        data1 = data[:c]
        data2 = data[c:]
        d1 = Classify(data1, n)
        d2 = Classify(data2, n)
        return d1 + d2

# Calculates n closest points of the seed point form the data

def closest_n_points(seed, data, n):
    closest_points = []
    X_0 = int(seed[0])
    Y_0 = int(seed[1])
    Z_0 = int(seed[2])
    i = 0

    #Going through all points and finding points that are closer than 4 meters from the point
    while i < len(data.points):
        point = data.points[i]
        X = int(point[0])
        Y = int(point[1])
        Z = int(point[2])

        #Euclidean distance between two points in cm
        eucl_dist = sqrt((abs(X - X_0))**2 + (abs(Y - Y_0))**2 + (abs(Z - Z_0))**2)
        point_to_add = (data.points[i], eucl_dist)
        if 5 < eucl_dist < 400:
            if len(closest_points) == 0:
                closest_points.append(point_to_add)
            else:
                j = 0
                while j < len(closest_points):
                    d = closest_points[j][1]
                    if eucl_dist < d:
                        closest_points.insert(j,point_to_add)
                        if len(closest_points) > n:
                            closest_points.pop(n - 1)
                        break
                    j += 1
        i += 1

    return closest_points

# Function that goes through all points in one of the divided data sets
# Input:
#   pcl: the point cloud
#   n: the number of close ponts that are used for classification
# Returns a list of points that have enough close points to be recognised as buildings
def check_coplanarity(p1, points):

    p2 = points[0][0]
    p3 = points[1][0]
    p4 = points[2][0]
    #print(p1, p2, p3, p4)
    c = (np.dot((np.cross((p2 - p1), (p4-p1))), (p3 - p1)))
    #print(c)
    if abs(c) < 100000:
        #print(c)
        return True
    else:
        return False

def select_building_points(pcl, n):

    i = 0
    closest_points_list =[]
    while i < len(pcl.points):
        seed = pcl.points[i]
        c_points = closest_n_points(seed, pcl, n)
        if len(c_points) > n - 3:
            #point = (seed, c_points)
            if check_coplanarity(seed, c_points):
                closest_points_list.append(seed)
        i += 1
    #print("--")
    return closest_points_list



    #point cloud size is 3km x 3km
    #print(las)
    #print("max X",max(las.X))
    #print("min X",min(las.X))

    #print("max Y",max(las.Y))
    #print("min Y",min(las.Y))

    #geom = o3d.geometry.PointCloud()
    #geom.points = o3d.utility.Vector3dVector(data)
    # o3d.visualization.draw_geometries([geom])

    #list_of_points = calculate_curvature(geom)






    #print(geom.normals[0])
    #print(len(geom.points))
    #i = 0


    #closest_points = geom.compute_nearest_neighbor_distance()

    """
     while i < len(geom.normals):
        #print(i)
        if closest_points[i] < 150:
            norm = geom.normals[i]
            if abs(0 - norm[0]) < 0.02 and abs(0 - norm[1]) < 0.02 and abs(0 - norm[2]) > 0.99:

                print(geom.points[i])
                classified_points.append(geom.points[i])
        #print(closest_points[i], "cm")
        #print(geom.normals[i])s
        i += 1
    
     i = 0
        while i < len(geom.points):
            if closest_points[i] < 120:
                norm = geom.normals[i]
                if abs(0 - norm[0]) < 0.05 and abs(0 - norm[1]) < 0.05 and abs(0 - norm[2]) > 0.95:
                    # print(geom.points[i])
                    classified_points.append(geom.points[i])
            i += 1
    """



