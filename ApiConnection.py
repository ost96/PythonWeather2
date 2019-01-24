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
    result = pyqtSignal(dict, dict)


class WeatherWorker(QRunnable):
    '''
    Worker thread for weather updates.
    '''
    signals = WorkerSignals()
    is_interrupted = False

    def __init__(self, location):
        super(WeatherWorker, self).__init__()
        self.location = location

    def run(self):
        try:
            params = dict(
                q=self.location,
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
                # with open('warsaw_weather.json', 'w') as f:
                #     f.write(r.text)

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

            self.signals.result.emit(weather, forecast)

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

        self.threadpool = QThreadPool()

        self.show()

    def alert(self, message):
        alert = QMessageBox.warning(self, "Warning", message)


    def update_weather(self):
        worker = WeatherWorker("Warsaw")
        worker.signals.result.connect(self.weather_result)
        worker.signals.error.connect(self.alert)
        self.threadpool.start(worker)


    def weather_result(self, weather, forecasts):
        self.windLabel.setText("%.2f m/s" % weather['wind']['speed'])
        self.temperatureLabel.setText("%.1f °C" % weather['main']['temp'])
        self.pressureLabel.setText("%d" % weather['main']['pressure'])
        self.humidityLabel.setText("%d" % weather['main']['humidity'])

        self.humidityVariable = weather['main']['humidity']
        self.cloudVariable = weather['clouds']['all']
        self.windSpeedVariable = weather['wind']['speed']
        self.tempVariable = weather['main']['temp']
        self.pressureVariable = weather['main']['pressure']

        self.cubeSource.SetZLength(self.humidityVariable * 2) # DZIWNA SPRAWA: ZADZWON / NAPISZ TO WYTŁUMACZE SKĄD TO *2
        self.sphere1.SetRadius(self.cloudVariable/4)

        if self.windSpeedVariable < 2:
            self.coneActor.GetProperty().SetColor(self.cols.GetColor3d("wind1"))
        elif self.windSpeedVariable < 4:
            self.coneActor.GetProperty().SetColor(self.cols.GetColor3d("wind2"))
        elif self.windSpeedVariable < 6:
            self.coneActor.GetProperty().SetColor(self.cols.GetColor3d("wind3"))
        elif self.windSpeedVariable < 8:
            self.coneActor.GetProperty().SetColor(self.cols.GetColor3d("wind4"))
        elif self.windSpeedVariable < 10:
            self.coneActor.GetProperty().SetColor(self.cols.GetColor3d("wind5"))
        elif self.windSpeedVariable < 12:
            self.coneActor.GetProperty().SetColor(self.cols.GetColor3d("wind6"))
        elif self.windSpeedVariable < 14:
            self.coneActor.GetProperty().SetColor(self.cols.GetColor3d("wind7"))
        else:
            self.coneActor.GetProperty().SetColor(self.cols.GetColor3d("wind8"))

        if self.tempVariable < -15:
            self.tempActor.GetProperty().SetColor(self.cols.GetColor3d("temp1"))
        elif self.tempVariable < -10:
            self.tempActor.GetProperty().SetColor(self.cols.GetColor3d("temp2"))
        elif self.tempVariable < -5:
            self.tempActor.GetProperty().SetColor(self.cols.GetColor3d("temp3"))
        elif self.tempVariable < 0:
            self.tempActor.GetProperty().SetColor(self.cols.GetColor3d("temp4"))
        elif self.tempVariable < 5:
            self.tempActor.GetProperty().SetColor(self.cols.GetColor3d("temp5"))
        elif self.tempVariable < 10:
            self.tempActor.GetProperty().SetColor(self.cols.GetColor3d("temp6"))
        elif self.tempVariable < 15:
            self.tempActor.GetProperty().SetColor(self.cols.GetColor3d("temp7"))
        elif self.tempVariable < 20:
            self.tempActor.GetProperty().SetColor(self.cols.GetColor3d("temp8"))
        elif self.tempVariable < 25:
            self.tempActor.GetProperty().SetColor(self.cols.GetColor3d("temp9"))
        else:
            self.tempActor.GetProperty().SetColor(self.cols.GetColor3d("temp10"))

        if self.pressureVariable < 950:
            self.pressActor.GetProperty().SetColor(self.cols.GetColor3d("pressure1"))
        elif self.pressureVariable < 960:
            self.pressActor.GetProperty().SetColor(self.cols.GetColor3d("pressure2"))
        elif self.pressureVariable < 970:
            self.pressActor.GetProperty().SetColor(self.cols.GetColor3d("pressure3"))
        elif self.pressureVariable < 980:
            self.pressActor.GetProperty().SetColor(self.cols.GetColor3d("pressure4"))
        elif self.pressureVariable < 990:
            self.pressActor.GetProperty().SetColor(self.cols.GetColor3d("pressure5"))
        elif self.pressureVariable < 1000:
            self.pressActor.GetProperty().SetColor(self.cols.GetColor3d("pressure6"))
        elif self.pressureVariable < 1010:
            self.pressActor.GetProperty().SetColor(self.cols.GetColor3d("pressure7"))
        elif self.pressureVariable < 1020:
            self.pressActor.GetProperty().SetColor(self.cols.GetColor3d("pressure8"))
        elif self.pressureVariable < 1030:
            self.pressActor.GetProperty().SetColor(self.cols.GetColor3d("pressure9"))
        else:
            self.pressActor.GetProperty().SetColor(self.cols.GetColor3d("pressure10"))


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