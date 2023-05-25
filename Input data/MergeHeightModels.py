
import rasterio
from matplotlib import pyplot
import numpy as np
from rasterio.windows import Window

mosaic1 = np.zeros(shape=(6000,6000)).astype(np.float64)

# jiust some dummy code to merge 16 images that are opened in certain order. Works only in this case

j = 1
while j < 5:
    i = 1
    print(j)
    while i < 5:
        if j == 1:
            with rasterio.open("L4131E" + str(i) +"_height_raster.tif") as r:
                raster = r.read(1)
                if i == 1:
                    x = 0
                elif i == 2:
                    x = 0
                elif i == 3:
                    x = 1500
                elif i == 4:
                    x = 1500
                X = 0
                while x < x + 1500 and X < 1500:
                    if i == 1:
                        y = 4500
                    elif i == 2:
                        y = 3000
                    elif i == 3:
                        y = 4500
                    elif i == 4:
                        y = 3000
                    Y = 0
                    while y < y + 1500 and Y < 1500:
                        h = raster[Y, X]
                        row = mosaic1[y]
                        row[x] = h
                        Y = Y + 1
                        y = y + 1
                    X = X + 1
                    x = x + 1
        if j == 2:
            with rasterio.open("L4131F" + str(i) +"_height_raster.tif") as r:
                raster = r.read(1)
                if i == 1:
                    x = 0
                elif i == 2:
                    x = 0
                    profile = r.profile
                    print(profile)
                    window = Window(0, 0, 1500, 1500)
                    transform =  r.window_transform(window)
                elif i == 3:
                    x = 1500
                elif i == 4:
                    x = 1500
                X = 0

                while x < x + 1500 and X < 1500:
                    Y = 0
                    if i == 1:
                        y = 1500
                    elif i == 2:
                        y = 0
                    elif i == 3:
                        y = 1500
                    elif i == 4:

                        y = 0
                    while y < y + 1500 and Y < 1500:
                        h = raster[Y, X]
                        row = mosaic1[y]
                        row[x] = h
                        #print(row[y])
                        Y = Y + 1
                        y = y + 1
                    X = X + 1
                    x = x + 1
        if j == 3:
            with rasterio.open("L4131G" + str(i) +"_height_raster.tif") as r:
                raster = r.read(1)
                if i == 1:
                    x = 3000
                elif i == 2:
                    x = 3000
                elif i == 3:
                    x = 4500
                elif i == 4:
                    x = 4500
                X = 0
                while x < x + 1500 and X < 1500:
                    Y = 0
                    if i == 1:
                        y = 4500
                    elif i == 2:
                        y = 3000
                    elif i == 3:
                        y = 4500
                    elif i == 4:
                        y = 3000
                    while y < y + 1500 and Y < 1500:
                        h = raster[Y,X]
                        row = mosaic1[y]
                        row[x] = h
                        Y = Y + 1
                        y = y + 1
                    X = X + 1
                    x = x + 1
        if j == 4:
            with rasterio.open("L4131H" + str(i) +"_height_raster.tif") as r:
                raster = r.read(1)
                if i == 1:
                    x = 3000
                elif i == 2:
                    x = 3000
                elif i == 3:
                    x = 4500
                elif i == 4:
                    x = 4500
                X = 0

                while x < x + 1500 and X < 1500:
                    Y = 0
                    if i == 1:
                        y = 1500
                    elif i == 2:
                        y = 0
                    elif i == 3:
                        y = 1500
                    elif i == 4:
                        y = 0
                    while y < y + 1500 and Y < 1500:
                        h = raster[Y, X]
                        row = mosaic1[y]
                        row[x] = h
                        Y = Y + 1
                        y = y + 1
                    X = X + 1
                    x = x + 1

        i = i + 1
    j = j + 1
pyplot.imshow(mosaic1)
pyplot.show()

# Create a new cropped raster to write to

profile.update({
    'height': 6000,
    'width': 6000,
    'transform': transform})

new_dataset = rasterio.open('Merged_height_model', 'w', driver='GTiff',
                                height = mosaic1.shape[0], width = mosaic1.shape[1],
                                count=1, dtype=str(mosaic1.dtype),
                                transform=transform)

new_dataset.write(mosaic1, 1)
new_dataset.close()
