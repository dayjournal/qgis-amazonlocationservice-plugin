import os
from PyQt5.QtWidgets import QDialog, QMessageBox
from qgis.PyQt import uic

from ...utils.configuration_handler import ConfigurationHandler
from ...functions.map import MapFunctions


class MapUi(QDialog):
    """
    A dialog for managing map configurations and adding vector tile layers to a
    QGIS project.
    """

    UI_PATH = os.path.join(os.path.dirname(__file__), "map.ui")
    KEY_MAP = "map_value"

    def __init__(self) -> None:
        """
        Initializes the Map dialog, loads UI components, and populates the map options.
        """
        super().__init__()
        self.ui = uic.loadUi(self.UI_PATH, self)
        self.button_add.clicked.connect(self._add)
        self.button_cancel.clicked.connect(self._cancel)
        self.map = MapFunctions()
        self.configuration_handler = ConfigurationHandler()
        self._populate_map_options()

    def _populate_map_options(self) -> None:
        """
        Populates the map options dropdown with available configurations.
        """
        map = self.configuration_handler.get_setting(self.KEY_MAP)
        self.map_comboBox.addItem(map)

    def _add(self) -> None:
        """
        Adds the selected vector tile layer to the QGIS project and closes the dialog.
        """
        try:
            self.map.add_vector_tile_layer()
            self.close()
        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"Failed to add vector tile layer: {str(e)}"
            )

    def _cancel(self) -> None:
        """
        Cancels the operation and closes the dialog without making changes.
        """
        self.close()
