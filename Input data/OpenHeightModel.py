import rasterio
from matplotlib import pyplot

with rasterio.open('Merged_height_model.tif') as src:
    raster = src.read(1)

pyplot.imshow(raster, cmap='terrain')
pyplot.show()

