from typing import List, Optional
from npe2.types import LayerData, ReaderFunction
import zarr


def get_reader(path) -> Optional[ReaderFunction]:
    if isinstance(path, list):
        # reader plugins may be handed single path, or a list of paths.
        # if it is a list, it is assumed to be an image stack...
        # so we are only going to look at the first file.
        path = path[0]

    if isinstance(path, str) and path.endswith('.zarr'):
        return read_zarr

    return None


def read_zarr(path: str) -> List[LayerData]:
    z = zarr.open(path, mode='r')
    attributes = {'scale': z.attrs['scale']}
    return [(z, attributes, 'image')]

