from app.models.weather import Weather
from app.models.weather_stats import WeatherStats
from app.serializer.weather_analytics_serializer import WeatherStatsSerializer, WeatherSerializer
from typing import Optional


class WeatherAnalyticsController:
    """
    Controller for retrieving weather data and weather statistics.

    Attributes:
        station_id (Optional[int]): The station ID to filter the weather data by.
        page (int): The page number for pagination.
        per_page (int): The number of items per page for pagination.
    """

    def __init__(self, station_id: Optional[int] = None, page: int = 1, per_page: int = 10) -> None:
        """
        Initialize the WeatherAnalyticsController with optional station ID, page, and per_page parameters.

        Args:
            station_id (Optional[int]): The station ID to filter the weather data by. Defaults to None.
            page (int): The page number for pagination. Defaults to 1.
            per_page (int): The number of items per page for pagination. Defaults to 10.
        """
        self.station_id = station_id
        self.page = page
        self.per_page = per_page

    def _paginate_query(self, query, page: int, per_page: int) -> list:
        """
        Helper method to paginate a query result.

        Args:
            query: The query to paginate.
            page (int): The page number for pagination.
            per_page (int): The number of items per page for pagination.

        Returns:
            list: The list of paginated items.
        """
        return query.paginate(page=page, per_page=per_page).items

    def get_weather_data(self, date: Optional[str] = None) -> list:
        """
        Retrieve weather data for a specific station and date, with pagination.

        Args:
            date (Optional[str]): The date to filter the weather data by. Defaults to None.

        Returns:
            list: The serialized weather data for the requested date and station, if provided.
        """
        query = Weather.query
        if self.station_id:
            query = query.filter_by(station_id=self.station_id)
        if date:
            query = query.filter_by(date=date)
        return WeatherSerializer.serialize(self._paginate_query(query, self.page, self.per_page))

    def get_weather_stats(self, year: Optional[int] = None) -> list:
        """
        Retrieve weather statistics for a specific station and year, with pagination.

        Args:
            year (Optional[int]): The year to filter the weather statistics by. Defaults to None.

        Returns:
            list: The serialized weather statistics for the requested year and station, if provided.
        """
        query = WeatherStats.query
        if self.station_id:
            query = query.filter_by(station_id=self.station_id)
        if year:
            query = query.filter_by(year=year)
        return WeatherStatsSerializer.serialize(self._paginate_query(query, self.page, self.per_page))
