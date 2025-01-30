import pytest
from app.models.weather import Weather
from app.models.weather_stats import WeatherStats
from app import db
from app.controllers.weather_analytics_controller import WeatherAnalyticsController

class TestWeatherAnalyticsController:
    @pytest.fixture
    def sample_weather_data(self,app):
        with app.app_context():
            weather1 = Weather(station_id="STN001", date="2023-01-01", max_temp=300, min_temp=150, precipitation=20)
            weather2 = Weather(station_id="STN001", date="2023-01-02", max_temp=310, min_temp=160, precipitation=25)
            db.session.add_all([weather1, weather2])
            db.session.commit()
            yield
            db.session.query(Weather).delete()
            db.session.commit()

    @pytest.fixture
    def sample_weather_stats_data(self,app):
        with app.app_context():
            stats1 = WeatherStats(station_id="STN001", year=2023, avg_max_temp=305, avg_min_temp=155, total_precipitation=45)
            db.session.add(stats1)
            db.session.commit()
            yield
            db.session.query(WeatherStats).delete()
            db.session.commit()

    def test_get_weather_data(self,sample_weather_data):
        controller = WeatherAnalyticsController(station_id="STN001")
        data = controller.get_weather_data()
        assert len(data) == 2
        assert data[0]["station_id"] == "STN001"
        assert data[0]["max_temp"] == 30.0 

    def test_get_weather_stats(self,sample_weather_stats_data):
        controller = WeatherAnalyticsController(station_id="STN001")
        data = controller.get_weather_stats()
        assert len(data) == 1
        assert data[0]["year"] == 2023
        assert data[0]["avg_max_temp"] == 305
