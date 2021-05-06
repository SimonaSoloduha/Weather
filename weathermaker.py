# -*- coding: utf-8 -*-
from imagemaker import ImageMaker
from import_weather_data import ImportWeatherData
from updater import Updater
from termcolor import cprint


class WeatherMaker:

    def __init__(self):
        self.days_dict = None
        self.ImportWeatherData = ImportWeatherData
        self.ImageMaker = ImageMaker
        self.weather_period = None
        self.Updater = Updater
        self.user_number = None
        self.action_number = None
        self.quantity = None
        self.no_exit = True
        self.dict_action = {
            '1': {'name': 'Добавить прогнозы за диапазон дат в базу данных', 'func': self.add_tp_db},
            '2': {'name': 'Получить прогнозы за диапазон дат из базы', 'func': self.pull_from_db},
            '3': {'name': 'Создать открытки из полученных прогнозов', 'func': self.make_card},
            '4': {'name': 'Вывести полученныу прогнозы на консоль', 'func': self.print_weather},
        }
        self.run()

    def run(self):
        while self.no_exit:
            cprint('Здесь вы можете узнать погоду для Киева', 'blue')
            cprint('Выберите номер действия:', 'blue')
            for number, action in self.dict_action.items():
                cprint(f'{number} -- {action["name"]}', 'grey')
            self.action_number = input()
            self.dict_action[self.action_number]['func']()
            self.want_to_continue()

    def add_tp_db(self):
        self.days_dict = self.ImportWeatherData().days_dict
        self.Updater(self.days_dict).write_data_to_db()
        cprint(f'Данные на неделю вперед загружены')

    def pull_from_db(self):
        cprint('Прогноз на какие дни вас интересует? Введите период, например:\nC : 10\nПо 15', 'blue')
        day_start = int(input("С:"))
        day_end = int(input("По:"))
        self.weather_period = self.Updater(self.days_dict, day_start, day_end).get_data_from_db()
        cprint(f'Данные о погоде с {day_start} по {day_end} взяты из базы данных')

    def print_weather(self):
        if self.weather_period is None:
            self.pull_from_db()
        # self.pull_from_db()
        for weather in self.weather_period:
            print(f'\nПогода на {weather.day_id} {weather.month}:\n\n** {weather.weather} **\n'
                  f'Минимальная температура: {weather.min_temperature}\n'
                  f'Максимальная температура: {weather.max_temperature}')

    def make_card(self):
        if self.weather_period is None:
            self.pull_from_db()
        for day in self.weather_period:
            self.ImageMaker(day)
        print("Открытки созданы и скоро будут загружены в папку cards")

    def want_to_continue(self):
        cprint('Хотите продолжить? введите 1, чтобы выйти введите 2', 'blue')
        user_response = input()
        if user_response == '2':
            self.no_exit = False


if __name__ == "__main__":
    WeatherMaker()

# Сделать программу с консольным интерфейсом, постаравшись все выполняемые действия вынести в отдельные функции.
# Среди действий, доступных пользователю, должны быть:
#   Добавление прогнозов за диапазон дат в базу данных
#   Получение прогнозов за диапазон дат из базы
#   Создание открыток из полученных прогнозов
#   Выведение полученных прогнозов на консоль
# При старте консольная утилита должна загружать прогнозы за прошедшую неделю.
