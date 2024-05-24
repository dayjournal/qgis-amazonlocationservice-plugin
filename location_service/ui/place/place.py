import os

from PyQt5.QtWidgets import QDialog, QMessageBox
from qgis.PyQt import uic
from qgis.utils import iface

from ...functions.place import PlaceFunctions
from ...utils.click_handler import MapClickCoordinateUpdater


class PlaceUi(QDialog):
    """
    Manages place search and visualization in a QGIS project.
    """

    UI_PATH = os.path.join(os.path.dirname(__file__), "place.ui")

    def __init__(self) -> None:
        """
        Initializes the Place dialog, loads UI components, and populates
        the place options.
        """
        super().__init__()
        self.ui = uic.loadUi(self.UI_PATH, self)
        self.canvas = iface.mapCanvas()
        self.button_click.clicked.connect(self._click)
        self.button_search.clicked.connect(self._search)
        self.button_cancel.clicked.connect(self._cancel)
        self.place_comboBox.addItem("SearchPlaceIndexForPosition")
        self.place = PlaceFunctions()

    def _search(self) -> None:
        """
        Performs a place search and visualizes the results on the map.
        """
        lon = self.lon_lineEdit.text()
        lat = self.lat_lineEdit.text()
        try:
            result = self.place.search_place_index_for_position(lon, lat)
            self.place.add_point_layer(result)
        except Exception as e:
            QMessageBox.critical(self, "Search Error", f"Failed to search place: {e!r}")
        finally:
            self.close()

    def _cancel(self) -> None:
        """
        Closes the dialog without making changes.
        """
        self.close()

    def _click(self) -> None:
        """
        Sets a custom map tool to capture map clicks and populate coordinates.
        """
        self.MapClick = MapClickCoordinateUpdater(self.canvas, self.ui, "place")
        self.canvas.setMapTool(self.MapClick)
