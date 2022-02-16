from typing import Any, List
from npe2.types import PathOrPaths
import zarr


def write_zarr(path: str, data: Any, attributes: dict) -> List[str]:
    z = zarr.open(path, mode='w', shape=data.shape, dtype=data.dtype)
    z[:] = data
    z.attrs['scale'] = attributes['scale']
    return [path]

