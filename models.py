from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class WeatherData(Base):
    """Модель базы данных учета погодных измерений."""

    __tablename__ = 'weather_data'
    id = Column(Integer, primary_key=True)
    temperature = Column(Float)
    wind_direction = Column(String)
    wind_speed = Column(Float)
    pressure = Column(Float)
    precipitation = Column(Float)
    precipitation_type = Column(String)
