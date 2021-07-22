# Weather

# Используемые библиотеки: 
import os

import cv2

from bs4 import BeautifulSoup

import requests

import peewee


## Программа для прогноза погоды с консольным интерфейсом позвояет пользователю:

   Добавять прогнозы погоды за диапазон дат в базу данных

   Получать прогнозы за диапазон дат из базы

   Создавать открытки из полученных прогнозов

   Выводить полученные прогнозы на консоль

   При старте консольная утилита загружает прогнозы за прошедшую неделю.

# Программа содержит модуль-движок с классом WeatherMaker для получения и формирования предсказаний погоды

В нём есть метод, получающий прогноз с выбранного вами сайта (парсинг + re) за некоторый диапазон дат, а затем, получив данные, формирует их в словарь {погода: Облачная, температура: 10, дата:datetime...}

# Класс ImageMaker может:

Позволяет рисовать открытки (использую OpenCV) с текстом, состоящим из полученных данных, а также с изображением, соответствующим типу погоды ( В качестве фона испотльзуется градиент цвета, отражающего тип погоды)

* Солнечно - от желтого к белому

* Дождь - от синего к белому

* Снег - от голубого к белому

* Облачно - от серого к белому

# Класс DatabaseUpdater может: 

Получать данные из базы данных за указанный диапазон дат.

Сохранять прогнозы в базу данных (использовать peewee)
