from PyQt5 import QtCore, QtGui, QtWidgets
import matplotlib
import matplotlib.pyplot as plt
from numpy.lib.function_base import select
matplotlib.use('Qt5Agg')
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from rubik import Rubik

class RubikCube:
    def __init__(self):
        self.rubik = Rubik()

        self.face_color = dict()
        self.get_face_color()

        self.edges = dict()
        self.reset_edges()

    def draw(self, axes):
        all_faces = ['F', 'B', 'L', 'R', 'U', 'D']
        for af in all_faces:
            faces = Poly3DCollection(self.edges[af], linewidths=1, edgecolors='k')
            faces.set_facecolors(self.face_color[af])
            axes.add_collection3d(faces)
        axes.set_xlim(-1.5, 1.5)
        axes.set_ylim(-1.5, 1.5)
        axes.set_zlim(-1.5, 1.5)
        axes.set_aspect('auto')
        axes._axis3don = False

    def rotate(self, yaw, pitch, roll):
        self.reset_edges()
        Ryaw = np.array([[np.cos(yaw), -np.sin(yaw), 0],
                        [np.sin(yaw), np.cos(yaw), 0],
                        [0, 0, 1]])
        Rpitch = np.array([[np.cos(pitch), 0, np.sin(pitch)],
                        [0, 1, 0],
                        [-np.sin(pitch), 0, np.cos(pitch)]])
        Rroll = np.array([[1, 0, 0],
                        [0, np.cos(roll), -np.sin(roll)],
                        [0, np.sin(roll), np.cos(roll)]])
        for key in self.edges.keys():
            self.edges[key] = self.edges[key].dot(Ryaw).dot(Rpitch).dot(Rroll)

    def reset_edges(self):
        self.edges['F'] = np.array([[[2, 0, 2], [2, 1, 2], [2, 1, 1], [2, 0, 1]],
                           [[2, 1, 2], [2, 2, 2], [2, 2, 1], [2, 1, 1]],
                           [[2, 0, 1], [2, 1, 1], [2, 1, 0], [2, 0, 0]],
                           [[2, 1, 1], [2, 2, 1], [2, 2, 0], [2, 1, 0]]])-1
        self.edges['B'] = np.array([
                           [[0, 1, 2], [0, 2, 2], [0, 2, 1], [0, 1, 1]],
                           [[0, 0, 2], [0, 1, 2], [0, 1, 1], [0, 0, 1]],
                           [[0, 1, 1], [0, 2, 1], [0, 2, 0], [0, 1, 0]],
                           [[0, 0, 1], [0, 1, 1], [0, 1, 0], [0, 0, 0]],
                           ])-1
        self.edges['L'] = np.array([[[0, 0, 2], [1, 0, 2], [1, 0, 1], [0, 0, 1]],
                           [[1, 0, 2], [2, 0, 2], [2, 0, 1], [1, 0, 1]],
                           [[0, 0, 1], [1, 0, 1], [1, 0, 0], [0, 0, 0]],
                           [[1, 0, 1], [2, 0, 1], [2, 0, 0], [1, 0, 0]]])-1
        self.edges['R'] = np.array([
                           [[1, 2, 2], [2, 2, 2], [2, 2, 1], [1, 2, 1]],
                           [[0, 2, 2], [1, 2, 2], [1, 2, 1], [0, 2, 1]],
                           [[1, 2, 1], [2, 2, 1], [2, 2, 0], [1, 2, 0]],
                           [[0, 2, 1], [1, 2, 1], [1, 2, 0], [0, 2, 0]]])-1
        self.edges['U'] = np.array([
                           [[0, 1, 2], [1, 1, 2], [1, 0, 2], [0, 0, 2]],
                           [[0, 2, 2], [1, 2, 2], [1, 1, 2], [0, 1, 2]],
                           [[1, 1, 2], [2, 1, 2], [2, 0, 2], [1, 0, 2]],
                           [[1, 2, 2], [2, 2, 2], [2, 1, 2], [1, 1, 2]],
                           ])-1
        self.edges['D'] = np.array([[[1, 1, 0], [2, 1, 0], [2, 0, 0], [1, 0, 0]],
                           [[1, 2, 0], [2, 2, 0], [2, 1, 0], [1, 1, 0]],
                           [[0, 1, 0], [1, 1, 0], [1, 0, 0], [0, 0, 0]],
                           [[0, 2, 0], [1, 2, 0], [1, 1, 0], [0, 1, 0]]])-1

    def get_face_color(self):
        hex2rgb = dict()
        hex2rgb['r'] = (189/255, 45/255, 69/255)
        hex2rgb['g'] = (67/255, 151/255, 106/255)
        hex2rgb['b'] = (40/255, 107/255, 176/255)
        hex2rgb['o'] = (233/255, 150/255, 77/255)
        hex2rgb['w'] = (254/255, 254/255, 254/255)
        hex2rgb['y'] = (254/255, 239/255, 80/255)

        self.face_color['F'] = [hex2rgb[f] for f in self.rubik.getFaceColor('F')]
        self.face_color['B'] = [hex2rgb[f] for f in self.rubik.getFaceColor('B')]
        self.face_color['L'] = [hex2rgb[f] for f in self.rubik.getFaceColor('L')]
        self.face_color['R'] = [hex2rgb[f] for f in self.rubik.getFaceColor('R')]
        self.face_color['U'] = [hex2rgb[f] for f in self.rubik.getFaceColor('U')]
        self.face_color['D'] = [hex2rgb[f] for f in self.rubik.getFaceColor('D')]

    def randomFace(self):
        self.rubik.randomFace(10)
        self.get_face_color()

    def resetFace(self):
        self.rubik = Rubik()
        self.get_face_color()

    def solve(self):
        pass

    def nextStep(self):
        pass

#TODO:
class my3DCanvas(FigureCanvas):
    '''Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.).'''

    def __init__(self, cube, parent=None, width=5, height=3):
        self.figure = Figure(figsize=(width, height), dpi=100)
        self.axes = self.figure.gca(projection='3d')

        cube.draw(self.axes)

        FigureCanvas.__init__(self, self.figure)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def updateMpl(self, cube):
        self.axes.cla()
        cube.draw(self.axes)
        self.draw()

#TODO:
class my2DCanvas(FigureCanvas):
    '''Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.).'''

    def __init__(self, solution=[], parent=None, width=5, height=3):
        self.figure = Figure(figsize=(width, height), dpi=100)
        self.axes = self.figure.gca()

        self.draw_solution(solution)

        FigureCanvas.__init__(self, self.figure)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def updateMpl(self, solution):
        self.axes.cla()
        self.draw_solution(solution)
        self.draw()

    def draw_solution(self, solution):
        im = np.ones([200, 1680, 4])
        #FIXME: Add image solution
        self.axes.imshow(im)
        self.axes.set_axis_off()

    def textOutput(self, txt):
        self.axes.cla()
        self.axes.text(-1, 0.5, txt, fontsize=20)
        self.axes.set_axis_off()
        self.draw()

#FIXME:
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.cube = RubikCube()
        self.solution = []
        #self.posColor = [['w', 'w', 'w']]*8
        self.posColor = [['w' for i in range(3)] for j in range(8)]

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1104, 810)
        MainWindow.setStyleSheet("background-color: rgb(245, 245, 245);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox_Config = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_Config.setGeometry(QtCore.QRect(70, 100, 491, 361))
        font = QtGui.QFont()
        font.setFamily("Apple SD Gothic Neo")
        font.setBold(True)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.groupBox_Config.setFont(font)
        self.groupBox_Config.setStyleSheet("background-color: rgb(238, 236, 234);\n"
"border-radius: 10px;")
        self.groupBox_Config.setFlat(True)
        self.groupBox_Config.setCheckable(False)
        self.groupBox_Config.setObjectName("groupBox_Config")

    #TODO: Random_Reset_Solve Button
        self.solveButton = QtWidgets.QPushButton(self.groupBox_Config)
        self.solveButton.setGeometry(QtCore.QRect(340, 330, 113, 32))
        self.solveButton.clicked.connect(self.solve)
        self.solveButton.setStyleSheet("margin: 6px;\n"
                                        "border-color: #0c457e;\n"
                                        "border-style: outset;\n"
                                        "border-radius: 5px;\n"
                                        "border-width: 1px;\n"
                                        "color: black;\n"
                                        "background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(245, 245, 245), stop: 1 rgb(245, 245, 245));")
        self.solveButton.setFlat(False)
        self.solveButton.setObjectName("solveButton")

        self.resetButton = QtWidgets.QPushButton(self.groupBox_Config)
        self.resetButton.setGeometry(QtCore.QRect(190, 330, 113, 32))
        self.resetButton.setStyleSheet("margin: 6px;\n"
                                        "border-color: #0c457e;\n"
                                        "border-style: outset;\n"
                                        "border-radius: 5px;\n"
                                        "border-width: 1px;\n"
                                        "color: black;\n"
                                        "background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(245, 245, 245), stop: 1 rgb(245, 245, 245));")
        self.resetButton.setFlat(False)
        self.resetButton.setObjectName("resetButton")
        self.resetButton.clicked.connect(self.resetColor)

        self.randomButton = QtWidgets.QPushButton(self.groupBox_Config)
        self.randomButton.setGeometry(QtCore.QRect(30, 330, 113, 32))
        self.randomButton.setStyleSheet("margin: 6px;\n"
                                        "border-color: #0c457e;\n"
                                        "border-style: outset;\n"
                                        "border-radius: 5px;\n"
                                        "border-width: 1px;\n"
                                        "color: black;\n"
                                        "background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(245, 245, 245), stop: 1 rgb(245, 245, 245));")
        self.randomButton.setFlat(False)
        self.randomButton.setObjectName("randomButton")
        self.randomButton.clicked.connect(self.randomFace)

        #TODO: Config
        self.groupBox_choosecolor = QtWidgets.QGroupBox(self.groupBox_Config)
        self.groupBox_choosecolor.setGeometry(QtCore.QRect(360, 30, 120, 291))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_choosecolor.setFont(font)
        self.groupBox_choosecolor.setStyleSheet("background-color: rgb(170, 255, 255);")
        self.groupBox_choosecolor.setObjectName("groupBox_choosecolor")
        
        #TODO: Choose one in six colors to Rubik
        self.orangeButton = QtWidgets.QRadioButton(self.groupBox_choosecolor)
        self.orangeButton.setGeometry(QtCore.QRect(10, 200, 95, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.orangeButton.setFont(font)
        self.orangeButton.setStyleSheet("color: rgb(255, 170, 0);")
        self.orangeButton.setCheckable(True)
        self.orangeButton.setChecked(False)
        self.orangeButton.setObjectName("orangeButton")
        self.yellowButton = QtWidgets.QRadioButton(self.groupBox_choosecolor)
        self.yellowButton.setGeometry(QtCore.QRect(10, 80, 95, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.yellowButton.setFont(font)
        self.yellowButton.setStyleSheet("color: rgb(255, 255, 0);")
        self.yellowButton.setCheckable(True)
        self.yellowButton.setChecked(False)
        self.yellowButton.setObjectName("yellowButton")
        self.redButton = QtWidgets.QRadioButton(self.groupBox_choosecolor)
        self.redButton.setGeometry(QtCore.QRect(10, 50, 51, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.redButton.setFont(font)
        self.redButton.setStyleSheet("color: rgb(255, 0, 0);")
        self.redButton.setCheckable(True)
        self.redButton.setChecked(False)
        self.redButton.setObjectName("redButton")
        self.blueButton = QtWidgets.QRadioButton(self.groupBox_choosecolor)
        self.blueButton.setGeometry(QtCore.QRect(10, 110, 95, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.blueButton.setFont(font)
        self.blueButton.setStyleSheet("color: rgb(0, 85, 255);")
        self.blueButton.setCheckable(True)
        self.blueButton.setChecked(False)
        self.blueButton.setObjectName("blueButton")
        self.greenButton = QtWidgets.QRadioButton(self.groupBox_choosecolor)
        self.greenButton.setGeometry(QtCore.QRect(10, 140, 95, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.greenButton.setFont(font)
        self.greenButton.setStyleSheet("color: rgb(0, 170, 0);")
        self.greenButton.setCheckable(True)
        self.greenButton.setChecked(False)
        self.greenButton.setObjectName("greenButton")
        self.whiteButton = QtWidgets.QRadioButton(self.groupBox_choosecolor)
        self.whiteButton.setGeometry(QtCore.QRect(10, 170, 95, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.whiteButton.setFont(font)
        self.whiteButton.setStyleSheet("color: rgb(255, 255, 255);")
        self.whiteButton.setCheckable(True)
        self.whiteButton.setChecked(True)
        self.whiteButton.setObjectName("whiteButton")

        self.loadButton = QtWidgets.QPushButton(self.groupBox_choosecolor)
        self.loadButton.setGeometry(QtCore.QRect(0, 240, 113, 32))
        self.loadButton.setStyleSheet("margin: 6px;\n"
"border-color: #0c457e;\n"
"border-style: outset;\n"
"border-radius: 5px;\n"
"border-width: 1px;\n"
"color: black;\n"
"background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(245, 245, 245), stop: 1 rgb(245, 245, 245));")
        self.loadButton.setFlat(False)
        self.loadButton.clicked.connect(self.printinput)
        self.loadButton.setObjectName("loadButton")

        #TODO: Group Rubik 2D (input)
        self.Rubik_2D = QtWidgets.QGroupBox(self.groupBox_Config)
        self.Rubik_2D.setGeometry(QtCore.QRect(10, 30, 341, 291))
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.Rubik_2D.setFont(font)
        self.Rubik_2D.setStyleSheet("background-color: rgb(170, 255, 255);")
        self.Rubik_2D.setObjectName("Rubik_2D")

        #TODO: 24 faces of Rubik
        self.button_F = QtWidgets.QPushButton(self.Rubik_2D)
        self.button_F.setGeometry(QtCore.QRect(130, 110, 41, 41))
        self.button_F.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.button_F.setText("")
        self.button_F.clicked.connect(lambda: self.applyColor(self.button_F, 2, 2))
        self.button_F.setObjectName("button_F")
        self.button_Z = QtWidgets.QPushButton(self.Rubik_2D)
        self.button_Z.setGeometry(QtCore.QRect(90, 230, 41, 41))
        self.button_Z.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.button_Z.setText("")
        self.button_Z.clicked.connect(lambda: self.applyColor(self.button_Z, 7, 0))
        self.button_Z.setObjectName("button_Z")
        self.button_V = QtWidgets.QPushButton(self.Rubik_2D)
        self.button_V.setGeometry(QtCore.QRect(130, 190, 41, 41))
        self.button_V.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.button_V.setText("")
        self.button_V.clicked.connect(lambda: self.applyColor(self.button_V, 5, 0))
        self.button_V.setObjectName("button_V")
        self.button_A = QtWidgets.QPushButton(self.Rubik_2D)
        self.button_A.setGeometry(QtCore.QRect(90, 30, 41, 41))
        self.button_A.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.button_A.setText("")
        self.button_A.clicked.connect(lambda: self.applyColor(self.button_A, 0, 0))
        self.button_A.setObjectName("button_A")
        self.button_M = QtWidgets.QPushButton(self.Rubik_2D)
        self.button_M.setGeometry(QtCore.QRect(250, 110, 41, 41))
        self.button_M.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.button_M.setText("")
        self.button_M.clicked.connect(lambda: self.applyColor(self.button_M, 1, 1))
        self.button_M.setObjectName("button_M")
        self.button_B = QtWidgets.QPushButton(self.Rubik_2D)
        self.button_B.setGeometry(QtCore.QRect(130, 30, 41, 41))
        self.button_B.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.button_B.setText("")
        self.button_B.clicked.connect(lambda: self.applyColor(self.button_B, 1, 0))
        self.button_B.setObjectName("button_B")
        self.button_K = QtWidgets.QPushButton(self.Rubik_2D)
        self.button_K.setGeometry(QtCore.QRect(210, 150, 41, 41))
        self.button_K.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.button_K.setText("")
        self.button_K.clicked.connect(lambda: self.applyColor(self.button_K, 6, 1))
        self.button_K.setObjectName("button_K")
        self.button_O = QtWidgets.QPushButton(self.Rubik_2D)
        self.button_O.setGeometry(QtCore.QRect(290, 150, 41, 41))
        self.button_O.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.button_O.setText("")
        self.button_O.clicked.connect(lambda: self.applyColor(self.button_O, 7, 1))
        self.button_O.setObjectName("button_O")
        self.button_Q = QtWidgets.QPushButton(self.Rubik_2D)
        self.button_Q.setGeometry(QtCore.QRect(10, 110, 41, 41))
        self.button_Q.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.button_Q.setText("")
        self.button_Q.clicked.connect(lambda: self.applyColor(self.button_Q, 0, 1))
        self.button_Q.setObjectName("button_Q")
        self.button_G = QtWidgets.QPushButton(self.Rubik_2D)
        self.button_G.setGeometry(QtCore.QRect(130, 150, 41, 41))
        self.button_G.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.button_G.setText("")
        self.button_G.clicked.connect(lambda: self.applyColor(self.button_G, 5, 1))
        self.button_G.setObjectName("button_G")
        self.button_L = QtWidgets.QPushButton(self.Rubik_2D)
        self.button_L.setGeometry(QtCore.QRect(170, 150, 41, 41))
        self.button_L.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.button_L.setText("")
        self.button_L.clicked.connect(lambda: self.applyColor(self.button_L, 5, 2))
        self.button_L.setObjectName("button_L")
        self.button_N = QtWidgets.QPushButton(self.Rubik_2D)
        self.button_N.setGeometry(QtCore.QRect(290, 110, 41, 41))
        self.button_N.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.button_N.setText("")
        self.button_N.clicked.connect(lambda: self.applyColor(self.button_N, 0, 2))
        self.button_N.setObjectName("button_N")
        self.button_E = QtWidgets.QPushButton(self.Rubik_2D)
        self.button_E.setGeometry(QtCore.QRect(90, 110, 41, 41))
        self.button_E.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.button_E.setText("")
        self.button_E.clicked.connect(lambda: self.applyColor(self.button_E, 3, 1))
        self.button_E.setObjectName("button_E")
        self.button_J = QtWidgets.QPushButton(self.Rubik_2D)
        self.button_J.setGeometry(QtCore.QRect(210, 110, 41, 41))
        self.button_J.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.button_J.setText("")
        self.button_J.clicked.connect(lambda: self.applyColor(self.button_J, 1, 2))
        self.button_J.setObjectName("button_J")
        self.button_T = QtWidgets.QPushButton(self.Rubik_2D)
        self.button_T.setGeometry(QtCore.QRect(10, 150, 41, 41))
        self.button_T.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.button_T.setText("")
        self.button_T.clicked.connect(lambda: self.applyColor(self.button_T, 7, 2))
        self.button_T.setObjectName("button_T")
        self.button_H = QtWidgets.QPushButton(self.Rubik_2D)
        self.button_H.setGeometry(QtCore.QRect(90, 150, 41, 41))
        self.button_H.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.button_H.setText("")
        self.button_H.clicked.connect(lambda: self.applyColor(self.button_H, 4, 2))
        self.button_H.setObjectName("button_H")
        self.button_W = QtWidgets.QPushButton(self.Rubik_2D)
        self.button_W.setGeometry(QtCore.QRect(130, 230, 41, 41))
        self.button_W.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.button_W.setText("")
        self.button_W.clicked.connect(lambda: self.applyColor(self.button_W, 6, 0))
        self.button_W.setObjectName("button_W")
        self.button_U = QtWidgets.QPushButton(self.Rubik_2D)
        self.button_U.setGeometry(QtCore.QRect(90, 190, 41, 41))
        self.button_U.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.button_U.setText("")
        self.button_U.clicked.connect(lambda: self.applyColor(self.button_U, 5, 0))
        self.button_U.setObjectName("button_U")
        self.button_D = QtWidgets.QPushButton(self.Rubik_2D)
        self.button_D.setGeometry(QtCore.QRect(90, 70, 41, 41))
        self.button_D.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.button_D.setText("")
        self.button_D.clicked.connect(lambda: self.applyColor(self.button_D, 3, 0))
        self.button_D.setObjectName("button_D")
        self.button_I = QtWidgets.QPushButton(self.Rubik_2D)
        self.button_I.setGeometry(QtCore.QRect(170, 110, 41, 41))
        self.button_I.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.button_I.setText("")
        self.button_I.clicked.connect(lambda: self.applyColor(self.button_I, 2, 1))
        self.button_I.setObjectName("button_I")
        self.button_R = QtWidgets.QPushButton(self.Rubik_2D)
        self.button_R.setGeometry(QtCore.QRect(50, 110, 41, 41))
        self.button_R.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.button_R.setText("")
        self.button_R.clicked.connect(lambda: self.applyColor(self.button_R, 3, 2))
        self.button_R.setObjectName("button_R")
        self.button_C = QtWidgets.QPushButton(self.Rubik_2D)
        self.button_C.setGeometry(QtCore.QRect(130, 70, 41, 41))
        self.button_C.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.button_C.setText("")
        self.button_C.clicked.connect(lambda: self.applyColor(self.button_C, 2, 0))
        self.button_C.setObjectName("button_C")
        self.button_P = QtWidgets.QPushButton(self.Rubik_2D)
        self.button_P.setGeometry(QtCore.QRect(250, 150, 41, 41))
        self.button_P.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.button_P.setText("")
        self.button_P.clicked.connect(lambda: self.applyColor(self.button_P, 6, 2))
        self.button_P.setObjectName("button_P")
        self.button_S = QtWidgets.QPushButton(self.Rubik_2D)
        self.button_S.setGeometry(QtCore.QRect(50, 150, 41, 41))
        self.button_S.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.button_S.setText("")
        self.button_S.clicked.connect(lambda: self.applyColor(self.button_S, 4, 1))
        self.button_S.setObjectName("button_S")
        self.groupBox_Visual = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_Visual.setGeometry(QtCore.QRect(580, 100, 461, 361))
        font = QtGui.QFont()
        font.setFamily("Apple SD Gothic Neo")
        font.setBold(True)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(75)

    #FIXME: ViSualization
        self.groupBox_Visual.setFont(font)
        self.groupBox_Visual.setStyleSheet("background-color: rgb(220, 226, 228);\n"
"border-radius: 10px;")
        self.groupBox_Visual.setFlat(True)
        self.groupBox_Visual.setObjectName("groupBox_Visual")
        self.frame_3D = QtWidgets.QFrame(self.groupBox_Visual)
        self.frame_3D.setGeometry(QtCore.QRect(40, 40, 381, 281))
        self.frame_3D.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.frame_3D.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3D.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3D.setObjectName("frame_3D")

        #TODO: Visualize Rubik Cube
        self.myMplCanvas = my3DCanvas(self.cube, self.frame_3D, width=3.7, height=3)
        
        #TODO: Slider
        self.horizontalSlider = QtWidgets.QSlider(self.groupBox_Visual)
        self.horizontalSlider.setGeometry(QtCore.QRect(60, 330, 331, 22))
        self.horizontalSlider.setSliderPosition(50)
        self.horizontalSlider.setRange(0, np.pi*20)
        self.horizontalSlider.setValue(0)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setInvertedAppearance(False)
        self.horizontalSlider.setInvertedControls(False)
        self.horizontalSlider.setObjectName('horizontalSlider')
        self.verticalSlider_right = QtWidgets.QSlider(self.groupBox_Visual)
        self.verticalSlider_right.setGeometry(QtCore.QRect(430, 30, 22, 301))
        self.horizontalSlider.setSliderPosition(50)
        self.verticalSlider_right.setRange(0, np.pi*20)
        self.verticalSlider_right.setValue(0)
        self.verticalSlider_right.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_right.setObjectName('verticalSlider_right')
        self.horizontalSlider.valueChanged.connect(self.rotateCube)
        self.verticalSlider_right.valueChanged.connect(self.rotateCube)
        self.verticalSlider_left = QtWidgets.QSlider(self.groupBox_Visual)
        self.verticalSlider_left.setGeometry(QtCore.QRect(10, 30, 22, 301))
        self.horizontalSlider.setSliderPosition(50)
        self.verticalSlider_left.setRange(0, np.pi*20)
        self.verticalSlider_left.setValue(0)
        self.verticalSlider_left.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_left.setObjectName('verticalSlider_left')
        self.verticalSlider_left.valueChanged.connect(self.rotateCube)

    #FIXME: Solution
        self.groupBox_Solution = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_Solution.setGeometry(QtCore.QRect(50, 480, 1011, 301))
        font = QtGui.QFont()
        font.setFamily("Apple SD Gothic Neo")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.groupBox_Solution.setFont(font)
        self.groupBox_Solution.setStyleSheet("background-color: rgb(225, 229, 233);\n"
"border-radius: 10px;")
        self.groupBox_Solution.setFlat(True)
        self.groupBox_Solution.setObjectName("groupBox_Solution")
        self.scrollArea_Solution = QtWidgets.QScrollArea(self.groupBox_Solution)
        self.scrollArea_Solution.setGeometry(QtCore.QRect(40, 50, 921, 181))
        self.scrollArea_Solution.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.scrollArea_Solution.setWidgetResizable(True)
        self.scrollArea_Solution.setObjectName("scrollArea_Solution")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 921, 181))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea_Solution.setWidget(self.scrollAreaWidgetContents)

        self.my2DCanvas = my2DCanvas(
            parent=self.scrollAreaWidgetContents,
            width=7.5,
            height=1.5)

        #TODO: Next Step Button
        self.nextButton = QtWidgets.QPushButton(self.groupBox_Solution, text = "Next Step")
        self.nextButton.setGeometry(QtCore.QRect(830, 250, 113, 32))
        self.nextButton.clicked.connect(self.solve_step)
        self.nextButton.setStyleSheet("margin: 6px;\n"
"border-color: #0c457e;\n"
"border-style: outset;\n"
"border-radius: 5px;\n"
"border-width: 1px;\n"
"color: black;\n"
"background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(245, 245, 245), stop: 1 rgb(245, 245, 245));")
        self.nextButton.setObjectName("nextButton")

    #FIXME: NameProject - Title
        self.NameProject = QtWidgets.QLabel(self.centralwidget)
        self.NameProject.setGeometry(QtCore.QRect(240, 15, 611, 71))
        font = QtGui.QFont()
        font.setFamily("Apple SD Gothic Neo")
        font.setPointSize(30)
        font.setBold(True)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.NameProject.setFont(font)
        self.NameProject.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.NameProject.setAutoFillBackground(False)
        self.NameProject.setStyleSheet("color: rgb(76, 76, 76);\n"
"color: rgb(255, 0, 0);")
        self.NameProject.setTextFormat(QtCore.Qt.RichText)
        self.NameProject.setAlignment(QtCore.Qt.AlignCenter)
        self.NameProject.setObjectName("NameProject")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.resetColor()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox_Config.setTitle(_translate("MainWindow", "Configuration"))
        self.solveButton.setText(_translate("MainWindow", "Solve"))
        self.resetButton.setText(_translate("MainWindow", "Reset"))
        self.randomButton.setText(_translate("MainWindow", "Random"))
        self.groupBox_choosecolor.setTitle(_translate("MainWindow", "Choose Color"))
        self.orangeButton.setText(_translate("MainWindow", "ORANGE"))
        self.yellowButton.setText(_translate("MainWindow", "YELLOW"))
        self.redButton.setText(_translate("MainWindow", "RED"))
        self.blueButton.setText(_translate("MainWindow", "BLUE"))
        self.greenButton.setText(_translate("MainWindow", "GREEN"))
        self.whiteButton.setText(_translate("MainWindow", "WHITE"))
        self.loadButton.setText(_translate("MainWindow", "Load"))
        self.Rubik_2D.setTitle(_translate("MainWindow", "2D Rubik"))
        self.groupBox_Visual.setTitle(_translate("MainWindow", "Visualization"))
        self.groupBox_Solution.setTitle(_translate("MainWindow", "Solution"))
        self.nextButton.setText(_translate("MainWindow", "Next Step"))
        self.NameProject.setText(_translate("MainWindow", "Rubic\'s Cube Solver"))

    #TODO: Add Color 2D Rubik
    def applyColor(self, button_pos, x, y):
        if self.orangeButton.isChecked():
            button_pos.setStyleSheet("background-color: rgb(255, 170, 0);")
            self.posColor[x][y] = 'o'
        elif self.yellowButton.isChecked():
            button_pos.setStyleSheet("background-color: rgb(255, 255, 0);")
            self.posColor[x][y] = 'y'
        elif self.redButton.isChecked():
            button_pos.setStyleSheet("background-color: rgb(255, 0, 0);")
            self.posColor[x][y] = 'r'
        elif self.blueButton.isChecked():
            button_pos.setStyleSheet("background-color: rgb(0, 85, 255);")
            self.posColor[x][y] = 'b'
        elif self.greenButton.isChecked():
            button_pos.setStyleSheet("background-color: rgb(0, 170, 0);")
            self.posColor[x][y] = 'g'
        elif self.whiteButton.isChecked():
            button_pos.setStyleSheet("background-color: rgb(255, 255, 255);")
            self.posColor[x][y] = 'w'
        else:
            print('Not Found')

#     #Print  input
    def printinput(self):
        print('Input: ', self.posColor)

    def rotateCube(self):
        yaw = self.horizontalSlider.value()/10
        pitch = self.verticalSlider_right.value()/10
        roll = self.verticalSlider_left.value()/10
        self.cube.rotate(yaw, pitch, roll)
        self.myMplCanvas.updateMpl(self.cube)

    def resetColor(self):
        self.cube.resetFace()
        self.myMplCanvas.updateMpl(self.cube)
    

    def solve(self):
        self.cube.solve()
        self.myMplCanvas.updateMpl(self.cube)
        

    def randomFace(self):
        self.cube.randomFace()
        self.myMplCanvas.updateMpl(self.cube)

    def solve_step(self):
        self.cube.nextStep()
        self.myMplCanvas.updateMpl(self.cube)
