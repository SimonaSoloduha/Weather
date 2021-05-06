# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests


class ImportWeatherData:

    def __init__(self):
        self.url = 'https://sinoptik.ua/%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0-%D0%BA%D0%B8%D0%B5%D0%B2'
        self.response = ''
        self.days_dict = {}
        self.weather_dict = {
            'day_of_week': '',
            'day': '',
            'month': '',
            'min_temperature': '',
            'man_temperature': '',
            'weather': ''
        }
        self.all_data_set = None
        self.weather = None
        self.run()

    def run(self):
        self.response = requests.get(self.url)
        if self.response.status_code == 200:
            soup = BeautifulSoup(self.response.text, features='html.parser')
            all_data = soup.find_all('div', {'class': 'tabs'})
            self.weather = soup.find_all('div', {'class': "weatherIco"})
            self.all_data_set = all_data[0].text.split('\xa0')
            self.make_weather_dict()

    def make_weather_dict(self):
        for data in self.all_data_set:
            if len(data) >= 2:
                data_weather_dict = {
                    'day_of_week': '',
                    'day': '',
                    'month': '',
                    'min_temperature': '',
                    'max_temperature': '',
                    'weather': ''
                }
                data = data[2:].split(' ')
                data_weather_dict['day_of_week'] = data[0]
                data_weather_dict['day'] = data[1]
                data_weather_dict['month'] = data[2]
                data_weather_dict['min_temperature'] = data[7][:-1]
                data_weather_dict['max_temperature'] = data[9][:-1]

                self.days_dict[data[1]] = data_weather_dict

        for day, data in enumerate(self.days_dict):
            self.days_dict[data]['weather'] = self.weather[day]['title']

        return self.days_dict


if __name__ == "__main__":
    ImportWeatherData()
