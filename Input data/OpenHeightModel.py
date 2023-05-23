import rasterio
from matplotlib import pyplot

with rasterio.open('Height model/height_raster_test4.tif') as src:
    raster = src.read(1)

pyplot.imshow(raster, cmap='viridis')
pyplot.show()

