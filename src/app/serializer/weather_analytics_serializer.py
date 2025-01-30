from flask_restx import fields
from flask import request
from typing import List, Optional

class WeatherSerializer:
    """
    Serializer for Weather model data.

    This class is responsible for serializing the weather data into a format
    that can be returned as JSON, with temperature and precipitation values adjusted.

    Attributes:
        model (dict): The field types for the weather data.
    """
    model = {
        "station_id": fields.String,
        "date": fields.String,
        "max_temp": fields.Float,
        "min_temp": fields.Float,
        "precipitation": fields.Float,
    }

    @staticmethod
    def serialize(data: List['Weather']) -> List[dict]:
        """
        Serialize a list of Weather objects into a list of dictionaries.

        Args:
            data (List[Weather]): A list of Weather objects to serialize.

        Returns:
            List[dict]: A list of dictionaries with serialized weather data.
        """
        return [
            {
                "station_id": d.station_id,
                "date": d.date.isoformat(),
                "max_temp": d.max_temp / 10 if d.max_temp else None,
                "min_temp": d.min_temp / 10 if d.min_temp else None,
                "precipitation": d.precipitation / 10 if d.precipitation else None,
            }
            for d in data
        ]


class WeatherStatsSerializer:
    """
    Serializer for WeatherStats model data.

    This class is responsible for serializing the weather statistics data into a
    format that can be returned as JSON.

    Attributes:
        model (dict): The field types for the weather statistics data.
    """
    model = {
        "station_id": fields.String,
        "year": fields.Integer,
        "avg_max_temp": fields.Float,
        "avg_min_temp": fields.Float,
        "total_precipitation": fields.Float,
    }

    @staticmethod
    def serialize(data: List['WeatherStats']) -> List[dict]:
        """
        Serialize a list of WeatherStats objects into a list of dictionaries.

        Args:
            data (List[WeatherStats]): A list of WeatherStats objects to serialize.

        Returns:
            List[dict]: A list of dictionaries with serialized weather statistics data.
        """
        return [
            {
                "station_id": s.station_id,
                "year": s.year,
                "avg_max_temp": s.avg_max_temp,
                "avg_min_temp": s.avg_min_temp,
                "total_precipitation": s.total_precipitation,
            }
            for s in data
        ]