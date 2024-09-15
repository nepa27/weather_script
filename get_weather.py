from aiohttp import ClientSession

from constants import (
    API_URL,
    API_PARAMS,
    DIRECTIONS,
    PA_TO_MM_RT_ST,
    WMO_CODE_MAP
)

async def get_weather() -> dict:
    """Функция получения данных о погоде."""
    async with ClientSession() as session:
        async with session.get(API_URL, params=API_PARAMS) as response:
            weather_json = await response.json()
            try:
                temperature = weather_json['current']['temperature']
                wind_direction = weather_json['current']['wind_direction_10m']
                wind_speed = weather_json['current']['wind_speed_10m']
                pressure = int(weather_json['current']['pressure_msl']) * PA_TO_MM_RT_ST
                precipitation = weather_json['current']['precipitation']
                weather_code = weather_json['current']['weather_code']

                for deg_range, direction in DIRECTIONS.items():
                    if deg_range[0] <= wind_direction < deg_range[1]:
                        current_wind_direction = direction
                precipitation_type = WMO_CODE_MAP[weather_code]
                return {
                    'temperature': temperature,
                    'current_wind_direction': current_wind_direction,
                    'wind_speed': wind_speed,
                    'pressure': pressure,
                    'precipitation': precipitation,
                    'precipitation_type': precipitation_type
                }
            except KeyError:
                print('Нет данных')
