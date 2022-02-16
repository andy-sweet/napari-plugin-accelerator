from napari_plugin_accelerator import smooth_image
import numpy as np


def test_smooth_image():
    rng = np.random.default_rng(0)
    data = rng.integers(low=0, high=255, size=(4, 5), dtype=np.uint8)

    smoothed_data = smooth_image(data)

    assert data.shape == smoothed_data.shape
    # Smoothing should never increase the range of values.
    assert np.min(data) <= np.min(smoothed_data)
    assert np.max(data) >= np.max(smoothed_data)


## make_napari_viewer is a pytest fixture that returns a napari viewer object
## capsys is a pytest fixture that captures stdout and stderr output streams
#def test_example_magic_widget(make_napari_viewer, capsys):
#    viewer = make_napari_viewer()
#    layer = viewer.add_image(np.random.random((100, 100)))
#
#    # this time, our widget will be a MagicFactory or FunctionGui instance
#    my_widget = example_magic_widget()
#
#    # if we "call" this object, it'll execute our function
#    my_widget(viewer.layers[0])
#
#    # read captured output and check that it's as we expected
#    captured = capsys.readouterr()
#    assert captured.out == f"you have selected {layer}\n"
