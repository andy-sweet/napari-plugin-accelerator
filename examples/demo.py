import os
import napari

from skimage import data

this_dir = os.path.dirname(os.path.abspath(__file__))
labels_path = os.path.join(this_dir, 'data', 'labels.tif')

viewer = napari.view_image(data.coins())
viewer.open(labels_path)
labels = viewer.layers['labels']
labels.features = {
    'index': [1, 2, 3],
    'class': ['penny', 'farthing', 'crown'],
    'confidence': [0.7, 0.2, 0.95],
}

napari.run()
