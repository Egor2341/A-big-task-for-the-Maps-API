import os
import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt

SCREEN_SIZE = [600, 500]


class Example(QWidget):
    def __init__(self, lon, lat, z):
        super().__init__()
        self.lon = lon
        self.lat = lat
        self.z = z
        self.layer = "map"
        self.inp = QLineEdit(self)
        self.inp.move(0, 450)
        self.search = QPushButton(self)
        self.search.move(0, 475)
        self.search.setText("Искать")
        self.search.clicked.connect(self.run)
        self.res = QPushButton(self)
        self.res.move(100, 475)
        self.res.setText("Сброс поискового результата")
        self.res.clicked.connect(self.reset)
        self.mark = False
        self.address = QLineEdit(self)
        self.address.setGeometry(200, 450, 350, 25)
        self.adrs = []
        self.i = 1
        self.getImage()
        self.initUI()

    def reset(self):
        self.mark = False
        self.inp.setText("")
        self.address.setText("")
        self.pixmap = QPixmap(self.getImage())
        self.image.setPixmap(self.pixmap)

    def run(self):
        if len(self.inp.text()) > 0:
            api_server = "http://geocode-maps.yandex.ru/1.x/"

            params = {
                "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
                "geocode": self.inp.text(),
                "format": "json"
            }
            response = requests.get(api_server, params=params)

            if response:
                self.adrs = []
                json_response = response.json()
                toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
                toponym_coodrinates = toponym["Point"]["pos"]
                if "postal_code" in toponym["metaDataProperty"]["GeocoderMetaData"]["Address"]:
                    self.address.setText(str(toponym["metaDataProperty"]["GeocoderMetaData"]["text"] + "," + " " +
                                             toponym["metaDataProperty"]["GeocoderMetaData"]["Address"]["postal_code"]))
                else:
                    self.address.setText(toponym["metaDataProperty"]["GeocoderMetaData"]["text"])

                for a in json_response["response"]["GeoObjectCollection"]["featureMember"]:
                    if "postal_code" in a["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["Address"]:
                        self.adrs.append([a["GeoObject"]["Point"]["pos"],
                                          a["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["text"] + "," + " " +
                                          a["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["Address"][
                                              "postal_code"]])
                    else:
                        self.adrs.append([a["GeoObject"]["Point"]["pos"],
                                          a["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["text"]])


                self.lat, self.lon = toponym_coodrinates.split()[1], toponym_coodrinates.split()[0]
                self.mark = True
                self.pixmap = QPixmap(self.getImage())
                self.image.setPixmap(self.pixmap)

            else:
                print("Ошибка выполнения запроса:")

    def getImage(self):
        if not self.mark:
            api_server = "http://static-maps.yandex.ru/1.x/"

            params = {
                "ll": ",".join([self.lon, self.lat]),
                "z": str(self.z),
                "l": self.layer
            }
            response = requests.get(api_server, params=params)

            if not response:
                print("Ошибка выполнения запроса:")
                print("Http статус:", response.status_code, "(", response.reason, ")")
                sys.exit(1)


            self.map_file = "map.png"
            with open(self.map_file, "wb") as file:
                file.write(response.content)
            return self.map_file
        api_server = "http://static-maps.yandex.ru/1.x/"

        params = {
            "ll": ",".join([self.lon, self.lat]),
            "z": str(self.z),
            "l": self.layer,
            "pt": ",".join([self.lon, self.lat, "pm2rdm"])
        }
        response = requests.get(api_server, params=params)

        if not response:
            print("Ошибка выполнения запроса:")
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        return self.map_file

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            if self.z <= 18:
                self.z += 1
                self.pixmap = QPixmap(self.getImage())
                self.image.setPixmap(self.pixmap)

        elif event.key() == Qt.Key_PageDown:
            if self.z >= 1:
                self.z -= 1
                self.pixmap = QPixmap(self.getImage())
                self.image.setPixmap(self.pixmap)

        elif event.key() == Qt.Key_F1:
            if self.layer == "map":
                self.layer = "sat"
                self.pixmap = QPixmap(self.getImage())
                self.image.setPixmap(self.pixmap)

            elif self.layer == "sat":
                self.layer = ",".join(["sat", "skl"])
                self.pixmap = QPixmap(self.getImage())
                self.image.setPixmap(self.pixmap)

            else:
                self.layer = "map"
                self.pixmap = QPixmap(self.getImage())
                self.image.setPixmap(self.pixmap)
        elif event.key() == Qt.Key_F2:

            if len(self.adrs) > 1:
                if self.i != len(self.adrs) - 1:
                    self.lat, self.lon = self.adrs[self.i][0].split()[1], self.adrs[self.i][0].split()[0]
                    self.pixmap = QPixmap(self.getImage())
                    self.image.setPixmap(self.pixmap)
                    self.i += 1

                else:
                    self.i = 0
                    self.lat, self.lon = self.adrs[self.i][0].split()[1], self.adrs[self.i][0].split()[0]
                    self.pixmap = QPixmap(self.getImage())
                    self.image.setPixmap(self.pixmap)
                    self.i += 1

    def closeEvent(self, event):
        os.remove(self.map_file)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example("37.530887", "55.703118", 10)
    ex.show()
    sys.exit(app.exec())
