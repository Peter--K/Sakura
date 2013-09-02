# This standalone script simply dumps out a 256-row lookup table
# of rgb values. By doing this, we avoid matplotlib as a dependency
# when it comes time to bundle Sakura for distribution.

import numpy as np
from matplotlib import cm

# specify the colourmap here
cmap_name = "gist_heat"

colourTable = eval('cm.' + cmap_name)

ROWS = 256
lookup = np.empty((ROWS, 3))
for i, x in enumerate(np.linspace(0, 1, 256)):
    lookup[i] = np.asarray(colourTable(x)[0:3])

np.savetxt(cmap_name + '.cmap', lookup, fmt='%0.5g')
