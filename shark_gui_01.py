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

calcGrosor = 11
calcGrosorAnalyzed = 10

color_labelled_data = "#000000"
color_labelled_analyzed_data = "#008000"
color_perimeter = "#ff0000"
color_vector1 = "#0000ff"
color_vector2 = "#ff0000"
color_dot1 = "#0000ff"
color_dot2 = "#008000"

color_layers = "#0000ff"

number_of_layers = 255

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


class OptionsMenu(QtWidgets.QWidget):

    def __init__(self):
        super(OptionsMenu, self).__init__()

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
        #self.slider_layers.setValue(number_of_layers)

        self.labelled_analyzed_data_color = QPushButton()
        self.labelled_analyzed_data_color.setStyleSheet("background-color: green")

        self.labelled_data_label = QtWidgets.QLabel('Labelled data')
        self.labelled_analyzed_data_label = QtWidgets.QLabel('Labelled data analyzed')
        self.perimeter_label = QtWidgets.QLabel('Perimeter')
        self.vector1_label = QtWidgets.QLabel('Vector 1')
        self.vector2_label = QtWidgets.QLabel('Vector 2')
        self.dot1_label = QtWidgets.QLabel('Dot 1')
        self.dot2_label = QtWidgets.QLabel('Dot 2')

        self.layers_label = QtWidgets.QLabel('Number of layers')
        self.layers_value = QtWidgets.QLabel("0")



        #Connect buttons

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

        # New layout
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


        grid.addWidget(self.savePreferencesButton,11,0)



        if os.path.exists('config.txt') == True:
            #print('existe el fichero')
            global color_labelled_data
            global color_perimeter
            global color_vector1
            global color_vector2
            global color_dot1
            global color_dot2
            global color_labelled_analyzed_data
            global number_of_layers
            global color_layers

            file = open("config.txt","r")

            string = file.readline()
            #print(string)
            color_labelled_data = string[:-1]
            self.labelled_data_color.setStyleSheet("QWidget { background-color: %s}" % color_labelled_data)

            string = file.readline()
            #print(string)
            color_perimeter = string[:-1]
            self.perimeter_color.setStyleSheet("QWidget { background-color: %s}" % color_perimeter)

            string = file.readline()
            #print(string)
            color_vector1 = string[:-1]
            self.vector1_color.setStyleSheet("QWidget { background-color: %s}" % color_vector1)

            string = file.readline()
            #print(string)
            color_vector2 = string[:-1]
            self.vector2_color.setStyleSheet("QWidget { background-color: %s}" % color_vector2)

            string = file.readline()
            #print(string)
            color_dot1 = string[:-1]
            self.dot1_color.setStyleSheet("QWidget { background-color: %s}" % color_dot1)

            string = file.readline()
            #print(string)
            color_dot2 = string[:-1]
            self.dot2_color.setStyleSheet("QWidget { background-color: %s}" % color_dot2)

            string = file.readline()
            #print(string)
            color_labelled_analyzed_data = string[:-1]
            self.labelled_analyzed_data_color.setStyleSheet("QWidget { background-color: %s}" % color_labelled_analyzed_data)

            string = file.readline()
            #print(string)
            number_of_layers = int(string[:-1])
            self.layers_value.setText(str(number_of_layers))
            self.slider_layers.setValue(number_of_layers)

            string = file.readline()
            #print(string)
            color_layers = string[:-1]
            self.layers_color.setStyleSheet("QWidget { background-color: %s}" % color_layers)

            #print(color_labelled_data)
            #print(color_perimeter)
            #print(color_vector1)
            #print(color_vector2)
            #print(color_dot1)
            #print(color_dot2)
            #print(color_labelled_analyzed_data)
            #print(str(number_of_layers))
            #print(color_layers)

        else:
            #print('no existe el fichero')
            color_labelled_data = self.labelled_data_color.palette().color(QtGui.QPalette.Base).name()
            color_perimeter = self.perimeter_color.palette().color(QtGui.QPalette.Base).name()
            color_vector1 = self.vector1_color.palette().color(QtGui.QPalette.Base).name()
            color_vector2 = self.vector2_color.palette().color(QtGui.QPalette.Base).name()
            color_dot1 = self.dot1_color.palette().color(QtGui.QPalette.Base).name()
            color_dot2 = self.dot2_color.palette().color(QtGui.QPalette.Base).name()
            color_labelled_analyzed_data = self.labelled_analyzed_data_color.palette().color(QtGui.QPalette.Base).name()
            color_layers = self.layers_color.palette().color(QtGui.QPalette.Base).name()

            self.slider_layers.setValue(number_of_layers)
        #self.show()

    def changeValue(self,val):
        global number_of_layers
        number_of_layers = val
        self.layers_value.setText(str(val))




    def saveDataInTextFile(self):

        #Hay que hacer lo de guardar los QColors en un fichero de texto con nombre config.txt
        #al abrir programa se carga el fichero y se asignan las variables globales
        # hay que cambiar todas al pintar en todas partes
        #habria que poner por defecto que sean los colores que se marcan
        global color_labelled_data
        global color_perimeter
        global color_vector1
        global color_vector2
        global color_dot1
        global color_dot2
        global color_labelled_analyzed_data
        global number_of_layers
        global color_layers

        file = open("config.txt","w")

        #print('Se van a guardar los siguientes colores:')

        #print(color_labelled_data)
        #print(color_perimeter)
        #print(color_vector1)
        #print(color_vector2)
        #print(color_dot1)
        #print(color_dot2)
        #print(color_labelled_analyzed_data)
        #print(number_of_layers)
        #print(color_layers)

        file.write(color_labelled_data+"\n")
        file.write(color_perimeter+"\n")
        file.write(color_vector1+"\n")
        file.write(color_vector2+"\n")
        file.write(color_dot1+"\n")
        file.write(color_dot2+"\n")
        file.write(color_labelled_analyzed_data+"\n")
        file.write(str(number_of_layers)+"\n")
        file.write(color_layers+"\n")

        file.close()
        self.hide()


    def layers_color_dialog(self):
        global color_layers
        color_layers = QColorDialog.getColor()
        if color_layers.isValid():
            #print(color_layers)
            self.layers_color.setStyleSheet("QWidget { background-color: %s}" % color_layers.name())
            color_layers = color_layers.name()
        else:
            color_layers = self.layers_color.palette().color(QtGui.QPalette.Base).name()

        #print(color_layers)

        #Se buscan todas las tonalidades existentes desde la seleccionada

        parte_R = color_layers[1:3]
        #print(parte_R)
        cant_R = int(parte_R,16)
        #print(cant_R)

        parte_G = color_layers[3:5]
        #print(parte_G)
        cant_G = int(parte_G,16)
        #print(cant_G)

        parte_B = color_layers[5:7]
        #print(parte_B)
        cant_B = int(parte_B,16)
        #print(cant_B)

        maximum = self.maximumOfRGB(cant_R,cant_G,cant_B)
        self.slider_layers.setMaximum(maximum)

    def maximumOfRGB(self,r,g,b):
        list = [r,g,b]
        return max(list)



    def labelled_data_color_dialog(self):
        global color_labelled_data
        color_labelled_data = QColorDialog.getColor()
        if color_labelled_data.isValid():
            #print(color_labelled_data)
            self.labelled_data_color.setStyleSheet("QWidget { background-color: %s}" % color_labelled_data.name())
            color_labelled_data = color_labelled_data.name()
        else:
            color_labelled_data = self.labelled_data_color.palette().color(QtGui.QPalette.Base).name()

        #print(color_labelled_data)

    def perimeter_color_dialog(self):
        global color_perimeter
        color_perimeter = QColorDialog.getColor()
        if color_perimeter.isValid():
            #print(color_perimeter)
            self.perimeter_color.setStyleSheet("QWidget { background-color: %s}" % color_perimeter.name())
            color_perimeter = color_perimeter.name()
        else:
            color_perimeter = self.perimeter_color.palette().color(QtGui.QPalette.Base).name()

        #print(color_perimeter)

    def vector1_color_dialog(self):
        global color_vector1
        color_vector1 = QColorDialog.getColor()
        if color_vector1.isValid():
            #print(color_vector1)
            self.vector1_color.setStyleSheet("QWidget { background-color: %s}" % color_vector1.name())
            color_vector1 = color_vector1.name()
        else:
            color_vector1 = self.vector1_color.palette().color(QtGui.QPalette.Base).name()

        #print(color_vector1)

    def vector2_color_dialog(self):
        global color_vector2
        color_vector2 = QColorDialog.getColor()
        if color_vector2.isValid():
            #print(color_vector2)
            self.vector2_color.setStyleSheet("QWidget { background-color: %s}" % color_vector2.name())
            color_vector2 = color_vector2.name()
        else:
            color_vector2 = self.vector2_color.palette().color(QtGui.QPalette.Base).name()

        #print(color_vector2)

    def dot1_color_dialog(self):
        global color_dot1
        color_dot1 = QColorDialog.getColor()
        if color_dot1.isValid():
            #print(color_dot1)
            self.dot1_color.setStyleSheet("QWidget { background-color: %s}" % color_dot1.name())
            color_dot1 = color_dot1.name()
        else:
            color_dot1 = self.dot1_color.palette().color(QtGui.QPalette.Base).name()

        #print(color_dot1)

    def dot2_color_dialog(self):
        global color_dot2
        color_dot2 = QColorDialog.getColor()
        if color_dot2.isValid():
            #print(color_dot2)
            self.dot2_color.setStyleSheet("QWidget { background-color: %s}" % color_dot2.name())
            color_dot2 = color_dot2.name()
        else:
            color_dot2 = self.dot2_color.palette().color(QtGui.QPalette.Base).name()

        #print(color_dot2)

    def labelled_analyzed_data_color_dialog(self):
        global color_labelled_analyzed_data
        color_labelled_analyzed_data = QColorDialog.getColor()
        if color_labelled_analyzed_data.isValid():
            #print(color_labelled_analyzed_data)
            self.labelled_analyzed_data_color.setStyleSheet("QWidget { background-color: %s}" % color_labelled_analyzed_data.name())
            color_labelled_analyzed_data = color_labelled_analyzed_data.name()
        else:
            color_labelled_analyzed_data = self.labelled_analyzed_data_color.palette().color(QtGui.QPalette.Base).name()

        #print(color_labelled_analyzed_data)


class WindowResults(QtWidgets.QWidget):

    hideandshowSignal = QtCore.pyqtSignal()

    rePaintAfterDensity = QtCore.pyqtSignal()

    def __init__(self):
        super(WindowResults, self).__init__()


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

        self.cb_labelled.stateChanged.connect(self.drawStuff)
        self.cb_analyzed.stateChanged.connect(self.drawStuff)
        self.cb_perimeter.stateChanged.connect(self.drawStuff)

        self.cb_density.stateChanged.connect(self.drawHeatMap)

        self.savebtn.clicked.connect(self.selecteds)
        self.backtolabel.clicked.connect(self.backmenu)

        self.viewerRes.editMassCenter.connect(self.editMassCenter)
        self.viewerRes.reDrawStuff.connect(self.drawStuff)

        self.viewerRes.editVelocityLabel.connect(self.editLabelVelocity)

        self.savegifbtn.clicked.connect(self.viewerRes.saveAnimation)

        self.savevideobtn.clicked.connect(self.viewerRes.saveVideo)


        self.rePaintAfterDensity.connect(self.viewerRes.rePaintAfterDensity)

        # Arrange layout

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
        #VBlayout1.addStretch(1)
        VBlayout1.addWidget(self.cb_labelled)
        VBlayout1.addWidget(self.cb_analyzed)
        VBlayout1.addWidget(self.cb_perimeter)
        VBlayout1.addWidget(self.cb_density)

        VBlayout1.addStretch(1)

        VBlayout1.addWidget(self.backtolabel)

        MainLayout.addLayout(VBlayout)
        MainLayout.addLayout(VBlayout1)

        #self.show()

    def backmenu(self):
        global densityCalculated
        global perimeterSaved

        if densityCalculated == True:
            #print('Borrando imagen cache')
            os.remove("cache_heatmap.JPG")
        self.hide()
        self.hideandshowSignal.emit()

        densityCalculated = False
        perimeterSaved = False

        self.cb_labelled.setChecked(False)
        self.cb_analyzed.setChecked(False)
        self.cb_perimeter.setChecked(False)
        self.cb_density.setChecked(False)


    def selecteds(self,q):
        self.viewerRes.saveImageAnalyzed()


    def drawHeatMap(self):
        global perAnalyze

        if self.cb_density.isChecked():
            #print('calc y mostrar densidad')

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



    def drawStuff(self):

        self.viewerRes.resetView(3)

        if self.cb_labelled.isChecked():
            #print('pintamos labelled')
            self.viewerRes.drawLoadedData(0)
        else:
            self.viewerRes.resetView(0)

        if self.cb_analyzed.isChecked():
            #print('pintamos analyzed')
            self.viewerRes.drawLoadedData(1)
        else:
            self.viewerRes.resetView(1)

        if self.cb_perimeter.isChecked():
            #print('calc y dibujar perimetro')

            if perAnalyze == True:
                self.viewerRes.ImageProcess(1,1)
            else:
                self.viewerRes.ImageProcess(0,1)
        else:
            self.viewerRes.resetView(2)

    def editMassCenter(self):

        self.editPixMassCenter.setText('%d, %d' % (valCenterMassX,valCenterMassY))


    def editLabelVelocity(self):
        global schoolVelocity

        self.centermassVals.setText("Average school velocity (pixels/s): ")
        self.editPixMassCenter.setText('%d' % schoolVelocity)




class DataResults(QtWidgets.QTableWidget):

    def __init__(self, r, c):
        super(DataResults,self).__init__(r, c)
        self.setWindowTitle('Results of Analysis - Data')
        col_headers = ['Tail X', 'Tail Y', 'Head X', 'Head Y', 'X med', 'Y med','u','v','Index','Distance','Angle']
        self.setHorizontalHeaderLabels(col_headers)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        dim = self.calcDimension(r)

        if dim > 600:
            dim = 600

        self.setGeometry(750,100,1120,dim)
        self.show()

    def calcDimension(self,r):
        total = r*30+40
        return total

    def save_sheet(self,var):
        #path = QFileDialog.getSaveFileName(self, 'Save data in CSV file', os.getcwd(), 'CSV(*.csv)')

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
            #print("Directory ", dirName , "Created")
        else:
            pass
            #print("Directory ", dirName , " already exists")

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

class PhotoVectorViewer(QtWidgets.QGraphicsView):

    editMassCenter = QtCore.pyqtSignal()
    reDrawStuff = QtCore.pyqtSignal()

    editVelocityLabel = QtCore.pyqtSignal()
    editVelDirTable = QtCore.pyqtSignal()

    def __init__(self,parent):
        super(PhotoVectorViewer,self).__init__()

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
        #self.show()

    def hasPhoto(self):
        return not self._empty
    #Ajusta la imagen al rectangulo creado
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
        #Cambia el raton de un tipo a otro y abre la imagen
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
        else:
            self._empty = True
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
            self._photo.setPixmap(QtGui.QPixmap())
        self.fitInView()

    #Func para hacer zoom con ruleta
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
        #print(self._zoom)
        self.rePaintWithZoom(self._zoom)


    def rePaintAfterDensity(self):

        self.rePaintWithZoom(self._zoom)


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

        if zoom <= zoomPararestar:
            calcGrosorAnalyzed = calcGrosor_max-zoom
        else:
            calcGrosorAnalyzed = 1

        #print('El nuevo grosor para pintar es')
        #print(calcGrosorAnalyzed)

        #if perAnalyze == False:
        self.resetView(3)
        self.resetView(2)
        self.resetView(1)
        self.resetView(0)

        self.reDrawStuff.emit()

        #elif perAnalyze == True:
        #    self.resetView(3)
        #    self.drawPerimeter()

    def generateFrames(self):

        global filesXPoints
        global filesYPoints
        global filesXPointsCenter
        global filesYPointsCenter
        global color_perimeter
        global readFilesLong
        global files
        global timElapse
        #print readFilesLong
        global renameFolderName
        global framesGenerated
        global veldir_angle
        global veldir_velocity


        c = QtGui.QColor(color_perimeter)
        penGreen = QtGui.QPen(Qt.red,3)
        penPerimetro = QtGui.QPen(c,3)

        cantidad = len(filesXPoints)
        #print(cantidad)
        #Pintamos los perimetros y luego los puntos centrales en la imagen

        valorInicialRango = 0

        #Se generan los frames para hacer el gif

        #Creamos directory o comprobamos si existe
        dirName = "framegeneratorGif"

        if not os.path.exists(dirName):
            os.mkdir(dirName)
            #print("Directory ", dirName , "Created")
        else:
            pass
            #print("Directory ", dirName , " already exists")

        for j in tqdm(range(0,len(readFilesLong))):

            nombreFichero = files[j].split('_')[0]

            fondo = renameFolderName+nombreFichero+".JPG"

            #print fondo

            self.pixmap = QPixmap(fondo)
            self.setPhoto(self.pixmap)

            for i in range(valorInicialRango,readFilesLong[j]-1):

                #print "El rango actual es de ", valorInicialRango, readFilesLong[j]-1
                valXTail = int(filesXPoints[i])
                valYTail = int(filesYPoints[i])
                valXHead = int(filesXPoints[i+1])
                valYHead = int(filesYPoints[i+1])
                #print(valXTail)
                #print(valYTail)
                #print(valXHead)
                #print(valYHead)
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

            #Hasta arriba bien

            for k in range(0,j+1):
                rad = 5.0 #1.0
                brush = QtGui.QBrush(Qt.SolidPattern)

                ellipse_item = QtWidgets.QGraphicsEllipseItem(int(filesXPointsCenter[k])-rad,int(filesYPointsCenter[k])-rad,rad*2.0,rad*2.0)
                ellipse_item.setPen(penGreen)
                ellipse_item.setBrush(brush)
                ellipse_item.setData(1,6)

                self._scene.addItem(ellipse_item)
                self.setScene(self._scene)

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

                separacion = int( self._scene.height() / 195 )

                if i == 0:
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

            #guardo cada fotograma generado del gif
            rect = QtCore.QRectF(self._photo.pixmap().rect())
            image = QtGui.QImage(rect.width(),rect.height(), QImage.Format_ARGB32_Premultiplied)
            painter = QtGui.QPainter(image)
            self._scene.render(painter)
            painter.end()

            image.save("framegeneratorGif/"+nombreFichero+"_frameGif"+".JPG")

        framesGenerated = True

    def saveAnimation(self):
        global framesGenerated


        if framesGenerated == False:
            self.generateFrames()

        #Se crea el gif y se guarda

        gifFramesDic = "framegeneratorGif/"

        imagesFrames = []

        pathArray = []

        for file_name in os.listdir(gifFramesDic):
            if file_name.endswith('.JPG'):
                file_path = os.path.join(gifFramesDic,file_name)

                #print file_path

                pathArray.append(file_path)


        pathArray = sorted(pathArray)
        #print pathArray

        for i in range(0,len(pathArray)):
            imagesFrames.append(imageio.imread(pathArray[i]))

        #Creamos directory o comprobamos si existe
        dirName = "generatedGifs"

        if not os.path.exists(dirName):
            os.mkdir(dirName)
            #print("Directory ", dirName , "Created")
        else:
            pass
            #print("Directory ", dirName , " already exists")

        for i in tqdm(range(1)):
            imageio.mimsave('generatedGifs/gifDePrueba.gif', imagesFrames, duration = 1)

    def drawVelandDir(self):
        global filesXPoints
        global filesYPoints
        global filesXPointsCenter
        global filesYPointsCenter
        global color_perimeter
        global readFilesLong

        global files
        global timElapse

        #print readFilesLong

        global renameFolderName

        #timElapse, okPressed = QInputDialog.getDouble(self, "Frame time lapse", "Timelapse(s):")

        #if okPressed:
            #print(timElapse)

        c = QtGui.QColor(color_perimeter)
        penGreen = QtGui.QPen(Qt.red,3)
        penPerimetro = QtGui.QPen(c,3)

        cantidad = len(filesXPoints)
        #print(cantidad)
        #Pintamos los perimetros y luego los puntos centrales en la imagen

        valorInicialRango = 0

        #Se dibuja todo de nuevo para tenerlo completo
        nombreFichero = files[-1].split('_')[0]

        #print "El fondo de la imagen es el siguiente"
        fondo = renameFolderName+nombreFichero+".JPG"
        #print fondo
        self.pixmap = QPixmap(fondo)
        self.setPhoto(self.pixmap)

        valorInicialRango = 0

        for j in range(0,len(readFilesLong)):



            for i in range(valorInicialRango,readFilesLong[j]-1):

                #print "El rango actual es de ", valorInicialRango, readFilesLong[j]-1
                valXTail = int(filesXPoints[i])
                valYTail = int(filesYPoints[i])
                valXHead = int(filesXPoints[i+1])
                valYHead = int(filesYPoints[i+1])
                #print(valXTail)
                #print(valYTail)
                #print(valXHead)
                #print(valYHead)
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

        self.cont = True

        timElapse, okPressed = QInputDialog.getDouble(self, "Frame time lapse", "Timelapse(s):")

        if okPressed and timElapse != 0.0:
            pass
            #print(timElapse)
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

            #print veldir_position

            #valorDiv = int( distanciaPixeles / (len(filesXPointsCenter)-1))

            #print valorDiv

            for i in range(0,len(veldir_position)):

                schoolVelocity = int(veldir_position[i] / timElapse)

                veldir_velocity.append(schoolVelocity)

            #print veldir_velocity


            for i in range(0,len(filesXPointsCenter)-1):

                valXHead = int(filesXPointsCenter[i+1])
                valXTail = int(filesXPointsCenter[i])

                valYHead = int(filesYPointsCenter[i+1])
                valYTail = int(filesYPointsCenter[i])

                vecU = int(valYHead-valYTail)
                vecV = int(valXHead-valXTail)

                veldir_vec_u.append(vecU)
                veldir_vec_v.append(vecV)


            #print veldir_vec_u
            #print veldir_vec_v


            #Calcular angulos

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


            #print veldir_angle

            #Se actualiza la tabla y se guarda en excel

            self.editVelDirTable.emit()

            #Se pintan los resultados

            self.paintSchoolResults()

    def paintSchoolResults(self):

        global veldir_angle
        global veldir_velocity
        global filesXPointsCenter
        global filesYPointsCenter



        #print self._scene.height()

        separacion = int( self._scene.height() / 195 )

        for i in range(0,len(veldir_velocity)):

            if i == 0:
                texto = QtWidgets.QGraphicsTextItem("v: "+str(veldir_velocity[i]))
            else:
                texto = QtWidgets.QGraphicsTextItem("v: "+str(veldir_velocity[i])+" , a: "+ str(veldir_angle[i-1]))
            texto.setPos(int(filesXPointsCenter[i+1]),int(filesYPointsCenter[i+1])-separacion)

            font = QFont()
            font.setBold(True)

            texto.setFont(font)
            self._scene.addItem(texto)
            self.setScene(self._scene)

    def unit_vector(self,vector):
        return vector / np.linalg.norm(vector)

    def angle_between(self,v1, v2):
        v1_u = self.unit_vector(v1)
        v2_u = self.unit_vector(v2)
        return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))


    def saveVideo(self):
        global framesGenerated


        if framesGenerated == False:
            self.generateFrames()

        image_folder = 'framegeneratorGif'
        video_name = 'generatedVideos/video.avi'

        images = [img for img in os.listdir(image_folder) if img.endswith(".JPG")]

        images = sorted(images)

        #Creamos directory o comprobamos si existe
        dirName = 'generatedVideos'

        if not os.path.exists(dirName):
            os.mkdir(dirName)
            #print("Directory ", dirName , "Created")
        else:
            pass
            #print("Directory ", dirName , " already exists")


        frame = cv2.imread(os.path.join(image_folder,images[0]))
        height,width,layers = frame.shape

        video = cv2.VideoWriter(video_name,0,1,(width,height))

        for image in images:
            video.write(cv2.imread(os.path.join(image_folder,image)))

        cv2.destroyAllWindows
        video.release()


    def calculateVelandDir(self):
        global files
        global filesXPoints
        global filesYPoints
        global filesXPointsCenter
        global filesYPointsCenter
        global color_perimeter
        global readFilesLong

        #print('Hola caracola')

        #Se meten todos los ficheros a analizar al array de ficheros
        for i in os.listdir("perimeterData"):
            if i.endswith('.txt'):
                files.append(i)
                #print("Archivo ", i , "added")
        #Se va pintando uno a uno
        #print files

        files = sorted(files)

        for i in range(0,len(files)):

            archiv = open("perimeterData/"+str(files[i]),"r")
            string = "a"
            #print("Se imprime el archivo", files[i])
            for reader in archiv:
                string = reader

                #print string
                valueX = string.split(',')[0]
                valueY = string.split(',')[1]

                #print valueX , valueY

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

        #print filesXPoints
        #print filesYPoints

        #print filesXPointsCenter
        #print filesYPointsCenter


        #dar vuelta array NO HACE FALTA POR EL MOMENTO SE QUEDA COMENTADO

        #filesXPointsCenter.reverse()
        #filesYPointsCenter.reverse()

        #print filesXPointsCenter
        #print filesYPointsCenter

        #Despues se calcula la velocidad en pixeles/segundo
        self.drawVelandDir()

    def saveImageAnalyzed(self):
        path, _ = QFileDialog.getSaveFileName(self, 'Save analyzed image', os.getcwd(), 'JPG(*.JPG)')
        rect = QtCore.QRectF(self._photo.pixmap().rect())

        if self._zoom == 0:
            #print('guardo todo')
            image = QtGui.QImage(rect.width(),rect.height(), QImage.Format_ARGB32_Premultiplied)
            painter = QtGui.QPainter(image)
            self._scene.render(painter)
            painter.end()
        else:
            #print('guardo con zoom')
            image = self.grab().toImage()
        image.save(str(path))


    def resetView(self,num):

        itemlist = self._scene.items()
        for items in itemlist:
            itemtype = type(items)
            if itemtype == QtWidgets.QGraphicsLineItem or itemtype == QtWidgets.QGraphicsEllipseItem:
                if items.data(1) == num:
                    self._scene.removeItem(items)

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

        #print('imprimiendo mediana')
        #print(sizes)
        #print(average_size)
        #print(average_angle)

    def convertQImageToMat(self,incomingImage):

        incomingImage = incomingImage.convertToFormat(4)

        width = incomingImage.width()
        height = incomingImage.height()

        ptr = incomingImage.bits()
        ptr.setsize(incomingImage.byteCount())
        arr = np.array(ptr).reshape(height,width,4)
        return arr


    def DensityProcess(self,var):

        #Para corregir el bug de que coja mal el rectangulo a analizar
        self.pixmap = QPixmap(imagePath)
        self._photo.setPixmap(self.pixmap)

        rect = QtCore.QRectF(self._photo.pixmap().rect())
        image = QtGui.QImage(rect.width(),rect.height(), QImage.Format_ARGB32_Premultiplied)
        painter = QtGui.QPainter(image)
        self._scene.render(painter)
        painter.end()
        #image = self.grab().toImage()
        imageReConverted = self.convertQImageToMat(image)

        global s_values
        global valXInsideConvexHull
        global valYInsideConvexHull
        global v_values

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

        #img_original = cv2.imread(imagePath)

        #scale_percent = 25
        #width = int(imageReConverted.shape[1] * scale_percent / 100)
        #height = int(imageReConverted.shape[0] * scale_percent / 100)
        #dim = (width, height)
        #resized_img_original = cv2.resize(imageReConverted,dim,interpolation = cv2.INTER_AREA)


        #imageReConverted = resized_img_original

        #rotated_img_original = imutils.rotate(img_original,90)



        imageFiltered = cv2.blur(imageReConverted,(5,5)) #15,15 o 10,10
        #imageFiltered = cv2.GaussianBlur(imageReConverted,(5,5),0)
        #imageFiltered = cv2.medianBlur(imageReConverted,5)

        #hsv_img_original = cv2.cvtColor(imageFiltered, cv2.COLOR_RGB2HSV)
        #h,s,v = cv2.split(hsv_img_original)

        #print('Dimensiones imagen imageReConverted')
        height,width,channels = imageReConverted.shape
        #print height, width, channels

        #print('Dimensiones imagen resized_img_original')
        #height,width = resized_img_original.shape
        #print height, width

        #print('Dimensiones imagen hsv')

        #height,width = hsv_img_original.shape
        #print height, width

        #gray_img_original = cv2.cvtColor(resized_img_original, cv2.COLOR_BGR2GRAY)
        #(minVal,maxVal,minLoc,maxLoc) = cv2.minMaxLoc(s)
        #print('min S val')
        #print(minVal)
        #print('max S val')
        #print(maxVal)
        #print('Location min,max')
        #print(minLoc)
        #print(maxLoc)


        if var == 0:

            hull = ConvexHull(midPointList)
            long = len(hull.vertices)

            for i in range(0,long):

                valXTail = int(valuesXMed[hull.vertices[i]])
                valYTail = int(valuesYMed[hull.vertices[i]])

                convexXHull.append(valXTail)
                convexYHull.append(valYTail)

                point = [valXTail,valYTail]
                convexPointList.append(point)

            #print('Valores puntos array convex')
            #print(convexPointList)

            #print('Valores vertices convex hull X e Y')
            #print(convexXHull)
            #print(convexYHull)

            #print('Valores max min X convex hull')
            minconvexValX = min(convexXHull)
            maxconvexValX = max(convexXHull)
            #print(minconvexValX)
            #print(maxconvexValX)

            #print('Valores max min Y convex hull')
            minconvexValY = min(convexYHull)
            maxconvexValY = max(convexYHull)
            #print(minconvexValY)
            #print(maxconvexValY)

            #print('Numero de vertices en el Convex Hull')
            #print(long)

            listadoDePuntos = convexPointList

            #print(convexPointList)
        elif var == 1:
            #print(perimeterPointList)

            listadoDePuntos = perimeterPointList

        #Una vez obtenidos puntos ConvexHull, buscamos obtener las ROI

        mask = np.zeros(imageFiltered.shape, dtype=np.uint8)

        roi_corners = np.array(listadoDePuntos)

        channel_count = imageFiltered.shape[2]

        ignore_mask_color = (255,)*channel_count

        cv2.fillConvexPoly(mask,roi_corners,ignore_mask_color)

        masked_image = cv2.bitwise_and(imageFiltered,mask)

        hsv_img_original = cv2.cvtColor(masked_image, cv2.COLOR_RGB2HSV)
        h,s,v = cv2.split(hsv_img_original)


        self.pruebaHexValuesArray()

        posOfArrays = np.where(v > 0) #index en X,Y de los puntos mayores a 0

        v_val_max = np.amax(v)
        v_val_min = np.amin(v[np.where(v>0)]) #no de toda la imagen sino de nuestra zona

        #print(posOfArrays[0])

        #print(posOfArrays[1])

        #print(posOfArrays[0][0])

        #Pintar directamente segun el valor de la S que se lea de las posiciones cuyo valor de S es mayor que cero

        for i in tqdm(range(0,len(posOfArrays[0]))):
            valordeV = v[posOfArrays[0][i],posOfArrays[1][i]]
            posArray = self.mapeador(valordeV,v_val_min,v_val_max,0,number_of_layers-1)
            colour = str(heatMapColorValues[posArray])
            #print colour
            #Descompongo color en rgb

            parte_R = colour.split(',')[0]

            #parte_R = colour[1:3]
            #print(parte_R)
            cant_R = int(parte_R)
            #print(cant_R)

            parte_G = colour.split(',')[1]
            #print(parte_G)
            cant_G = int(parte_G)
            #print(cant_G)

            parte_B = colour.split(',')[2]
            #print(parte_B)
            cant_B = int(parte_B)
            #print(cant_B)

            #imageReConverted[500,500] = (50,50,50,50)
            imageReConverted[posOfArrays[0][i],posOfArrays[1][i]] = (cant_B,cant_G,cant_R,1)
            #cv2.circle(imageReConverted,(posOfArrays[1][i],posOfArrays[0][i]),1,(cant_B,cant_G,cant_R),-1)

        cv2.imwrite('cache_heatmap.JPG',imageReConverted)

        self.pixmap = QPixmap("cache_heatmap.JPG")
        self.setPhoto(self.pixmap)

        densityCalculated = True


        #cv2.namedWindow('original', cv2.WINDOW_NORMAL)
        #cv2.resizeWindow('original',600,600)
        #cv2.moveWindow('original',200,100)
        #cv2.imshow('original',imageReConverted)

        #cv2.namedWindow('filtered', cv2.WINDOW_NORMAL)
        #cv2.resizeWindow('filtered',600,600)
        #cv2.moveWindow('filtered',200,100)
        #cv2.imshow('filtered',imageFiltered)


        #cv2.namedWindow('masked_image', cv2.WINDOW_NORMAL)
        #cv2.resizeWindow('masked_image',600,600)
        #cv2.moveWindow('masked_image',200,100)
        #cv2.imshow('masked_image',masked_image)

        #cv2.namedWindow('v', cv2.WINDOW_NORMAL)
        #cv2.resizeWindow('v',600,600)
        #cv2.moveWindow('v',200,100)
        #cv2.imshow('v',v)



    def mapeador(self, x,in_min,in_max,out_min,out_max):

        return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

    def pruebaHexValuesArray(self):
        global heatMapColorValues
        global number_of_layers
        global color_layers
        global maxRangeValue


        parte_R = color_layers[1:3]
        #print(parte_R)
        cant_R = int(parte_R,16)
        #print(cant_R)

        parte_G = color_layers[3:5]
        #print(parte_G)
        cant_G = int(parte_G,16)
        #print(cant_G)

        parte_B = color_layers[5:7]
        #print(parte_B)
        cant_B = int(parte_B,16)
        #print(cant_B)

        maximum = self.maximumOfRGB(cant_R,cant_G,cant_B)

        for i in range(0,number_of_layers):

            escalar = int(maxRangeValue/number_of_layers)*i

            #value = hex(escalar*i)[2:]

            if maximum == cant_R:
                value_string = str(cant_R)+","+str(escalar)+","+str(escalar)
            elif maximum == cant_G:
                value_string = str(escalar)+","+str(cant_G)+","+str(escalar)
            elif maximum == cant_B:
                value_string = str(escalar)+","+str(escalar)+","+str(cant_B)

            #print i , str(escalar), value_string
            heatMapColorValues.append(value_string)


        #Se invierte el array de capas de  color (al final no)
        #heatMapColorValues.reverse()

        #print heatMapColorValues
        #coger los cachos dinamicamente


    def maximumOfRGB(self,r,g,b):
        list = [r,g,b]
        return max(list)

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


        if var == 0:
            valCenterMassX = statistics.mean(valuesXMed)
            valCenterMassY = statistics.mean(valuesYMed)
        elif var == 1:
            valCenterMassX = statistics.mean(valuesXPerimeter)
            valCenterMassY = statistics.mean(valuesYPerimeter)

        #print('Mid Point List')
        #print(midPointList)

        #print('Mass Center X')
        #print(int(valCenterMassX))
        #print('Mass Center Y')
        #print(int(valCenterMassY))

        self.editMassCenter.emit()

        # Dibujar punto medio
        rad = 3.0+calcGrosorAnalyzed #1.0
        brush = QtGui.QBrush(Qt.SolidPattern)

        c = QtGui.QColor(color_perimeter)

        penGreen = QtGui.QPen(c,calcGrosorAnalyzed)

        if pintar == 1:
            ellipse_item = QtWidgets.QGraphicsEllipseItem(valCenterMassX-rad,valCenterMassY-rad,rad*2.0,rad*2.0)
            ellipse_item.setPen(penGreen)
            ellipse_item.setBrush(brush)
            ellipse_item.setData(1,2)

            self._scene.addItem(ellipse_item)
            self.setScene(self._scene)

        if var == 0: #Caso normal de etiquetado

            hull = ConvexHull(midPointList)

            #print(hull.vertices)

            #print('cantidad de tiburones')

            #print(tiburonesTotales)

            #print("List values XTail: ", valuesXTail[0:tiburonesTotales])
            #print("List values YTail: ", valuesYTail[0:tiburonesTotales])
            #print("List values XHead: ", valuesXHead[0:tiburonesTotales])
            #print("List values YHead: ", valuesYHead[0:tiburonesTotales])

            #print("List values XMed: ", valuesXMed[0:tiburonesTotales])
            #print("List values YMed: ", valuesYMed[0:tiburonesTotales])
            #print("List hull Vertices", hull.vertices)

            #print(hull.points[0,1])

            #print(len(hull.points))

            long = len(hull.vertices)

            #print('Cantidad vertices en el convex hull')
            #print long

            for i in range(0,long-1):

                #print('Llego hasta: ', i)
                valXTail = int(valuesXMed[hull.vertices[i]])
                valYTail = int(valuesYMed[hull.vertices[i]])
                valXHead = int(valuesXMed[hull.vertices[i+1]])
                valYHead = int(valuesYMed[hull.vertices[i+1]])

                convexXHull.append(valXTail)
                convexYHull.append(valYTail)

                #print(valXTail)
                #print(valYTail)
                #print(valXHead)
                #print(valYHead)

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

            #print(convexXHull)
            #print(convexYHull)

            #print('Cantidad vertices Convex Hull')
            #print(long)

            #print(imagePath)
            nameofFile = imagePath.split('/')[-1]
            nameofFileFiltered = nameofFile.split('.')[0]
            #print(nameofFileFiltered)


            if perimeterSaved == False:
                #Creamos directory o comprobamos si existe
                dirName = 'perimeterData'

                if not os.path.exists(dirName):
                    os.mkdir(dirName)
                    #print("Directory ", dirName , "Created")
                else:
                    #print("Directory ", dirName , " already exists")

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
                        #print(valXTail)
                        #print(valYTail)
                        #print(valXHead)
                        #print(valYHead)
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

            #print(imagePath)
            nameofFile = imagePath.split('/')[-1]
            nameofFileFiltered = nameofFile.split('.')[0]
            #print(nameofFileFiltered)


            if perimeterSaved == False:
                #Creamos directory o comprobamos si existe
                dirName = 'perimeterData'

                if not os.path.exists(dirName):
                    os.mkdir(dirName)
                    #print("Directory ", dirName , "Created")
                else:
                    pass
                    #print("Directory ", dirName , " already exists")

                file = open("perimeterData/"+nameofFileFiltered+"_perimeter"+".txt","w")

                for i in range(0,len(valuesXPerimeter)):
                    file.write(str(int(valuesXPerimeter[i]))+","+str(int(valuesYPerimeter[i]))+"\n")
                file.write(str(int(valCenterMassX))+","+str(int(valCenterMassY))+"\n")
                file.close()

            if perimeterSaved == False:
                self.msg = QtWidgets.QMessageBox.about(self,'Save perimeter data','Perimeter data has been saved sucessfully')
                perimeterSaved = True



    def cross(self,o, a, b):

        return (a[0] - o[0]) * (b[1] - o[1]) -\
               (a[1] - o[1]) * (b[0] - o[0])



    def drawLoadedData(self,num):
        #print(tiburonesTotales)

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


        #self.resetView()

        self.calcMedian()

        #Imprimir toda la chicha

        #print("List values XTail: ", valuesXTail[0:tiburonesTotales])
        #print("List values YTail: ", valuesYTail[0:tiburonesTotales])
        #print("List values XHead: ", valuesXHead[0:tiburonesTotales])
        #print("List values YHead: ", valuesYHead[0:tiburonesTotales])
        #print("List values XMed: ", valuesXMed[0:tiburonesTotales])
        #print("List values YMed: ", valuesYMed[0:tiburonesTotales])
        #print("List values vec_u: ", vec_u[0:tiburonesTotales])
        #print("List values vec_v: ", vec_v[0:tiburonesTotales])
        #print("List values neighList: ", neighList[0:tiburonesTotales])
        #print("List values angleList: ", angleList[0:tiburonesTotales])

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
            #print('ValoresXT:',valXTail)
            #print('ValoresYT:',valYTail)
            #print('ValoresXH:',valXHead)
            #print('ValoresYH:',valYHead)

            valXMed = float(valuesXMed[i])
            valYMed = float(valuesYMed[i])
            valU = float(vec_u[i])
            valV = float(vec_v[i])

            valDist = float(neighList[i])
            valAngle = float(angleList[i])

            #print('valoresXMed:',valXMed)
            #print('ValoresYMed:',valYMed)




            # Dibujar punto medio
            rad = 1.0+calcGrosorAnalyzed #1.0
            brush = QtGui.QBrush(Qt.SolidPattern)

            #print(calcGrosorAnalyzed)

            #comprobar si la i del angulo de los sizes es mayor o menor a lo que sea etc

            if valDist <= 2*average_size:
                genericPen = penRed

            elif valDist > 2*average_size:
                genericPen = penBlue

            if num == 0:
                ellipse_item = QtWidgets.QGraphicsEllipseItem(valXMed-rad,valYMed-rad,rad*2.0,rad*2.0)
                ellipse_item.setPen(genericPen)
                ellipse_item.setBrush(brush)
                ellipse_item.setData(1,0)
                #self._scene.addItem(ellipse_item)

                #print('dibujo circulito')
                #print(i)
                #self._scene.addItem(self._scene.addEllipse(valXMed-rad,valYMed-rad,rad*2.0,rad*2.0,genericPen,brush))

            # Dibujar vectors
            vector_uv = QtCore.QLineF(0,0,valV,valU)
            vector_uv.translate(valXMed,valYMed)
            #vector_uv.setLength(30)

            linea_item_vector = QtWidgets.QGraphicsLineItem(vector_uv)
            linea_item_vector.setData(1,1)

            if valAngle <= average_angle:
                genericPen = penVector1
            elif valAngle >= average_angle:
                genericPen = penVector2
            linea_item_vector.setPen(genericPen)

            if num == 0:
                linea_item = QtWidgets.QGraphicsLineItem(valXTail,valYTail,valXHead,valYHead)
                linea_item.setData(0,i)
                linea_item.setPen(penGreen)

                linea_item.setData(1,0)
            #poner vector_uv.y1() y vector_uv.y2() v y u
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

            #linea_item.setFlags(QtWidgets.QGraphicsLineItem.ItemIsSelectable | QtWidgets.QGraphicsLineItem.ItemIsMovable)
            if num == 0:
                self._scene.addItem(linea_item)
                self._scene.addItem(ellipse_item)
            if num == 1:
                self._scene.addItem(linea_item_vector)
                self._scene.addItem(linea_item_flecha_1)
                self._scene.addItem(linea_item_flecha_2)

            self.setScene(self._scene)
            #print('Pez' + str(i) + 'impreso')


class PhotoDataViewer(QtWidgets.QGraphicsView):
    photoClicked = QtCore.pyqtSignal(QtCore.QPointF)
    labelUpdater = QtCore.pyqtSignal(int,int,QtCore.QPointF)
    tableUpdater = QtCore.pyqtSignal(int)
    ResetInfoSig = QtCore.pyqtSignal()
    DragModeConnecter = QtCore.pyqtSignal(bool,int)

    labelChecker = QtCore.pyqtSignal(int)

    tableRowCounter = QtCore.pyqtSignal()

    def __init__(self, parent):
        super(PhotoDataViewer, self).__init__(parent)

        #Variables para controlar si hay imagen, el zoom, archivos en la escena, fotos, y add fotos a la escena
        #Asi como modificar la escena para eliminar anchos y demas
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

    #Se comprueba simplemente si la variable empty esta en false o true
    def hasPhoto(self):
        return not self._empty
    #Ajusta la imagen al rectangulo creado
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

    #Cambia el raton de un tipo a otro y abre la imagen
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
        else:
            self._empty = True
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
            self._photo.setPixmap(QtGui.QPixmap())
        self.fitInView()

    #Func para hacer zoom con ruleta
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

        #print(self._zoom)

        #if self.sharkCount > 0 or self.perimeterPointCounter > 0:
        self.rePaintWithZoom(self._zoom)

    def rePaintWithZoom(self,zoom):

        global filasActuales
        global empty_row

        self.errorAtZoom = False

        self.tableRowCounter.emit()

        longitud_comprobacion = filasActuales

        #print longitud_comprobacion

        if self.sharkCount == 0 and empty_row == True:
            pass
        elif self.sharkCount < longitud_comprobacion:
            #print "El ultimo dato es incorrecto"
            self.errorAtZoom = True
        elif self.sharkCount == longitud_comprobacion:
            #print "El ultimo dato es correcto"
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


            #print self._scene.width(), self._scene.height()

            x = self._scene.width()
            y = self._scene.height()

            zoomPararestar = 10
            calcGrosor_max = 11

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

            if zoom <= zoomPararestar:
                calcGrosor = calcGrosor_max-zoom
            else:
                calcGrosor = 1

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

            #print('Cantidad tiburones globales')
            #print(tiburonesTotales)
            #print('Cantidad tiburones locales')
            #print(self.sharkCount)


            #print('Tiburones almacenados al mover rueda raton')
            #print("List values XTail: ", valuesXTail[0:self.sharkCount])
            #print("List values YTail: ", valuesYTail[0:self.sharkCount])
            #print("List values XHead: ", valuesXHead[0:self.sharkCount])
            #print("List values YHead: ", valuesYHead[0:self.sharkCount])

            longiShark = len(valuesXTail)
            #print('Cantidad de tiburones arrays')
            #print(longiShark)

            if longiShark >= 1:
                for i in range(0,longiShark):
                    #print('pinto el tiburon ',i)

                    valXTail = float(valuesXTail[i])
                    valYTail = float(valuesYTail[i])
                    valXHead = float(valuesXHead[i])
                    valYHead = float(valuesYHead[i])
                    #print('ValoresXT:',valXTail)
                    #print('ValoresYT:',valYTail)
                    #print('ValoresXH:',valXHead)
                    #print('ValoresYH:',valYHead)

                    lineaper = QtWidgets.QGraphicsLineItem(valXTail,valYTail,valXHead,valYHead)
                    lineaper.setPen(penBlack)
                    lineaper.setData(0,i)
                    self._scene.addItem(lineaper)
                    self.setScene(self._scene)

        else:

            self.msg = QtWidgets.QMessageBox.about(self,'Error zooming','Finish selection before zooming')



    def resetParcial(self):

        itemlist = self._scene.items()
        for items in itemlist:
            itemtype = type(items)
            if itemtype == QtWidgets.QGraphicsLineItem or itemtype == QtWidgets.QGraphicsEllipseItem:
                self._scene.removeItem(items)


    #Func para activar la recogida de datos
    def toggleDragMode(self):
        self.startSelecting = True
        self.labelUpdater.emit(self.selectorActual,self.sharkCount,QtCore.QPoint())
        self.rePaintWithZoom(self._zoom)
        global cargarDatos
        global tiburonesTotales
        if cargarDatos == True:
            self.sharkCount = tiburonesTotales
            #cargarDatos = False
            #print('Cantidad tiburones locales-globales')
            #print(self.sharkCount)

        if self.dragMode() == QtWidgets.QGraphicsView.ScrollHandDrag:
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        elif not self._photo.pixmap().isNull():
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
    #Funcion para obtener datos cuando hacemos click con el raton
    def mousePressEvent(self, event):
        global color_labelled_data
        global color_perimeter
        global color_vector1
        global color_vector2
        global color_dot1
        global color_dot2
        global color_labelled_analyzed_data
        if self._photo.isUnderMouse():
            if event.button() == QtCore.Qt.LeftButton:
                #print('contador tiburones interno')
                #print(self.sharkCount)
                if self.handDrag == False and self.startSelecting == True and deleteIt == False and perimeterClick == False:
                    self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
                    self.photoClicked.emit(QtCore.QPointF(self.mapToScene(event.pos())))
                    if self.selectorActual == 1:

                        self.selectorActual += 1
                        self.labelUpdater.emit(self.selectorActual,self.sharkCount,QtCore.QPointF(self.mapToScene(event.pos())))
                        e = QtCore.QPointF(self.mapToScene(event.pos()))

                        self.startX = e.x()
                        self.startY = e.y()

                        self.clicked = True

                    elif self.selectorActual == 2 and doubleClick == True and perimeterClick == False:
                        e = QtCore.QPointF(self.mapToScene(event.pos()))
                        #print(color_labelled_data)
                        c = QtGui.QColor(color_labelled_data)
                        pen = QtGui.QPen(c,calcGrosor)
                        #self._scene.addItem(self._scene.addLine(self.startX,self.startY,e.x(),e.y(),pen))

                        linea_item = QtWidgets.QGraphicsLineItem(self.startX,self.startY,e.x(),e.y())
                        linea_item.setData(0,self.sharkCount)
                        linea_item.setPen(pen)
                        self._scene.addItem(linea_item)
                        self.setScene(self._scene)

                        self.selectorActual = 1
                        self.labelUpdater.emit(self.selectorActual,self.sharkCount,QtCore.QPointF(self.mapToScene(event.pos())))
                        self.sharkCount += 1

                        #Activar funcion de analisis
                        self.labelChecker.emit(1)


                #Seleccionar perimetros
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
                    #e = QtCore.QPointF(self.mapToScene(event.pos()))
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
                    #print(point)
                    perimeterPointList.append(point)
                    #print(perimeterPointList)
                    self.perimeterPointCounter += 1

                    #Activar funcion analisis perimetro
                    self.labelChecker.emit(2)

                    #print('Dibujo un punto de perimetro')
                    self.startX = e.x()
                    self.startY = e.y()
                #Para borrar tiburones
                if self.handDrag == False and self.startSelecting == True and deleteIt == True and perimeterClick == False:
                    #itemlist = self._scene.items()
                    item = self.itemAt(event.pos())
                    index = item.data(0)
                    #print(item.data(0))
                    #print(itemlist)
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
            #Para cambiar al modo drag a no drag
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

    def updateSharkIndex(self,numero):
        itemlist = self._scene.items()

        for item in itemlist:
            itemtype = type(item)
            if itemtype == QtWidgets.QGraphicsLineItem:
                dataActual = item.data(0)
                if dataActual > numero:
                    item.setData(0,dataActual-1)

    def updatePointIndex(self,numero):
        itemlist = self._scene.items()

        for item in itemlist:
            itemtype = type(item)
            if itemtype == QtWidgets.QGraphicsEllipseItem:
                dataActual = item.data(2)
                if dataActual > numero:
                    item.setData(2,dataActual-1)


    def resetEmit(self):
        #print('recibo')
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

    def mouseReleaseEvent(self, event):
        global color_labelled_data
        global calcGrosor
        if self._photo.isUnderMouse():
            if event.button() == QtCore.Qt.LeftButton:
                if self.handDrag == False and self.startSelecting == True and doubleClick == False and deleteIt == False and perimeterClick == False:
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
                    self.labelChecker.emit(1)

                    self.clicked = False
        super(PhotoDataViewer, self).mouseReleaseEvent(event)

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


    def drawLoadedData(self):
        global calcGrosor
        #Al cargar datos se reinician las variables de interes
        self.startSelecting = True
        pixmap = QPixmap(imagePath)
        self.setPhoto(pixmap)

        #print(tiburonesTotales)

        for i in range(0,tiburonesTotales):
            valXTail = float(valuesXTail[i])
            valYTail = float(valuesYTail[i])
            valXHead = float(valuesXHead[i])
            valYHead = float(valuesYHead[i])
            c = QtGui.QColor(color_labelled_data)
            pen = QtGui.QPen(c,calcGrosor)
            #print('ValoresXT:',valXTail)
            #print('ValoresYT:',valYTail)
            #print('ValoresXH:',valXHead)
            #print('ValoresYH:',valYHead)

            linea_item = QtWidgets.QGraphicsLineItem(valXTail,valYTail,valXHead,valYHead)
            linea_item.setData(0,i)
            linea_item.setPen(pen)
            self._scene.addItem(linea_item)
            self.setScene(self._scene)
            #print('Pez' + str(i) + 'impreso')

        self.toggleDragMode()

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



class DataTable(QtWidgets.QTableWidget):

    sharkUpdater = QtCore.pyqtSignal()
    loadLinesData = QtCore.pyqtSignal()

    labelChecker = QtCore.pyqtSignal(int)

    def __init__(self, r, c):
        super(DataTable,self).__init__(r, c)
        col_headers = ['Tail X', 'Tail Y', 'Head X', 'Head Y']
        self.setHorizontalHeaderLabels(col_headers)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.show()

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



    def save_sheet(self,var):
        #path = QFileDialog.getSaveFileName(self, 'Save data in CSV file', os.getcwd(), 'CSV(*.csv)')

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

        #Creamos directory o comprobamos si existe
        dirName = cacheDir

        if not os.path.exists(dirName):
            os.mkdir(dirName)
            #print("Directory ", dirName , "Created")
        else:
            pass
            #print("Directory ", dirName , " already exists")

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
        if var == 0:
            self.msg = QtWidgets.QMessageBox.about(self,cacheTitle,cacheInfo)

    def open_sheet(self):
        path = QFileDialog.getOpenFileName(self, 'Open CSV', os.getcwd(), 'CSV(*.csv)')
        if path[0] != '':
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



        if path[0] != '':

            numColumnas = self.columnCount()
            if numColumnas > 4:
                #print('error al cargar datos')
                self.msg = QtWidgets.QMessageBox.about(self,'Error loading',"Please load non analyzed data")


            global cargarDatos
            cargarDatos = True
            self.sharkUpdater.emit()
            self.loadLinesData.emit()


class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()

        self.dialog = WindowResults()
        self.viewer = PhotoDataViewer(self)
        self.data = DataTable(1,4)
        # Button to change from drag/pan to getting pixel info

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

        self.primeraLlamada = False

        self.viewer.labelUpdater.connect(self.labelUpdater)
        self.data.sharkUpdater.connect(self.sharkUpdater)
        self.data.loadLinesData.connect(self.loadLinesData)
        self.viewer.tableUpdater.connect(self.tableUpdater)
        self.viewer.DragModeConnecter.connect(self.DragModeConnecter)

        self.viewer.ResetInfoSig.connect(self.ResetInfo)

        self.dialog.viewerRes.editVelDirTable.connect(self.editVelDirTable)

        self.viewer.tableRowCounter.connect(self.data.counter)





        # Arrange layout
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

        # New layout
        grid = QtWidgets.QGridLayout(self)
        grid.addLayout(HBlayout1,0,0,50,2)
        grid.addLayout(HBlayout2,51,1)

    def editVelDirTable(self):
        #print("Modifying table")

        global veldir_position
        global veldir_angle
        global veldir_vec_u
        global veldir_vec_v
        global veldir_velocity
        global filesXPointsCenter
        global filesYPointsCenter


        #print veldir_position
        #print veldir_velocity
        #print veldir_vec_u
        #print veldir_vec_v
        #print veldir_angle
        #print filesXPointsCenter
        #print filesYPointsCenter


        for i in range(0,len(veldir_vec_u)):
            self.dialog_2.insertRow(i+1)

        #Para combinar celdas
        #self.dialog_2.setSpan(0,4,2,1)

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

        #Se guarda la tabla en un excel
        self.dialog_2.save_sheet(2)




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



    def restablecerDatos(self):

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

        self.data.clear()
        col_headers = ['Tail X', 'Tail Y', 'Head X', 'Head Y']
        self.data.setHorizontalHeaderLabels(col_headers)
        self.data.setRowCount(1)
        self.data.setColumnCount(4)
        self.startSelecting = True
        self.primeraLlamada = False
        #self.viewer.toggleDragMode()
        if doubleClick == True:
            self.label_status.setText('Point and click. Status: Select Tail')
        elif doubleClick == False:
            self.label_status.setText('Drag and release. Status: Select Tail')

        #print('recargando datos de nuevo')
        #print(self.viewer.sharkCount)
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




    #Boton que abre la imagen seleccionada
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
        #print(imagePath)
        nameofFile = imagePath.split('/')[-1]
        nameofFileFiltered = nameofFile.split('.')[0]
        #print(nameofFileFiltered)

        # Al abrir una imagen se reinician todas las variables de interes
        self.data.clear()
        col_headers = ['Tail X', 'Tail Y', 'Head X', 'Head Y']
        self.data.setHorizontalHeaderLabels(col_headers)
        self.data.setRowCount(1)
        self.primeraLlamada = False


        self.viewer.resetEmit()


        self.viewer.toggleDragMode()



    def ResetInfo(self):

        global doubleClick
        global perimeterClick
        #self.label_status.setText('Status...')
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
        self.primeraLlamada = True #esto estaba en False
        global cargarDatos
        cargarDatos = False
        self.viewer.resetEmit()

    #Al hacer click se escribe la pos del cursor
    def photoClicked(self, pos):
        if self.viewer.dragMode()  == QtWidgets.QGraphicsView.NoDrag:
            self.editPixInfo.setText('%d, %d' % (pos.x(), pos.y()))

    def labelUpdater(self, num, tibur, pos):

        global valuesXHead
        global valuesYHead
        global valuesXTail
        global valuesYTail

        if num == 1:

            if doubleClick == True:
                self.label_status.setText('Point and click. Status: Select Tail')
            elif doubleClick == False:
                self.label_status.setText('Drag and release. Status: Select Tail')

            #print(self.primeraLlamada)

            if self.primeraLlamada == True:
                self.data.setItem(tibur,2, QtWidgets.QTableWidgetItem(str(int(pos.x()))))
                valuesXHead.append(self.data.item(tibur,2).text())
                self.data.setItem(tibur,3, QtWidgets.QTableWidgetItem(str(int(pos.y()))))
                valuesYHead.append(self.data.item(tibur,3).text())
            self.primeraLlamada = True

        elif num == 2:
            if doubleClick == True:
                self.label_status.setText('Point and click. Status: Select Head')
            elif doubleClick == False:
                self.label_status.setText('Drag and release. Status: Select Head')
            #print(tibur)
            if tibur >= 1:
                #print('llego hasta aqui')
                self.data.insertRow(tibur)

            self.data.setItem(tibur,0, QtWidgets.QTableWidgetItem(str(int(pos.x()))))
            valuesXTail.append(self.data.item(tibur,0).text())
            self.data.setItem(tibur,1, QtWidgets.QTableWidgetItem(str(int(pos.y()))))
            valuesYTail.append(self.data.item(tibur,1).text())

        #print('Cantidad tiburones locales')
        #print(self.viewer.sharkCount)
        #print("List values XTail: ", valuesXTail[0:self.viewer.sharkCount])
        #print("List values YTail: ", valuesYTail[0:self.viewer.sharkCount])
        #print("List values XHead: ", valuesXHead[0:self.viewer.sharkCount])
        #print("List values YHead: ", valuesYHead[0:self.viewer.sharkCount])


    def tableUpdater(self,num):
        self.data.removeRow(num)

        if self.data.rowCount() == 0:
            self.data.insertRow(0)

    def saveData(self,var):
        self.data.save_sheet(var)

    def loadData(self):
        if imag_loaded == False:
            #Se reinician los labels de status al cargar datos

            global valuesXTail
            del valuesXTail[:]
            global valuesYTail
            del valuesYTail[:]
            global valuesXHead
            del valuesXHead[:]
            global valuesYHead
            del valuesYHead[:]

            self.primeraLlamada = False
            self.label_status.setText('Status...')
            self.editPixInfo.setText(' ')
            self.viewer.resetEmit()
            self.data.open_sheet()

            #global valuesXTail
            #del valuesXTail[:]
            #global valuesYTail
            #del valuesYTail[:]
            #global valuesXHead
            #del valuesXHead[:]
            #global valuesYHead
            #del valuesYHead[:]

        else:
            self.showDialog()

    def showDialog(self):
        self.msg = QtWidgets.QMessageBox.about(self,'Information',"Please load an image before loading data")

    def sharkUpdater(self):
        global tiburonesTotales
        tiburonesTotales = self.data.rowCount()

    def loadLinesData(self):
        #print('hola')
        global valuesXTail
        global valuesYTail
        global valuesXHead
        global valuesYHead
        global tiburonesTotales

        #print('Cargo datos y compruebo total tiburones')
        #print(tiburonesTotales)

        for i in range(0,tiburonesTotales):
            valuesXTail.append(self.data.item(i,0).text())
            valuesYTail.append(self.data.item(i,1).text())

            valuesXHead.append(self.data.item(i,2).text())
            valuesYHead.append(self.data.item(i,3).text())

        #print("List values XTail: ", valuesXTail[0:tiburonesTotales])
        #print("List values YTail: ", valuesYTail[0:tiburonesTotales])
        #print("List values XHead: ", valuesXHead[0:tiburonesTotales])
        #print("List values YHead: ", valuesYHead[0:tiburonesTotales])

        self.viewer.drawLoadedData()

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

            self.label_status.setText('Point and click. Status: Select Tail')

            self.viewer.startX = None
            self.viewer.startY = None

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

            self.viewer.clicked = False

            self.label_status.setText('Drag and release. Status: Select Tail')

            self.viewer.startX = None
            self.viewer.startY = None

    def ClickPerimeter(self):

        wantToChangeToPerimeter = True

        cambio = self.viewer.deleteDataOnSwitchMode(wantToChangeToPerimeter)

        if cambio == 1:
            global perimeterClick
            perimeterClick = True
            global deleteIt
            deleteIt = False

            self.label_status.setText('Select perimeter points. Status: Select points to obtain perimeter')

            self.viewer.startX = None
            self.viewer.startY = None




    def DeleteItem(self):
        global deleteIt
        deleteIt = True
        global perimeterClick
        perimeterClick = False

        self.label_status.setText('Delete single item. Status: Select an item to delete it')

        self.viewer.startX = None
        self.viewer.startY = None


    def VelDirAnalyze(self):
        #print('analisis vel/dir')

        self.dialog.viewerRes.setPhoto(self.pixmap)

        self.dialog.cb_labelled.setEnabled(False)
        self.dialog.cb_analyzed.setEnabled(False)
        self.dialog.cb_perimeter.setEnabled(False)
        self.dialog.cb_density.setEnabled(False)

        self.dialog.savegifbtn.setVisible(True)
        self.dialog.savevideobtn.setVisible(True)

        self.dialog.show()
        self.dialog_2 = DataResults(1,5)

        col_headers = ['Vector U', 'Vector V', 'Distance', 'Velocity', 'Angle']
        self.dialog_2.setHorizontalHeaderLabels(col_headers)
        self.dialog.viewerRes.calculateVelandDir()



    def PerimeterAnalyze(self):
        global perAnalyze

        #print('analisis perimetro de escuela')

        self.dialog.viewerRes.setPhoto(self.pixmap)

        self.dialog.cb_labelled.setEnabled(False)
        self.dialog.cb_analyzed.setEnabled(False)
        self.dialog.cb_perimeter.setEnabled(True)
        self.dialog.cb_density.setEnabled(True)

        #print perAnalyze

        self.dialog.show()

        if perAnalyze == True:
            self.dialog.viewerRes.ImageProcess(1,0)
        else:
            self.dialog.viewerRes.ImageProcess(0,0)


        self.dialog_2 = DataResults(1,1)

        #self.dialog.viewerRes.drawPerimeter()


    def DataAnalyze(self):
        #print('analisis')

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

        #if cargarDatos == True:
        #    self.viewer.sharkCount = tiburonesTotales

        tiburonesTotales = self.viewer.sharkCount

        #print('contador tiburones viewer')
        #print(self.viewer.sharkCount)
        #print('contador tiburones totales')
        #print(tiburonesTotales)


        #Se comprueba que esten todos los datos correctamente (ultimo pez marcado bien)

        longitud_comprobacion = self.data.rowCount()

        #print longitud_comprobacion



        if self.viewer.sharkCount < longitud_comprobacion:
            #print "El ultimo dato es incorrecto"
            errorAnalyzing = True
        elif self.viewer.sharkCount == longitud_comprobacion:
            #print "El ultimo dato es correcto"
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




    def copyDataInNewTable(self):
        for i in range(self.viewer.sharkCount):
            for j in range(11):
                valToCopy_item = self.data.item(i,j)
                valToCopy_val = valToCopy_item.text()
                self.dialog_2.setItem(i,j,QtWidgets.QTableWidgetItem(str(valToCopy_val)))
        self.dialog_2.show()


    def AngleVectors(self):
        global vec_u
        global vec_v


        #print('Vec u list')
        #print vec_u
        #print('Vec v list')
        #print vec_v
        #print('Index List')
        #print indexList

        for i in range(self.viewer.sharkCount):
            valU = vec_u[i]
            valV = vec_v[i]

            vector_1 = (valU,valV)

            #indexVec = self.data.item(i,8)
            indexVec = indexList[i]

            #indexVec_val = int(indexVec.text())
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

    def unit_vector(self,vector):
        return vector / np.linalg.norm(vector)

    def angle_between(self,v1, v2):
        v1_u = self.unit_vector(v1)
        v2_u = self.unit_vector(v2)
        return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

    def ClosestPoint(self):

        for posicion in range(self.viewer.sharkCount):
            valX = valuesXMed[posicion]
            valY = valuesYMed[posicion]
            point = [valX,valY]
            #print(point)
            midPointList.append(point)

        X = np.array(midPointList)

        #print(X[0])
        #print('Se imprime listado de puntos centricos')
        #print(X)
        tree = KDTree(X,leaf_size=2)
        dist,ind = tree.query(X[:self.viewer.sharkCount],k=2)

        #print('Se imprime el listado de indices')
        #print(ind)
        #print('Se imprime el listado de distancias')
        #print(dist)

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


        #print(indexList)
        #print(neighList)

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
        #print("List values Vec_u: ", vec_u[0:self.viewer.sharkCount])
        #print("List values Vec_v: ", vec_v[0:self.viewer.sharkCount])

    def MidPointCalc(self):
        global valuesXMed
        global valuesYMed


    #    #print(self.data.rowCount())
    #    print(tiburonesTotales)
        #print("List values XTail: ", valuesXTail[0:self.viewer.sharkCount])
        #print("List values YTail: ", valuesYTail[0:self.viewer.sharkCount])
        #print("List values XHead: ", valuesXHead[0:self.viewer.sharkCount])
        #print("List values YHead: ", valuesYHead[0:self.viewer.sharkCount])

        for i in range(self.data.rowCount()):
            number = float((float(valuesXHead[i])+float(valuesXTail[i]))/2)
            valuesXMed.append(number)
            self.data.setItem(i,4, QtWidgets.QTableWidgetItem(str(int(valuesXMed[i]))))

            number = float((float(valuesYHead[i])+float(valuesYTail[i]))/2)
            valuesYMed.append(number)
            self.data.setItem(i,5, QtWidgets.QTableWidgetItem(str(int(valuesYMed[i]))))

        #print("List values XMed: ", valuesXMed[0:self.viewer.sharkCount])
        #print("List values YMed: ", valuesYMed[0:self.viewer.sharkCount])



    def renameData(self):
        global renameFolderName

        #print('holacaracola')
        i = 0

        directorio = QFileDialog.getExistingDirectory(self, 'Select Dataset of raw images')

        #print(directorio)


        renameFolderName = directorio.split('/')[-1] + "/"

        #print renameFolderName

        files = sorted(os.listdir(directorio))

        dataName, okPressed = QInputDialog.getText(self, "Rename Dataset", "Insert new name:")

        if okPressed:
            #print(dataName)

            for filename in files:
                src = directorio + "/" + filename
                format = src.split('.')[-1]
                dst = dataName + str(i) + "."+ format
                dst = directorio + "/" + dst

                #print(src)
                #print(dst)

                os.rename(src,dst)
                i+=1

class Interfaz(QMainWindow):
    def __init__(self):
        super(Interfaz,self).__init__()



        self.optMen = OptionsMenu()
        self.win = Window()
        self.setCentralWidget(self.win)
        self.init_ui()

    def init_ui(self):

        # Create Menu Bar
        bar = self.menuBar()
        bar.setNativeMenuBar(False)

        # Create Root Menus
        file = bar.addMenu('File')
        analyze_info = bar.addMenu('Analyze Labelled Info')
        labelling_methods = bar.addMenu('Labelling Method')
        delete_options = bar.addMenu('Delete Options')

        personal_options = bar.addMenu('Options')

        # Signals
        self.win.dialog.hideandshowSignal.connect(self.mostrar)

        self.win.data.labelChecker.connect(self.labelChecker)
        self.win.viewer.labelChecker.connect(self.labelChecker)


        # Create Actions for Menus


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

        open_action = QAction('&New file',self)
        open_action.setShortcut('Ctrl+N')

        self.open_data_action = QAction('&Load data',self)
        self.open_data_action.setShortcut('Ctrl+L')

        self.open_data_action.setEnabled(False)

        quit_action = QAction('&Quit program',self)
        quit_action.setShortcut('Ctrl+Q')

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

        # Add actions to menus
        file.addAction(open_action)
        file.addAction(self.open_data_action)
        file.addAction(self.save_action)
        file.addAction(self.rename_dataset_action)
        file.addAction(quit_action)

        labelling_methods.addAction(self.click_and_click)
        labelling_methods.addAction(self.click_and_release)

        labelling_methods.addAction(self.click_perimeter)

        delete_options.addAction(self.reset_action)
        delete_options.addAction(self.delete_items)


        analyze_info.addAction(self.analyze_action)
        analyze_info.addAction(self.analyze_perimeter_action)
        analyze_info.addAction(self.analyze_dir_vel_action)

        personal_options.addAction(self.options)

        # Events
        quit_action.triggered.connect(self.quit_trigger)
        file.triggered.connect(self.selected)
        labelling_methods.triggered.connect(self.selected)
        delete_options.triggered.connect(self.selected)
        analyze_info.triggered.connect(self.analyze)

        personal_options.triggered.connect(self.showOptions)


        self.setWindowTitle("Shark gui")

        self.show()

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
        else:
            self.analyze_perimeter_action.setEnabled(False)
            self.click_and_release.setEnabled(True)
            self.click_and_click.setEnabled(True)



    def mostrar(self):
        self.win.dialog_2.hide()

        #al volver se elimina analisis y se quedan datos
        self.win.restablecerDatos()

        self.show()

    def quit_trigger(self):
        qApp.quit()

    def selected(self,q):

        #print(q.text() + ' selected')

        option = q.text()

        if option == '&New file':
            self.win.loadImage()

            if imag_loaded == False:
                self.save_action.setEnabled(True)
                self.open_data_action.setEnabled(True)
                self.reset_action.setEnabled(True)
                self.delete_items.setEnabled(True)
                self.click_and_click.setEnabled(True)
                self.click_and_release.setEnabled(True)
                #self.analyze_action.setEnabled(True)
                #self.analyze_perimeter_action.setEnabled(True)
                self.click_perimeter.setEnabled(True)
                self.analyze_dir_vel_action.setEnabled(True)

        elif option == '&Rename Dataset':
            self.win.renameData()
        elif option == '&Save data':
            self.win.saveData(0)
        elif option == '&Load data':
            self.win.loadData()
        elif option == '&Point and click':
            #print('point and click')
            self.click_and_release.setChecked(False)
            self.click_and_click.setChecked(True)
            self.delete_items.setChecked(False)
            self.click_perimeter.setChecked(False)
            self.win.ClickClick()
        elif option == 'Drag and &release':
            #print('drag and r')
            self.click_and_release.setChecked(True)
            self.click_and_click.setChecked(False)
            self.delete_items.setChecked(False)
            self.click_perimeter.setChecked(False)
            self.win.ClickRelease()
        elif option == '&Delete single item':
            #print('delete item')
            self.click_and_release.setChecked(False)
            self.click_and_click.setChecked(False)
            self.delete_items.setChecked(True)
            self.click_perimeter.setChecked(False)
            self.win.DeleteItem()
        elif option == '&Reset labelling info':
            self.win.ResetInfo()
        elif option == '&Select perimeter points':
            #print('select perimeter')
            self.click_perimeter.setChecked(True)
            self.click_and_release.setChecked(False)
            self.click_and_click.setChecked(False)
            self.delete_items.setChecked(False)

            self.win.ClickPerimeter()

    def analyze(self,q):
        global perAnalyze

        #print(q.text() + ' selected')

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

    def showOptions(self):
        #print('Mostramos nuevo Widget')
        self.optMen.show()




if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Interfaz()
    window.setGeometry(400, 200, 1280, 768)
    window.show()
    sys.exit(app.exec_())
