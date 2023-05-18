
import fiona
#from fiona.crs import CRS


#crs = fiona.from_epsg('3067')

crs = '3067'

point = {'geometry': {
    'type': 'Point',
    'coordinates': (268280,6731924)},
    'properties': dict([('name', 'test_point')])}

schema = {'geometry': 'Point',
          'properties': dict([('name', 'str')])}

with fiona.open('vector_csc_output_file.gpkg', 'w', driver='GPKG', crs=fiona._crs.from_epsg('3067'), schema=schema) as output:
    output.write(point)
    
print('Testing of this python script is complete.')
