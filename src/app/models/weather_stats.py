from app import db


class WeatherStats(db.Model):
    """
    Model representing weather statistics for a specific station and year.

    Attributes:
        id (int): The primary key of the record.
        station_id (str): The unique identifier for the weather station.
        year (int): The year for which the weather statistics are recorded.
        avg_max_temp (Optional[float]): The average maximum temperature for the year.
        avg_min_temp (Optional[float]): The average minimum temperature for the year.
        total_precipitation (Optional[float]): The total precipitation for the year.
    """
    
    __tablename__ = 'weather_stats'

    id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    avg_max_temp = db.Column(db.Float)
    avg_min_temp = db.Column(db.Float)
    total_precipitation = db.Column(db.Float)