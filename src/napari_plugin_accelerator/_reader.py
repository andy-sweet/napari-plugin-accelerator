from typing import List, Optional
from npe2.types import LayerData, ReaderFunction
import zarr


def get_reader(path) -> Optional[ReaderFunction]:
    """Gets the reader associated with a path or list of paths.

    Parameters
    ----------
    path : str or list of str
        Path to file, or list of paths.

    Returns
    -------
    Optional[ReaderFunction]
        If the path is a recognized format, return a function that accepts the
        same path or list of paths, and returns a list of layer data tuples.
    """
    if isinstance(path, list):
        # reader plugins may be handed single path, or a list of paths.
        # if it is a list, it is assumed to be an image stack...
        # so we are only going to look at the first file.
        path = path[0]

    if isinstance(path, str) and path.endswith('.zarr'):
        return read_zarr

    return None


def read_zarr(path: str) -> List[LayerData]:
    """Reads a zarr array as an image layer from a path.

    Parameters
    ----------
    path : str
        Path to zarr directory.

    Returns
    -------
    layer_data : List[LayerData]
        A list containing one napari image layer tuple.
    """
    z = zarr.open(path, mode='r')
    attributes = {'scale': z.attrs['scale']}
    return [(z, attributes, 'image')]

