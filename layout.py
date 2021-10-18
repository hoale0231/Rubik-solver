from time import sleep
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
from solver import A_star
from copy import deepcopy

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
        self.rubik = Rubik()
        #self.rubik.moves("lffFLffl")
        self.rubik.randomFace(20)
        self.get_face_color()

    def resetFace(self):
        self.rubik = Rubik()
        self.get_face_color()

    def solve(self, mode):
        goal = A_star(deepcopy(self.rubik), mode)
        return goal

    def nextStep(self, move):
        self.rubik.moves(move)
        self.get_face_color()

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

        self.axes.imshow(im)
        self.axes.set_axis_off()

    def textOutput(self, txt):
        self.axes.cla()
        self.axes.text(-1, 0.5, txt, fontsize=20)
        self.axes.set_axis_off()
        self.draw()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.cube = RubikCube()
        self.solution = []
        self.currStep = 0
        MainWindow.setObjectName('MainWindow')
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet('background-color: rgb(245, 245, 245);')
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName('centralwidget')
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(30, 60, 371, 241))
        font = QtGui.QFont()
        font.setFamily('Apple SD Gothic Neo')
        font.setBold(True)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.groupBox.setFont(font)
        self.groupBox.setStyleSheet('background-color: rgb(238, 236, 234);\n'
                                    'border-radius: 10px;')
        self.groupBox.setFlat(True)
        self.groupBox.setCheckable(False)
        self.groupBox.setObjectName('groupBox')

        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(240, 200, 113, 32))
        self.pushButton.clicked.connect(self.solve)
        self.pushButton.setStyleSheet(  'margin: 6px;\n'
                                        'border-color: #0c457e;\n'
                                        'border-style: outset;\n'
                                        'border-radius: 5px;\n'
                                        'border-width: 1px;\n'
                                        'color: black;\n'
                                        'background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(245, 245, 245), stop: 1 rgb(245, 245, 245));')
        self.pushButton.setObjectName('pushButton')
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_2.setGeometry(QtCore.QRect(130, 200, 113, 32))
        self.pushButton_2.setStyleSheet('margin: 6px;\n'
                                        'border-color: #0c457e;\n'
                                        'border-style: outset;\n'
                                        'border-radius: 5px;\n'
                                        'border-width: 1px;\n'
                                        'color: black;\n'
                                        'background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(245, 245, 245), stop: 1 rgb(245, 245, 245));')
        self.pushButton_2.setFlat(False)
        self.pushButton_2.setObjectName('pushButton_2')
        self.pushButton_2.clicked.connect(self.resetColor)
        self.pushButton_3 = QtWidgets.QPushButton(self.groupBox, text='Random')
        self.pushButton_3.setGeometry(QtCore.QRect(20, 200, 113, 32))
        self.pushButton_3.setStyleSheet('margin: 6px;\n'
                                        'border-color: #0c457e;\n'
                                        'border-style: outset;\n'
                                        'border-radius: 5px;\n'
                                        'border-width: 1px;\n'
                                        'color: black;\n'
                                        'background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(245, 245, 245), stop: 1 rgb(245, 245, 245));')
        self.pushButton_3.setFlat(False)
        self.pushButton_3.setObjectName('pushButton_3')
        self.pushButton_3.clicked.connect(self.randomFace)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(420, 60, 351, 241))
        font = QtGui.QFont()
        font.setFamily('Apple SD Gothic Neo')
        font.setBold(True)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setStyleSheet(  'background-color: rgb(220, 226, 228);\n'
                                        'border-radius: 10px;')
        self.groupBox_2.setFlat(True)
        self.groupBox_2.setObjectName('groupBox_2')
        self.frame = QtWidgets.QFrame(self.groupBox_2)
        self.frame.setGeometry(QtCore.QRect(40, 30, 275, 181))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName('frame')
        self.myMplCanvas = my3DCanvas(self.cube, self.frame, width=3, height=2)
        self.horizontalSlider = QtWidgets.QSlider(self.groupBox_2)
        self.horizontalSlider.setGeometry(QtCore.QRect(40, 220, 275, 22))
        self.horizontalSlider.setRange(0, np.pi*20)
        self.horizontalSlider.setValue(0)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setInvertedAppearance(False)
        self.horizontalSlider.setInvertedControls(False)
        self.horizontalSlider.setObjectName('horizontalSlider')
        self.verticalSlider = QtWidgets.QSlider(self.groupBox_2)
        self.verticalSlider.setGeometry(QtCore.QRect(320, 30, 22, 201))
        self.verticalSlider.setRange(0, np.pi*20)
        self.verticalSlider.setValue(0)
        self.verticalSlider.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider.setObjectName('verticalSlider')
        self.horizontalSlider.valueChanged.connect(self.rotateCube)
        self.verticalSlider.valueChanged.connect(self.rotateCube)
        self.verticalSlider_2 = QtWidgets.QSlider(self.groupBox_2)
        self.verticalSlider_2.setGeometry(QtCore.QRect(15, 30, 22, 201))
        self.verticalSlider_2.setRange(0, np.pi*20)
        self.verticalSlider_2.setValue(0)
        self.verticalSlider_2.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_2.setObjectName('verticalSlider')
        self.verticalSlider_2.valueChanged.connect(self.rotateCube)
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(30, 310, 741, 251))
        font = QtGui.QFont()
        font.setFamily('Apple SD Gothic Neo')
        font.setBold(True)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.groupBox_3.setFont(font)
        self.groupBox_3.setStyleSheet(  'background-color: rgb(225, 229, 233);\n'
                                        'border-radius: 10px;')
        self.groupBox_3.setFlat(True)
        self.groupBox_3.setObjectName('groupBox_3')
        self.scrollArea = QtWidgets.QScrollArea(self.groupBox_3)
        self.scrollArea.setGeometry(QtCore.QRect(10, 30, 721, 211))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName('scrollArea')
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 721, 211))
        self.scrollAreaWidgetContents.setObjectName('scrollAreaWidgetContents')
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.my2DCanvas = my2DCanvas(
                                parent=self.scrollAreaWidgetContents,
                                width=7.5,
                                height=1.5)
        self.pushButton_4 = QtWidgets.QPushButton(self.scrollAreaWidgetContents, text='Next Step')
        self.pushButton_4.setGeometry(QtCore.QRect(600, 160, 113, 32))
        self.pushButton_4.clicked.connect(self.solve_step)
        self.pushButton_4.setStyleSheet('margin: 6px;\n'
                                        'border-color: #0c457e;\n'
                                        'border-style: outset;\n'
                                        'border-radius: 5px;\n'
                                        'border-width: 1px;\n'
                                        'color: black;\n'
                                        'background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(245, 245, 245), stop: 1 rgb(245, 245, 245));')
        self.pushButton_4.setObjectName('pushButton_4')
        
        self.cube.rotate(1.5, 0, 0)
        font = QtGui.QFont()
        font.setFamily('Apple SD Gothic Neo')
        font.setPointSize(30)
        font.setBold(True)
        font.setWeight(75)
        font.setStrikeOut(False)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName('statusbar')
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
  
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.resetColor()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate('MainWindow', 'MainWindow'))
        self.groupBox.setTitle(_translate('MainWindow', 'Configuration'))

       
        self.pushButton.setText(_translate('MainWindow', 'Solve'))
        self.pushButton_2.setText(_translate('MainWindow', 'Reset'))
        self.groupBox_2.setTitle(_translate('MainWindow', 'Visualization'))
        self.groupBox_3.setTitle(_translate('MainWindow', 'Solution'))

    def rotateCube(self):
        yaw = self.horizontalSlider.value()/10
        pitch = self.verticalSlider.value()/10
        roll = self.verticalSlider_2.value()/10
        self.cube.rotate(yaw, pitch, roll)
        self.myMplCanvas.updateMpl(self.cube)

    def resetColor(self):
        self.cube.resetFace()
        self.myMplCanvas.updateMpl(self.cube)
    
    def solve2(self):
        self.printSolution(self.cube.solve(0))

    def solve1(self):
        self.printSolution(self.cube.solve(1))

    def solve(self):
        self.printSolution(self.cube.solve(2))
        

    def printSolution(self, goal):
        textRoute = ""
        self.solution = []
        self.currStep = 0
        goalState, created, visited = goal
        for c in goalState.route:
            if c.islower():
                textRoute += c.upper() + '\''
            else:
                textRoute += c
            textRoute += ' '
            self.solution.append(c)
        self.my2DCanvas.textOutput(textRoute)
        self.myMplCanvas.updateMpl(self.cube)

    def randomFace(self):
        self.cube.randomFace()
        self.myMplCanvas.updateMpl(self.cube)

    def solve_step(self):
        if self.currStep < len(self.solution):
            self.cube.nextStep(self.solution[self.currStep])
            self.currStep += 1
            self.myMplCanvas.updateMpl(self.cube)