from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import vtk
from vtk.qt.QVTKRenderWindowInteractor import *


class Ui_MainWindow(QWidget):
    '''
    def __init__(self):
        super().__init__()
        self.hasLoadBeenVisited = False
        self.frame = QFrame()
        self.initUI()
    '''

    def initUI(self):
        # CZĘŚ APLIKACJI Z WYKRESAMI
        hboxw1 = QHBoxLayout()
        lbl = QLabel("Choose city:")
        hboxw1.addWidget(lbl)

        dropdown1 = QComboBox()
        dropdown1.addItem("Warszawa")
        dropdown1.addItem("Kraków")
        dropdown1.addItem("Poznań")
        hboxw1.addWidget(dropdown1)

        # CZĘŚ APLIKACJI Z MAPĄ POLSKI
        hbox1 = QHBoxLayout()
        lbl = QLabel("Choose date:")
        hbox1.addWidget(lbl)

        dropdown1 = QComboBox()
        dropdown1.addItem("16.01.19")
        dropdown1.addItem("17.01.19")
        dropdown1.addItem("18.01.19")
        hbox1.addWidget(dropdown1)

        self.pushButton = QPushButton()
        self.pushButton.setText("")
        icon = QIcon()
        icon.addPixmap(QPixmap("images/arrow-circle-225.png"), QIcon.Normal, QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setObjectName("pushButton")
        hbox1.addWidget(self.pushButton)

        hbox3 = QHBoxLayout()

        lbl = QLabel("Humidity: ")
        hbox3.addWidget(lbl)

        self.humidityLabel = QLabel()
        self.humidityLabel.setText("")
        self.humidityLabel.setObjectName("humidityLabel")
        hbox3.addWidget(self.humidityLabel)

        hbox4 = QHBoxLayout()

        lbl = QLabel("Temperature: ")
        hbox4.addWidget(lbl)

        self.temperatureLabel = QLabel()
        self.temperatureLabel.setText("")
        self.temperatureLabel.setObjectName("temperatureLabel")
        hbox4.addWidget(self.temperatureLabel)

        hbox5 = QHBoxLayout()

        lbl = QLabel("Pressure: ")
        hbox5.addWidget(lbl)

        self.pressureLabel = QLabel()
        self.pressureLabel.setText("")
        self.pressureLabel.setObjectName("pressureLabel")
        hbox5.addWidget(self.pressureLabel)

        hbox6 = QHBoxLayout()

        lbl = QLabel("Wind: ")
        hbox6.addWidget(lbl)

        self.windLabel = QLabel()
        self.windLabel.setText("")
        self.windLabel.setObjectName("windLabel")
        hbox6.addWidget(self.windLabel)

        # VTK PART
        self.humidityVariable = 10
        self.cubeSource = vtk.vtkCubeSource()
        self.cubeSource.SetCenter(430, 350, 0)
        self.cubeSource.SetXLength(10)
        self.cubeSource.SetYLength(10)
        self.cubeSource.SetZLength(self.humidityVariable)

        self.mapper = vtk.vtkPolyDataMapper()
        self.mapper.SetInputConnection(self.cubeSource.GetOutputPort())

        self.humidityActor = vtk.vtkActor()
        self.humidityActor.SetMapper(self.mapper)
        self.humidityActor.GetProperty().SetColor(0.0, 0.0, 1.0)

        #map of Poland

        hbox2 = QHBoxLayout()

        vtk_widget = QVTKRenderWindowInteractor(self.frame)

        png_reader = vtk.vtkPNGReader()
        png_reader.SetFileName("Polska.png")
        png_reader.Update()
        image_data = png_reader.GetOutput()

        image_actor = vtk.vtkImageActor()
        image_actor.SetInputData(image_data) #mb zła wersja

        self.ren = vtk.vtkRenderer()

        self.ren.AddActor(image_actor)

        #weather data
        self.ren.AddActor(self.humidityActor)

        self.render_window = vtk_widget.GetRenderWindow()

        self.render_window.AddRenderer(self.ren)

        render_window_interactor = vtk.vtkRenderWindowInteractor()
        render_window_interactor.SetRenderWindow(self.render_window)

        # 2 linijki poniżej regulują interaktor, nie wiem czemu nie działa.
        int_style = vtk.vtkInteractorStyleTrackballCamera()
        render_window_interactor.SetInteractorStyle(int_style)

        self.render_window.Render()

        vtk_widget.Initialize()
        vtk_widget.Start()
        hbox2.addWidget(vtk_widget)

        # END OF VTK PART

        mainhbox = QHBoxLayout()

        vbox1 = QVBoxLayout()
        vbox1.addLayout(hboxw1)

        vbox2 = QVBoxLayout()
        vbox2.addLayout(hbox1)

        vbox2.addLayout(hbox3)
        vbox2.addLayout(hbox4)
        vbox2.addLayout(hbox5)
        vbox2.addLayout(hbox6)

        vbox2.addLayout(hbox2)

        mainhbox.addLayout(vbox1)
        mainhbox.addLayout(vbox2)
        self.setLayout(mainhbox)
        self.show()

'''
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
'''