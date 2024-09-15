from datetime import datetime
import threading

import asyncio
from openpyxl import Workbook
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from constants import DB_URL, TIME_CHECK_WEATHER
from get_weather import get_weather
from models import Base, WeatherData


engine = create_engine(DB_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

async def save_weather_data(data: dict) -> None:
    """Функция сохранения данных о погоде в БД."""
    session = Session()
    try:
        weather_data = WeatherData(
            temperature=data['temperature'],
            wind_direction=data['current_wind_direction'],
            wind_speed=data['wind_speed'],
            pressure=data['pressure'],
            precipitation=data['precipitation'],
            precipitation_type=data['precipitation_type']
        )
        session.add(weather_data)
        session.commit()
    except BaseException as error:
        print(f'Ошибка сохранения данных в БД: {error}')
    finally:
        session.close()

async def export_to_excel() -> None:
    """Функция экспорта данных из БД в Excel."""
    session = Session()
    try:
        weather_data = session.query(
            WeatherData
        ).order_by(WeatherData.id.desc()).limit(10).all()
        wb = Workbook()
        ws = wb.active
        ws.append(
            ['Температура (°C)',
             'Направление ветра',
             'Скорость ветра (м/с)',
             'Давление (мм рт.ст.)',
             'Количество осадков (mm)',
             'Тип осадков']
        )
        for data in weather_data:
            ws.append([
                data.temperature,
                data.wind_direction,
                data.wind_speed,
                data.pressure,
                data.precipitation,
                data.precipitation_type
            ])
        time_now = datetime.now().time().strftime('%H_%M_%S')
        wb.save(f'weather_data_{time_now}.xlsx')
    except BaseException as error:
        print(f'Ошибка экспорта в Excel: {error}')
    finally:
        session.close()

async def export_input_loop():
    """Цикл ожидания ввода пользователя для экспорта данных."""
    while True:
        command = input('Введите \'export\' чтобы сделать экспорт данных из БД в Excel: ')
        if command == 'export':
            await export_to_excel()

async def add_data_to_db():
    """Цикл добавления данных о погоде в БД."""
    while True:
        data = await get_weather()
        await save_weather_data(data)
        await asyncio.sleep(TIME_CHECK_WEATHER)


def run_export_input_loop():
    """
    Запускает цикл ожидания ввода пользователя
    для экспорта данных в отдельном потоке.

    Это необходимо, чтобы не блокировать основной
    цикл событий, позволяя другим задачам выполняться параллельно.
    """
    loop = asyncio.new_event_loop()
    loop.run_until_complete(export_input_loop())


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(add_data_to_db())
    threading.Thread(target=run_export_input_loop).start()
    loop.run_forever()
