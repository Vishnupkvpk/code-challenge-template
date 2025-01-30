import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://postgres:postgres123@localhost:5432/weather_analysis"
