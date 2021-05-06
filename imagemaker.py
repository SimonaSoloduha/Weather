# -*- coding: utf-8 -*-
import os
import cv2


# from weathermaker import WeatherMaker


class ImageMaker:
    project = os.path.abspath(os.curdir)
    cards_directory = "cards"
    PATH_CARDS_DIRECTORY = os.path.join(project, cards_directory)
    os.makedirs(PATH_CARDS_DIRECTORY, exist_ok=True)

    def __init__(self, weather, path_cards_directory=PATH_CARDS_DIRECTORY):
        self.weather_image = None
        self.base = 'weather_img/probe.jpg'
        self.image = None
        # self.days_dict = days_dict
        self.weather = weather
        self.data = None
        self.font_size = 2
        self.font = cv2.FONT_HERSHEY_COMPLEX
        self.color_blue = (99, 32, 0)
        self.color_black = (0, 0, 0)
        self.color_grey = (99, 69, 0)
        self.color_text_date = None
        self.color_text_weather = None
        self.cloud_path = "weather_img/cloudy.png"
        self.rain_path = "weather_img/rain1.png"
        self.snow_path = "weather_img/snowflake.png"
        self.sun_path = "weather_img/sun.png"
        self.path_cards_directory = path_cards_directory
        self.run()

    def run(self):
        self.select_image_and_color()
        self.add_image_in_image()
        self.maker_card_add_text()
        self.save(self.image, self.weather.day_id)

    def select_image_and_color(self):
        if 'облачн' in self.weather.weather.lower():
            self.weather_image = self.cloud_path
            self.image = self.point_color(1)
            self.color_text_date = (0, 0, 0)
            self.color_text_weather = (99, 32, 0)
        if 'солн' in self.weather.weather.lower():
            self.weather_image = self.sun_path
            self.image = self.point_color(2)
            self.color_text_date = (0, 0, 0)
            self.color_text_weather = (75, 0, 130)
        if 'дож' in self.weather.weather.lower():
            self.weather_image = self.rain_path
            self.image = self.point_color(3)
            self.color_text_date = (255, 255, 255)
            self.color_text_weather = (175, 238, 238)
        if 'сне' in self.weather.weather.lower():
            self.weather_image = self.snow_path
            self.image = self.point_color(1)
            self.color_text_date = (0, 0, 0)
            self.color_text_weather = (99, 32, 0)

    def point_color(self, color=7):
        # TODO я имел ввиду, что можно получить параметром цвет, например (0, 0, 255)
        # TODO и рисовать линию, изменяя цвет от (0,0,255) до (255,255,255)
        # TODO и так в целом можно с любым цветом - увеличивать, пока не придём к 255 255 255
        # grey
        image_base = cv2.imread(self.base)
        start = 0
        step = 2
        b = 255
        g = 255
        r = 255
        delta_b = 1
        delta_g = 1
        delta_r = 1
        end = step
        if color == 1:
            # 1 - blue white
            delta_b = 0
            delta_g = 2
            delta_r = 2
        elif color == 2:
            # 2 - yellow white
            delta_b = 2
            delta_g = 0
            delta_r = 0
        elif color == 3:
            # 3 - blue black
            b = 0
            g = 0
            r = 0
            delta_b = -1
            delta_g = 0
            delta_r = 0
        while end <= 256:
            image_base[start:end, :] = (b, g, r)
            start = end
            end += step
            b -= delta_b
            g -= delta_g
            r -= delta_r
        return image_base

    def add_image_in_image(self):
        image_base = self.image
        weather_image = cv2.imread(self.weather_image)

        scale_percent = 25
        width = int(weather_image.shape[1] * scale_percent / 100)
        height = int(weather_image.shape[0] * scale_percent / 100)
        dim = (width, height)
        weather_image = cv2.resize(weather_image, dim, interpolation=cv2.INTER_AREA)

        rows, cols, channels = weather_image.shape
        roi = image_base[0:rows, 0:cols]

        img2gray = cv2.cvtColor(weather_image, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)

        image_base_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
        weather_image_fg = cv2.bitwise_and(weather_image, weather_image, mask=mask)

        dst = cv2.add(image_base_bg, weather_image_fg)
        image_base[50:rows + 50, 270:cols + 270] = dst

        return image_base

    def maker_card_add_text(self):
        cv2.putText(self.image, f'{self.weather.day_of_week}', (70, 80), self.font, 0.5,
                    self.color_text_date, 1, cv2.LINE_AA)
        cv2.putText(self.image, f'{self.weather.day_id}', (70, 110), self.font, 0.4,
                    self.color_text_date, 1, cv2.LINE_AA)
        cv2.putText(self.image, f'{self.weather.month}', (70, 140), self.font, 0.4,
                    self.color_text_date, 1, cv2.LINE_AA)
        cv2.putText(self.image, f'{self.weather.weather}', (20, 20), self.font, 0.4,
                    self.color_text_weather, 1, cv2.LINE_AA)
        cv2.putText(self.image, f'Минимальная температура: {self.weather.min_temperature}', (200, 200), self.font, 0.35,
                    self.color_text_weather, 1, cv2.LINE_AA)
        cv2.putText(self.image, f'Максимальная температура: {self.weather.max_temperature}', (200, 220), self.font,
                    0.35,
                    self.color_text_weather, 1, cv2.LINE_AA)

    def save(self, image, day):
        path = os.path.join(self.cards_directory, f'{self.weather.month}')
        path = os.path.normpath(path)
        os.makedirs(path, exist_ok=True)
        cv2.imwrite(f'{path}/{day}.jpg', image)

    def viewImage(self, image, name_of_window):
        cv2.namedWindow(name_of_window, cv2.WINDOW_NORMAL)
        cv2.imshow(name_of_window, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__mane__":
    ImageMaker.run()
