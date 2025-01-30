from flask_restx import Namespace, Resource, fields
from flask import request
from app.controllers.weather_analytics_controller import WeatherAnalyticsController 

weather_analytics = Namespace("weather", description="Weather data operations")


@weather_analytics.route("/")
class Weather(Resource):

    """
    Endpoint to get weather data by station ID and date.
    """

    @weather_analytics.param("station_id", "Station ID", type=str, required=True)
    @weather_analytics.param(
        "date", "Date in ISO format (YYYY-MM-DD)", type=str, required=True
    )
    @weather_analytics.param("page", "Page number for pagination", type=int, default=1)
    def get(self):
        """
        Get weather data for a given station and date.

        Args:
            station_id (str): The unique identifier for the weather station.
            date (str): The date for which weather data is requested (in ISO format).
            page (int): The page number for pagination (default is 1).

        Returns:
            dict: The serialized weather data, with status code 200 if successful.
        """
        station_id = request.args.get("station_id")
        date = request.args.get("date")
        page = request.args.get("page", 1, type=int)

        data = WeatherAnalyticsController(station_id,page).get_weather_data(date)
        return data, 200

@weather_analytics.route("/stats")
class WeatherStats(Resource):
    """
    Endpoint to get weather statistics for a station for a specific year.
    """
    @weather_analytics.param("station_id", "Station ID", type=str, required=True)
    @weather_analytics.param("year", "Year for weather statistics", type=int, required=True)
    @weather_analytics.param("page", "Page number for pagination", type=int, default=1)
    def get(self):
        """
        Get weather statistics for a station in a specific year.

        Args:
            station_id (str): The unique identifier for the weather station.
            year (int): The year for which weather statistics are requested.
            page (int): The page number for pagination (default is 1).

        Returns:
            dict: The serialized weather statistics data, with status code 200 if successful.
        """
        station_id = request.args.get("station_id")
        year = request.args.get("year", type=int)
        page = request.args.get("page", 1, type=int)

        data = WeatherAnalyticsController(station_id,page).get_weather_stats(year)
        return data, 200

