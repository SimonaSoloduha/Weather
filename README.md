# Weather

# Используемые библиотеки: 
import os
import cv2
from bs4 import BeautifulSoup
import requests
import peewee


## Программа для прогноза погоды с консольным интерфейсом позвояет пользователю:

   Добавление прогнозов за диапазон дат в базу данных
   Получение прогнозов за диапазон дат из базы
   Создание открыток из полученных прогнозов
   Выведение полученных прогнозов на консоль
   При старте консольная утилита загружает прогнозы за прошедшую неделю.

# Программа содержит модуль-движок с классом WeatherMaker для получения и формирования предсказаний погоды

В нём есть метод, получающий прогноз с выбранного вами сайта (парсинг + re) за некоторый диапазон дат, а затем, получив данные, формирует их в словарь {погода: Облачная, температура: 10, дата:datetime...}

# Класс ImageMaker может:

Рисовать открытки (использую OpenCV). 

С текстом, состоящим из полученных данных (пригодится cv2.putText)
С изображением, соответствующим типу погоды ( В качестве фона испотльзуется градиент цвета, отражающего тип погоды)

* Солнечно - от желтого к белому

* Дождь - от синего к белому

* Снег - от голубого к белому

* Облачно - от серого к белому

# Класс DatabaseUpdater может: 

Получать данные из базы данных за указанный диапазон дат.

Сохранять прогнозы в базу данных (использовать peewee)
