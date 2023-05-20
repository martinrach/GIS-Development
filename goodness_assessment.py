
import numpy as np


def goodness(viewshed, antennas):
    # check for correct input formats
    if type(viewshed) != np.ndarray:
        print("Format of the viewshed must be an np.ndarray!")
        return None
    elif type(antennas) != list:
        print("Format of the antennas must be a list!")
        return None    
    
    # calculate coverage of the viewshed in [%]
    coverage = np.count_nonzero(viewshed) / viewshed.size * 100
    
    # avergae coverage per antenna
    avg_coverage = coverage / len(antennas)
    
    # print result
    print('{:.0f} % of the area is covered by the base stations.'.format(coverage))
    print('Average coverage per base-station: {:.2f}%'.format(avg_coverage))



