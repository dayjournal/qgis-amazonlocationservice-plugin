from typing import Tuple
from qgis.core import QgsProject, QgsVectorTileLayer

from ..utils.configuration_handler import ConfigurationHandler


class MapFunctions:
    """
    Manages the loading of vector tile layers into a QGIS project
    based on configurations.
    """

    KEY_REGION = "region_value"
    KEY_MAP = "map_value"
    KEY_APIKEY = "apikey_value"

    def __init__(self) -> None:
        """
        Initializes the MapFunctions with a configuration handler.
        """
        self.configuration_handler = ConfigurationHandler()

    def get_configuration_settings(self) -> Tuple[str, str, str]:
        """
        Fetches necessary configuration settings from the settings manager.

        Returns:
            Tuple[str, str, str]: A tuple containing the region,
            route calculator name, and API key.
        """
        region = self.configuration_handler.get_setting(self.KEY_REGION)
        map = self.configuration_handler.get_setting(self.KEY_MAP)
        apikey = self.configuration_handler.get_setting(self.KEY_APIKEY)
        return region, map, apikey

    def add_vector_tile_layer(self) -> None:
        """
        Adds a vector tile layer into the current QGIS project using
        configuration settings.
        """
        try:
            region_value, map_value, apikey_value = self.get_configuration_settings()
            style_url = (
                f"https://maps.geo.{region_value}.amazonaws.com/maps/v0/maps/"
                f"{map_value}/style-descriptor?key={apikey_value}"
            )
            tile_url = (
                f"https://maps.geo.{region_value}.amazonaws.com/maps/v0/maps/"
                f"{map_value}/tiles/{{z}}/{{x}}/{{y}}?key={apikey_value}"
            )
            layer_url = f"styleUrl={style_url}&type=xyz&url={tile_url}&zmax=14&zmin=0"
            vector_tile = QgsVectorTileLayer(layer_url, map_value)
            QgsProject.instance().addMapLayer(vector_tile)
            vector_tile.loadDefaultStyle()
        except KeyError as e:
            raise KeyError(f"Missing configuration for {e}")
        except Exception as e:
            raise Exception(f"Failed to load vector tile layer: {str(e)}")
