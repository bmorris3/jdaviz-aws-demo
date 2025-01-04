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
from astroquery.mast import Observations

Observations.enable_cloud_dataset()

cubes = Observations.query_criteria(target_name='Io', proposal_id=1373, instrument_name='MIRI/IFU')
cubes.rename_column('dataURL', 'dataURI')

images = Observations.query_criteria(target_name='Jupiter*', proposal_id=1373, instrument_name='NIRCAM/IMAGE', filters='*M')
images.rename_column('dataURL', 'dataURI')

s3_uris = sorted(Observations.get_cloud_uris(cubes) + Observations.get_cloud_uris(images))

filename_to_s3_uri = {os.path.basename(uri): uri for uri in s3_uris}

filenames = list(filename_to_s3_uri.keys())
filename = solara.reactive(filenames[0])


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

    config = 'Imviz' if 'i2d' in filename.value else 'Cubeviz'

    viz = getattr(jdaviz, config)()

    uri = filename_to_s3_uri[filename.value]
    with fits.open(uri, use_fsspec=True, fsspec_kwargs={"anon": True}) as file:
        hdulist = file[:]

        viz.load_data(hdulist)

    with solara.Column():
        solara.Markdown("# Demo: jdaviz on AWS")
        # solara.Markdown(f"Load MIRI IFU cube from MAST's holdings on AWS S3 at {uri.value}")

        solara.Select(
            label="Dataset",
            values=filenames,
            value=filename
        )

        with solara.Row():
            solara.display(viz.app)
