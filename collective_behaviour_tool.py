# Last update 02/02/2021

# Se importan los paquetes necesarios para el correcto funcionamiento de la
# aplicación
import numpy as np
from sklearn.neighbors import NearestNeighbors, KDTree
from PyQt5 import QtCore, QtGui, QtWidgets
import os
import csv
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPalette, QFont
from PyQt5.QtWidgets import QFileDialog, QWidget, QLabel, QMessageBox, QGraphicsLineItem, QGraphicsEllipseItem, QCheckBox, QSplitter, QSlider, QGraphicsTextItem
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, qApp, QPushButton, QVBoxLayout, QHBoxLayout, QAbstractItemView, QColorDialog, QInputDialog
from PyQt5.QtCore import QLineF, Qt
from math import sqrt
import statistics
import cv2
import imutils
import time
import imageio
from scipy.spatial import ConvexHull
from tqdm import tqdm
import re
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm

# Listado de variables, listados, arrays, boolean y otros empleados
# para el almacenamiento y procesado de datos
tiburonesTotales = 0
cargarDatos = False
valuesXTail = []
valuesYTail = []
valuesXHead = []
valuesYHead = []
imag_loaded = True
imagePath = None
doubleClick = True
deleteIt = False
perimeterClick = False
perAnalyze = False
measureClick = False
valuesXMed = []
valuesYMed = []
vec_u = []
vec_v = []
midPointList = []
indexList = []
neighList = []
angleList = []
sizes = []
average_size = 0
average_angle = 0
valCenterMassX = 0
valCenterMassY = 0
perimeterPointList = []
valuesXPerimeter = []
valuesYPerimeter = []
s_values = []
s_pointList = []
v_values = []

calcGrosor = 5 # 11
calcGrosorAnalyzed = 4 # 10

# Variables fichero configuración de Preferencias
color_labelled_data = "#000000"
color_labelled_analyzed_data = "#008000"
color_perimeter = "#ff0000"
color_vector1 = "#0000ff"
color_vector2 = "#ff0000"
color_dot1 = "#0000ff"
color_dot2 = "#008000"
color_layers = "#0000ff"
number_of_layers = 255
percentage_subsampling = 100

convexXHull = []
convexYHull = []
convexPointList = []
valXInsideConvexHull = []
valYInsideConvexHull = []
densityCalculated = False
heatMapColorValues = []
files = []
filesXPoints = []
filesYPoints = []
filesXPointsCenter = []
filesYPointsCenter = []
readFilesLong = []
schoolVelocity = 0
timElapse = 0
nameofFileFiltered = None
perimeterSaved = False

# Directorio por defecto, se puede modificar al renombrar el folder deseado
# al comenzar con el programa
renameFolderName = "imagesToAnalyze/"

veldir_vec_u = []
veldir_vec_v = []
veldir_velocity = []
veldir_angle = []
veldir_position = []
maxRangeValue = 255
framesGenerated = False
errorAnalyzing = False
filasActuales = 0
empty_row = True
gifFileName = None
formato = None


# Variables para el calculo y mostrado de la superficie de una ROI seleccionada
# por el usuario
dist_pixeles = 0
dist_cm = 0
ratio_cm_pixel = 0
ratio_cm_pixel_cuadrado = 0
measure_pointList = []
posOfArrays = []
areaROI = 0
areaROI_cm = 0
cte_pos_x = 2
cte_pos_y = 12

primeraLlamada = False
areaCalculated = False ###-




# Definicion de la clase del menu de Preferencias dentro del apartado de Opciones
class OptionsMenu(QtWidgets.QWidget):

    def __init__(self):
        super(OptionsMenu, self).__init__()

        # Se definen todos los botones y apartados de configuracion dentro del
        # menu de preferencias
        self.setWindowTitle('Preferences')
        self.setGeometry(800,300,100,300)
        self.labelling_title = QtWidgets.QLabel('Labelling')
        self.labelling_title.setStyleSheet("border-bottom-width: 1px; border-bottom-style: solid; border-radius: 0px; font: bold 14px")
        self.analysis_title = QtWidgets.QLabel('Analysis')
        self.analysis_title.setStyleSheet("border-bottom-width: 1px; border-bottom-style: solid; border-radius: 0px; font: bold 14px")
        self.savePreferencesButton = QPushButton('Save Preferences')
        self.labelled_data_color = QPushButton()
        self.labelled_data_color.setStyleSheet("background-color: black")
        self.perimeter_color = QPushButton()
        self.perimeter_color.setStyleSheet("background-color: green")
        self.vector1_color = QPushButton()
        self.vector1_color.setStyleSheet("background-color: red")
        self.vector2_color = QPushButton()
        self.vector2_color.setStyleSheet("background-color: blue")
        self.dot1_color = QPushButton()
        self.dot1_color.setStyleSheet("background-color: red")
        self.dot2_color = QPushButton()
        self.dot2_color.setStyleSheet("background-color: blue")
        self.layers_color = QPushButton()
        self.layers_color.setStyleSheet("background-color: blue")
        self.slider_layers = QSlider(Qt.Horizontal)
        self.slider_layers.setFocusPolicy(Qt.StrongFocus)
        self.slider_layers.setTickPosition(QSlider.TicksBelow)
        self.slider_layers.setTickInterval(40)
        self.slider_layers.setSingleStep(1)
        self.slider_layers.setMaximum(255)

        self.slider_subsampling = QSlider(Qt.Horizontal)
        self.slider_subsampling.setFocusPolicy(Qt.StrongFocus)
        self.slider_subsampling.setTickPosition(QSlider.TicksBelow)
        self.slider_subsampling.setTickInterval(10)
        self.slider_subsampling.setSingleStep(1)
        self.slider_subsampling.setMaximum(100)

        #self.slider_layers.setValue(number_of_layers)
        self.labelled_analyzed_data_color = QPushButton()
        self.labelled_analyzed_data_color.setStyleSheet("background-color: green")
        self.labelled_data_label = QtWidgets.QLabel('Labelled data')
        self.labelled_analyzed_data_label = QtWidgets.QLabel('Labelled data analyzed')
        self.perimeter_label = QtWidgets.QLabel('Perimeter')
        self.vector1_label = QtWidgets.QLabel('Aligned individuals')
        self.vector2_label = QtWidgets.QLabel('Non-aligned individuals')
        self.dot1_label = QtWidgets.QLabel('Close neighbors')
        self.dot2_label = QtWidgets.QLabel('Far neighbors')
        self.layers_label = QtWidgets.QLabel('Density map increments')
        self.layers_value = QtWidgets.QLabel("0")

        self.subsampling_label = QtWidgets.QLabel('3D Density map subsampling %')
        self.subsampling_value = QtWidgets.QLabel("0")

        # Se conectan los diferentes elementos del menu de Preferencias
        self.labelled_data_color.clicked.connect(self.labelled_data_color_dialog)
        self.perimeter_color.clicked.connect(self.perimeter_color_dialog)
        self.vector1_color.clicked.connect(self.vector1_color_dialog)
        self.vector2_color.clicked.connect(self.vector2_color_dialog)
        self.dot1_color.clicked.connect(self.dot1_color_dialog)
        self.dot2_color.clicked.connect(self.dot2_color_dialog)
        self.labelled_analyzed_data_color.clicked.connect(self.labelled_analyzed_data_color_dialog)
        self.layers_color.clicked.connect(self.layers_color_dialog)
        self.savePreferencesButton.clicked.connect(self.saveDataInTextFile)
        self.slider_layers.valueChanged.connect(self.changeValue)

        self.slider_subsampling.valueChanged.connect(self.changeSubsamplingValue)

        # Se añaden al layout los diferentes elementos del menu de Preferencias
        grid = QtWidgets.QGridLayout(self)
        grid.addWidget(self.labelling_title,0,0)
        grid.addWidget(self.labelled_data_label,1,0)
        grid.addWidget(self.labelled_data_color,1,1)
        grid.addWidget(self.analysis_title,2,0)
        grid.addWidget(self.labelled_analyzed_data_label,3,0)
        grid.addWidget(self.labelled_analyzed_data_color,3,1)
        grid.addWidget(self.perimeter_label,4,0)
        grid.addWidget(self.perimeter_color,4,1)
        grid.addWidget(self.vector1_label,5,0)
        grid.addWidget(self.vector1_color,5,1)
        grid.addWidget(self.vector2_label,6,0)
        grid.addWidget(self.vector2_color,6,1)
        grid.addWidget(self.dot1_label,7,0)
        grid.addWidget(self.dot1_color,7,1)
        grid.addWidget(self.dot2_label,8,0)
        grid.addWidget(self.dot2_color,8,1)
        grid.addWidget(self.layers_label,9,0)
        grid.addWidget(self.slider_layers,10,0)
        grid.addWidget(self.layers_value,10,1)
        grid.addWidget(self.layers_color,10,2)

        grid.addWidget(self.subsampling_label,11,0)
        grid.addWidget(self.slider_subsampling,12,0)
        grid.addWidget(self.subsampling_value,12,1)

        grid.addWidget(self.savePreferencesButton,13,0)


        # En caso de que exista un fichero de configuracion previo, se cargan
        # dichos valores a la aplicación
        if os.path.exists('config.txt') == True:
            global color_labelled_data
            global color_perimeter
            global color_vector1
            global color_vector2
            global color_dot1
            global color_dot2
            global color_labelled_analyzed_data
            global number_of_layers
            global color_layers
            global percentage_subsampling

            file = open("config.txt","r")

            string = file.readline()
            color_labelled_data = string[:-1]
            self.labelled_data_color.setStyleSheet("QWidget { background-color: %s}" % color_labelled_data)
            string = file.readline()
            color_perimeter = string[:-1]
            self.perimeter_color.setStyleSheet("QWidget { background-color: %s}" % color_perimeter)
            string = file.readline()
            color_vector1 = string[:-1]
            self.vector1_color.setStyleSheet("QWidget { background-color: %s}" % color_vector1)
            string = file.readline()
            color_vector2 = string[:-1]
            self.vector2_color.setStyleSheet("QWidget { background-color: %s}" % color_vector2)
            string = file.readline()
            color_dot1 = string[:-1]
            self.dot1_color.setStyleSheet("QWidget { background-color: %s}" % color_dot1)
            string = file.readline()
            color_dot2 = string[:-1]
            self.dot2_color.setStyleSheet("QWidget { background-color: %s}" % color_dot2)
            string = file.readline()
            color_labelled_analyzed_data = string[:-1]
            self.labelled_analyzed_data_color.setStyleSheet("QWidget { background-color: %s}" % color_labelled_analyzed_data)
            string = file.readline()
            number_of_layers = int(string[:-1])
            self.layers_value.setText(str(number_of_layers))
            self.slider_layers.setValue(number_of_layers)
            string = file.readline()
            color_layers = string[:-1]
            self.layers_color.setStyleSheet("QWidget { background-color: %s}" % color_layers)

            string = file.readline()
            percentage_subsampling = int(string[:-1])
            self.subsampling_value.setText(str(percentage_subsampling))
            self.slider_subsampling.setValue(percentage_subsampling)

        # Si no existe el fichero de configuracion, se crea uno nuevo
        else:
            color_labelled_data = self.labelled_data_color.palette().color(QtGui.QPalette.Base).name()
            color_perimeter = self.perimeter_color.palette().color(QtGui.QPalette.Base).name()
            color_vector1 = self.vector1_color.palette().color(QtGui.QPalette.Base).name()
            color_vector2 = self.vector2_color.palette().color(QtGui.QPalette.Base).name()
            color_dot1 = self.dot1_color.palette().color(QtGui.QPalette.Base).name()
            color_dot2 = self.dot2_color.palette().color(QtGui.QPalette.Base).name()
            color_labelled_analyzed_data = self.labelled_analyzed_data_color.palette().color(QtGui.QPalette.Base).name()
            color_layers = self.layers_color.palette().color(QtGui.QPalette.Base).name()
            self.slider_layers.setValue(number_of_layers)
            self.slider_subsampling.setValue(percentage_subsampling)

    # Funcion para cambiar el numero de capas de densidad
    def changeValue(self,val):
        global number_of_layers
        number_of_layers = val
        self.layers_value.setText(str(val))

    # Funcion para cambiar el porcentaje de submuestreo de puntos del mapa de densidad 3D
    def changeSubsamplingValue(self,val):
        global percentage_subsampling
        percentage_subsampling = val
        self.subsampling_value.setText(str(val))

    # Funcion para almacenar el fichero de configuracion en el disco
    def saveDataInTextFile(self):

        global color_labelled_data
        global color_perimeter
        global color_vector1
        global color_vector2
        global color_dot1
        global color_dot2
        global color_labelled_analyzed_data
        global number_of_layers
        global color_layers
        global percentage_subsampling

        file = open("config.txt","w")

        file.write(color_labelled_data+"\n")
        file.write(color_perimeter+"\n")
        file.write(color_vector1+"\n")
        file.write(color_vector2+"\n")
        file.write(color_dot1+"\n")
        file.write(color_dot2+"\n")
        file.write(color_labelled_analyzed_data+"\n")
        file.write(str(number_of_layers)+"\n")
        file.write(color_layers+"\n")
        file.write(str(percentage_subsampling)+"\n")
        file.close()
        self.hide()

    # Funcion para escoger tonalidades de color elegidas por el usuario para
    # los mapas de densidad
    def layers_color_dialog(self):
        global color_layers
        color_layers = QColorDialog.getColor()

        # Si el color escogido por el usuario es valido se selecciona dicho color
        # en caso contrario se carga uno por defecto
        if color_layers.isValid():
            self.layers_color.setStyleSheet("QWidget { background-color: %s}" % color_layers.name())
            color_layers = color_layers.name()
        else:
            color_layers = self.layers_color.palette().color(QtGui.QPalette.Base).name()

        # Se buscan todas las tonalidades existentes desde la seleccionada
        parte_R = color_layers[1:3]
        cant_R = int(parte_R,16)
        parte_G = color_layers[3:5]
        cant_G = int(parte_G,16)
        parte_B = color_layers[5:7]
        cant_B = int(parte_B,16)
        maximum = self.maximumOfRGB(cant_R,cant_G,cant_B)
        self.slider_layers.setMaximum(maximum)

    # Funcion para obtener el maximo entre las coordenadas R,G,B de un color
    def maximumOfRGB(self,r,g,b):
        list = [r,g,b]
        return max(list)

    # Funcion para escoger el color deseado por el usuario para los datos de
    # etiquetado
    def labelled_data_color_dialog(self):
        global color_labelled_data
        color_labelled_data = QColorDialog.getColor()
        if color_labelled_data.isValid():
            self.labelled_data_color.setStyleSheet("QWidget { background-color: %s}" % color_labelled_data.name())
            color_labelled_data = color_labelled_data.name()
        else:
            color_labelled_data = self.labelled_data_color.palette().color(QtGui.QPalette.Base).name()

    # Funcion para escoger el color deseado por el usuario para los datos de
    # perimetro
    def perimeter_color_dialog(self):
        global color_perimeter
        color_perimeter = QColorDialog.getColor()
        if color_perimeter.isValid():
            self.perimeter_color.setStyleSheet("QWidget { background-color: %s}" % color_perimeter.name())
            color_perimeter = color_perimeter.name()
        else:
            color_perimeter = self.perimeter_color.palette().color(QtGui.QPalette.Base).name()

    # Funcion para escoger el color deseado por el usuario para los datos de
    # los vectores - 1
    def vector1_color_dialog(self):
        global color_vector1
        color_vector1 = QColorDialog.getColor()
        if color_vector1.isValid():
            self.vector1_color.setStyleSheet("QWidget { background-color: %s}" % color_vector1.name())
            color_vector1 = color_vector1.name()
        else:
            color_vector1 = self.vector1_color.palette().color(QtGui.QPalette.Base).name()

    # Funcion para escoger el color deseado por el usuario para los datos de
    # los vectores - 2
    def vector2_color_dialog(self):
        global color_vector2
        color_vector2 = QColorDialog.getColor()
        if color_vector2.isValid():
            self.vector2_color.setStyleSheet("QWidget { background-color: %s}" % color_vector2.name())
            color_vector2 = color_vector2.name()
        else:
            color_vector2 = self.vector2_color.palette().color(QtGui.QPalette.Base).name()

    # Funcion para escoger el color deseado por el usuario para los datos de
    # los centros de cada animal etiquetado - 1
    def dot1_color_dialog(self):
        global color_dot1
        color_dot1 = QColorDialog.getColor()
        if color_dot1.isValid():
            self.dot1_color.setStyleSheet("QWidget { background-color: %s}" % color_dot1.name())
            color_dot1 = color_dot1.name()
        else:
            color_dot1 = self.dot1_color.palette().color(QtGui.QPalette.Base).name()

    # Funcion para escoger el color deseado por el usuario para los datos de
    # los centros de cada animal etiquetado - 2
    def dot2_color_dialog(self):
        global color_dot2
        color_dot2 = QColorDialog.getColor()
        if color_dot2.isValid():
            self.dot2_color.setStyleSheet("QWidget { background-color: %s}" % color_dot2.name())
            color_dot2 = color_dot2.name()
        else:
            color_dot2 = self.dot2_color.palette().color(QtGui.QPalette.Base).name()

    # Funcion para escoger el color deseado por el usuario para los datos de
    # analisis de los datos
    def labelled_analyzed_data_color_dialog(self):
        global color_labelled_analyzed_data
        color_labelled_analyzed_data = QColorDialog.getColor()
        if color_labelled_analyzed_data.isValid():
            self.labelled_analyzed_data_color.setStyleSheet("QWidget { background-color: %s}" % color_labelled_analyzed_data.name())
            color_labelled_analyzed_data = color_labelled_analyzed_data.name()
        else:
            color_labelled_analyzed_data = self.labelled_analyzed_data_color.palette().color(QtGui.QPalette.Base).name()

# Definicion de la clase de la interfaz de Análisis Avanzada para el estudio
# del movimiento de escuelas
class WindowResults(QtWidgets.QWidget):

    # Señales para comunicarse entre diferentes clases
    hideandshowSignal = QtCore.pyqtSignal()
    rePaintAfterDensity = QtCore.pyqtSignal()

    # Inicializacion de la clase
    def __init__(self):
        super(WindowResults, self).__init__()

        # Se definen todos los botones, etiquetas y listados de dicha interfaz
        # avanzada
        self.setWindowTitle('Results of Analysis - Vectors')
        self.setGeometry(100,100,700,600) #600,600
        self.viewerRes = PhotoVectorViewer(self)
        self.savebtn = QPushButton('Save Analyzed Image')
        self.backtolabel = QPushButton('Back to Labelling Menu')
        self.savegifbtn = QPushButton('Save as gif')
        self.savegifbtn.setVisible(False)
        self.savevideobtn = QPushButton('Save as video')
        self.savevideobtn.setVisible(False)
        self.editPixMassCenter = QtWidgets.QLineEdit(self)
        self.editPixMassCenter.setReadOnly(True)
        self.centermassVals = QtWidgets.QLabel('Mass Center Coord: ')

        # Listado de checkboxs
        self.cb_labelled = QCheckBox('Show labelled data')
        self.cb_analyzed = QCheckBox('Show analyzed data')
        self.cb_perimeter = QCheckBox('Show data perimeter')
        self.cb_density = QCheckBox('Show image density')
        self.cb_3Ddensity = QCheckBox('Show 3D map density')

        # Se conectan los diferentes elementos
        self.cb_labelled.stateChanged.connect(self.drawStuff)
        self.cb_analyzed.stateChanged.connect(self.drawStuff)
        self.cb_perimeter.stateChanged.connect(self.drawStuff)
        self.cb_density.stateChanged.connect(self.drawHeatMap)
        self.cb_3Ddensity.stateChanged.connect(self.draw3DHeatMap)
        self.savebtn.clicked.connect(self.selecteds)
        self.backtolabel.clicked.connect(self.backmenu)
        self.viewerRes.editMassCenter.connect(self.editMassCenter)
        self.viewerRes.reDrawStuff.connect(self.drawStuff)
        self.viewerRes.editVelocityLabel.connect(self.editLabelVelocity)
        self.savegifbtn.clicked.connect(self.viewerRes.saveAnimation)
        self.savevideobtn.clicked.connect(self.viewerRes.saveVideo)
        self.rePaintAfterDensity.connect(self.viewerRes.rePaintAfterDensity)

        # Se configura la disposicion de los diferentes elementos en la GUI
        MainLayout = QtWidgets.QHBoxLayout(self)
        VBlayout = QtWidgets.QVBoxLayout()
        VBlayout1 = QtWidgets.QVBoxLayout()
        HBlayout = QtWidgets.QHBoxLayout()
        HBlayout1 = QtWidgets.QHBoxLayout()

        HBlayout.addWidget(self.savebtn)
        HBlayout.addWidget(self.savegifbtn)
        HBlayout.addWidget(self.savevideobtn)
        HBlayout1.addWidget(self.centermassVals)
        HBlayout1.addWidget(self.editPixMassCenter)
        VBlayout.addWidget(self.viewerRes)
        VBlayout.addLayout(HBlayout1)
        VBlayout.addLayout(HBlayout)
        VBlayout1.addWidget(self.cb_labelled)
        VBlayout1.addWidget(self.cb_analyzed)
        VBlayout1.addWidget(self.cb_perimeter)
        VBlayout1.addWidget(self.cb_density)
        VBlayout1.addWidget(self.cb_3Ddensity)
        VBlayout1.addStretch(1)
        VBlayout1.addWidget(self.backtolabel)
        MainLayout.addLayout(VBlayout)
        MainLayout.addLayout(VBlayout1)


    # Funcion para regresar a la Interfaz básica o de etiquetado
    def backmenu(self):
        global densityCalculated
        global perimeterSaved

        # Se borran las imagenes de caché en caso de existir
        if densityCalculated == True:
            os.remove("cache_heatmap.JPG")
        self.hide()
        self.hideandshowSignal.emit()

        # Se reinician los checkbox y las variables de analisis pertinentes
        self.cb_labelled.setChecked(False)
        self.cb_analyzed.setChecked(False)
        self.cb_perimeter.setChecked(False)
        self.cb_density.setChecked(False)
        self.cb_3Ddensity.setChecked(False)

        densityCalculated = False
        perimeterSaved = False

    # Funcion para guardar la imagen analizada en el disco
    def selecteds(self,q):
        self.viewerRes.saveImageAnalyzed()

    # Funcion para pintar el mapa de densidad 3D
    def draw3DHeatMap(self):
        if self.cb_3Ddensity.isChecked():
            # Nos aseguramos de que se haya calculado anteriormente la densidad
            self.cb_density.setChecked(True)
            self.drawHeatMap()
            self.cb_density.setChecked(False)
            # Se calcula el mapa 3D
            self.viewerRes.Density3DProcess()

    # Funcion para pintar el mapa de densidad 2D
    def drawHeatMap(self):
        global perAnalyze
        global imagePath

        if self.cb_density.isChecked():
            if densityCalculated == False:
                if perAnalyze == True:
                    self.pixmap = QPixmap(imagePath)
                    self.viewerRes.setPhoto(self.pixmap)
                    self.viewerRes.DensityProcess(1)
                else:
                    self.pixmap = QPixmap(imagePath)
                    self.viewerRes.setPhoto(self.pixmap)
                    self.viewerRes.DensityProcess(0)
            else:
                self.pixmap = QPixmap("cache_heatmap.JPG")
                self.viewerRes.setPhoto(self.pixmap)
                self.rePaintAfterDensity.emit()
        else:
            cv2.destroyAllWindows()
            self.viewerRes.resetView(4)
            self.pixmap = QPixmap(imagePath)
            self.viewerRes.setPhoto(self.pixmap)
            self.rePaintAfterDensity.emit()

    # Funcion de pintado de datos en la interfaz avanzada
    def drawStuff(self):
        self.viewerRes.resetView(3)
        if self.cb_labelled.isChecked():
            self.viewerRes.drawLoadedData(0)
        else:
            self.viewerRes.resetView(0)
        if self.cb_analyzed.isChecked():
            self.viewerRes.drawLoadedData(1)
        else:
            self.viewerRes.resetView(1)
        if self.cb_perimeter.isChecked():
            if perAnalyze == True:
                self.viewerRes.ImageProcess(1,1)
            else:
                self.viewerRes.ImageProcess(0,1)
        else:
            self.viewerRes.resetView(2)
            self.viewerRes.resetView(7)

    # Funcion para editar el valor del dentro de masas
    def editMassCenter(self):
        self.editPixMassCenter.setText('%d, %d' % (valCenterMassX,valCenterMassY))

    # Funcion para editar la etiqueta con la velocidad de la escuela
    def editLabelVelocity(self):
        global schoolVelocity
        self.centermassVals.setText("Average school velocity (pixels/s): ")
        self.editPixMassCenter.setText('%d' % schoolVelocity)


# Clase que contiene la tabla con los datos analizados marcados por el usuario
class DataResults(QtWidgets.QTableWidget):
    # Se inicializa la clase
    def __init__(self, r, c):
        super(DataResults,self).__init__(r, c)
        self.setWindowTitle('Results of Analysis - Data')
        col_headers = ['Tail X', 'Tail Y', 'Head X', 'Head Y', 'X med', 'Y med','u','v','Index','Distance','Angle']
        self.setHorizontalHeaderLabels(col_headers)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # Se calculan las dimensiones de la ventana de forma dinamica en función
        # de los datos que haya
        dim = self.calcDimension(r)
        if dim > 600:
            dim = 600
        self.setGeometry(750,100,1120,dim)
        self.show()

    # Funcion para calcular las dimensiones de la tabla de datos
    def calcDimension(self,r):
        total = r*30+40
        return total

    # Funcion para almacenar la tabla en el disco
    def save_sheet(self,var):
        cacheDir = None
        cacheType = None
        cacheTitle = None
        cacheInfo = None

        if var == 0: #Datos sin analizar
            cacheDir = 'labelledData'
            cacheType = "_labelled"
            cacheTitle = 'Labelled data saved'
            cacheInfo = "Labelled data has been saved sucessfully"

        elif var == 1: #Datos analizados
            cacheDir = 'analyzedData'
            cacheType = "_analyzed"
            cacheTitle = 'Analyzed data saved'
            cacheInfo = "Analyzed data has been saved sucessfully"
        elif var == 2: #VelDir analizado
            cacheDir = 'analyzedSchool'
            cacheType = "_analyzedSchool"
            cacheTitle = 'School analyzed data saved'
            cacheInfo = "School analyzed data has been saved sucessfully"

        #Creamos directory o comprobamos si existe
        dirName = cacheDir
        if not os.path.exists(dirName):
            os.mkdir(dirName)
        else:
            pass
        global nameofFileFiltered
        path = cacheDir + "/" + nameofFileFiltered + cacheType +".csv"
        if path != '':
            with open(path, 'w') as csv_file:
                writer = csv.writer(csv_file, dialect='excel')
                for row in range(self.rowCount()):
                    row_data = []
                    for column in range(self.columnCount()):
                        item = self.item(row, column)
                        if item is not None:
                            row_data.append(item.text())
                        else:
                            row_data.append('')
                    writer.writerow(row_data)
        self.msg = QtWidgets.QMessageBox.about(self,cacheTitle,cacheInfo)

# Clase que contiene la Interfaz avanzada con las opciones de analisis para el
# estudio de colectivos
class PhotoVectorViewer(QtWidgets.QGraphicsView):
    # Se crean señales para comunicar diferentes clases
    editMassCenter = QtCore.pyqtSignal()
    reDrawStuff = QtCore.pyqtSignal()
    editVelocityLabel = QtCore.pyqtSignal()
    editVelDirTable = QtCore.pyqtSignal()

    global ratio_cm_pixel
    # Funcion de inicializacion
    def __init__(self,parent):
        super(PhotoVectorViewer,self).__init__()
        # Se inicializan las dimensiones, fotos, y datos de interes
        self.handDrag = False
        self._zoom = 0
        self._empty = True
        self._scene = QtWidgets.QGraphicsScene(self)
        self._photo = QtWidgets.QGraphicsPixmapItem()
        self._scene.addItem(self._photo)
        self.setScene(self._scene)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(30, 30, 30)))
        self.setFrameShape(QtWidgets.QFrame.NoFrame)


    # Funcion que comprueba si existe una foto cargada en la interfaz
    def hasPhoto(self):
        return not self._empty

    # Funcion que ajusta la imagen al rectangulo diseñado para visualizar imagenes
    def fitInView(self, scale=True):
        rect = QtCore.QRectF(self._photo.pixmap().rect())
        if not rect.isNull():
            self.setSceneRect(rect)
            if self.hasPhoto():
                unity = self.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
                self.scale(1 / unity.width(), 1 / unity.height())
                viewrect = self.viewport().rect()
                scenerect = self.transform().mapRect(rect)
                factor = min(viewrect.width() / scenerect.width(),
                             viewrect.height() / scenerect.height())
                self.scale(factor, factor)
            self._zoom = 0

    # Función que asigna la imagen al rectangulo diseñado para visualizar imagenes
    def setPhoto(self, pixmap=None):
        self._zoom = 0
        if pixmap and not pixmap.isNull():
            #Al cargar una imagen se reinician las variables de interes
            self._scene.clear()
            self._photo = QtWidgets.QGraphicsPixmapItem()
            self._scene.addItem(self._photo)
            self._empty = False
            global imag_loaded
            imag_loaded = self._empty
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag) #ScrollHandDrag
            self._photo.setPixmap(pixmap)

            # Redimensiono la escena en funcion de la imagen nueva
            self._scene.width = pixmap.width
            self._scene.height = pixmap.height

            #print("[INFO] Cargo una imagen en analisis con unas dimensiones X,Y: {}, {}".format(self._scene.width(), self._scene.height()))

            # Se pinta para que se reescale el grosor de los items
            #self.rePaintWithZoom(self._zoom) ##-

        else:
            self._empty = True
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
            self._photo.setPixmap(QtGui.QPixmap())
        self.fitInView()

    # Funcion para hacer zoom en la imagen con la ruleta
    def wheelEvent(self, event):
        if self.hasPhoto():
            if event.angleDelta().y() > 0:
                factor = 1.25
                self._zoom += 1
            else:
                factor = 0.8
                self._zoom -= 1
            if self._zoom > 0:
                self.scale(factor, factor)
            elif self._zoom == 0:
                pass
                self.fitInView()
            else:
                self._zoom = 0
        self.rePaintWithZoom(self._zoom)

    # Funcion para repintar los datos en funcion del zoom tras pintar la densidad
    def rePaintAfterDensity(self):

        self.rePaintWithZoom(self._zoom)

    # Funcion para repintar los datos en funcion del zoom
    def rePaintWithZoom(self,zoom):

        global calcGrosorAnalyzed
        global perAnalyze
        global convexXHull
        del convexXHull[:]
        global convexYHull
        del convexYHull[:]
        x = self._scene.width()
        y = self._scene.height()

        zoomPararestar = 9
        calcGrosor_max = 10

        '''
        if x >= 3800 and y >= 2100:
            calcGrosor_max = 10
            zoomPararestar = 9
        elif x < 3800 and x >= 2300 and y < 2100 and y >= 1500:
            calcGrosor_max = 7
            zoomPararestar = 6
        elif x < 2300 and x >= 1250 and y < 1500 and y >= 700:
            calcGrosor_max = 4
            zoomPararestar = 3
        else:
            calcGrosor_max = 2
            zoomPararestar = 1
        '''

        if x >= 3800 or y >= 2100:
            calcGrosor_max = 10
            zoomPararestar = 9
        elif x < 3800 and x >= 2300 or y < 2100 and y >= 1500:
            calcGrosor_max = 7
            zoomPararestar = 6
        elif x < 2300 and x >= 1250 or y < 1500 and y >= 700:
            calcGrosor_max = 4
            zoomPararestar = 3
        else:
            calcGrosor_max = 2
            zoomPararestar = 1

        if zoom <= zoomPararestar:
            calcGrosorAnalyzed = calcGrosor_max-zoom
        else:
            calcGrosorAnalyzed = 1

        #print("[INFO] X,Y: {}, {}, Zoom: {}, Zoom para restar: {}, Grosor calculado: {}, Grosor maximo: {}".format(x, y, zoom, zoomPararestar, calcGrosorAnalyzed, calcGrosor_max))

        self.resetView(3)
        self.resetView(2)
        self.resetView(1)
        self.resetView(0)
        self.reDrawStuff.emit()

    # Funcion para generar fotogramas analizados y almacenarlos individualmente
    def generateFrames(self):

        # Se modifica el contenido de las variables listadas debajo
        global filesXPoints
        global filesYPoints
        global filesXPointsCenter
        global filesYPointsCenter
        global color_perimeter
        global readFilesLong
        global files
        global timElapse
        global renameFolderName
        global framesGenerated
        global veldir_angle
        global veldir_velocity
        global gifFileName
        global formato

        c = QtGui.QColor(color_perimeter)
        penGreen = QtGui.QPen(Qt.red,3)
        penPerimetro = QtGui.QPen(c,3)
        cantidad = len(filesXPoints)

        #Pintamos los perimetros y luego los puntos centrales en la imagen
        valorInicialRango = 0

        #Creamos directory o comprobamos si existe
        dirName = "framegeneratorGif"

        if not os.path.exists(dirName):
            os.mkdir(dirName)
        else:
            pass

        # Se muestran los ficheros
        for j in tqdm(range(0,len(readFilesLong))):
            nombreFichero = files[j].split('.')[0]
            gifFileName = nombreFichero
            fondo = renameFolderName + nombreFichero + "." + formato

            self.pixmap = QPixmap(fondo)
            self.setPhoto(self.pixmap)
            # Dibujo del perimetro
            for i in range(valorInicialRango,readFilesLong[j]-1):
                valXTail = int(filesXPoints[i])
                valYTail = int(filesYPoints[i])
                valXHead = int(filesXPoints[i+1])
                valYHead = int(filesYPoints[i+1])
                linea_item = QtWidgets.QGraphicsLineItem(valXTail,valYTail,valXHead,valYHead)
                linea_item.setPen(penPerimetro)
                linea_item.setData(1,6)
                self._scene.addItem(linea_item)
                self.setScene(self._scene)

            valXTail = int(filesXPoints[valorInicialRango])
            valYTail = int(filesYPoints[valorInicialRango])
            valXHead = int(filesXPoints[readFilesLong[j]-1])
            valYHead = int(filesYPoints[readFilesLong[j]-1])
            linea_item = QtWidgets.QGraphicsLineItem(valXTail,valYTail,valXHead,valYHead)
            linea_item.setPen(penPerimetro)
            linea_item.setData(1,6)
            self._scene.addItem(linea_item)
            self.setScene(self._scene)

            # Dibujo del centroide
            for k in range(0,j+1):
                rad = 5.0 #1.0 #5.0
                brush = QtGui.QBrush(Qt.SolidPattern)

                ellipse_item = QtWidgets.QGraphicsEllipseItem(int(filesXPointsCenter[k])-rad,int(filesYPointsCenter[k])-rad,rad*2.0,rad*2.0)
                ellipse_item.setPen(penGreen)
                ellipse_item.setBrush(brush)
                ellipse_item.setData(1,6)

                self._scene.addItem(ellipse_item)
                self.setScene(self._scene)

            # Dibujo flecha
            for i in range(0,j):

                valXHead = int(filesXPointsCenter[i+1])
                valXTail = int(filesXPointsCenter[i])
                valYHead = int(filesYPointsCenter[i+1])
                valYTail = int(filesYPointsCenter[i])
                linea_item = QtWidgets.QGraphicsLineItem(valXTail,valYTail,valXHead,valYHead)
                linea_item.setData(1,6)
                linea_item.setPen(penGreen)

                dX = valXHead - valXTail
                dY = valYHead - valYTail
                Len = sqrt(dX* dX + dY * dY)
                udX = dX / Len
                udY = dY / Len
                perpX = -udY
                perpY = udX

                L = 10 #longitud cabeza vector 2 #20
                H = 3 #anchura vector 4 #6

                leftX = valXHead - L * udX + H * perpX
                leftY = valYHead - L * udY + H * perpY
                rightX = valXHead - L * udX - H * perpX
                rightY = valYHead - L * udY - H * perpY

                vector_flecha_1 = QtCore.QLineF(valXHead,valYHead,leftX,leftY)
                vector_flecha_2 = QtCore.QLineF(valXHead,valYHead,rightX,rightY)

                linea_item_flecha_1 = QtWidgets.QGraphicsLineItem(vector_flecha_1)
                linea_item_flecha_1.setPen(penGreen)
                linea_item_flecha_2 = QtWidgets.QGraphicsLineItem(vector_flecha_2)
                linea_item_flecha_2.setPen(penGreen)
                linea_item_flecha_1.setData(1,6)
                linea_item_flecha_2.setData(1,6)
                self._scene.addItem(linea_item)
                self._scene.addItem(linea_item_flecha_1)
                self._scene.addItem(linea_item_flecha_2)
                self.setScene(self._scene)
            # Dibujo del texto en el fotograma
            for i in range(j-1,j):
                separacion = int( self._scene.height() / 195 )
                if i == -1:
                    texto = QtWidgets.QGraphicsTextItem(" ")
                elif i == 0:
                    texto = QtWidgets.QGraphicsTextItem("v: "+str(veldir_velocity[i]))
                else:
                    texto = QtWidgets.QGraphicsTextItem("v: "+str(veldir_velocity[i])+" , a: "+ str(veldir_angle[i-1]))
                texto.setPos(int(filesXPointsCenter[i+1]),int(filesYPointsCenter[i+1])-separacion)

                font = QFont()
                font.setBold(True)
                texto.setFont(font)
                self._scene.addItem(texto)
                self.setScene(self._scene)

            valorInicialRango = readFilesLong[j]

            # Se guarda cada fotograma generado del gif
            rect = QtCore.QRectF(self._photo.pixmap().rect())
            image = QtGui.QImage(rect.width(),rect.height(), QImage.Format_ARGB32_Premultiplied)
            painter = QtGui.QPainter(image)
            self._scene.render(painter)
            painter.end()
            image.save("framegeneratorGif/"+nombreFichero+"_frameGif"+".JPG")
        framesGenerated = True

    # Funcion para guardar el analisis en formato GIF
    def saveAnimation(self):
        global framesGenerated
        global gifFileName

        if framesGenerated == False:
            self.generateFrames()

        #Se crea el gif y se guarda
        gifFramesDic = "framegeneratorGif/"
        imagesFrames = []
        pathArray = []

        for file_name in os.listdir(gifFramesDic):
            if file_name.endswith('.JPG'):
                file_path = os.path.join(gifFramesDic,file_name)
                pathArray.append(file_path)

        pathArray = sorted(pathArray)

        for i in range(0,len(pathArray)):
            imagesFrames.append(imageio.imread(pathArray[i]))

        #Creamos directory o comprobamos si existe
        dirName = "generatedGifs"

        if not os.path.exists(dirName):
            os.mkdir(dirName)
        else:
            pass

        # Se pide el nombre del gif y se ajusta duracion para crearlo
        gifFileName = gifFileName[:-1]
        for i in tqdm(range(1)):
            imageio.mimsave('generatedGifs/'+gifFileName+'_animation.gif', imagesFrames, duration = timElapse)
        self.msg = QtWidgets.QMessageBox.about(self,"Gif saved","Gif has been saved sucessfully")

    # Funcion para dibujar la velocidad y el angulo de la escuela analizada
    def drawVelandDir(self):
        global filesXPoints
        global filesYPoints
        global filesXPointsCenter
        global filesYPointsCenter
        global color_perimeter
        global readFilesLong
        global files
        global timElapse
        global renameFolderName
        global formato

        c = QtGui.QColor(color_perimeter)
        penGreen = QtGui.QPen(Qt.red,3)
        penPerimetro = QtGui.QPen(c,3)
        cantidad = len(filesXPoints)
        # Pintamos los perimetros y luego los puntos centrales en la imagen
        valorInicialRango = 0
        # Se dibuja todo de nuevo para tenerlo completo
        nombreFichero = files[-1].split('_')[0]
        # Se busca el formato de las imagenes contenidas en la carpeta de
        # muestras
        files = sorted(os.listdir(renameFolderName))
        for filename in files:
            src = renameFolderName + "/" + filename
            formato = src.split('.')[-1]

        fondo = renameFolderName + nombreFichero + "." + formato
        self.pixmap = QPixmap(fondo)
        self.setPhoto(self.pixmap)
        valorInicialRango = 0

        for j in range(0,len(readFilesLong)):
            for i in range(valorInicialRango,readFilesLong[j]-1):
                valXTail = int(filesXPoints[i])
                valYTail = int(filesYPoints[i])
                valXHead = int(filesXPoints[i+1])
                valYHead = int(filesYPoints[i+1])
                linea_item = QtWidgets.QGraphicsLineItem(valXTail,valYTail,valXHead,valYHead)
                linea_item.setPen(penPerimetro)
                linea_item.setData(1,6)
                self._scene.addItem(linea_item)
                self.setScene(self._scene)

            valXTail = int(filesXPoints[valorInicialRango])
            valYTail = int(filesYPoints[valorInicialRango])
            valXHead = int(filesXPoints[readFilesLong[j]-1])
            valYHead = int(filesYPoints[readFilesLong[j]-1])
            linea_item = QtWidgets.QGraphicsLineItem(valXTail,valYTail,valXHead,valYHead)
            linea_item.setPen(penPerimetro)
            linea_item.setData(1,6)
            self._scene.addItem(linea_item)
            self.setScene(self._scene)
            valorInicialRango = readFilesLong[j]

        #Se dibujan centroides
        for i in range(0,len(filesXPointsCenter)):
            rad = 5.0 #1.0
            brush = QtGui.QBrush(Qt.SolidPattern)
            ellipse_item = QtWidgets.QGraphicsEllipseItem(int(filesXPointsCenter[i])-rad,int(filesYPointsCenter[i])-rad,rad*2.0,rad*2.0)
            ellipse_item.setPen(penGreen)
            ellipse_item.setBrush(brush)
            ellipse_item.setData(1,6)
            self._scene.addItem(ellipse_item)
            self.setScene(self._scene)

        #Se dibujan lineas centroide
        for i in range(0,len(filesXPointsCenter)-1):

            valXHead = int(filesXPointsCenter[i+1])
            valXTail = int(filesXPointsCenter[i])
            valYHead = int(filesYPointsCenter[i+1])
            valYTail = int(filesYPointsCenter[i])
            linea_item = QtWidgets.QGraphicsLineItem(valXTail,valYTail,valXHead,valYHead)
            linea_item.setData(1,6)
            linea_item.setPen(penGreen)
            dX = valXHead - valXTail
            dY = valYHead - valYTail
            Len = sqrt(dX* dX + dY * dY)
            udX = dX / Len
            udY = dY / Len
            perpX = -udY
            perpY = udX

            L = 20 #longitud cabeza vector 2
            H = 6 #anchura vector 4

            leftX = valXHead - L * udX + H * perpX
            leftY = valYHead - L * udY + H * perpY
            rightX = valXHead - L * udX - H * perpX
            rightY = valYHead - L * udY - H * perpY

            vector_flecha_1 = QtCore.QLineF(valXHead,valYHead,leftX,leftY)
            vector_flecha_2 = QtCore.QLineF(valXHead,valYHead,rightX,rightY)
            linea_item_flecha_1 = QtWidgets.QGraphicsLineItem(vector_flecha_1)
            linea_item_flecha_1.setPen(penGreen)
            linea_item_flecha_2 = QtWidgets.QGraphicsLineItem(vector_flecha_2)
            linea_item_flecha_2.setPen(penGreen)
            linea_item_flecha_1.setData(1,6)
            linea_item_flecha_2.setData(1,6)
            self._scene.addItem(linea_item)
            self._scene.addItem(linea_item_flecha_1)
            self._scene.addItem(linea_item_flecha_2)
            self.setScene(self._scene)

        #Se calcula todo y se completa la tabla de datos
        self.showandCalcVel()

    # Funcion para calcular la velocidad y añadirla a la tabla de datos
    def showandCalcVel(self):
        global timElapse
        global filesXPointsCenter
        global filesYPointsCenter
        global schoolVelocity
        global veldir_vec_v
        global veldir_vec_u
        global veldir_angle
        global veldir_velocity
        global veldir_position

        del timElapse
        del schoolVelocity
        del veldir_vec_v[:]
        del veldir_vec_u[:]
        del veldir_angle[:]
        del veldir_velocity[:]
        del veldir_position[:]

        self.cont = True
        timElapse, okPressed = QInputDialog.getDouble(self, "Frame time lapse", "Timelapse(s):")

        if okPressed and timElapse != 0.0:
            pass
        else:
            self.msg = QtWidgets.QMessageBox.about(self,'Cancelling...','0.0 is not a valid number')
            self.cont = False

        if self.cont == True:
            distanciaPixeles = 0
            for i in range(0,len(filesXPointsCenter)-1):

                valXHead = int(filesXPointsCenter[i+1])
                valXTail = int(filesXPointsCenter[i])
                valYHead = int(filesYPointsCenter[i+1])
                valYTail = int(filesYPointsCenter[i])
                dX = valXHead - valXTail
                dY = valYHead - valYTail
                dist = int(sqrt(dX* dX + dY * dY))
                veldir_position.append(dist)

            for i in range(0,len(veldir_position)):
                schoolVelocity = int(veldir_position[i] / timElapse)
                veldir_velocity.append(schoolVelocity)

            for i in range(0,len(filesXPointsCenter)-1):
                valXHead = int(filesXPointsCenter[i+1])
                valXTail = int(filesXPointsCenter[i])
                valYHead = int(filesYPointsCenter[i+1])
                valYTail = int(filesYPointsCenter[i])
                vecU = int(valYHead-valYTail)
                vecV = int(valXHead-valXTail)
                veldir_vec_u.append(vecU)
                veldir_vec_v.append(vecV)

            # Se calculan los angulos entre los diferentes grupos de animales
            for i in range(0,len(veldir_vec_u)-1):
                valU = veldir_vec_u[i]
                valV = veldir_vec_v[i]
                vector_1 = (valU,valV)
                valU_neigh = veldir_vec_u[i+1]
                valV_neigh = veldir_vec_v[i+1]
                vector_2 = (valU_neigh,valV_neigh)
                angulo_rad = self.angle_between(vector_1,vector_2)
                angulo_degree = np.rad2deg(angulo_rad)

                #Se redondea el angulo a dos decimales
                angulo_degree = round(angulo_degree,2)
                veldir_angle.append(angulo_degree)

            #Se actualiza la tabla y se guarda en excel
            self.editVelDirTable.emit()

            #Se pintan los resultados
            self.paintSchoolResults()

    # Funcion para pintar los resultados en la imagen
    def paintSchoolResults(self):
        global veldir_angle
        global veldir_velocity
        global filesXPointsCenter
        global filesYPointsCenter

        separacion = int( self._scene.height() / 195 )

        for i in range(0,len(veldir_velocity)):
            if i == -1:
                texto = QtWidgets.QGraphicsTextItem(" ")
            elif i == 0:
                texto = QtWidgets.QGraphicsTextItem("v: "+str(veldir_velocity[i]))
            else:
                texto = QtWidgets.QGraphicsTextItem("v: "+str(veldir_velocity[i])+" , a: "+ str(veldir_angle[i-1]))
            texto.setPos(int(filesXPointsCenter[i+1]),int(filesYPointsCenter[i+1])-separacion)
            font = QFont()
            font.setBold(True)
            texto.setFont(font)
            self._scene.addItem(texto)
            self.setScene(self._scene)

    # Funcion para calcular el vector unitario
    def unit_vector(self,vector):
        return vector / np.linalg.norm(vector)

    # Funcion para calcular el angulo entre dos vectores
    def angle_between(self,v1, v2):
        v1_u = self.unit_vector(v1)
        v2_u = self.unit_vector(v2)
        return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

    # Funcion para guardar en formato de video el estudio del movimiento
    # de la agrupacion de animales
    def saveVideo(self):
        global framesGenerated

        if framesGenerated == False:
            self.generateFrames()

        image_folder = 'framegeneratorGif'
        video_name = 'generatedVideos/video.avi'
        images = [img for img in os.listdir(image_folder) if img.endswith(".JPG")]
        images = sorted(images)

        # Creamos directory o comprobamos si existe
        dirName = 'generatedVideos'

        if not os.path.exists(dirName):
            os.mkdir(dirName)
        else:
            pass



        frame = cv2.imread(os.path.join(image_folder,images[0]))
        height,width,layers = frame.shape
        video = cv2.VideoWriter(video_name,0,1,(width,height))
        for image in images:
            video.write(cv2.imread(os.path.join(image_folder,image)))
        cv2.destroyAllWindows()
        video.release()
        self.msg = QtWidgets.QMessageBox.about(self,"Video saved","Video has been saved sucessfully")

    # Funcion para calcular la velocidad y la dirección
    def calculateVelandDir(self):
        global files
        global filesXPoints
        global filesYPoints
        global filesXPointsCenter
        global filesYPointsCenter
        global color_perimeter
        global readFilesLong

        del files[:]
        del filesXPoints[:]
        del filesYPoints[:]
        del filesXPointsCenter[:]
        del filesYPointsCenter[:]
        del readFilesLong[:]


        # Se meten todos los ficheros a analizar al array de ficheros
        for i in os.listdir("perimeterData"):
            if i.endswith('.txt'):
                files.append(i)

        # Se van pintando uno a uno
        files = sorted(files)

        for i in range(0,len(files)):
            archiv = open("perimeterData/"+str(files[i]),"r")
            string = "a"
            for reader in archiv:
                string = reader
                valueX = string.split(',')[0]
                valueY = string.split(',')[1]
                filesXPoints.append(int(valueX))
                filesYPoints.append(int(valueY))

            del filesXPoints[-1]
            del filesYPoints[-1]

            longit = len(filesXPoints)
            readFilesLong.append(longit)
            archiv2 = open("perimeterData/"+str(files[i]),"r")
            strings = archiv2.readlines()
            strings = strings[-1]
            valueX = strings.split(',')[0]
            valueY = strings.split(',')[1]
            valueY = valueY[:-1]
            filesXPointsCenter.append(valueX)
            filesYPointsCenter.append(valueY)
            archiv.close()
            archiv2.close()

        # Dar vuelta array NO HACE FALTA POR EL MOMENTO SE QUEDA COMENTADO
        #filesXPointsCenter.reverse()
        #filesYPointsCenter.reverse()

        #Despues se calcula la velocidad en pixeles/segundo
        self.drawVelandDir()

    # Funcion para guardar la imagen analizada en el disco
    def saveImageAnalyzed(self):
        path, _ = QFileDialog.getSaveFileName(self, 'Save analyzed image', os.getcwd(), 'JPG(*.JPG)')
        rect = QtCore.QRectF(self._photo.pixmap().rect())

        if self._zoom == 0:
            image = QtGui.QImage(rect.width(),rect.height(), QImage.Format_ARGB32_Premultiplied)
            painter = QtGui.QPainter(image)
            self._scene.render(painter)
            painter.end()
        else:
            image = self.grab().toImage()
        image.save(str(path))

    # Funcion para reiniciar el zoom en la imagen
    def resetView(self,num):
        itemlist = self._scene.items()
        for items in itemlist:
            itemtype = type(items)
            if itemtype == QtWidgets.QGraphicsLineItem or itemtype == QtWidgets.QGraphicsEllipseItem:
                if items.data(1) == num:
                    self._scene.removeItem(items)

            if itemtype == QtWidgets.QGraphicsTextItem:
                if items.data(1) == num:
                    self._scene.removeItem(items)

    # Funcion para calcular la mediana de los datos
    def calcMedian(self):
        global sizes
        global average_size
        global average_angle

        for i in range(0,tiburonesTotales):
            valXTail = float(valuesXTail[i])
            valYTail = float(valuesYTail[i])
            valXHead = float(valuesXHead[i])
            valYHead = float(valuesYHead[i])
            dX = valXHead - valXTail
            dY = valYHead - valYTail
            Len = sqrt(dX* dX + dY * dY)
            sizes.append(Len)

        average_size = statistics.median(sizes)
        average_angle = statistics.median(angleList)

    # Funcion para convertir del formato QImage de PyQt5 al formato Mat
    # admitido por OpenCV (cv2)
    def convertQImageToMat(self,incomingImage):

        incomingImage = incomingImage.convertToFormat(4)
        width = incomingImage.width()
        height = incomingImage.height()
        ptr = incomingImage.bits()
        ptr.setsize(incomingImage.byteCount())
        arr = np.array(ptr).reshape(height,width,4)
        return arr

    # Funcion para calcular el mapa de densidad 3D
    def Density3DProcess(self):
        global posOfArrays
        global v_values
        global percentage_subsampling

        print("[INFO] Total points: {}".format(len(v_values)))

        # Se coge una submuestra del mapa de densidad
        percent = percentage_subsampling / 100
        idxs = np.random.randint(0, len(posOfArrays[0]), size=(int(len(posOfArrays[0]) * percent),))

        posArrayX = []
        posArrayY = []
        vvalues = []

        posArrayX = list(posOfArrays[0])
        posArrayY = list(posOfArrays[1])

        posArrayX = np.array(posArrayX)[idxs.astype(int)]
        posArrayY = np.array(posArrayY)[idxs.astype(int)]
        vvalues = np.array(v_values)[idxs.astype(int)]

        print("[INFO] Points after subsampling: {}".format(len(posArrayX)))
        #print(len(posArrayX))
        #print(len(posArrayY))
        #print(len(vvalues))

        fig = plt.figure()
        ax = Axes3D(fig)
        #surf = ax.plot_trisurf(posOfArrays[0],posOfArrays[1],v_values, cmap=cm.jet, linewidth=0.1)
        surf = ax.plot_trisurf(posArrayX,posArrayY,vvalues, cmap=cm.jet, linewidth=0.1)
        fig.colorbar(surf, shrink=0.5, aspect=5)
        plt.show()


    # Funcion para calcular el mapa de densidad 2D
    def DensityProcess(self,var):

        #Para corregir el bug de que coja mal el rectangulo a analizar
        self.pixmap = QPixmap(imagePath)
        self._photo.setPixmap(self.pixmap)
        rect = QtCore.QRectF(self._photo.pixmap().rect())
        image = QtGui.QImage(rect.width(),rect.height(), QImage.Format_ARGB32_Premultiplied)
        painter = QtGui.QPainter(image)
        self._scene.render(painter)
        painter.end()
        imageReConverted = self.convertQImageToMat(image)

        # Se vacian los listados en caso de haberlo calculado previamente
        # y se inicializan para poder almcenar datos de nuevo
        global posOfArrays
        global s_values
        del s_values[:]
        global valXInsideConvexHull
        global valYInsideConvexHull
        global v_values
        del v_values[:]
        global convexXHull
        del convexXHull[:]
        global convexYHull
        del convexYHull[:]
        global densityCalculated
        global heatMapColorValues
        global number_of_layers
        global valuesXPerimeter
        global valuesYPerimeter
        global convexPointList
        global perimeterPointList
        global nameofFileFiltered

        imageFiltered = cv2.blur(imageReConverted,(5,5)) #15,15 o 10,10
        height,width,channels = imageReConverted.shape

        if var == 0:

            #print("[INFO] Calculo el mapa de densidad etiquetado individual...")

            hull = ConvexHull(midPointList)
            long = len(hull.vertices)
            for i in range(0,long):
                valXTail = int(valuesXMed[hull.vertices[i]])
                valYTail = int(valuesYMed[hull.vertices[i]])

                convexXHull.append(valXTail)
                convexYHull.append(valYTail)
                point = [valXTail,valYTail]
                convexPointList.append(point)

            minconvexValX = min(convexXHull)
            maxconvexValX = max(convexXHull)
            minconvexValY = min(convexYHull)
            maxconvexValY = max(convexYHull)
            listadoDePuntos = convexPointList
        elif var == 1:

            #print("[INFO] Calculo el mapa de densidad etiquetado colectivo...")

            listadoDePuntos = perimeterPointList

        #Una vez obtenidos puntos ConvexHull, buscamos obtener las ROI
        mask = np.zeros(imageFiltered.shape, dtype=np.uint8)
        roi_corners = np.array(listadoDePuntos)
        channel_count = imageFiltered.shape[2]
        ignore_mask_color = (255,)*channel_count
        #cv2.fillConvexPoly(mask,roi_corners,ignore_mask_color) # A veces hay poligonos no convexos NO VALIDO
        cv2.fillPoly(mask, pts=[roi_corners], color=ignore_mask_color)
        masked_image = cv2.bitwise_and(imageFiltered,mask)
        hsv_img_original = cv2.cvtColor(masked_image, cv2.COLOR_RGB2HSV)
        h,s,v = cv2.split(hsv_img_original)


        #cv2.imshow("Original", imageReConverted)
        #cv2.imshow("mask", mask)
        #cv2.imshow("v", v)
        #cv2.waitKey(1)



        # Funcion para obtener los valores HEX de la gama de colores
        self.pruebaHexValuesArray()
        posOfArrays = np.where(v > 0) # Index en X,Y de los puntos mayores a 0

        #print("[INFO] Hay un total de posOfArrays: {}".format(len(posOfArrays[0])))
        #print("[INFO] Hay un total de listadoDePuntos: {}".format(len(listadoDePuntos)))

        # Se buscan los valores MAX y MIN de la componente V de la imagen HSV
        # dichos valores se buscan solo en la zona de la ROI no en toda la imagen
        v_val_max = np.amax(v)
        v_val_min = np.amin(v[np.where(v>0)]) #no de toda la imagen sino de nuestra zona

        #Pintar directamente segun el valor de la S que se lea de las posiciones cuyo valor de S es mayor que cero
        for i in tqdm(range(0,len(posOfArrays[0]))):
            valordeV = v[posOfArrays[0][i],posOfArrays[1][i]]
            posArray = self.mapeador(valordeV,v_val_min,v_val_max,0,number_of_layers-1)
            colour = str(heatMapColorValues[posArray])

            #Descompongo color en rgb
            v_values.append(valordeV)
            parte_R = colour.split(',')[0]
            cant_R = int(parte_R)
            parte_G = colour.split(',')[1]
            cant_G = int(parte_G)
            parte_B = colour.split(',')[2]
            cant_B = int(parte_B)
            imageReConverted[posOfArrays[0][i],posOfArrays[1][i]] = (cant_B,cant_G,cant_R,1)

        cv2.imwrite('cache_heatmap.JPG',imageReConverted)

        # Se guarda el mapa de calor solo para hacer prueba de gif
        self.pixmap = QPixmap("cache_heatmap.JPG")
        self.setPhoto(self.pixmap)


        # Se guardan los datos del mapa de calor en el ordenador

        if densityCalculated == False:
            # Creamos directory o comprobamos si existe
            dirName = 'densityMapData'

            if not os.path.exists(dirName):
                os.mkdir(dirName)
            else:
                pass

            file = open(dirName + '/' + nameofFileFiltered + "_density" + ".txt","w")
            for i in range(0,len(posOfArrays[0])):
                file.write(str(int(posOfArrays[0][i])) + "," + str(int(posOfArrays[1][i])) + "," + str(int(v_values[i])) + "\n")
            file.close()

        if densityCalculated == False:
            self.msg = QtWidgets.QMessageBox.about(self,'Save density map data','Density map data has been saved sucessfully')
            densityCalculated = True


        #densityCalculated = True

        self.rePaintWithZoom(self._zoom) ##-

    # Funcion para interpolar valores
    def mapeador(self, x,in_min,in_max,out_min,out_max):
        return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

    # Funcion para generar valores HEX a partir de RGB
    def pruebaHexValuesArray(self):
        global heatMapColorValues
        global number_of_layers
        global color_layers
        global maxRangeValue

        parte_R = color_layers[1:3]
        cant_R = int(parte_R,16)
        parte_G = color_layers[3:5]
        cant_G = int(parte_G,16)
        parte_B = color_layers[5:7]
        cant_B = int(parte_B,16)
        maximum = self.maximumOfRGB(cant_R,cant_G,cant_B)

        for i in range(0,number_of_layers):
            escalar = int(maxRangeValue/number_of_layers)*i
            if maximum == cant_R:
                value_string = str(cant_R)+","+str(escalar)+","+str(escalar)
            elif maximum == cant_G:
                value_string = str(escalar)+","+str(cant_G)+","+str(escalar)
            elif maximum == cant_B:
                value_string = str(escalar)+","+str(escalar)+","+str(cant_B)
            heatMapColorValues.append(value_string)

        # Se invierte el array de capas de  color (al final no)
        #heatMapColorValues.reverse()

    # Funcion para obtener el maximo en las componentes R,G,B de una imagen
    def maximumOfRGB(self,r,g,b):
        list = [r,g,b]
        return max(list)

    # Funcion para calcular y pintar los datos de analisis de una imagen
    def ImageProcess(self,var,pintar):
        global valCenterMassX
        global valCenterMassY
        global valuesXHead
        global valuesYHead
        global valuesYTail
        global valuesXTail
        global color_labelled_data
        global color_perimeter
        global color_vector1
        global color_vector2
        global color_dot1
        global color_dot2
        global color_labelled_analyzed_data
        global convexXHull
        global convexYHull
        global perimeterSaved
        global valuesXPerimeter
        global valuesYPerimeter
        global valuesXMed
        global valuesYMed
        global midPointList
        global ratio_cm_pixel
        global ratio_cm_pixel_cuadrado
        global areaROI
        global areaROI_cm
        global areaCalculated

        global nameofFileFiltered

        if var == 0:
            valCenterMassX = statistics.mean(valuesXMed)
            valCenterMassY = statistics.mean(valuesYMed)
        elif var == 1:
            valCenterMassX = statistics.mean(valuesXPerimeter)
            valCenterMassY = statistics.mean(valuesYPerimeter)

        self.editMassCenter.emit()

        # Dibujar punto medio
        rad = 3.0+calcGrosorAnalyzed #1.0
        brush = QtGui.QBrush(Qt.SolidPattern)

        c = QtGui.QColor(color_perimeter)

        penGreen = QtGui.QPen(c,calcGrosorAnalyzed)

        if pintar == 1 and ratio_cm_pixel == 0:
            ellipse_item = QtWidgets.QGraphicsEllipseItem(valCenterMassX-rad,valCenterMassY-rad,rad*2.0,rad*2.0)
            ellipse_item.setPen(penGreen)
            ellipse_item.setBrush(brush)
            ellipse_item.setData(1,2)
            self._scene.addItem(ellipse_item)
            self.setScene(self._scene)

        if var == 0: #Caso normal de etiquetado
            hull = ConvexHull(midPointList)
            long = len(hull.vertices)

            for i in range(0,long-1):
                valXTail = int(valuesXMed[hull.vertices[i]])
                valYTail = int(valuesYMed[hull.vertices[i]])
                valXHead = int(valuesXMed[hull.vertices[i+1]])
                valYHead = int(valuesYMed[hull.vertices[i+1]])
                convexXHull.append(valXTail)
                convexYHull.append(valYTail)

                if pintar == 1:
                    linea_item = QtWidgets.QGraphicsLineItem(valXTail,valYTail,valXHead,valYHead)
                    linea_item.setPen(penGreen)
                    linea_item.setData(1,2)
                    self._scene.addItem(linea_item)
                    self.setScene(self._scene)

            valXTail = int(valuesXMed[hull.vertices[0]])
            valYTail = int(valuesYMed[hull.vertices[0]])
            valXHead = int(valuesXMed[hull.vertices[long-1]])
            valYHead = int(valuesYMed[hull.vertices[long-1]])
            convexXHull.append(valXHead)
            convexYHull.append(valYHead)

            if pintar == 1:
                linea_item = QtWidgets.QGraphicsLineItem(valXTail,valYTail,valXHead,valYHead)
                linea_item.setPen(penGreen)
                linea_item.setData(1,2)
                self._scene.addItem(linea_item)
                self.setScene(self._scene)

            nameofFile = imagePath.split('/')[-1]
            nameofFileFiltered = nameofFile.split('.')[0]

            if perimeterSaved == False:
                # Creamos directory o comprobamos si existe
                dirName = 'perimeterData'

                if not os.path.exists(dirName):
                    os.mkdir(dirName)
                else:
                    file = open("perimeterData/"+nameofFileFiltered+"_perimeter"+".txt","w")
                    for i in range(0,len(convexXHull)):
                        file.write(str(int(convexXHull[i]))+","+str(int(convexYHull[i]))+"\n")
                    file.write(str(int(valCenterMassX))+","+str(int(valCenterMassY))+"\n")
                    file.close()

            if perimeterSaved == False:
                self.msg = QtWidgets.QMessageBox.about(self,'Saved data','Perimeter and analyzed data have been saved sucessfully')
                perimeterSaved = True


        elif var == 1: #Caso perimetro sin etiquetar
            cantidad = len(perimeterPointList)
            for i in range(0,cantidad-1):
                        valXTail = int(valuesXPerimeter[i])
                        valYTail = int(valuesYPerimeter[i])
                        valXHead = int(valuesXPerimeter[i+1])
                        valYHead = int(valuesYPerimeter[i+1])
                        if pintar == 1:
                            linea_item = QtWidgets.QGraphicsLineItem(valXTail,valYTail,valXHead,valYHead)
                            linea_item.setPen(penGreen)
                            linea_item.setData(1,2)
                            self._scene.addItem(linea_item)
                            self.setScene(self._scene)

            valXTail = int(valuesXPerimeter[0])
            valYTail = int(valuesYPerimeter[0])
            valXHead = int(valuesXPerimeter[cantidad-1])
            valYHead = int(valuesYPerimeter[cantidad-1])

            if pintar == 1:
                linea_item = QtWidgets.QGraphicsLineItem(valXTail,valYTail,valXHead,valYHead)
                linea_item.setPen(penGreen)
                linea_item.setData(1,2)
                self._scene.addItem(linea_item)
                self.setScene(self._scene)

                if ratio_cm_pixel != 0 and not areaCalculated:
                    # Se calcula el area que ocupa el perimetro (en pixeles)
                    # y se convierte a cm2

                    #print("[INFO] Calculo areas felizmente...")

                    rect = QtCore.QRectF(self._photo.pixmap().rect())
                    image = QtGui.QImage(rect.width(),rect.height(), QImage.Format_ARGB32_Premultiplied)
                    painter = QtGui.QPainter(image)
                    self._scene.render(painter)
                    painter.end()
                    imageReConverted = self.convertQImageToMat(image)
                    mask = np.zeros(imageReConverted.shape, dtype=np.uint8)
                    roi_corners = np.array(perimeterPointList)
                    channel_count = imageReConverted.shape[2]
                    ignore_mask_color = (255,)*channel_count
                    #cv2.fillConvexPoly(mask,roi_corners,ignore_mask_color) Hay poligonos NO CONVEXOS NO VALIDO
                    cv2.fillPoly(mask, pts=[roi_corners], color=ignore_mask_color)
                    masked_image = cv2.bitwise_and(imageReConverted,mask)
                    contours_image = cv2.cvtColor(masked_image, cv2.COLOR_BGR2GRAY)
                    cnts, hierarchy = cv2.findContours(contours_image.copy(),
                        cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                    cnt = cnts[0]
                    cv2.drawContours(contours_image, cnts, -1, 255, 3)
                    areaROI  = cv2.contourArea(cnt)
                    areaROI_cm = areaROI / ratio_cm_pixel_cuadrado
                    x = self._scene.width()
                    y = self._scene.height()
                    separacion = int ( self._scene.height() / 195)
                    texto = QtWidgets.QGraphicsTextItem("Area (cm2): " + str(areaROI_cm))
                    texto.setPos(0 + cte_pos_x * separacion, 0 + cte_pos_y* separacion)
                    font = QFont("Helvetica [Cronyx]", y / 40)
                    font.setBold(True)
                    texto.setFont(font)
                    c = QtGui.QColor(color_perimeter)
                    texto.setDefaultTextColor(c)
                    texto.setData(1,7)
                    self._scene.addItem(texto)
                    self.setScene(self._scene)

                    areaCalculated = True

            nameofFile = imagePath.split('/')[-1]
            nameofFileFiltered = nameofFile.split('.')[0]


            if perimeterSaved == False:
                # Creamos directory o comprobamos si existe
                dirName = 'perimeterData'

                if not os.path.exists(dirName):
                    os.mkdir(dirName)
                else:
                    pass

                file = open("perimeterData/"+nameofFileFiltered+"_perimeter"+".txt","w")
                for i in range(0,len(valuesXPerimeter)):
                    file.write(str(int(valuesXPerimeter[i]))+","+str(int(valuesYPerimeter[i]))+"\n")
                file.write(str(int(valCenterMassX))+","+str(int(valCenterMassY))+"\n")
                file.close()

            if perimeterSaved == False:
                self.msg = QtWidgets.QMessageBox.about(self,'Save perimeter data','Perimeter data has been saved sucessfully')
                perimeterSaved = True

    # Funcion para pintar los datos cargados al programa
    def drawLoadedData(self,num):
        global valuesXTail
        global valuesYTail
        global valuesXHead
        global valuesYHead
        global valuesXMed
        global valuesYMed
        global vec_u
        global vec_v
        global neighList
        global angleList
        global calcGrosorAnalyzed
        global color_labelled_data
        global color_perimeter
        global color_vector1
        global color_vector2
        global color_dot1
        global color_dot2
        global color_labelled_analyzed_data

        #print("[INFO] Pinto con un grosor: {}".format(calcGrosorAnalyzed))

        self.calcMedian()

        for i in range(0,tiburonesTotales):
            valXTail = float(valuesXTail[i])
            valYTail = float(valuesYTail[i])
            valXHead = float(valuesXHead[i])
            valYHead = float(valuesYHead[i])
            colordelAnalizado = QtGui.QColor(color_labelled_analyzed_data)
            colordelVector1 = QtGui.QColor(color_vector1)
            colordelVector2 = QtGui.QColor(color_vector2)
            colordelDot1 = QtGui.QColor(color_dot1)
            colordelDot2 = QtGui.QColor(color_dot2)
            penGreen = QtGui.QPen(colordelAnalizado,calcGrosorAnalyzed)
            penVector1 = QtGui.QPen(colordelVector1,calcGrosorAnalyzed)
            penBlack = QtGui.QPen(QtCore.Qt.black,calcGrosorAnalyzed)
            penVector2 = QtGui.QPen(colordelVector2,calcGrosorAnalyzed)
            penRed = QtGui.QPen(colordelDot1,calcGrosorAnalyzed)
            penBlue = QtGui.QPen(colordelDot2,calcGrosorAnalyzed)
            valXMed = float(valuesXMed[i])
            valYMed = float(valuesYMed[i])
            valU = float(vec_u[i])
            valV = float(vec_v[i])
            valDist = float(neighList[i])
            valAngle = float(angleList[i])




            # Dibujar punto medio
            rad = 1.0+calcGrosorAnalyzed #1.0
            brush = QtGui.QBrush(Qt.SolidPattern)


            # Se comprueba si la i del angulo de los sizes es mayor o menor a lo que sea etc
            if valDist <= 2*average_size:
                genericPen = penRed
            elif valDist > 2*average_size:
                genericPen = penBlue

            if num == 0:
                ellipse_item = QtWidgets.QGraphicsEllipseItem(valXMed-rad,valYMed-rad,rad*2.0,rad*2.0)
                ellipse_item.setPen(genericPen)
                ellipse_item.setBrush(brush)
                ellipse_item.setData(1,0)


            # Se dibujan los vectores
            vector_uv = QtCore.QLineF(0,0,valV,valU)
            vector_uv.translate(valXMed,valYMed)
            linea_item_vector = QtWidgets.QGraphicsLineItem(vector_uv)
            linea_item_vector.setData(1,1)

            if valAngle <= average_angle:
                genericPen = penVector1
            elif valAngle > average_angle:
                genericPen = penVector2
            linea_item_vector.setPen(genericPen)

            if num == 0:
                linea_item = QtWidgets.QGraphicsLineItem(valXTail,valYTail,valXHead,valYHead)
                linea_item.setData(0,i)
                linea_item.setPen(penGreen)
                linea_item.setData(1,0)

            dX = valXHead - valXTail
            dY = valYHead - valYTail
            Len = sqrt(dX* dX + dY * dY)
            udX = dX / Len
            udY = dY / Len
            perpX = -udY
            perpY = udX

            L = 2 #longitud cabeza vector
            H = 4 #anchura vector

            leftX = valXHead - L * udX + H * perpX
            leftY = valYHead - L * udY + H * perpY
            rightX = valXHead - L * udX - H * perpX
            rightY = valYHead - L * udY - H * perpY

            vector_flecha_1 = QtCore.QLineF(valV+valXMed,valU+valYMed,leftX,leftY)
            vector_flecha_2 = QtCore.QLineF(valV+valXMed,valU+valYMed,rightX,rightY)

            if num == 1:
                linea_item_flecha_1 = QtWidgets.QGraphicsLineItem(vector_flecha_1)
                linea_item_flecha_1.setPen(genericPen)
                linea_item_flecha_2 = QtWidgets.QGraphicsLineItem(vector_flecha_2)
                linea_item_flecha_2.setPen(genericPen)
                linea_item_flecha_1.setData(1,1)
                linea_item_flecha_2.setData(1,1)
            if num == 0:
                self._scene.addItem(linea_item)
                self._scene.addItem(ellipse_item)
            if num == 1:
                self._scene.addItem(linea_item_vector)
                self._scene.addItem(linea_item_flecha_1)
                self._scene.addItem(linea_item_flecha_2)

            self.setScene(self._scene)


# Clase que contiene la Interfaz Básica o de etiquetado
class PhotoDataViewer(QtWidgets.QGraphicsView):
    photoClicked = QtCore.pyqtSignal(QtCore.QPointF)
    labelUpdater = QtCore.pyqtSignal(int,int,QtCore.QPointF)
    tableUpdater = QtCore.pyqtSignal(int)
    ResetInfoSig = QtCore.pyqtSignal()
    DragModeConnecter = QtCore.pyqtSignal(bool,int)
    labelChecker = QtCore.pyqtSignal(int)
    tableRowCounter = QtCore.pyqtSignal()
    editAnalyzeImageLabel = QtCore.pyqtSignal()
    resetEmit = QtCore.pyqtSignal()



    # Funcion de inicializacion de la clase
    def __init__(self, parent):
        super(PhotoDataViewer, self).__init__(parent)

        # Variables para controlar si hay imagen, el zoom, archivos en la escena,
        # fotos, y add fotos a la escena
        # Asi como modificar la escena para eliminar anchos y demas
        self.startSelecting = False
        self.selectorActual = 1
        self.sharkCount = 0
        self.perimeterPointCounter = 0
        self.startX = 0
        self.startY = 0
        self.handDrag = False
        self._zoom = 0
        self._empty = True
        self._scene = QtWidgets.QGraphicsScene(self)
        self._photo = QtWidgets.QGraphicsPixmapItem()
        self._scene.addItem(self._photo)
        self.setScene(self._scene)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(30, 30, 30)))
        self.setFrameShape(QtWidgets.QFrame.NoFrame)

    # Se comprueba simplemente si la variable empty esta en false o true
    def hasPhoto(self):
        return not self._empty
    # Ajusta la imagen al rectangulo creado
    def fitInView(self, scale=True):
        rect = QtCore.QRectF(self._photo.pixmap().rect())
        if not rect.isNull():
            self.setSceneRect(rect)
            if self.hasPhoto():
                unity = self.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
                self.scale(1 / unity.width(), 1 / unity.height())
                viewrect = self.viewport().rect()
                scenerect = self.transform().mapRect(rect)
                factor = min(viewrect.width() / scenerect.width(),
                             viewrect.height() / scenerect.height())
                self.scale(factor, factor)
            self._zoom = 0

    # Funcion para cargar la imagen en el rectangulo de la interfaz
    def setPhoto(self, pixmap=None):
        self._zoom = 0
        if pixmap and not pixmap.isNull():
            #Al cargar una imagen se reinician las variables de interes
            self.startSelecting = True
            self.selectorActual = 1
            self.sharkCount = 0
            self.startX = 0
            self.startY = 0
            self._scene.clear()
            self._photo = QtWidgets.QGraphicsPixmapItem()
            self._scene.addItem(self._photo)
            self.perimeterPointCounter = 0
            self.clicked = False
            self._empty = False
            global imag_loaded
            imag_loaded = self._empty
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag) #ScrollHandDrag
            self._photo.setPixmap(pixmap)

            # Redimensiono la escena en funcion de la imagen nueva
            self._scene.width = pixmap.width
            self._scene.height = pixmap.height

            #print(self._scene.width)

            #print(type(self._scene.width())) # = pixmap.width()
            #self._scene.height() = pixmap.height()

            #print("[INFO] Cargo una imagen en etiquetado con unas dimensiones X,Y: {}, {}".format(self._scene.width(), self._scene.height()))


        else:
            self._empty = True
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
            self._photo.setPixmap(QtGui.QPixmap())
        self.fitInView()

    # Funcion para hacer zoom con la rueda del raton
    def wheelEvent(self, event):
        if self.hasPhoto():
            if event.angleDelta().y() > 0:
                factor = 1.25
                self._zoom += 1
            else:
                factor = 0.8
                self._zoom -= 1
            if self._zoom > 0:
                self.scale(factor, factor)
            elif self._zoom == 0:
                self.fitInView()
            else:
                self._zoom = 0

        self.rePaintWithZoom(self._zoom)

    # Funcion para repintar los datos en funcion del zoom del raton
    def rePaintWithZoom(self,zoom):
        global filasActuales
        global empty_row
        global tiburonesTotales

        self.errorAtZoom = False
        self.tableRowCounter.emit()
        longitud_comprobacion = filasActuales

        if self.sharkCount == 0 and empty_row == True:
            pass
        # Condicion added para cuando se cargan datos bug desconocido
        # dado que la variable sharkCount tarda en actualizarse y primero intenta
        # comprobar el rePaintWithZoom
        elif tiburonesTotales == longitud_comprobacion:
            self.errorAtZoom = False
        elif self.sharkCount < longitud_comprobacion:
            self.errorAtZoom = True
        elif self.sharkCount == longitud_comprobacion:
            self.errorAtZoom = False
        else:
            self.errorAtZoom = True

        if self.errorAtZoom == False:
            self.resetParcial()
            global calcGrosor
            global color_labelled_data
            global color_perimeter
            global color_vector1
            global color_vector2
            global color_dot1
            global color_dot2
            global color_labelled_analyzed_data

            #print("[INFO] Repinto con nivel de zoom en etiquetado")

            x = self._scene.width()
            y = self._scene.height()

            zoomPararestar = 10
            calcGrosor_max = 11

            '''
            if x >= 3800 and y >= 2100:
                calcGrosor_max = 11
                zoomPararestar = 10
            elif x < 3800 and x >= 2300 and y < 2100 and y >= 1500:
                calcGrosor_max = 8
                zoomPararestar = 7
            elif x < 2300 and x >= 1250 and y < 1500 and y >= 700:
                calcGrosor_max = 5
                zoomPararestar = 4
            else:
                calcGrosor_max = 3
                zoomPararestar = 2
            '''

            if x >= 3800 or y >= 2100:
                calcGrosor_max = 11
                zoomPararestar = 10
            elif x < 3800 and x >= 2300 or y < 2100 and y >= 1500:
                calcGrosor_max = 8
                zoomPararestar = 7
            elif x < 2300 and x >= 1250 or y < 1500 and y >= 700:
                calcGrosor_max = 5
                zoomPararestar = 4
            else:
                calcGrosor_max = 3
                zoomPararestar = 2

            if zoom <= zoomPararestar:
                calcGrosor = calcGrosor_max-zoom
            else:
                calcGrosor = 1

            #print("[INFO] X,Y: {}, {}, Zoom: {}, Zoom para restar: {}, Grosor calculado: {}, Grosor maximo: {}".format(x, y, zoom, zoomPararestar, calcGrosor, calcGrosor_max))

            c = QtGui.QColor(color_labelled_data)
            d = QtGui.QColor(color_perimeter)
            penGreen = QtGui.QPen(d,calcGrosor)
            penBlack = QtGui.QPen(c,calcGrosor)
            rad = calcGrosor #1.0
            longi = len(perimeterPointList)

            if longi >= 2:
                for i in range(0,longi-1):
                    lineaper = QtWidgets.QGraphicsLineItem(valuesXPerimeter[i],valuesYPerimeter[i],valuesXPerimeter[i+1],valuesYPerimeter[i+1])
                    lineaper.setPen(penGreen)
                    lineaper.setData(2,i)
                    self._scene.addItem(lineaper)
                    self.setScene(self._scene)

            if longi >= 1:
                for i in range(0,longi):
                    brush = QtGui.QBrush(Qt.SolidPattern)
                    ellipse_item = QtWidgets.QGraphicsEllipseItem(valuesXPerimeter[i]-rad,valuesYPerimeter[i]-rad,rad*2.0,rad*2.0)
                    ellipse_item.setPen(penGreen)
                    ellipse_item.setData(2,i)
                    ellipse_item.setBrush(brush)
                    self._scene.addItem(ellipse_item)
                    self.setScene(self._scene)

            global valuesXTail
            global valuesYTail
            global valuesXHead
            global valuesYHead

            longiShark = len(valuesXTail)


            if longiShark >= 1:
                for i in range(0,longiShark):
                    valXTail = float(valuesXTail[i])
                    valYTail = float(valuesYTail[i])
                    valXHead = float(valuesXHead[i])
                    valYHead = float(valuesYHead[i])
                    lineaper = QtWidgets.QGraphicsLineItem(valXTail,valYTail,valXHead,valYHead)
                    lineaper.setPen(penBlack)
                    lineaper.setData(0,i)
                    self._scene.addItem(lineaper)
                    self.setScene(self._scene)
        else:
            self.msg = QtWidgets.QMessageBox.about(self,'Error zooming','Finish selection before zooming')


    # Funcion para hacer un reseteado parcial de los datos
    def resetParcial(self):
        itemlist = self._scene.items()
        for items in itemlist:
            itemtype = type(items)
            if itemtype == QtWidgets.QGraphicsLineItem or itemtype == QtWidgets.QGraphicsEllipseItem:
                self._scene.removeItem(items)


    # Funcion para activar el registro de datos
    def toggleDragMode(self):
        self.startSelecting = True
        self.labelUpdater.emit(self.selectorActual,self.sharkCount,QtCore.QPoint())
        self.rePaintWithZoom(self._zoom)
        global cargarDatos
        global tiburonesTotales
        if cargarDatos == True:
            self.sharkCount = tiburonesTotales
        if self.dragMode() == QtWidgets.QGraphicsView.ScrollHandDrag:
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        elif not self._photo.pixmap().isNull():
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)

    # Funcion para obtener datos cuando hacemos click con el raton
    def mousePressEvent(self, event):
        global color_labelled_data
        global color_perimeter
        global color_vector1
        global color_vector2
        global color_dot1
        global color_dot2
        global color_labelled_analyzed_data
        global measure_pointList

        if self._photo.isUnderMouse():
            if event.button() == QtCore.Qt.LeftButton:
                if self.handDrag == False and self.startSelecting == True and deleteIt == False and perimeterClick == False:
                    self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
                    self.photoClicked.emit(QtCore.QPointF(self.mapToScene(event.pos())))

                    if self.selectorActual == 1 and measureClick == True:
                        self.selectorActual +=1
                        e = QtCore.QPointF(self.mapToScene(event.pos()))
                        self.startX = e.x()
                        self.startY = e.y()
                        self.clicked = True

                    elif self.selectorActual == 2 and measureClick == True:
                        e = QtCore.QPointF(self.mapToScene(event.pos()))
                        c = QtGui.QColor(color_labelled_data)
                        pen = QtGui.QPen(c,calcGrosor)
                        linea_item = QtWidgets.QGraphicsLineItem(self.startX,self.startY,e.x(),e.y())
                        linea_item.setData(0,self.sharkCount)
                        linea_item.setPen(pen)
                        self._scene.addItem(linea_item)
                        self.setScene(self._scene)
                        self.selectorActual = 1

                        # Calculo distancia real
                        dX = self.startX - e.x()
                        dY = self.startY - e.y()
                        dist = int(sqrt(dX* dX + dY * dY))
                        global dist_pixeles
                        dist_pixeles = dist

                        # Se guardan los puntos de la distancia
                        pointIniDist = [self.startX,self.startY]
                        pointFinDist = [e.x(),e.y()]

                        global measure_pointList
                        del measure_pointList[:]

                        measure_pointList.append(pointIniDist)
                        measure_pointList.append(pointFinDist)

                        # Se pide introducir equivalencia real en centimetros
                        distCm, okPressed = QInputDialog.getDouble(self, "Actual Image Distance", "Distance(cm):")

                        if okPressed and distCm != 0.0:
                            global dist_cm
                            dist_cm = distCm
                        else:
                            self.msg = QtWidgets.QMessageBox.about(self,'Cancelling...','0.0 is not a valid number')

                        # Se calcula relacion entre cm y pixeles
                        global ratio_cm_pixel
                        global ratio_cm_pixel_cuadrado

                        ratio_cm_pixel = dist_pixeles / dist_cm
                        ratio_cm_pixel_cuadrado = ratio_cm_pixel**2


                        # Se muestra en pantalla la equivalencia en la esquina inferior izquierda
                        x = self._scene.width()
                        y = self._scene.height()
                        separacion = int( self._scene.height() / 195 )
                        texto = QtWidgets.QGraphicsTextItem("Ratio (pixel/cm): " + str(ratio_cm_pixel))
                        texto.setPos(0 + cte_pos_x * separacion,y - cte_pos_y * separacion)
                        font = QFont("Helvetica [Cronyx]", y / 40)
                        font.setBold(True)
                        texto.setFont(font)
                        c = QtGui.QColor(color_perimeter)
                        texto.setDefaultTextColor(c)
                        self._scene.addItem(texto)
                        self.setScene(self._scene)
                        self.editAnalyzeImageLabel.emit()
                        self.clicked = False

                    if self.selectorActual == 1 and measureClick == False:
                        self.selectorActual += 1
                        self.labelUpdater.emit(self.selectorActual,self.sharkCount,QtCore.QPointF(self.mapToScene(event.pos())))
                        e = QtCore.QPointF(self.mapToScene(event.pos()))
                        self.startX = e.x()
                        self.startY = e.y()
                        self.clicked = True

                    elif self.selectorActual == 2 and doubleClick == True and perimeterClick == False and measureClick == False:
                        e = QtCore.QPointF(self.mapToScene(event.pos()))
                        c = QtGui.QColor(color_labelled_data)
                        pen = QtGui.QPen(c,calcGrosor)
                        linea_item = QtWidgets.QGraphicsLineItem(self.startX,self.startY,e.x(),e.y())
                        linea_item.setData(0,self.sharkCount)
                        linea_item.setPen(pen)
                        self._scene.addItem(linea_item)
                        self.setScene(self._scene)
                        self.selectorActual = 1
                        self.labelUpdater.emit(self.selectorActual,self.sharkCount,QtCore.QPointF(self.mapToScene(event.pos())))
                        self.sharkCount += 1
                        #Activar funcion de analisis
                        if self.sharkCount > 2:
                            self.labelChecker.emit(1)

                # Para seleccionar perimetros
                if self.handDrag == False and self.startSelecting == True and perimeterClick == True:
                    global perimeterPointList
                    e = QtCore.QPointF(self.mapToScene(event.pos()))
                    c = QtGui.QColor(color_perimeter)
                    penGreen = QtGui.QPen(c,calcGrosor)
                    if self.perimeterPointCounter >= 1:
                        lineaper = QtWidgets.QGraphicsLineItem(self.startX,self.startY,e.x(),e.y())
                        lineaper.setPen(penGreen)
                        lineaper.setData(2,self.perimeterPointCounter)
                        self._scene.addItem(lineaper)
                        self.setScene(self._scene)

                    self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
                    self.photoClicked.emit(QtCore.QPointF(self.mapToScene(event.pos())))

                    # Dibujar punto medio
                    rad = calcGrosor #1.0
                    brush = QtGui.QBrush(Qt.SolidPattern)
                    penGreen = QtGui.QPen(c,calcGrosor)
                    ellipse_item = QtWidgets.QGraphicsEllipseItem(e.x()-rad,e.y()-rad,rad*2.0,rad*2.0)
                    ellipse_item.setPen(penGreen)
                    ellipse_item.setData(2,self.perimeterPointCounter)
                    ellipse_item.setBrush(brush)
                    self._scene.addItem(ellipse_item)
                    self.setScene(self._scene)
                    valuesXPerimeter.append(e.x())
                    valuesYPerimeter.append(e.y())
                    point = [int(e.x()),int(e.y())]
                    perimeterPointList.append(point)
                    self.perimeterPointCounter += 1
                    #Activar funcion analisis perimetro
                    self.labelChecker.emit(2)
                    self.startX = e.x()
                    self.startY = e.y()

                # En el caso de querer borrar datos etiquetados de manera individual
                if self.handDrag == False and self.startSelecting == True and deleteIt == True and perimeterClick == False:
                    item = self.itemAt(event.pos())
                    index = item.data(0)
                    itemtype = type(item)
                    if itemtype == QtWidgets.QGraphicsLineItem and index is not None:
                        self._scene.removeItem(item)
                        self.tableUpdater.emit(index)
                        self.sharkCount -= 1

                        if self.sharkCount == 0:
                            self.labelChecker.emit(0)

                        self.updateSharkIndex(index)
                        #Al borrar tambien borro del array global los datos
                        del valuesXTail[index]
                        del valuesYTail[index]
                        del valuesXHead[index]
                        del valuesYHead[index]

                    elif itemtype == QtWidgets.QGraphicsLineItem:
                        self._scene.removeItem(item)

                    index = item.data(2)
                    if itemtype == QtWidgets.QGraphicsEllipseItem:
                        self._scene.removeItem(item)
                        self.perimeterPointCounter -= 1
                        self.updatePointIndex(index)
                        del perimeterPointList[index]
                        del valuesXPerimeter[index]
                        del valuesYPerimeter[index]

            # Para cambiar al modo drag a no drag
            elif event.button() == QtCore.Qt.RightButton:
                if self.handDrag == False:
                    self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
                    self.handDrag = True
                    self.DragModeConnecter.emit(self.handDrag,self.selectorActual)
                else:
                    self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
                    self.handDrag = False
                    self.DragModeConnecter.emit(self.handDrag,self.selectorActual)
        super(PhotoDataViewer, self).mousePressEvent(event)

    # Funcion para actualizar el index de registro de animales
    def updateSharkIndex(self,numero):
        itemlist = self._scene.items()

        for item in itemlist:
            itemtype = type(item)
            if itemtype == QtWidgets.QGraphicsLineItem:
                dataActual = item.data(0)
                if dataActual > numero:
                    item.setData(0,dataActual-1)

    # Funcion para actualizar el index de puntos de perimetro
    def updatePointIndex(self,numero):
        itemlist = self._scene.items()

        for item in itemlist:
            itemtype = type(item)
            if itemtype == QtWidgets.QGraphicsEllipseItem:
                dataActual = item.data(2)
                if dataActual > numero:
                    item.setData(2,dataActual-1)

    # Funcion para emitir el reseteo de datos
    def resetEmit(self):

        #print("[INFO] Se resetea toda la informacion de etiquetado...")

        self.sharkCount = 0
        self.perimeterPointCounter = 0
        self.startSelecting = True
        global tiburonesTotales
        tiburonesTotales = 0
        global valuesXTail
        del valuesXTail[:]
        global valuesYTail
        del valuesYTail[:]
        global valuesXHead
        del valuesXHead[:]
        global valuesYHead
        del valuesYHead[:]
        global perimeterPointList
        del perimeterPointList[:]
        global valuesXPerimeter
        del valuesXPerimeter[:]
        global valuesYPerimeter
        del valuesYPerimeter[:]
        self.labelChecker.emit(0)
        itemlist = self._scene.items()
        for items in itemlist:
            itemtype = type(items)
            if itemtype == QtWidgets.QGraphicsLineItem or itemtype == QtWidgets.QGraphicsEllipseItem:
                self._scene.removeItem(items)

    # Funcion que registra la accion de soltar el clic del raton (Click and Release)
    def mouseReleaseEvent(self, event):
        global color_labelled_data
        global calcGrosor
        if self._photo.isUnderMouse():
            if event.button() == QtCore.Qt.LeftButton:
                if self.handDrag == False and self.startSelecting == True and doubleClick == False and deleteIt == False and perimeterClick == False and measureClick == False:
                    self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
                    e = QtCore.QPointF(self.mapToScene(event.pos()))
                    c = QtGui.QColor(color_labelled_data)
                    pen = QtGui.QPen(c,calcGrosor)
                    linea_item = QtWidgets.QGraphicsLineItem(self.startX,self.startY,e.x(),e.y())
                    linea_item.setData(0,self.sharkCount)
                    linea_item.setPen(pen)
                    self._scene.addItem(linea_item)
                    self.setScene(self._scene)
                    self.selectorActual = 1
                    self.labelUpdater.emit(self.selectorActual,self.sharkCount,QtCore.QPointF(self.mapToScene(event.pos())))
                    self.sharkCount += 1
                    if self.sharkCount > 2:
                        self.labelChecker.emit(1)
                    self.clicked = False
        super(PhotoDataViewer, self).mouseReleaseEvent(event)

    # Funcion que registra el movimiento del raton en el cuadro de la imagen
    def mouseMoveEvent(self, event):
        itemlist = self._scene.items()
        for items in itemlist:
            itemtype = type(items)
            if itemtype == QtWidgets.QGraphicsLineItem and perimeterClick == False: #or itemtype == QtWidgets.QGraphicsEllipseItem
                if items.data(2) == 0:
                    self._scene.removeItem(items)
        if self._photo.isUnderMouse():
            if self.handDrag == False and self.startSelecting == True and doubleClick == False and deleteIt == False and self.clicked == True:
                self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
                e = QtCore.QPointF(self.mapToScene(event.pos()))
                c = QtGui.QColor(color_labelled_data)
                pen = QtGui.QPen(c,calcGrosor)
                pen.setStyle(QtCore.Qt.DashLine)
                linea_item = QtWidgets.QGraphicsLineItem(self.startX,self.startY,e.x(),e.y())
                linea_item.setPen(pen)
                linea_item.setData(2,0)
                self._scene.addItem(linea_item)
                self.setScene(self._scene)
        super(PhotoDataViewer, self).mouseMoveEvent(event)

    # Funcion para cargar los datos etiquetados
    def drawLoadedData(self):
        global calcGrosor
        #Al cargar datos se reinician las variables de interes
        self.startSelecting = True
        pixmap = QPixmap(imagePath)
        self.setPhoto(pixmap)
        for i in range(0,tiburonesTotales):
            valXTail = float(valuesXTail[i])
            valYTail = float(valuesYTail[i])
            valXHead = float(valuesXHead[i])
            valYHead = float(valuesYHead[i])
            c = QtGui.QColor(color_labelled_data)
            pen = QtGui.QPen(c,calcGrosor)
            linea_item = QtWidgets.QGraphicsLineItem(valXTail,valYTail,valXHead,valYHead)
            linea_item.setData(0,i)
            linea_item.setPen(pen)
            self._scene.addItem(linea_item)
            self.setScene(self._scene)
        self.toggleDragMode()

    # Funcion para eliminar los datos registrados al cambiar de un modo de
    # etiquetado a otro modo diferente
    def deleteDataOnSwitchMode(self,perimeter):
        msgBox = QtWidgets.QMessageBox()
        if self.perimeterPointCounter > 0 and perimeter == False:
            msgBox.setWindowTitle("Labelling mode has been selected")
            msgBox.setText("All perimeter data stored will be deleted")
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msgBox.setDefaultButton(QMessageBox.Ok)
            ret = msgBox.exec_()
            if ret == QMessageBox.Ok:
                self.ResetInfoSig.emit()
                return 1
            elif ret == QMessageBox.Cancel:
                return 0
        elif self.sharkCount > 0 and perimeter == True:
            msgBox.setWindowTitle("Select perimeter mode has been selected")
            msgBox.setText("All labelled data stored will be deleted")
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msgBox.setDefaultButton(QMessageBox.Ok)
            ret = msgBox.exec_()
            if ret == QMessageBox.Ok:
                self.ResetInfoSig.emit()
                return 1
            elif ret == QMessageBox.Cancel:
                return 0
        else:
            return 1


# Clase que contiene la tabla con los datos etiquetados por el usuario
class DataTable(QtWidgets.QTableWidget):
    sharkUpdater = QtCore.pyqtSignal()
    loadLinesData = QtCore.pyqtSignal()
    labelChecker = QtCore.pyqtSignal(int)
    resetEmit = QtCore.pyqtSignal()

    # Funcion para inicializar la clase
    def __init__(self, r, c):
        super(DataTable,self).__init__(r, c)
        col_headers = ['Tail X', 'Tail Y', 'Head X', 'Head Y']
        self.setHorizontalHeaderLabels(col_headers)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.show()

    # Funcion para contar las filas que tiene la tabla
    def counter(self):
        global filasActuales
        global empty_row
        filasActuales = self.rowCount()

        item = self.item(0,0)
        item2 = self.item(0,2)
        if item is None and item2 is None:
            empty_row = True
        else:
            empty_row = False

    # Funcion para guardar la tabla de datos en el ordenador
    def save_sheet(self,var):
        cacheDir = None
        cacheType = None
        cacheTitle = None
        cacheInfo = None

        if var == 0 or var == 9: #Datos sin analizar
            cacheDir = 'labelledData'
            cacheType = "_labelled"
            cacheTitle = 'Labelled data saved'
            cacheInfo = "Labelled data has been saved sucessfully"
        elif var == 1: #Datos analizados
            cacheDir = 'analyzedData'
            cacheType = "_analyzed"
            cacheTitle = 'Analyzed data saved'
            cacheInfo = "Analyzed data has been saved sucessfully"

        # Creamos directory o comprobamos si existe
        dirName = cacheDir
        if not os.path.exists(dirName):
            os.mkdir(dirName)
        else:
            pass

        global nameofFileFiltered
        path = cacheDir + "/" + nameofFileFiltered + cacheType +".csv"

        if var == 9:
            path, _ = QFileDialog.getSaveFileName(self, 'Save CSV data', os.getcwd(), 'CSV(*.csv)')

        if path[0] != '':
            with open(path, 'w', newline='') as csv_file:
                writer = csv.writer(csv_file, dialect='excel')
                for row in range(self.rowCount()):
                    row_data = []
                    for column in range(self.columnCount()):
                        item = self.item(row, column)
                        if item is not None:
                            row_data.append(item.text())
                        else:
                            row_data.append('')
                    writer.writerow(row_data)
        if var == 0:
            self.msg = QtWidgets.QMessageBox.about(self,cacheTitle,cacheInfo)

    # Funcion para cargar los datos de un fichero al programa
    def open_sheet(self):
        path = QFileDialog.getOpenFileName(self, 'Open CSV', os.getcwd(), 'CSV(*.csv)')
        if path[0] != '':

            global primeraLlamada
            primeraLlamada = False
            # Se reinician todas las variables de etiquetado
            self.resetEmit.emit()


            with open(path[0], 'r') as csv_file: #rb
                self.setRowCount(0)
                self.setColumnCount(4)
                my_file = csv.reader(csv_file, dialect='excel')
                for row_data in my_file:
                    row = self.rowCount()
                    self.insertRow(row)
                    if len(row_data) > 10:
                        self.setColumnCount(len(row_data))
                    for column, stuff in enumerate(row_data):
                        item = QtWidgets.QTableWidgetItem(stuff)
                        self.setItem(row, column, item)
            #Se activa el menu de analisis
            self.labelChecker.emit(1)

            numColumnas = self.columnCount()
            if numColumnas > 4:
                self.msg = QtWidgets.QMessageBox.about(self,'Error loading',"Please load non analyzed data")
            global cargarDatos
            cargarDatos = True
            self.sharkUpdater.emit()
            self.loadLinesData.emit()
        else:
            return False

# Clase principal que contiene las dos clases: numerica y gráfica
class Window(QtWidgets.QWidget):
    # Funcion de inicializacion
    def __init__(self):
        super(Window, self).__init__()
        self.dialog = WindowResults()
        self.viewer = PhotoDataViewer(self)
        self.data = DataTable(1,4)
        self.editPixInfo = QtWidgets.QLineEdit()
        self.editPixInfo.setReadOnly(True)
        self.viewer.photoClicked.connect(self.photoClicked)
        self.labelling_zone = QtWidgets.QLabel('Labelling Area')
        self.labelling_zone.setStyleSheet("border-bottom-width: 1px; border-bottom-style: solid; border-radius: 0px; font: bold 14px")
        self.labelled_elements = QtWidgets.QLabel('Labelled Elements')
        self.labelled_elements.setStyleSheet("border-bottom-width: 1px; border-bottom-style: solid; border-radius: 0px; font: bold 14px")
        self.label_status = QtWidgets.QLabel('Status...')
        self.label_status.setStyleSheet("font: bold 14px")
        self.splitter = QSplitter(Qt.Horizontal)

        global primeraLlamada
        primeraLlamada = False

        self.viewer.labelUpdater.connect(self.labelUpdater)
        self.data.sharkUpdater.connect(self.sharkUpdater)
        self.data.loadLinesData.connect(self.loadLinesData)
        self.viewer.tableUpdater.connect(self.tableUpdater)
        self.viewer.DragModeConnecter.connect(self.DragModeConnecter)
        self.viewer.ResetInfoSig.connect(self.ResetInfo)
        self.dialog.viewerRes.editVelDirTable.connect(self.editVelDirTable)
        self.viewer.tableRowCounter.connect(self.data.counter)

        # Se conecta el reset del data con el del viewer
        self.data.resetEmit.connect(self.viewer.resetEmit)

        # Se organiza la disposicion de los elementos en la interfaz
        VBlayout = QtWidgets.QVBoxLayout()
        VBlayout1 = QtWidgets.QVBoxLayout()
        HBlayout1 = QtWidgets.QHBoxLayout()
        HBlayout2 = QtWidgets.QHBoxLayout()
        self.widget = QtWidgets.QWidget()
        self.widget.setLayout(VBlayout)
        self.widget1 = QtWidgets.QWidget()
        self.widget1.setLayout(VBlayout1)

        VBlayout.addWidget(self.labelling_zone)
        VBlayout1.addWidget(self.labelled_elements)
        VBlayout.addWidget(self.viewer)
        VBlayout1.addWidget(self.data)
        self.splitter.addWidget(self.widget)
        self.splitter.addWidget(self.widget1)
        self.splitter.setSizes([152,100])
        self.splitter.setHandleWidth(0)
        HBlayout1.addWidget(self.splitter)
        HBlayout2.addWidget(self.editPixInfo)
        HBlayout2.addWidget(self.label_status)
        HBlayout2.addStretch(1)

        grid = QtWidgets.QGridLayout(self)
        grid.addLayout(HBlayout1,0,0,50,2)
        grid.addLayout(HBlayout2,51,1)

    # Funcion para editar la tabla numerica con los datos etiquetados
    def editVelDirTable(self):
        global veldir_position
        global veldir_angle
        global veldir_vec_u
        global veldir_vec_v
        global veldir_velocity
        global filesXPointsCenter
        global filesYPointsCenter

        for i in range(0,len(veldir_vec_u)):
            self.dialog_2.insertRow(i+1)

        r = self.dialog_2.rowCount()
        dim = self.dialog_2.calcDimension(r)

        if dim > 600:
            dim = 600

        self.dialog_2.setGeometry(750,100,1120,dim)
        for i in range(0,len(veldir_vec_u)):
            self.dialog_2.setItem(i,0,QtWidgets.QTableWidgetItem(str(veldir_vec_u[i])))
            self.dialog_2.setItem(i,1,QtWidgets.QTableWidgetItem(str(veldir_vec_v[i])))
            self.dialog_2.setItem(i,2,QtWidgets.QTableWidgetItem(str(veldir_position[i])))
            self.dialog_2.setItem(i,3,QtWidgets.QTableWidgetItem(str(veldir_velocity[i])))
            if i > 0:
                self.dialog_2.setItem(i,4,QtWidgets.QTableWidgetItem(str(veldir_angle[i-1])))

        # Se guarda la tabla en un excel
        self.dialog_2.save_sheet(2)

    # Funcion para alternar modos de seleccion con el cursor o puntero
    def DragModeConnecter(self,var,num):
        if var == True:
            self.label_status.setText('Drag mode selected')
        else:
            if num == 1:
                if perimeterClick == True:
                    self.label_status.setText('Select perimeter points. Status: Select points to obtain perimeter')
                elif doubleClick == True and perimeterClick == False:
                    self.label_status.setText('Point and click. Status: Select Tail')
                elif doubleClick == False and perimeterClick == False:
                    self.label_status.setText('Drag and release. Status: Select Tail')
            elif num == 2:
                if perimeterClick == True:
                    self.label_status.setText('Select perimeter points. Status: Select points to obtain perimeter')
                elif doubleClick == True and perimeterClick == False:
                    self.label_status.setText('Point and click. Status: Select Head')
                elif doubleClick == False and perimeterClick == False:
                    self.label_status.setText('Drag and release. Status: Select Head')

    # Funcion de reseteo de datos
    def restablecerDatos(self):

        #print("[INFO] Yo tambien reseteo cosas...")

        global valuesXTail
        global valuesYTail
        global valuesXHead
        global valuesYHead
        global perimeterPointList
        del perimeterPointList[:]
        global valuesXPerimeter
        del valuesXPerimeter[:]
        global valuesYPerimeter
        del valuesYPerimeter[:]
        global ratio_cm_pixel

        global convexPointList ##-
        del convexPointList[:] ##-

        global areaCalculated ###-
        areaCalculated = False ###-


        self.data.clear()
        col_headers = ['Tail X', 'Tail Y', 'Head X', 'Head Y']
        self.data.setHorizontalHeaderLabels(col_headers)
        self.data.setRowCount(1)
        self.data.setColumnCount(4)
        self.startSelecting = True
        global primeraLlamada
        primeraLlamada = False

        if doubleClick == True:
            self.label_status.setText('Point and click. Status: Select Tail')
        elif doubleClick == False:
            self.label_status.setText('Drag and release. Status: Select Tail')

        tiburones = self.viewer.sharkCount
        for i in range(0,self.viewer.sharkCount):
            if i >= 1:
                self.data.insertRow(i)

            self.data.setItem(i,0, QtWidgets.QTableWidgetItem(str(int(valuesXTail[i]))))
            self.data.setItem(i,1, QtWidgets.QTableWidgetItem(str(int(valuesYTail[i]))))
            self.data.setItem(i,2, QtWidgets.QTableWidgetItem(str(int(valuesXHead[i]))))
            self.data.setItem(i,3, QtWidgets.QTableWidgetItem(str(int(valuesYHead[i]))))
        self.viewer.drawLoadedData()
        self.viewer.sharkCount = tiburones

        if ratio_cm_pixel != 0:
            x = self.viewer._scene.width()
            y = self.viewer._scene.height()
            separacion = int( self.viewer._scene.height() / 195 )
            texto = QtWidgets.QGraphicsTextItem("Ratio (pixel/cm): " + str(ratio_cm_pixel))
            texto.setPos(0 + cte_pos_x * separacion,y - cte_pos_y * separacion)
            font = QFont("Helvetica [Cronyx]", y / 40)
            font.setBold(True)
            texto.setFont(font)
            c = QtGui.QColor(color_perimeter)
            texto.setDefaultTextColor(c)
            self.viewer._scene.addItem(texto)
            self.viewer.setScene(self.viewer._scene)

    # Funcion que carga alprograma la imagen seleccionada
    def loadImage(self):
        global nameofFileFiltered
        #Se reinician los labels de status al abrir una nueva imagen
        self.label_status.setText('Status...')
        self.editPixInfo.setText(' ')
        global cargarDatos
        cargarDatos = False
        global imagePath
        imagePath, _ = QFileDialog.getOpenFileName(self, 'Open File')
        self.pixmap = QPixmap(imagePath)
        self.viewer.setPhoto(self.pixmap)
        #Nos quedamos con el nombre de la imagen para futuro analisis
        nameofFile = imagePath.split('/')[-1]
        nameofFileFiltered = nameofFile.split('.')[0]
        # Al abrir una imagen se reinician todas las variables de interes
        self.data.clear()
        col_headers = ['Tail X', 'Tail Y', 'Head X', 'Head Y']
        self.data.setHorizontalHeaderLabels(col_headers)
        self.data.setRowCount(1)
        global primeraLlamada
        primeraLlamada = False
        self.viewer.resetEmit()
        self.viewer.toggleDragMode()

    # Funcion de reseteo de datos
    def ResetInfo(self):


        #print("[INFO] Hago un reseteo de todo...")

        global doubleClick
        global perimeterClick
        if doubleClick == True:
            self.label_status.setText('Point and click. Status: Select Tail')
        elif doubleClick == False:
            self.label_status.setText('Drag and release. Status: Select Tail')
        if perimeterClick == True:
            self.label_status.setText('Select perimeter points. Status: Select points to obtain perimeter')

        self.editPixInfo.setText(' ')
        self.data.clear()
        col_headers = ['Tail X', 'Tail Y', 'Head X', 'Head Y']
        self.data.setHorizontalHeaderLabels(col_headers)
        self.data.setRowCount(1)
        global primeraLlamada
        primeraLlamada = True #esto estaba en False
        global cargarDatos
        cargarDatos = False
        self.viewer.resetEmit()

    # Funcion para editar la etiqueta con las coordenadas X,Y del mouse
    def photoClicked(self, pos):
        if self.viewer.dragMode()  == QtWidgets.QGraphicsView.NoDrag:
            self.editPixInfo.setText('%d, %d' % (pos.x(), pos.y()))

    # Funcion para actualizar la barra de estado
    def labelUpdater(self, num, tibur, pos):
        global valuesXHead
        global valuesYHead
        global valuesXTail
        global valuesYTail

        global primeraLlamada

        if num == 1:
            if doubleClick == True:
                self.label_status.setText('Point and click. Status: Select Tail')
            elif doubleClick == False:
                self.label_status.setText('Drag and release. Status: Select Tail')
            if primeraLlamada == True:
                self.data.setItem(tibur,2, QtWidgets.QTableWidgetItem(str(int(pos.x()))))
                valuesXHead.append(self.data.item(tibur,2).text())
                self.data.setItem(tibur,3, QtWidgets.QTableWidgetItem(str(int(pos.y()))))
                valuesYHead.append(self.data.item(tibur,3).text())
            primeraLlamada = True
        elif num == 2:
            if doubleClick == True:
                self.label_status.setText('Point and click. Status: Select Head')
            elif doubleClick == False:
                self.label_status.setText('Drag and release. Status: Select Head')
            if tibur >= 1:
                self.data.insertRow(tibur)
            self.data.setItem(tibur,0, QtWidgets.QTableWidgetItem(str(int(pos.x()))))
            valuesXTail.append(self.data.item(tibur,0).text())
            self.data.setItem(tibur,1, QtWidgets.QTableWidgetItem(str(int(pos.y()))))
            valuesYTail.append(self.data.item(tibur,1).text())

    # Funcion para actualizar la tabla numerica
    def tableUpdater(self,num):
        self.data.removeRow(num)
        if self.data.rowCount() == 0:
            self.data.insertRow(0)

    # Funcion para almacenar los datos en el disco
    def saveData(self,var):
        self.data.save_sheet(var)

    # Funcion para cargar los datos del ordenador en el programa
    def loadData(self):
        if imag_loaded == False:
            checker = self.data.open_sheet()
            if checker == False:
                print("[INFO] Se cancela el cargado de datos...")
        else:
            self.showDialog()

    # Funcion para mostrar un cuadro de dialogo de aviso
    def showDialog(self):
        self.msg = QtWidgets.QMessageBox.about(self,'Information',"Please load an image before loading data")

    # Funcion para actualizar el contador de animales etiquetados
    def sharkUpdater(self):
        global tiburonesTotales
        tiburonesTotales = self.data.rowCount()

    # Funcion para dibujar las lineas con los datos de etiquetado
    def loadLinesData(self):
        global valuesXTail
        global valuesYTail
        global valuesXHead
        global valuesYHead
        global tiburonesTotales

        for i in range(0,tiburonesTotales):
            valuesXTail.append(self.data.item(i,0).text())
            valuesYTail.append(self.data.item(i,1).text())
            valuesXHead.append(self.data.item(i,2).text())
            valuesYHead.append(self.data.item(i,3).text())

        self.viewer.drawLoadedData()


    # Funcion para seleccionar datos don dos clics
    def ClickClick(self):
        wantToChangeToPerimeter = False
        cambio = self.viewer.deleteDataOnSwitchMode(wantToChangeToPerimeter)
        if cambio == 1:
            global doubleClick
            doubleClick = True
            global deleteIt
            deleteIt = False
            global perimeterClick
            perimeterClick = False
            global measureClick
            measureClick = False

            self.label_status.setText('Point and click. Status: Select Tail')
            self.viewer.startX = None
            self.viewer.startY = None

    # Funcion para seleccionar datos con clic y arrastre
    def ClickRelease(self):
        wantToChangeToPerimeter = False
        cambio = self.viewer.deleteDataOnSwitchMode(wantToChangeToPerimeter)
        if cambio == 1:
            global doubleClick
            doubleClick = False
            global deleteIt
            deleteIt = False
            global perimeterClick
            perimeterClick = False
            global measureClick
            measureClick = False

            self.viewer.clicked = False
            self.label_status.setText('Drag and release. Status: Select Tail')
            self.viewer.startX = None
            self.viewer.startY = None

    # Funcion para seleccionar datos de perimetro
    def ClickPerimeter(self):
        wantToChangeToPerimeter = True
        cambio = self.viewer.deleteDataOnSwitchMode(wantToChangeToPerimeter)

        if cambio == 1:
            global perimeterClick
            perimeterClick = True
            global deleteIt
            deleteIt = False
            global measureClick
            measureClick = False
            self.label_status.setText('Select perimeter points. Status: Select points to obtain perimeter')
            self.viewer.startX = None
            self.viewer.startY = None

    # Funcion para seleccionar medidas reales en la imagen con dos clics
    def SelectDist(self):
        wantToChangeToPerimeter = False
        cambio = self.viewer.deleteDataOnSwitchMode(wantToChangeToPerimeter)

        if cambio == 1:
            global perimeterClick
            perimeterClick = False
            global doubleClick
            doubleClick = False
            global deleteIt
            deleteIt = False
            global measureClick
            measureClick = True
            self.viewer.clicked = False
            self.label_status.setText('Select actual measurements. Status: Select two points to measure')
            self.viewer.startX = None
            self.viewer.startY = None

    # Funcion para eliminar un dato etiquetado en la imagen
    def DeleteItem(self):
        global deleteIt
        deleteIt = True
        global perimeterClick
        perimeterClick = False
        self.label_status.setText('Delete single item. Status: Select an item to delete it')
        self.viewer.startX = None
        self.viewer.startY = None

    # Funcion para analizar la velocidad y direccion de un grupo de animales
    def VelDirAnalyze(self):
        self.dialog.viewerRes.setPhoto(self.pixmap)
        self.dialog.cb_labelled.setEnabled(False)
        self.dialog.cb_analyzed.setEnabled(False)
        self.dialog.cb_perimeter.setEnabled(False)
        self.dialog.cb_density.setEnabled(False)
        self.dialog.cb_3Ddensity.setEnabled(False)
        self.dialog.savegifbtn.setVisible(True)
        self.dialog.savevideobtn.setVisible(True)
        self.dialog.show()
        self.dialog_2 = DataResults(1,5)
        col_headers = ['Vector U', 'Vector V', 'Distance', 'Velocity', 'Angle']
        self.dialog_2.setHorizontalHeaderLabels(col_headers)
        self.dialog.viewerRes.calculateVelandDir()

    # FUNCIONALIDAD EXTRA (NO IMPLEMENTADA):
    # Esta función se encargaria de detectar heridas en una imagen de forma
    # automatica con herramientas de aprendizaje
    def ImageAnalyze(self):
        #########################################
        print('Se analiza la imagen en busca de heridas...')
        #########################################
        # Se tiene que llamar a una funcion de viewerRes dentro de dialog y que se muestre
        # etc etc...

    # Función para analizar los datos de perímetro
    def PerimeterAnalyze(self):
        global perAnalyze

        self.dialog.viewerRes.setPhoto(self.pixmap)
        self.dialog.cb_labelled.setEnabled(False)
        self.dialog.cb_analyzed.setEnabled(False)
        self.dialog.cb_perimeter.setEnabled(True)
        self.dialog.cb_density.setEnabled(True)
        self.dialog.show()

        if perAnalyze == True:
            self.dialog.viewerRes.ImageProcess(1,0)
        else:
            self.dialog.viewerRes.ImageProcess(0,0)
            self.dialog_2 = DataResults(1,1)

        #self.dialog_2 = DataResults(1,1)

        if ratio_cm_pixel != 0:
            x = self.dialog.viewerRes._scene.width()
            y = self.dialog.viewerRes._scene.height()
            separacion = int( self.dialog.viewerRes._scene.height() / 195 )
            texto = QtWidgets.QGraphicsTextItem("Ratio (pixel/cm): " + str(ratio_cm_pixel))
            texto.setPos(0 + cte_pos_x * separacion,y - cte_pos_y * separacion)
            font = QFont("Helvetica [Cronyx]", y / 40)
            font.setBold(True)
            texto.setFont(font)
            c = QtGui.QColor(color_perimeter)
            texto.setDefaultTextColor(c)
            self.dialog.viewerRes._scene.addItem(texto)
            self.dialog.viewerRes.setScene(self.dialog.viewerRes._scene)

    # Función para analizar los datos etiquetados
    def DataAnalyze(self):
        global valuesXTail
        del valuesXTail[:]
        global valuesYTail
        del valuesYTail[:]
        global valuesXHead
        del valuesXHead[:]
        global valuesYHead
        del valuesYHead[:]
        global valuesXMed
        del valuesXMed[:]
        global valuesYMed
        del valuesYMed[:]
        global vec_u
        del vec_u[:]
        global vec_v
        del vec_v[:]
        global neighList
        del neighList[:]
        global angleList
        del angleList[:]
        global indexList
        del indexList[:]
        global midPointList
        del midPointList[:]
        global perAnalyze
        global tiburonesTotales
        global errorAnalyzing
        global ratio_cm_pixel

        tiburonesTotales = self.viewer.sharkCount
        #Se comprueba que esten todos los datos correctamente (ultimo pez marcado bien)
        longitud_comprobacion = self.data.rowCount()

        if self.viewer.sharkCount < longitud_comprobacion:
            errorAnalyzing = True
        elif self.viewer.sharkCount == longitud_comprobacion:
            errorAnalyzing = False

        if errorAnalyzing == False:
            #Se cargan los valores en las listas para operar con ellos
            for i in range(0,self.viewer.sharkCount):
                valuesXTail.append(self.data.item(i,0).text())
                valuesYTail.append(self.data.item(i,1).text())
                valuesXHead.append(self.data.item(i,2).text())
                valuesYHead.append(self.data.item(i,3).text())
            for columna in range(4,11):
                self.data.insertColumn(columna)
            col_headers = ['Tail X', 'Tail Y', 'Head X', 'Head Y', 'X med', 'Y med','u','v','Index','Distance','Angle']
            self.data.setHorizontalHeaderLabels(col_headers)
            #Se calcula y add a la tabla el punto medio X e Y de los datos en Pixeles
            self.MidPointCalc()
            #Se calcula y add a la tabla el vector u y v
            self.VectorsCalc()
            #Se calcula el vecino mas proximo y la distancia al mismo
            self.ClosestPoint()
            #Se calcula el angulo entre los vectores propios y el vecino mas proximo
            self.AngleVectors()
            #Se guardan los datos analizados
            self.saveData(1)
            #Tocaria abrir una nueva ventana que muestre los vectores dibujados y los datos en otro excel
            #self.dialog = WindowResults()
            self.dialog.viewerRes.setPhoto(self.pixmap)
            self.dialog.cb_labelled.setEnabled(True)
            self.dialog.cb_analyzed.setEnabled(True)
            self.dialog.cb_perimeter.setEnabled(True)
            self.dialog.cb_density.setEnabled(True)

            self.dialog.cb_3Ddensity.setEnabled(True)
            self.dialog.savegifbtn.setVisible(False)
            self.dialog.savevideobtn.setVisible(False)



            if ratio_cm_pixel != 0:
                x = self.dialog.viewerRes._scene.width()
                y = self.dialog.viewerRes._scene.height()
                separacion = int( self.dialog.viewerRes._scene.height() / 195 )
                texto = QtWidgets.QGraphicsTextItem("Ratio (pixel/cm): " + str(ratio_cm_pixel))
                texto.setPos(0 + cte_pos_x * separacion,y - cte_pos_y * separacion)
                font = QFont("Helvetica [Cronyx]", y / 40)
                font.setBold(True)
                texto.setFont(font)
                c = QtGui.QColor(color_perimeter)
                texto.setDefaultTextColor(c)
                self.dialog.viewerRes._scene.addItem(texto)
                self.dialog.viewerRes.setScene(self.dialog.viewerRes._scene)

            self.dialog.show()
            self.sharkUpdater()
            self.dialog.viewerRes.drawLoadedData(3)
            if perAnalyze == True:
                self.dialog.viewerRes.ImageProcess(1,0)
            else:
                self.dialog.viewerRes.ImageProcess(0,0)

            #self.dialog.viewerRes.saveImageAnalyzed()
            self.dialog_2 = DataResults(self.viewer.sharkCount,11)
            self.copyDataInNewTable()
        else:
            self.msg = QtWidgets.QMessageBox.about(self,'Error analyzing','There is an incomplete selected fish')


    # Función para copiar los datos analizados de la Interfaz Básica a la
    # Interfaz Avanzada
    def copyDataInNewTable(self):
        for i in range(self.viewer.sharkCount):
            for j in range(11):
                valToCopy_item = self.data.item(i,j)
                valToCopy_val = valToCopy_item.text()
                self.dialog_2.setItem(i,j,QtWidgets.QTableWidgetItem(str(valToCopy_val)))
        self.dialog_2.show()

    # Función para calcular los ángulos y los vectores
    def AngleVectors(self):
        global vec_u
        global vec_v

        for i in range(self.viewer.sharkCount):
            valU = vec_u[i]
            valV = vec_v[i]
            vector_1 = (valU,valV)
            indexVec = indexList[i]
            indexVec_val = indexVec
            valU_neigh = vec_u[indexVec_val]
            valV_neigh = vec_v[indexVec_val]
            vector_2 = (valU_neigh,valV_neigh)
            angulo_rad = self.angle_between(vector_1,vector_2)
            angulo_degree = np.rad2deg(angulo_rad)
            #Se redondea el angulo a dos decimales
            angulo_degree = round(angulo_degree,2)
            angleList.append(angulo_degree)
            self.data.setItem(i,10,QtWidgets.QTableWidgetItem(str(angleList[i])))

    # Función para calcular el vector unitario
    def unit_vector(self,vector):
        return vector / np.linalg.norm(vector)

    # Función para calcular el ángulo entre dos vectores
    def angle_between(self,v1, v2):
        v1_u = self.unit_vector(v1)
        v2_u = self.unit_vector(v2)
        return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

    # Función para buscar el punto más próximo a un listado de puntos
    def ClosestPoint(self):
        for posicion in range(self.viewer.sharkCount):
            valX = valuesXMed[posicion]
            valY = valuesYMed[posicion]
            point = [valX,valY]
            midPointList.append(point)

        X = np.array(midPointList)
        tree = KDTree(X,leaf_size=2)
        dist,ind = tree.query(X[:self.viewer.sharkCount],k=2)

        global indexList
        global neighList
        for i in range(self.viewer.sharkCount):
            indexNum = ind[i]
            realIndex = indexNum[1]
            indexList.append(realIndex)
            self.data.setItem(i,8,QtWidgets.QTableWidgetItem(str(indexList[i]+1)))
            indexNum = dist[i]
            realIndex = indexNum[1]
            neighList.append(realIndex)
            self.data.setItem(i,9,QtWidgets.QTableWidgetItem(str(int(neighList[i]))))


    # Función para calcular los vectores
    def VectorsCalc(self):
        global vec_u
        global vec_v
        for i in range(self.data.rowCount()):
            number = float(float(valuesYHead[i])-float(valuesYTail[i]))
            vec_u.append(number)
            self.data.setItem(i,6, QtWidgets.QTableWidgetItem(str(int(vec_u[i]))))
            number = float(float(valuesXHead[i])-float(valuesXTail[i]))
            vec_v.append(number)
            self.data.setItem(i,7, QtWidgets.QTableWidgetItem(str(int(vec_v[i]))))


    # Función para calcular el punto medio de cada dato etiquetado
    def MidPointCalc(self):
        global valuesXMed
        global valuesYMed

        for i in range(self.data.rowCount()):
            number = float((float(valuesXHead[i])+float(valuesXTail[i]))/2)
            valuesXMed.append(number)
            self.data.setItem(i,4, QtWidgets.QTableWidgetItem(str(int(valuesXMed[i]))))
            number = float((float(valuesYHead[i])+float(valuesYTail[i]))/2)
            valuesYMed.append(number)
            self.data.setItem(i,5, QtWidgets.QTableWidgetItem(str(int(valuesYMed[i]))))


    # Funcion para ordenar datos de manera alphanumerica
    def sorted_aphanumeric(self,data):
        convert = lambda text: int(text) if text.isdigit() else text.lower()
        alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
        return sorted(data, key=alphanum_key)

    # Función para renombrar datos
    def renameData(self):
        global renameFolderName

        i = 0
        directorio = QFileDialog.getExistingDirectory(self, 'Select Dataset of raw images')

        if directorio != '':

            renameFolderName = directorio.split('/')[-1] + "/"

            files = os.listdir(directorio)
            files = self.sorted_aphanumeric(files)
            dataName, okPressed = QInputDialog.getText(self, "Rename Dataset", "Insert new name:")

            if okPressed:
                for filename in files:
                    src = directorio + "/" + filename
                    format = src.split('.')[-1]
                    number = '{0:03}'.format(i)
                    dst = dataName + str(number) + "."+ format
                    dst = directorio + "/" + dst
                    os.rename(src,dst)
                    i+=1

# Clase principal o Main del programa que contiene la ventana principal
# que a su vez contiene al resto de clases
class Interfaz(QMainWindow):
    # Función de inicializacion
    def __init__(self):
        super(Interfaz,self).__init__()
        self.optMen = OptionsMenu()
        self.win = Window()
        self.setCentralWidget(self.win)
        self.init_ui()
    def init_ui(self):
        # Create images folder if it doesn't exist
        dirName = "imagesToAnalyze"
        if not os.path.exists(dirName):
            os.mkdir(dirName)
        else:
            pass
        # Se crea la barra de herramientas
        bar = self.menuBar()
        bar.setNativeMenuBar(False)
        # Se crean los menús y submenús de la barra de herramientas
        file = bar.addMenu('File')
        analyze_info = bar.addMenu('Analyze Labelled Info')
        #analyze_image = bar.addMenu('Analyze Image')
        labelling_methods = bar.addMenu('Labelling Method')
        delete_options = bar.addMenu('Delete Options')
        personal_options = bar.addMenu('Options')

        # Señales que conectan esta clase con otras clases
        self.win.dialog.hideandshowSignal.connect(self.mostrar)
        self.win.data.labelChecker.connect(self.labelChecker)
        self.win.viewer.labelChecker.connect(self.labelChecker)
        self.win.viewer.editAnalyzeImageLabel.connect(self.editAnalyzeImageLabel)

        # Se crean las acciones al interactuar con los menús
        #self.analyze_image_action = QAction('Analyze &loaded Image', self)
        #self.analyze_image_action.setShortcut('Ctrl+K')
        #self.analyze_image_action.setEnabled(False)
        self.rename_dataset_action = QAction('&Rename Dataset', self)
        self.rename_dataset_action.setShortcut('Ctrl+T')
        self.options = QAction('Preferences', self)
        self.options.setShortcut('Ctrl+I')
        self.analyze_action = QAction('&Analyze labelled data',self)
        self.analyze_action.setShortcut('Ctrl+A')
        self.analyze_action.setEnabled(False)
        self.analyze_perimeter_action = QAction('Analyze &perimeter data',self)
        self.analyze_perimeter_action.setShortcut('Ctrl+U')
        self.analyze_perimeter_action.setEnabled(False)
        self.analyze_dir_vel_action = QAction('Analyze &velocity and direction of school', self)
        self.analyze_dir_vel_action.setShortcut('Ctrl+V')
        self.analyze_dir_vel_action.setEnabled(False)
        self.save_action = QAction('&Save data',self)
        self.save_action.setShortcut('Ctrl+S')
        self.save_action.setEnabled(False)

        self.save_as_action = QAction('Save &as',self)
        self.save_as_action.setShortcut('Ctrl+E')
        self.save_as_action.setEnabled(False)

        self.open_action = QAction('&New file',self)
        self.open_action.setShortcut('Ctrl+N')
        self.open_data_action = QAction('&Load data',self)
        self.open_data_action.setShortcut('Ctrl+L')
        self.open_data_action.setEnabled(False)
        self.quit_action = QAction('&Quit program',self)
        self.quit_action.setShortcut('Ctrl+Q')
        self.reset_action = QAction('&Reset labelling info', self)
        self.reset_action.setShortcut('Ctrl+X')
        self.reset_action.setEnabled(False)
        self.delete_items = QAction('&Delete single item', self)
        self.delete_items.setShortcut('Ctrl+D')
        self.delete_items.setCheckable(True)
        self.delete_items.setChecked(False)
        self.delete_items.setEnabled(False)
        self.click_perimeter = QAction('&Select perimeter points', self)
        self.click_perimeter.setShortcut('Ctrl+B')
        self.click_perimeter.setCheckable(True)
        self.click_perimeter.setChecked(False)
        self.click_perimeter.setEnabled(False)
        self.click_and_click = QAction('&Point and click', self)
        self.click_and_click.setShortcut('Ctrl+P')
        self.click_and_click.setCheckable(True)
        self.click_and_click.setChecked(True)
        self.click_and_click.setEnabled(False)
        self.click_and_release = QAction('Drag and &release', self)
        self.click_and_release.setShortcut('Ctrl+R')
        self.click_and_release.setCheckable(True)
        self.click_and_release.setChecked(False)
        self.click_and_release.setEnabled(False)
        self.select_actual_measurements = QAction('Select &actual measurements', self)
        self.select_actual_measurements.setShortcut('Ctrl+M')
        self.select_actual_measurements.setCheckable(True)
        self.select_actual_measurements.setChecked(False)
        self.select_actual_measurements.setEnabled(False)
        # Se añaden acciones a cada menú
        file.addAction(self.open_action)
        file.addAction(self.open_data_action)
        file.addAction(self.save_action)
        file.addAction(self.save_as_action)
        file.addAction(self.rename_dataset_action)
        file.addAction(self.quit_action)
        labelling_methods.addAction(self.click_and_click)
        labelling_methods.addAction(self.click_and_release)
        labelling_methods.addAction(self.click_perimeter)
        labelling_methods.addAction(self.select_actual_measurements)
        delete_options.addAction(self.reset_action)
        delete_options.addAction(self.delete_items)
        analyze_info.addAction(self.analyze_action)
        analyze_info.addAction(self.analyze_perimeter_action)
        analyze_info.addAction(self.analyze_dir_vel_action)
        #analyze_image.addAction(self.analyze_image_action)
        personal_options.addAction(self.options)
        # Eventos al hacer clic con el raton
        self.quit_action.triggered.connect(self.quit_trigger)
        file.triggered.connect(self.selected)
        labelling_methods.triggered.connect(self.selected)
        delete_options.triggered.connect(self.selected)
        analyze_info.triggered.connect(self.analyze)
        #analyze_image.triggered.connect(self.image_analyze_selected)
        personal_options.triggered.connect(self.showOptions)

        self.setWindowTitle("Collective Behaviour Tool")
        self.show()

    # Función para activar el submenu de Análisis automatico en busca de heridas
    # en una imagen (FUNCIÓN NO IMPLEMENTADA)
    def editAnalyzeImageLabel(self):
        pass
        #self.analyze_image_action.setEnabled(True)

    # Función para activar/desactivar los menús de la barra de herramientas
    # según el tipo de etiquetado activo o de datos registrados
    def labelChecker(self,num):
        global perimeterPointList
        if num == 1:
            self.analyze_action.setEnabled(True)
            self.click_perimeter.setEnabled(False)
        elif num == 0:
            self.analyze_action.setEnabled(False)
            self.click_perimeter.setEnabled(True)
        if len(perimeterPointList) >= 3:
            self.analyze_perimeter_action.setEnabled(True)
            self.click_and_release.setEnabled(False)
            self.click_and_click.setEnabled(False)
            self.select_actual_measurements.setEnabled(False)
        else:
            self.analyze_perimeter_action.setEnabled(False)
            self.click_and_release.setEnabled(True)
            self.click_and_click.setEnabled(True)
            self.select_actual_measurements.setEnabled(True)

    # Función para mostrar la Interfaz Básica tras regresar de la Interfaz
    # Avanzada
    def mostrar(self):
        global perAnalyze

        if not perAnalyze:
            self.win.dialog_2.hide()
        #al volver se elimina analisis y se quedan datos
        self.win.restablecerDatos()
        self.labelChecker(9) # numero al azar ##-
        self.show()

    # Función para cerrar la aplicación
    def quit_trigger(self):
        qApp.quit()

    # Función para escoger una opción de la barra de herramientas
    def selected(self,q):
        option = q.text()
        if option == '&New file':
            self.win.loadImage()
            if imag_loaded == False:
                self.save_action.setEnabled(True)
                self.save_as_action.setEnabled(True)
                self.open_data_action.setEnabled(True)
                self.reset_action.setEnabled(True)
                self.delete_items.setEnabled(True)
                self.click_and_click.setEnabled(True)
                self.click_and_release.setEnabled(True)
                #self.analyze_action.setEnabled(True)
                #self.analyze_perimeter_action.setEnabled(True)
                self.click_perimeter.setEnabled(True)
                self.analyze_dir_vel_action.setEnabled(True)
                self.select_actual_measurements.setEnabled(True)
        elif option == '&Rename Dataset':
            self.win.renameData()
        elif option == '&Save data':
            self.win.saveData(0)
        elif option == 'Save &as':
            self.win.saveData(9)
        elif option == '&Load data':
            self.win.loadData()
        elif option == '&Point and click':
            self.click_and_release.setChecked(False)
            self.click_and_click.setChecked(True)
            self.delete_items.setChecked(False)
            self.click_perimeter.setChecked(False)
            self.select_actual_measurements.setChecked(False)
            self.win.ClickClick()
        elif option == 'Drag and &release':
            self.click_and_release.setChecked(True)
            self.click_and_click.setChecked(False)
            self.delete_items.setChecked(False)
            self.click_perimeter.setChecked(False)
            self.select_actual_measurements.setChecked(False)
            self.win.ClickRelease()
        elif option == '&Delete single item':
            self.click_and_release.setChecked(False)
            self.click_and_click.setChecked(False)
            self.delete_items.setChecked(True)
            self.click_perimeter.setChecked(False)
            self.select_actual_measurements.setChecked(False)
            self.win.DeleteItem()
        elif option == '&Reset labelling info':
            self.win.ResetInfo()
        elif option == '&Select perimeter points':
            self.click_perimeter.setChecked(True)
            self.click_and_release.setChecked(False)
            self.click_and_click.setChecked(False)
            self.delete_items.setChecked(False)
            self.select_actual_measurements.setChecked(False)
            self.win.ClickPerimeter()
        elif option == 'Select &actual measurements':
            self.click_perimeter.setChecked(False)
            self.click_and_release.setChecked(False)
            self.click_and_click.setChecked(False)
            self.delete_items.setChecked(False)
            self.select_actual_measurements.setChecked(True)
            self.win.SelectDist()

    # Función para analizar la imagen escogida de forma automatica
    # (FUNCIONALIDAD NO IMPLEMENTADA)
    def image_analyze_selected(self,q):
        option = q.text()
        if option == 'Analyze &loaded Image':
            self.win.ImageAnalyze()

    # Función para escoger el tipo de análisis
    def analyze(self,q):
        global perAnalyze

        option = q.text()
        if option == '&Analyze labelled data':
            self.win.DataAnalyze()
        elif option == 'Analyze &perimeter data':
            perAnalyze = True
            self.win.PerimeterAnalyze()
        elif option == 'Analyze &velocity and direction of school':
            self.win.VelDirAnalyze()

        if errorAnalyzing == False:
            self.hide()

    # Función para mostrar el menú de Preferencias
    def showOptions(self):
        self.optMen.show()

# Inicializacion del programa
if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Interfaz()
    window.setGeometry(400, 200, 1280, 768)
    window.show()
    sys.exit(app.exec_())
