import os
import solara
from IPython.display import display

import numpy as np
import astropy.units as u
from specutils import Spectrum1D
from jdaviz import Specviz

url = "https://www.dropbox.com/scl/fi/fwhxqwvg8h9pyeqn6k321/hr8781.0039.wfrmcpc.fits?rlkey=vasftjdzlomnim5d2kw3pzulz&st=dqty2ukk&dl=0"

@solara.component
def Page():
    n_channels = 1000
    flux = np.random.normal(size=n_channels) * u.electron
    wavelength = np.sort(np.random.uniform(1, 5, size=n_channels)) * u.um

    spectrum = Spectrum1D(flux=flux, spectral_axis=wavelength)

    viz = Specviz()
    viz.load_data(spectrum)
    viz.show()