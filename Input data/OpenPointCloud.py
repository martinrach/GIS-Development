import laspy
import Visualize_data
import numpy as np


with laspy.open("C:/Users/Janne Niskanen/Documents/opiskelu/GIS-project/Input data/L4131H3.laz_classified.las") as temp:
    input_las = temp.read()

point_data = np.stack([input_las.X, input_las.Y, input_las.Z], axis=0).transpose((1, 0))

Visualize_data.visualize_data(point_data)
