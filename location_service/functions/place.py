from typing import Dict, Tuple, Any
from PyQt5.QtCore import QVariant
from PyQt5.QtGui import QColor
from qgis.core import (
    QgsProject,
    QgsVectorLayer,
    QgsFields,
    QgsField,
    QgsPointXY,
    QgsFeature,
    QgsGeometry,
    QgsTextFormat,
    QgsVectorLayerSimpleLabeling,
    QgsPalLayerSettings,
    QgsSimpleMarkerSymbolLayer,
    QgsMarkerSymbol,
    QgsSingleSymbolRenderer,
)

from ..utils.configuration_handler import ConfigurationHandler
from ..utils.external_api_handler import ExternalApiHandler


class PlaceFunctions:
    """
    Manages the searching and visualization of places based on coordinates.
    """

    KEY_REGION = "region_value"
    KEY_PLACE = "place_value"
    KEY_APIKEY = "apikey_value"
    PLACE_LANGUAGE = None
    PLACE_MAX_RESULTS = 10
    WGS84_CRS = "EPSG:4326"
    LAYER_TYPE = "Point"
    FIELD_LABEL = "Label"
    FIELD_MUNICIPALITY = "Municipality"
    FIELD_REGION = "Region"
    FIELD_COUNTRY = "Country"
    SYMBOL_SHAPE = QgsSimpleMarkerSymbolLayer.Circle
    SYMBOL_COLOR = QColor(0, 124, 191)
    SYMBOL_SIZE = 3.0
    LABEL_TEXT_COLOR = QColor("black")
    LABEL_TEXT_SIZE = 10

    def __init__(self) -> None:
        """
        Initializes the PlaceFunctions with configuration and API handlers.
        """
        self.configuration_handler = ConfigurationHandler()
        self.api_handler = ExternalApiHandler()

    def get_configuration_settings(self) -> Tuple[str, str, str]:
        """
        Fetches necessary configuration settings from the settings manager.

        Returns:
            Tuple[str, str, str]: A tuple containing the
            region, route calculator name, and API key.
        """
        region = self.configuration_handler.get_setting(self.KEY_REGION)
        place = self.configuration_handler.get_setting(self.KEY_PLACE)
        apikey = self.configuration_handler.get_setting(self.KEY_APIKEY)
        return region, place, apikey

    def search_place_index_for_position(self, lon: float, lat: float) -> Dict[str, Any]:
        """
        Searches for a place index based on the provided longitude and
        latitude coordinates.

        Args:
            lon (float): Longitude of the position to search.
            lat (float): Latitude of the position to search.

        Returns:
            A dictionary containing the API request results with place information.
        """
        region, place, apikey = self.get_configuration_settings()
        place_url = (
            f"https://places.geo.{region}.amazonaws.com/places/v0/indexes/"
            f"{place}/search/position?key={apikey}"
        )
        data = {
            "Language": self.PLACE_LANGUAGE,
            "MaxResults": self.PLACE_MAX_RESULTS,
            "Position": [lon, lat],
        }
        result = self.api_handler.send_json_post_request(place_url, data)
        if result is None:
            raise Exception("Failed to receive a valid response from the API.")
        return result

    def add_point_layer(self, data: Dict) -> None:
        """
        Adds a new point layer to the current QGIS project based on search results.

        Args:
            data (Dict): Data containing results from the search, including
                         location and place information.
        """
        place = self.configuration_handler.get_setting(self.KEY_PLACE)
        layer = QgsVectorLayer(
            f"{self.LAYER_TYPE}?crs={self.WGS84_CRS}", place, "memory"
        )
        self.setup_layer(layer, data)

    def setup_layer(self, layer: QgsVectorLayer, data: Dict) -> None:
        """
        Configures the given layer with attributes, features,
        styling, and labeling based on search results.

        Args:
            layer (QgsVectorLayer): The vector layer to be configured.
            data (Dict): Search results data used to populate the layer.
        """
        self.add_attributes(layer)
        self.add_features(layer, data["Results"])
        self.apply_layer_style(layer)
        self.apply_label_style(layer)
        layer.triggerRepaint()
        QgsProject.instance().addMapLayer(layer)

    def add_attributes(self, layer: QgsVectorLayer) -> None:
        """
        Adds necessary fields to the vector layer.

        Args:
            layer (QgsVectorLayer): The layer to which fields are added.
        """
        fields = QgsFields()
        fields.append(QgsField(self.FIELD_LABEL, QVariant.String))
        fields.append(QgsField(self.FIELD_MUNICIPALITY, QVariant.String))
        fields.append(QgsField(self.FIELD_REGION, QVariant.String))
        fields.append(QgsField(self.FIELD_COUNTRY, QVariant.String))
        layer.dataProvider().addAttributes(fields)
        layer.updateFields()

    def add_features(self, layer: QgsVectorLayer, data: Dict) -> None:
        """
        Adds features to the given layer based on search results.

        Args:
            layer (QgsVectorLayer): The layer to which features are added.
            data (Dict): The search results containing place information.
        """
        features = []
        for result in data:
            place = result["Place"]
            feature = QgsFeature(layer.fields())
            feature.setGeometry(
                QgsGeometry.fromPointXY(
                    QgsPointXY(
                        place["Geometry"]["Point"][0], place["Geometry"]["Point"][1]
                    )
                )
            )
            feature.setAttributes(
                [
                    place.get("Label", ""),
                    place.get("Municipality", ""),
                    place.get("Region", ""),
                    place.get("Country", ""),
                ]
            )
            features.append(feature)
        layer.dataProvider().addFeatures(features)

    def apply_layer_style(self, layer: QgsVectorLayer) -> None:
        """
        Sets up styling for the given layer.

        Args:
            layer (QgsVectorLayer): The layer to set up styling for.
        """
        symbol_layer = QgsSimpleMarkerSymbolLayer()
        symbol_layer.setShape(self.SYMBOL_SHAPE)
        symbol_layer.setColor(self.SYMBOL_COLOR)
        symbol_layer.setSize(self.SYMBOL_SIZE)
        symbol = QgsMarkerSymbol.createSimple({})
        symbol.changeSymbolLayer(0, symbol_layer)
        layer.setRenderer(QgsSingleSymbolRenderer(symbol))

    def apply_label_style(self, layer: QgsVectorLayer) -> None:
        """
        Sets up labeling for the given layer.

        Args:
            layer (QgsVectorLayer): The layer to set up labeling for.
        """
        label_settings = QgsPalLayerSettings()
        label_settings.fieldName = self.FIELD_LABEL
        label_settings.enabled = True
        text_format = QgsTextFormat()
        text_format.setSize(self.LABEL_TEXT_SIZE)
        text_format.setColor(self.LABEL_TEXT_COLOR)
        label_settings.setFormat(text_format)
        layer.setLabelsEnabled(True)
        layer.setLabeling(QgsVectorLayerSimpleLabeling(label_settings))
