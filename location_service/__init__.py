def classFactory(iface):
    from .location_service import LocationService

    return LocationService(iface)
