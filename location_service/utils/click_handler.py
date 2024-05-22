from typing import Any
from qgis.gui import QgsMapTool, QgsMapCanvas, QgsMapMouseEvent
from qgis.core import (
    QgsCoordinateReferenceSystem,
    QgsProject,
    QgsCoordinateTransform,
    QgsPointXY,
)


class MapClickCoordinateUpdater(QgsMapTool):
    """
    A tool for updating UI fields with geographic coordinates based on map clicks.
    """

    WGS84_CRS = "EPSG:4326"
    PLACE_LONGITUDE = "lon_lineEdit"
    PLACE_LATITUDE = "lat_lineEdit"
    ST_ROUTES_LONGITUDE = "st_lon_lineEdit"
    ST_ROUTES_LATITUDE = "st_lat_lineEdit"
    ED_ROUTES_LONGITUDE = "ed_lon_lineEdit"
    ED_ROUTES_LATITUDE = "ed_lat_lineEdit"

    def __init__(self, canvas: QgsMapCanvas, active_ui: Any, active_type: str) -> None:
        """
        Initializes the MapClickCoordinateUpdater with a map canvas, UI references,
        and the type of coordinates to update.
        """
        super().__init__(canvas)
        self.active_ui = active_ui
        self.active_type = active_type

    def canvasPressEvent(self, e: QgsMapMouseEvent) -> None:
        """
        Processes mouse press events on the map canvas, converting the click location
        to WGS84 coordinates and updating the UI.
        """
        map_point = self.toMapCoordinates(e.pos())
        wgs84_point = self.transform_to_wgs84(map_point)
        self.update_ui(wgs84_point)

    def update_ui(self, wgs84_point: QgsPointXY) -> None:
        """
        Dynamically updates UI fields designated for longitude and latitude with
        new coordinates from map interactions.
        """
        field_mapping = {
            "st_routes": (self.ST_ROUTES_LONGITUDE, self.ST_ROUTES_LATITUDE),
            "ed_routes": (self.ED_ROUTES_LONGITUDE, self.ED_ROUTES_LATITUDE),
            "place": (self.PLACE_LONGITUDE, self.PLACE_LATITUDE),
        }
        if self.active_type in field_mapping:
            lon_field, lat_field = field_mapping[self.active_type]
            self.set_text_fields(lon_field, lat_field, wgs84_point)

    def set_text_fields(
        self, lon_field: str, lat_field: str, wgs84_point: QgsPointXY
    ) -> None:
        """
        Helper method to set the text of UI fields designated for longitude and
        latitude.
        """
        getattr(self.active_ui, lon_field).setText(str(wgs84_point.x()))
        getattr(self.active_ui, lat_field).setText(str(wgs84_point.y()))

    def transform_to_wgs84(self, map_point: QgsPointXY) -> QgsPointXY:
        """
        Converts map coordinates to the WGS84 coordinate system, ensuring global
        standardization of the location data.

        Args:
            map_point (QgsPointXY): A point in the current map's coordinate system
                                    that needs to be standardized.

        Returns:
            QgsPointXY: The transformed point in WGS84 coordinates, suitable for
                        global mapping applications.
        """
        canvas_crs = QgsProject.instance().crs()
        wgs84_crs = QgsCoordinateReferenceSystem(self.WGS84_CRS)
        transform = QgsCoordinateTransform(canvas_crs, wgs84_crs, QgsProject.instance())
        return transform.transform(map_point)
