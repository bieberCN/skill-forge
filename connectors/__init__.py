"""Pluggable data connectors used by Skills."""

from .base import Connector, ConnectorError
from .fixture import FixtureConnector

__all__ = ["Connector", "ConnectorError", "FixtureConnector"]
