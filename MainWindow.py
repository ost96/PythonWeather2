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
        #colors
        self.cols = vtk.vtkNamedColors()
        self.cols.SetColor("wind1", [87, 243, 55, 255])
        self.cols.SetColor("wind2", [33, 175, 5, 255])
        self.cols.SetColor("wind3", [18, 104, 1, 255])
        self.cols.SetColor("wind4", [241, 247, 65, 255])
        self.cols.SetColor("wind5", [247, 255, 0, 255])
        self.cols.SetColor("wind6", [245, 151, 11, 255])
        self.cols.SetColor("wind7", [253, 64, 51, 255])
        self.cols.SetColor("wind8", [206, 14, 0, 255])

        self.cols.SetColor("temp1", [13, 242, 51, 255])
        self.cols.SetColor("temp2", [51, 242, 13, 255])
        self.cols.SetColor("temp3", [39, 196, 8, 255])
        self.cols.SetColor("temp4", [23, 138, 0, 255])
        self.cols.SetColor("temp5", [240, 255, 95, 255])
        self.cols.SetColor("temp6", [223, 247, 0, 255])
        self.cols.SetColor("temp7", [228, 150, 48, 255])
        self.cols.SetColor("temp8", [255, 145, 0, 255])
        self.cols.SetColor("temp9", [239, 60, 60, 255])
        self.cols.SetColor("temp10", [255, 0, 0, 255])

        self.cols.SetColor("pressure1", [0, 255, 213, 255])
        self.cols.SetColor("pressure2", [44, 196, 171, 255])
        self.cols.SetColor("pressure3", [44, 115, 196, 255])
        self.cols.SetColor("pressure4", [0, 68, 255, 255])
        self.cols.SetColor("pressure5", [0, 20, 146, 255])
        self.cols.SetColor("pressure6", [198, 115, 246, 255])
        self.cols.SetColor("pressure7", [138, 0, 218, 255])
        self.cols.SetColor("pressure8", [255, 0, 230, 255])
        self.cols.SetColor("pressure9", [226, 200, 223, 255])
        self.cols.SetColor("pressure10", [176, 176, 176, 255])

        ##############################################
        # WARSAW actors

        #humidity
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

        #wind
        cone = vtk.vtkConeSource()
        cone.SetHeight(35)
        cone.SetRadius(12)
        cone.SetResolution(60)
        cone.SetCenter(430, 310, 20)

        '''
        transform = vtk.vtkTransform()
        #transform.RotateWXYZ(90, 0, 0, 1)
        #transform.RotateZ(90)                     Brzydko działa, nie wiem co z tym zrobić

        transformFilter = vtk.vtkTransformPolyDataFilter()
        transformFilter.SetTransform(transform)
        transformFilter.SetInputConnection(cone.GetOutputPort())
        transformFilter.Update()
        '''
        coneMapper = vtk.vtkPolyDataMapper()
        coneMapper.SetInputConnection(cone.GetOutputPort())

        self.coneActor = vtk.vtkActor()
        self.coneActor.SetMapper(coneMapper)
        self.coneActor.GetProperty().SetColor(self.cols.GetColor3d("wind1"))

        #cloud

        self.sphere1 = vtk.vtkSphereSource()
        self.sphere1.SetCenter(430, 320, 50)
        self.sphere1.SetRadius(10)

        self.cloudMapper = vtk.vtkPolyDataMapper()
        self.cloudMapper.SetInputConnection(self.sphere1.GetOutputPort())

        self.cloudActor = vtk.vtkActor()
        self.cloudActor.SetMapper(self.cloudMapper)
        self.cloudActor.GetProperty().SetColor(0.1, 0.4, 0.6)

        #temperature square
        self.tempSource = vtk.vtkCubeSource()
        self.tempSource.SetCenter(415, 310, 0)
        self.tempSource.SetXLength(30)
        self.tempSource.SetYLength(30)
        self.tempSource.SetZLength(1)

        self.tempmapper = vtk.vtkPolyDataMapper()
        self.tempmapper.SetInputConnection(self.tempSource.GetOutputPort())

        self.tempActor = vtk.vtkActor()
        self.tempActor.SetMapper(self.tempmapper)
        self.tempActor.GetProperty().SetColor(self.cols.GetColor3d("temp1"))

        # pressure square
        self.pressSource = vtk.vtkCubeSource()
        self.pressSource.SetCenter(445, 310, 0)
        self.pressSource.SetXLength(30)
        self.pressSource.SetYLength(30)
        self.pressSource.SetZLength(1)

        self.pressmapper = vtk.vtkPolyDataMapper()
        self.pressmapper.SetInputConnection(self.pressSource.GetOutputPort())

        self.pressActor = vtk.vtkActor()
        self.pressActor.SetMapper(self.pressmapper)
        self.pressActor.GetProperty().SetColor(self.cols.GetColor3d("pressure1"))

        ###########################################################################

        # Cracow actors

        # humidity
        self.humidityVariable2 = 10
        self.cubeSource2 = vtk.vtkCubeSource()
        self.cubeSource2.SetCenter(380, 120, 0)
        self.cubeSource2.SetXLength(10)
        self.cubeSource2.SetYLength(10)
        self.cubeSource2.SetZLength(self.humidityVariable2)

        self.mapper2 = vtk.vtkPolyDataMapper()
        self.mapper2.SetInputConnection(self.cubeSource2.GetOutputPort())

        self.humidityActor2 = vtk.vtkActor()
        self.humidityActor2.SetMapper(self.mapper2)
        self.humidityActor2.GetProperty().SetColor(0.0, 0.0, 1.0)

        # wind
        cone2 = vtk.vtkConeSource()
        cone2.SetHeight(35)
        cone2.SetRadius(12)
        cone2.SetResolution(60)
        cone2.SetCenter(380, 80, 20)

        coneMapper2 = vtk.vtkPolyDataMapper()
        coneMapper2.SetInputConnection(cone2.GetOutputPort())

        self.coneActor2 = vtk.vtkActor()
        self.coneActor2.SetMapper(coneMapper2)
        self.coneActor2.GetProperty().SetColor(self.cols.GetColor3d("wind1"))

        # cloud

        self.sphere2 = vtk.vtkSphereSource()
        self.sphere2.SetCenter(380, 80, 50)
        self.sphere2.SetRadius(10)

        self.cloudMapper2 = vtk.vtkPolyDataMapper()
        self.cloudMapper2.SetInputConnection(self.sphere2.GetOutputPort())

        self.cloudActor2 = vtk.vtkActor()
        self.cloudActor2.SetMapper(self.cloudMapper2)
        self.cloudActor2.GetProperty().SetColor(0.1, 0.4, 0.6)

        # temperature square
        self.tempSource2 = vtk.vtkCubeSource()
        self.tempSource2.SetCenter(365, 80, 0)
        self.tempSource2.SetXLength(30)
        self.tempSource2.SetYLength(30)
        self.tempSource2.SetZLength(1)

        self.tempmapper2 = vtk.vtkPolyDataMapper()
        self.tempmapper2.SetInputConnection(self.tempSource2.GetOutputPort())

        self.tempActor2 = vtk.vtkActor()
        self.tempActor2.SetMapper(self.tempmapper2)
        self.tempActor2.GetProperty().SetColor(self.cols.GetColor3d("temp1"))

        # pressure square
        self.pressSource2 = vtk.vtkCubeSource()
        self.pressSource2.SetCenter(395, 80, 0)
        self.pressSource2.SetXLength(30)
        self.pressSource2.SetYLength(30)
        self.pressSource2.SetZLength(1)

        self.pressmapper2 = vtk.vtkPolyDataMapper()
        self.pressmapper2.SetInputConnection(self.pressSource2.GetOutputPort())

        self.pressActor2 = vtk.vtkActor()
        self.pressActor2.SetMapper(self.pressmapper2)
        self.pressActor2.GetProperty().SetColor(self.cols.GetColor3d("pressure1"))


        ###############################################################
        # Poznan actors

        # humidity
        self.humidityVariable3 = 10
        self.cubeSource3 = vtk.vtkCubeSource()
        self.cubeSource3.SetCenter(160, 360, 0)
        self.cubeSource3.SetXLength(10)
        self.cubeSource3.SetYLength(10)
        self.cubeSource3.SetZLength(self.humidityVariable3)

        self.mapper3 = vtk.vtkPolyDataMapper()
        self.mapper3.SetInputConnection(self.cubeSource3.GetOutputPort())

        self.humidityActor3 = vtk.vtkActor()
        self.humidityActor3.SetMapper(self.mapper3)
        self.humidityActor3.GetProperty().SetColor(0.0, 0.0, 1.0)

        # wind
        cone3 = vtk.vtkConeSource()
        cone3.SetHeight(35)
        cone3.SetRadius(12)
        cone3.SetResolution(60)
        cone3.SetCenter(160, 330, 20)

        coneMapper3 = vtk.vtkPolyDataMapper()
        coneMapper3.SetInputConnection(cone3.GetOutputPort())

        self.coneActor3 = vtk.vtkActor()
        self.coneActor3.SetMapper(coneMapper3)
        self.coneActor3.GetProperty().SetColor(self.cols.GetColor3d("wind1"))

        # cloud

        self.sphere3 = vtk.vtkSphereSource()
        self.sphere3.SetCenter(160, 330, 50)
        self.sphere3.SetRadius(10)

        self.cloudMapper3 = vtk.vtkPolyDataMapper()
        self.cloudMapper3.SetInputConnection(self.sphere3.GetOutputPort())

        self.cloudActor3 = vtk.vtkActor()
        self.cloudActor3.SetMapper(self.cloudMapper3)
        self.cloudActor3.GetProperty().SetColor(0.1, 0.4, 0.6)

        # temperature square
        self.tempSource3 = vtk.vtkCubeSource()
        self.tempSource3.SetCenter(145, 330, 0)
        self.tempSource3.SetXLength(30)
        self.tempSource3.SetYLength(30)
        self.tempSource3.SetZLength(1)

        self.tempmapper3 = vtk.vtkPolyDataMapper()
        self.tempmapper3.SetInputConnection(self.tempSource3.GetOutputPort())

        self.tempActor3 = vtk.vtkActor()
        self.tempActor3.SetMapper(self.tempmapper3)
        self.tempActor3.GetProperty().SetColor(self.cols.GetColor3d("temp1"))

        # pressure square
        self.pressSource3 = vtk.vtkCubeSource()
        self.pressSource3.SetCenter(175, 330, 0)
        self.pressSource3.SetXLength(30)
        self.pressSource3.SetYLength(30)
        self.pressSource3.SetZLength(1)

        self.pressmapper3 = vtk.vtkPolyDataMapper()
        self.pressmapper3.SetInputConnection(self.pressSource3.GetOutputPort())

        self.pressActor3 = vtk.vtkActor()
        self.pressActor3.SetMapper(self.pressmapper3)
        self.pressActor3.GetProperty().SetColor(self.cols.GetColor3d("pressure1"))

        ###############################################################
        # Gdansk actors

        # humidity
        self.humidityVariable4 = 10
        self.cubeSource4 = vtk.vtkCubeSource()
        self.cubeSource4.SetCenter(260, 560, 0)
        self.cubeSource4.SetXLength(10)
        self.cubeSource4.SetYLength(10)
        self.cubeSource4.SetZLength(self.humidityVariable4)

        self.mapper4 = vtk.vtkPolyDataMapper()
        self.mapper4.SetInputConnection(self.cubeSource4.GetOutputPort())

        self.humidityActor4 = vtk.vtkActor()
        self.humidityActor4.SetMapper(self.mapper4)
        self.humidityActor4.GetProperty().SetColor(0.0, 0.0, 1.0)

        # wind
        cone4 = vtk.vtkConeSource()
        cone4.SetHeight(35)
        cone4.SetRadius(12)
        cone4.SetResolution(60)
        cone4.SetCenter(260, 530, 20)

        coneMapper4 = vtk.vtkPolyDataMapper()
        coneMapper4.SetInputConnection(cone4.GetOutputPort())

        self.coneActor4 = vtk.vtkActor()
        self.coneActor4.SetMapper(coneMapper4)
        self.coneActor4.GetProperty().SetColor(self.cols.GetColor3d("wind1"))

        # cloud

        self.sphere4 = vtk.vtkSphereSource()
        self.sphere4.SetCenter(260, 530, 50)
        self.sphere4.SetRadius(10)

        self.cloudMapper4 = vtk.vtkPolyDataMapper()
        self.cloudMapper4.SetInputConnection(self.sphere4.GetOutputPort())

        self.cloudActor4 = vtk.vtkActor()
        self.cloudActor4.SetMapper(self.cloudMapper4)
        self.cloudActor4.GetProperty().SetColor(0.1, 0.4, 0.6)

        # temperature square
        self.tempSource4 = vtk.vtkCubeSource()
        self.tempSource4.SetCenter(245, 530, 0)
        self.tempSource4.SetXLength(30)
        self.tempSource4.SetYLength(30)
        self.tempSource4.SetZLength(1)

        self.tempmapper4 = vtk.vtkPolyDataMapper()
        self.tempmapper4.SetInputConnection(self.tempSource4.GetOutputPort())

        self.tempActor4 = vtk.vtkActor()
        self.tempActor4.SetMapper(self.tempmapper4)
        self.tempActor4.GetProperty().SetColor(self.cols.GetColor3d("temp1"))

        # pressure square
        self.pressSource4 = vtk.vtkCubeSource()
        self.pressSource4.SetCenter(275, 530, 0)
        self.pressSource4.SetXLength(30)
        self.pressSource4.SetYLength(30)
        self.pressSource4.SetZLength(1)

        self.pressmapper4 = vtk.vtkPolyDataMapper()
        self.pressmapper4.SetInputConnection(self.pressSource4.GetOutputPort())

        self.pressActor4 = vtk.vtkActor()
        self.pressActor4.SetMapper(self.pressmapper4)
        self.pressActor4.GetProperty().SetColor(self.cols.GetColor3d("pressure1"))

        ###############################################################

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

        #weather data actors
        self.ren.AddActor(self.humidityActor)
        self.ren.AddActor(self.coneActor)
        self.ren.AddActor(self.cloudActor)
        self.ren.AddActor(self.tempActor)
        self.ren.AddActor(self.pressActor)

        self.ren.AddActor(self.humidityActor2)
        self.ren.AddActor(self.coneActor2)
        self.ren.AddActor(self.cloudActor2)
        self.ren.AddActor(self.tempActor2)
        self.ren.AddActor(self.pressActor2)

        self.ren.AddActor(self.humidityActor3)
        self.ren.AddActor(self.coneActor3)
        self.ren.AddActor(self.cloudActor3)
        self.ren.AddActor(self.tempActor3)
        self.ren.AddActor(self.pressActor3)

        self.ren.AddActor(self.humidityActor4)
        self.ren.AddActor(self.coneActor4)
        self.ren.AddActor(self.cloudActor4)
        self.ren.AddActor(self.tempActor4)
        self.ren.AddActor(self.pressActor4)

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