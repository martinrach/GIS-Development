import numpy as np
from math import sqrt
import open3d as o3d
import Visualize_data

def closest_n_points(seed, data, n):
    closest_points = []
    #print(seed[0])
    #print(seed[1])
    #print(seed[2])
    X_0 = int(seed[0])
    Y_0 = int(seed[1])
    Z_0 = int(seed[2])
    i = 0

    #Going through all points and finding points that are closer than 4 meters from the point
    while i < len(data.points):
        #print(data.points[i])
        point = data.points[i]
        X = int(point[0])
        Y = int(point[1])
        Z = int(point[2])

        #print(X, Y, Z)
        #print(X_0, Y_0, Z_0)
        #print(abs(X - X_0))
        #print(abs(Y - Y_0))
        #print(abs(Z - Z_0))
        eucl_dist = sqrt((abs(X - X_0))**2 + (abs(Y - Y_0))**2 + (abs(Z - Z_0))**2)
        #print(eucl_dist, "eucl distance")
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

def calculate_distances(pcl): #or flatness
    #print(pcl)
    i = 0
    closest_points_list =[]
    while i < len(pcl.points):
        seed = pcl.points[i]
        c_points = closest_n_points(seed, pcl, 10)
        #print(c_points, "closest n points")
        if len(c_points) > 6:
            point = (seed, c_points)
            closest_points_list.append(seed)
        i += 1
    return closest_points_list


def classify_buildings(data):
    if len(data) < 1000:
        geom = o3d.geometry.PointCloud()
        geom.points = o3d.utility.Vector3dVector(data)

        list_of_points = calculate_distances(geom)
        #print(list_of_points)



        return list_of_points

    else:
        # print(data[199])
        c = int(len(data) / 2)
        # print(c)
        data1 = data[:c]
        data2 = data[c:]
        d1 = classify_buildings(data1)
        d2 = classify_buildings(data2)
        return d1 + d2



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



