from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from MainWindow import Ui_MainWindow

from datetime import datetime
import json
import os
import sys
import requests
from urllib.parse import urlencode
import argparse
import vtk

OPENWEATHERMAP_API_KEY = 'e738a7fa3df63ebd9c57653a348c2972'
"""
Get an API key from https://openweathermap.org/ to use with this
application.
"""


def from_ts_to_time_of_day(ts):
    dt = datetime.fromtimestamp(ts)
    # %H - hour in 24 hours
    return dt.strftime("%H").lstrip("0")


class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.
    '''
    finished = pyqtSignal()
    error = pyqtSignal(str)
    result = pyqtSignal(dict, dict, dict, dict, dict)


class WeatherWorker(QRunnable):
    '''
    Worker thread for weather updates.
    '''
    signals = WorkerSignals()
    is_interrupted = False

    def __init__(self, location, location2, location3, location4):
        super(WeatherWorker, self).__init__()
        self.location = location
        self.location2 = location2
        self.location3 = location3
        self.location4 = location4

    def run(self):
        try:
            params = dict(
                q=self.location,
                appid=args.appid
            )
            params2 = dict(
                q=self.location2,
                appid=args.appid
            )
            params3 = dict(
                q=self.location3,
                appid=args.appid
            )
            params4 = dict(
                q=self.location4,
                appid=args.appid
            )

            if args.weather is not None:
                print(f"Reading weather information from file '{args.weather}'")
                with open(args.weather) as f:
                    weather = json.loads(f.read())
            else:
                url = 'http://api.openweathermap.org/data/2.5/weather?%s&units=metric' % urlencode(params)
                r = requests.get(url)
                weather = json.loads(r.text)
                print(weather)

                url2 = 'http://api.openweathermap.org/data/2.5/weather?%s&units=metric' % urlencode(params2)
                r2 = requests.get(url2)
                weather2 = json.loads(r2.text)
                print(weather2)

                url3 = 'http://api.openweathermap.org/data/2.5/weather?%s&units=metric' % urlencode(params3)
                r3 = requests.get(url3)
                weather3 = json.loads(r3.text)
                print(weather3)

                url4 = 'http://api.openweathermap.org/data/2.5/weather?%s&units=metric' % urlencode(params4)
                r4 = requests.get(url4)
                weather4 = json.loads(r4.text)
                print(weather4)


            # Check if we had a failure (the forecast will fail in the same way).
            if weather['cod'] != 200:
                raise Exception(weather['message'])

            if args.forecast is not None:
                print(f"Reading forecast from file '{args.forecast}'")
                with open(args.forecast) as f:
                    forecast = json.loads(f.read())
            else:
                url = 'http://api.openweathermap.org/data/2.5/forecast?%s&units=metric' % urlencode(params)
                r = requests.get(url)
                forecast = json.loads(r.text)

            # with open('warsaw_forecast.json', 'w') as f:
            #     f.write(r.text)

            self.signals.result.emit(weather, weather2, weather3, weather4, forecast)

        except Exception as e:
            self.signals.error.emit(str(e))

        self.signals.finished.emit()


class MainWindow(Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hasLoadBeenVisited = False
        self.frame = QFrame()
        self.initUI()

        self.pushButton.pressed.connect(self.update_weather)
        self.button1.toggled.connect(self.checkBut1)
        self.button2.toggled.connect(self.checkBut2)
        self.button3.toggled.connect(self.checkBut3)
        self.button4.toggled.connect(self.checkBut4)
        self.button5.toggled.connect(self.checkBut5)

        self.threadpool = QThreadPool()

        self.show()

    # checkbox methods

    def checkBut1(self):
        if self.button1.isChecked():
            self.ren.AddActor(self.tempActor)
            self.ren.AddActor(self.tempActor2)
            self.ren.AddActor(self.tempActor3)
            self.ren.AddActor(self.tempActor4)
            self.render_window.Render()
        else:
            self.ren.RemoveActor(self.tempActor)
            self.ren.RemoveActor(self.tempActor2)
            self.ren.RemoveActor(self.tempActor3)
            self.ren.RemoveActor(self.tempActor4)
            self.render_window.Render()

    def checkBut2(self):
        if self.button2.isChecked():
            self.ren.AddActor(self.pressActor)
            self.ren.AddActor(self.pressActor2)
            self.ren.AddActor(self.pressActor3)
            self.ren.AddActor(self.pressActor4)
            self.render_window.Render()
        else:
            self.ren.RemoveActor(self.pressActor)
            self.ren.RemoveActor(self.pressActor2)
            self.ren.RemoveActor(self.pressActor3)
            self.ren.RemoveActor(self.pressActor4)
            self.render_window.Render()

    def checkBut3(self):
        if self.button3.isChecked():
            self.ren.AddActor(self.cloudActor)
            self.ren.AddActor(self.cloudActor2)
            self.ren.AddActor(self.cloudActor3)
            self.ren.AddActor(self.cloudActor4)
            self.render_window.Render()
        else:
            self.ren.RemoveActor(self.cloudActor)
            self.ren.RemoveActor(self.cloudActor2)
            self.ren.RemoveActor(self.cloudActor3)
            self.ren.RemoveActor(self.cloudActor4)
            self.render_window.Render()

    def checkBut4(self):
        if self.button4.isChecked():
            self.ren.AddActor(self.coneActor)
            self.ren.AddActor(self.coneActor2)
            self.ren.AddActor(self.coneActor3)
            self.ren.AddActor(self.coneActor4)
            self.render_window.Render()
        else:
            self.ren.RemoveActor(self.coneActor)
            self.ren.RemoveActor(self.coneActor2)
            self.ren.RemoveActor(self.coneActor3)
            self.ren.RemoveActor(self.coneActor4)
            self.render_window.Render()

    def checkBut5(self):
        if self.button5.isChecked():
            self.ren.AddActor(self.humidityActor)
            self.ren.AddActor(self.humidityActor2)
            self.ren.AddActor(self.humidityActor3)
            self.ren.AddActor(self.humidityActor4)
            self.render_window.Render()
        else:
            self.ren.RemoveActor(self.humidityActor)
            self.ren.RemoveActor(self.humidityActor2)
            self.ren.RemoveActor(self.humidityActor3)
            self.ren.RemoveActor(self.humidityActor4)
            self.render_window.Render()


    def alert(self, message):
        alert = QMessageBox.warning(self, "Warning", message)


    def update_weather(self):
        worker = WeatherWorker("Warsaw","Krakow","Poznan, Pl","Gdansk")

        worker.signals.result.connect(self.weather_result)

        worker.signals.error.connect(self.alert)
        self.threadpool.start(worker)


    def weather_result(self, weather, weather2, weather3, weather4, forecasts):
        self.windLabel.setText("%.2f m/s" % weather['wind']['speed'])
        self.temperatureLabel.setText("%.1f °C" % weather['main']['temp'])
        self.pressureLabel.setText("%d" % weather['main']['pressure'])
        self.humidityLabel.setText("%d" % weather['main']['humidity'])

        for i in range (1,5):
            if i == 1:
                humidityVariable = weather['main']['humidity']
                cloudVariable = weather['clouds']['all']
                windSpeedVariable = weather['wind']['speed']
                tempVariable = weather['main']['temp']
                pressureVariable = weather['main']['pressure']
                cubeSource = self.cubeSource
                sphere = self.sphere1
                coneActor = self.coneActor
                tempActor = self.tempActor
                pressActor = self.pressActor
            elif i ==2:
                humidityVariable = weather2['main']['humidity']
                cloudVariable = weather2['clouds']['all']
                windSpeedVariable = weather2['wind']['speed']
                tempVariable = weather2['main']['temp']
                pressureVariable = weather2['main']['pressure']
                cubeSource = self.cubeSource2
                sphere = self.sphere2
                coneActor = self.coneActor2
                tempActor = self.tempActor2
                pressActor = self.pressActor2
            elif i ==3:
                humidityVariable = weather3['main']['humidity']
                cloudVariable = weather3['clouds']['all']
                windSpeedVariable = weather3['wind']['speed']
                tempVariable = weather3['main']['temp']
                pressureVariable = weather3['main']['pressure']
                cubeSource = self.cubeSource3
                sphere = self.sphere3
                coneActor = self.coneActor3
                tempActor = self.tempActor3
                pressActor = self.pressActor3
            elif i ==4:
                humidityVariable = weather4['main']['humidity']
                cloudVariable = weather4['clouds']['all']
                windSpeedVariable = weather4['wind']['speed']
                tempVariable = weather4['main']['temp']
                pressureVariable = weather4['main']['pressure']
                cubeSource = self.cubeSource4
                sphere = self.sphere4
                coneActor = self.coneActor4
                tempActor = self.tempActor4
                pressActor = self.pressActor4

            cubeSource.SetZLength(humidityVariable * 2)  # DZIWNA SPRAWA: ZADZWON / NAPISZ TO WYTŁUMACZE SKĄD TO *2
            sphere.SetRadius(cloudVariable / 4)

            if windSpeedVariable < 2:
                coneActor.GetProperty().SetColor(self.cols.GetColor3d("wind1"))
            elif windSpeedVariable < 4:
                coneActor.GetProperty().SetColor(self.cols.GetColor3d("wind2"))
            elif windSpeedVariable < 6:
                coneActor.GetProperty().SetColor(self.cols.GetColor3d("wind3"))
            elif windSpeedVariable < 8:
                coneActor.GetProperty().SetColor(self.cols.GetColor3d("wind4"))
            elif windSpeedVariable < 10:
                coneActor.GetProperty().SetColor(self.cols.GetColor3d("wind5"))
            elif windSpeedVariable < 12:
                coneActor.GetProperty().SetColor(self.cols.GetColor3d("wind6"))
            elif windSpeedVariable < 14:
                coneActor.GetProperty().SetColor(self.cols.GetColor3d("wind7"))
            else:
                coneActor.GetProperty().SetColor(self.cols.GetColor3d("wind8"))

            if tempVariable < -15:
                tempActor.GetProperty().SetColor(self.cols.GetColor3d("temp1"))
            elif tempVariable < -10:
                tempActor.GetProperty().SetColor(self.cols.GetColor3d("temp2"))
            elif tempVariable < -5:
                tempActor.GetProperty().SetColor(self.cols.GetColor3d("temp3"))
            elif tempVariable < 0:
                tempActor.GetProperty().SetColor(self.cols.GetColor3d("temp4"))
            elif tempVariable < 5:
                tempActor.GetProperty().SetColor(self.cols.GetColor3d("temp5"))
            elif tempVariable < 10:
                tempActor.GetProperty().SetColor(self.cols.GetColor3d("temp6"))
            elif tempVariable < 15:
                tempActor.GetProperty().SetColor(self.cols.GetColor3d("temp7"))
            elif tempVariable < 20:
                tempActor.GetProperty().SetColor(self.cols.GetColor3d("temp8"))
            elif tempVariable < 25:
                tempActor.GetProperty().SetColor(self.cols.GetColor3d("temp9"))
            else:
                tempActor.GetProperty().SetColor(self.cols.GetColor3d("temp10"))

            if pressureVariable < 950:
                pressActor.GetProperty().SetColor(self.cols.GetColor3d("pressure1"))
            elif pressureVariable < 960:
                pressActor.GetProperty().SetColor(self.cols.GetColor3d("pressure2"))
            elif pressureVariable < 970:
                pressActor.GetProperty().SetColor(self.cols.GetColor3d("pressure3"))
            elif pressureVariable < 980:
                pressActor.GetProperty().SetColor(self.cols.GetColor3d("pressure4"))
            elif pressureVariable < 990:
                pressActor.GetProperty().SetColor(self.cols.GetColor3d("pressure5"))
            elif pressureVariable < 1000:
                pressActor.GetProperty().SetColor(self.cols.GetColor3d("pressure6"))
            elif pressureVariable < 1010:
                pressActor.GetProperty().SetColor(self.cols.GetColor3d("pressure7"))
            elif pressureVariable < 1020:
                pressActor.GetProperty().SetColor(self.cols.GetColor3d("pressure8"))
            elif pressureVariable < 1030:
                pressActor.GetProperty().SetColor(self.cols.GetColor3d("pressure9"))
            else:
                pressActor.GetProperty().SetColor(self.cols.GetColor3d("pressure10"))

        self.render_window.Render()


if __name__ == '__main__':
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--forecast", type=str, help="Path to json file containing weather (this will be read instead of http request)")
    parser.add_argument("-w", "--weather", type=str, help="Path to json file containing weather (this will be read instead of http request)")
    parser.add_argument("-id", "--appid", type=str, help="Get an API key from https://openweathermap.org/ to use with this application.", default=OPENWEATHERMAP_API_KEY)
    args = parser.parse_args()

    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())