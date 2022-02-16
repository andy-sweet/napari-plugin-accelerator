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

