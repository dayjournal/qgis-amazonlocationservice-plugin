import json
from typing import Dict, Any, Optional
from PyQt5.QtCore import QUrl, QEventLoop
from PyQt5.QtNetwork import QNetworkRequest, QNetworkReply
from qgis.core import QgsNetworkAccessManager


class ExternalApiHandler:
    """
    A utility class for handling external API requests using the QGIS network manager.
    """

    JSON_CONTENT_TYPE = "application/json"
    UTF8_ENCODING = "utf-8"

    def __init__(self) -> None:
        """
        Initializes the network manager instance from QGIS core libraries.
        """
        self.network_manager = QgsNetworkAccessManager.instance()

    def send_json_post_request(
        self, url: str, data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Sends a POST request to the specified URL with the provided data and
        handles the network response.

        Args:
            url: The URL to which the POST request should be sent.
            data: The data to be sent in the POST request, as a dictionary.

        Returns:
            A dictionary parsed from the JSON response of the server, or None
            if an error occurs.
        """
        request = QNetworkRequest(QUrl(url))
        request.setHeader(QNetworkRequest.ContentTypeHeader, self.JSON_CONTENT_TYPE)
        encoded_data = json.dumps(data).encode(self.UTF8_ENCODING)
        eventLoop = QEventLoop()
        reply = self.network_manager.post(request, encoded_data)
        reply.finished.connect(eventLoop.quit)
        eventLoop.exec_()
        return self.handle_network_reply(reply)

    def handle_network_reply(self, reply: QNetworkReply) -> Optional[Dict[str, Any]]:
        """
        Processes the network reply, checking for errors and decoding the JSON response.

        Args:
            reply: The network reply object.

        Returns:
            The decoded JSON object if no network errors occurred, or None if an error
            is encountered.

        Raises:
            RuntimeError: If a network error occurs or the response cannot be decoded
            as JSON.
        """
        try:
            if reply.error() == QNetworkReply.NoError:  # type: ignore
                response_data = reply.readAll().data().decode(self.UTF8_ENCODING)
                return json.loads(response_data)
            else:
                error_msg = f"Network error occurred: {reply.errorString()}"
                raise RuntimeError(error_msg)
        finally:
            reply.deleteLater()
