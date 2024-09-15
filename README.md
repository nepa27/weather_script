# Приложение для получения данных о погоде
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
## Описание
Программа автоматически запрашивает данные погоды в
текущий момент в указанном районе через заданные промежутки времени.
## Основные особенности
- Автоматический запрос данных о погоде через API open-meteo;
- Сохранение полученных данных в БД; 
- Экспорт данных из БД в файл Excel по запросу.
## Стек использованных технологий
+ Python 3.11
+ asynco
+ SQLAlchemy

## Запуск проекта
1. Клонируйте репозиторий на вашем локальном компьютере:

```
   git clone https://github.com/nepa27/weather_script
   cd weather_script
```
   
2. Установите и активируйте виртуальное окружение c учетом версии Python 3.11:
* Если у вас Linux/macOS

```
    python3 -m venv env
    source env/bin/activate
```

* Если у вас Windows

```
    python -m venv venv
    source venv/Scripts/activate
```

+ Обновите менеджер пакетов pip:

```
python -m pip install --upgrade pip
```

+ Затем установите зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

+ Запускаем скрипт командой:

```
python main.py
```

2. Для настройки скрипта измените константы в файле constants.py:

    ```
    LATITUDE                # широта
    LONGITUDE               # долгота
    TIME_CHECK_WEATHER      # время, через которое скрипт производит сбор данных
    ```
   
## Автор

+ [Александр Непочатых](https://github.com/nepa27) 
