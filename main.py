import os
import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

SCREEN_SIZE = [600, 450]





class Example(QWidget):
    def __init__(self, lon, lat, delta):
        super().__init__()
        self.lon = lon
        self.lat = lat
        self.delta = delta
        self.getImage()
        self.initUI()


    def getImage(self):
        api_server = "http://static-maps.yandex.ru/1.x/"



        params = {
            "ll": ",".join([self.lon, self.lat]),
            "spn": ",".join([self.delta, self.delta]),
            "l": "map"
        }
        response = requests.get(api_server, params=params)

        if not response:
            print("Ошибка выполнения запроса:")
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        ## Изображение
        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example("37.530887", "55.703118", "0.002")
    ex.show()
    sys.exit(app.exec())
