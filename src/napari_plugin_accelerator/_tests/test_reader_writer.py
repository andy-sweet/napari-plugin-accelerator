import numpy as np
from napari_plugin_accelerator import get_reader, write_zarr

from numpy.random import default_rng
rng = default_rng()

# tmp_path is a pytest fixture that is a temporary directory as a pathlib.Path
def test_writer_reader_consistency(tmp_path):
    tmp_file = str(tmp_path / 'image.zarr')
    rng = np.random.default_rng(0)
    data = rng.integers(low=0, high=255, size=(4, 5), dtype=np.uint8)
    #data = np.ones((4, 5))
    attributes = {'scale': [0.5, 2]}

    written_files = write_zarr(tmp_file, data, attributes)

    assert len(written_files) == 1
    assert written_files[0] == tmp_file

    reader = get_reader(tmp_file)
    layer_tuples = reader(tmp_file)
    assert len(layer_tuples) == 1
    read_data, read_attributes, read_type = layer_tuples[0]

    np.testing.assert_array_equal(read_data, data)
    np.testing.assert_equal(read_attributes, attributes)
    assert read_type == 'image'


def test_get_reader_pass():
    reader = get_reader("image.not_zarr")
    assert reader is None

