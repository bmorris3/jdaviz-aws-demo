import os
from pathlib import Path
import signal
import solara
from IPython.display import display

import numpy as np
from astropy.io import fits
from specutils import Spectrum1D

import ipygoldenlayout
import ipysplitpanes
import ipyvue

import jdaviz
from jdaviz.app import custom_components

config = 'Cubeviz'
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

    viz = jdaviz.Cubeviz()

    uri = 's3://stpubdata/jwst/public/jw01373/L3/t/o031/jw01373-o031_t007_miri_ch1-shortmediumlong_s3d.fits'
    with fits.open(uri, use_fsspec=True, fsspec_kwargs={"anon": True}) as file:
        hdulist = file[:]

        viz.load_data(hdulist)

    with solara.Column():
        solara.Markdown("# Demo: jdaviz on AWS")
        solara.Markdown(f"Load MIRI IFU cube from MAST's holdings on AWS S3 at {uri}")

        with solara.Row():
            solara.display(viz.app)
