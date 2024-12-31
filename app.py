import os
from pathlib import Path
import signal
import solara
from IPython.display import display

import numpy as np
import astropy.units as u
from specutils import Spectrum1D
from jdaviz import Specviz

import ipygoldenlayout
import ipysplitpanes
import ipyvue

import jdaviz
from jdaviz.app import custom_components

config = 'Specviz'
data_list = []
load_data_kwargs = {}
jdaviz_verbosity = 'error'
jdaviz_history_verbosity = 'info'

@solara.lab.on_kernel_start
def on_kernel_start():
    # at import time, solara runs with a dummy kernel
    # we simply ignore that
    if "dummy" in solara.get_kernel_id():
        return

    def on_kernel_close():
        # for some reason, sys.exit(0) does not work here
        # see https://github.com/encode/uvicorn/discussions/1103
        signal.raise_signal(signal.SIGINT)
    return on_kernel_close


@solara.component
def Page():
    ipysplitpanes.SplitPanes()
    ipygoldenlayout.GoldenLayout()
    for name, path in custom_components.items():
        ipyvue.register_component_from_file(None, name,
                                            os.path.join(os.path.dirname(jdaviz.__file__), path))

    ipyvue.register_component_from_file('g-viewer-tab', "container.vue", jdaviz.__file__)

    solara.Style(Path(__file__).parent / "solara.css")

    n_channels = 1000
    flux = np.random.normal(size=n_channels) * u.electron
    wavelength = np.sort(np.random.uniform(1, 5, size=n_channels)) * u.um

    spectrum = Spectrum1D(flux=flux, spectral_axis=wavelength)
    viz = Specviz()
    viz.load_data(spectrum)

    with solara.Column():
        solara.Markdown("# Demo: jdaviz on AWS")

        with solara.Row():
            solara.display(viz.app)
