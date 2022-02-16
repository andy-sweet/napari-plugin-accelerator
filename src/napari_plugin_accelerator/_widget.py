from enum import auto
import pandas as pd
from qtpy.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout
from napari import Viewer
from napari.layers import Image, Labels, Layer
from napari.types import ImageData
from napari.utils.misc import StringEnum
from npe2.types import FullLayerData
from skimage.filters import gaussian
from skimage.measure import regionprops_table


class FilterMode(StringEnum):
    REFLECT = auto()
    NEAREST = auto()
    MIRROR = auto()
    WRAP = auto()


def smooth_image(
        image: ImageData,
        sigma: float = 1,
        mode: FilterMode = FilterMode.NEAREST,
) -> ImageData:
    return gaussian(image, sigma=sigma, mode=str(mode), preserve_range=True)


def measure_features(image: Image, labels: Labels) -> None:
    prop_names = ('label', 'area', 'intensity_mean')
    prop_values = regionprops_table(
            labels.data,
            intensity_image=image.data,
            properties=prop_names,
    )
    features = pd.DataFrame(prop_values)
    features.rename(columns={'label': 'index'}, inplace=True)
    labels.features = features


class FeaturesTable(QWidget):
    def __init__(self, layer: Layer, parent=None):
        super().__init__(parent)
        self._layer = layer
        self._table = QTableWidget()
        self.set_data(layer.features)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self._table)
        layer.events.properties.connect(self._on_features_changed)

    def _on_features_changed(self, event=None):
        self.set_data(self._layer.features)

    def set_data(self, features: pd.DataFrame) -> None:
        self._table.setRowCount(features.shape[0])
        self._table.setColumnCount(features.shape[1])
        self._table.setVerticalHeaderLabels([str(i) for i in features.index])
        for c, column in enumerate(features.columns):
            self._table.setHorizontalHeaderItem(c, QTableWidgetItem(column))
            for r, value in enumerate(features[column]):
                self._table.setItem(r, c, QTableWidgetItem(str(value)))
        self._table.resizeColumnsToContents()


def view_features(layer: Layer, viewer: Viewer) -> None:
    table = FeaturesTable(layer)
    name = f'Features of {layer.name}'
    viewer.window.add_dock_widget(table, name=name)

