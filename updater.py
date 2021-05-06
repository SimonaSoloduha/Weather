# -*- coding: utf-8 -*-
import peewee

database = peewee.SqliteDatabase('db/updater_weather.db')


class DatabaseUpdater(peewee.Model):
    class Meta:
        database = database


class Day(DatabaseUpdater):
    name = peewee.CharField(unique=True)


class Weather(DatabaseUpdater):
    day = peewee.ForeignKeyField(Day)
    day_of_week = peewee.CharField()
    month = peewee.CharField()
    min_temperature = peewee.CharField()
    max_temperature = peewee.CharField()
    weather = peewee.CharField()


database.create_tables([Day, Weather])


class Updater:

    def __init__(self, days_dict, date_from=0, date_to=0):
        self.db = database
        self.days_dict = days_dict
        self.date_from = date_from
        self.date_to = date_to

    def write_data_to_db(self):
        for day, data in self.days_dict.items():
            try:
                Day(name=day).save()
                Weather.insert_many(data).execute()
            except peewee.IntegrityError:
                pass

    def get_data_from_db(self):
        return Weather.select().where(Weather.day_id.between(self.date_from, self.date_to))



# days_dict = ImportWeatherData().days_dict
# # print(days_dict)
# #
# day_start = 23
# day_end = 28
# Updater(days_dict, day_start, day_end).write_data_to_db()
# Updater(days_dict, day_start, day_end).get_data_from_db()


if __name__ == "__main__":
    Updater()
#
# from Weather.import_weather_data import ImportWeatherData
#
#
# class Updater:  TODO А вот класс можно оставить, который будет работать с БД
# TODO и иметь 2 метода - запись данных в базу(с перезаписью старый записей)
# TODO - получение данных из базы (по диапазону дат)
#
#     def __init__(self, days_dict):
#         self.days_dict = days_dict
#         self.database = peewee.SqliteDatabase('db/updater_weather.db')
#         self.run()
#
#     def run(self):
#         class DatabaseUpdater(peewee.Model):
#             class Meta:
#                 database = self.database
#
#         class Day(DatabaseUpdater):
#             name = peewee.CharField()
#
#         class Weather(DatabaseUpdater):
#             day = peewee.ForeignKeyField(Day)
#             day_of_week = peewee.CharField()
#             month = peewee.CharField()
#             min_temperature = peewee.CharField()
#             max_temperature = peewee.CharField()
#             weather = peewee.CharField()
#
#         self.database.create_tables([Day, Weather])
#
#         for day, data in self.days_dict.items():
#             Day(name=day).save()
#             Weather.insert_many(data).execute()
#
#
# if __name__ == "__main__":
#     Updater(ImportWeatherData().days_dict).run()
