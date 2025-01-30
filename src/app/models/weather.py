from app import db


class Weather(db.Model):
    """
    Model representing daily weather data for a specific station.

    Attributes:
        id (int): The primary key of the record.
        station_id (str): The unique identifier for the weather station.
        date (date): The date for which the weather data is recorded.
        max_temp (Optional[int]): The maximum temperature for the day.
        min_temp (Optional[int]): The minimum temperature for the day.
        precipitation (Optional[int]): The precipitation for the day, in millimeters.
    """
    
    __tablename__ = 'weather'
    
    id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)
    max_temp = db.Column(db.Integer)
    min_temp = db.Column(db.Integer)
    precipitation = db.Column(db.Integer)