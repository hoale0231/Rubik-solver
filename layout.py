import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import*
import matplotlib
import matplotlib.pyplot as plt
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
        self.rubik.randomFace(20)
        self.get_face_color()

    def resetFace(self):
        self.rubik = Rubik()
        self.get_face_color()

    def solve(self, mode):
        temp = deepcopy(self.rubik)
        start = time.time()
        goal = A_star(temp, mode)
        end = time.time()
        if goal is None: return None
        return goal[0], goal[1], goal[2], end - start

    def nextStep(self, move):
        self.rubik.moves(move)
        self.get_face_color()

    def moveByStep(self, move):
        self.rubik = Rubik()
        self.rubik.moves(move)
        self.get_face_color()

    def loadColor(self, color):
        if not self.rubik.loadColor(color):
            return False
        self.get_face_color()
        return True

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
        im = np.ones([267, 2310, 4])
        imlib = [plt.imread('Images/F.png'),
                 plt.imread('Images/Fi.png'),
                 plt.imread('Images/L.png'),
                 plt.imread('Images/Li.png'),
                 plt.imread('Images/U.png'),
                 plt.imread('Images/Ui.png'),
                 plt.imread('Images/B.png'),
                 plt.imread('Images/Bi.png'),
                 plt.imread('Images/R.png'),
                 plt.imread('Images/Ri.png'),
                 plt.imread('Images/D.png'),
                 plt.imread('Images/Di.png')]
        copySolution = []
        for move in solution:
            if move == 'F':
                copySolution.append(0)
            elif move == 'f':
                copySolution.append(1)
            elif move == 'L':
                copySolution.append(2)
            elif move == 'l':
                copySolution.append(3)
            elif move == 'U':
                copySolution.append(4)
            elif move == 'u':
                copySolution.append(5)
            elif move == 'B':
                copySolution.append(6)
            elif move == 'b':
                copySolution.append(7)
            elif move == 'R':
                copySolution.append(8)
            elif move == 'r':
                copySolution.append(9)
            elif move == 'D':
                copySolution.append(10)
            elif move == 'd':
                copySolution.append(11)
        for i, s in enumerate(copySolution):
            im[:, i*165:(i+1)*165, :] = imlib[s]
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
        self.posColor = [['w' for i in range(3)] for j in range(8)]
        self.currentStep = 0
        MainWindow.setObjectName('MainWindow')
        MainWindow.resize(1200, 900)
        MainWindow.setStyleSheet('background-color: rgb(245, 245, 245);')
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName('centralwidget')
        width = MainWindow.frameGeometry().width()
        height = MainWindow.frameGeometry().height()
        
        # Group 1: Set Input
        styleButton = 'margin: 6px; \
                border-color: #0c457e; \
                border-style: outset; \
                border-radius: 5px; \
                border-width: 1px;  \
                color: black; \
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(245, 245, 245), stop: 1 rgb(245, 245, 245));'

        self.groupBox_1 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_1.setGeometry(QtCore.QRect(30, 50, width * 0.5, height * 0.6))
        font = QtGui.QFont()
        font.setFamily('Apple SD Gothic Neo')
        font.setBold(True)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.groupBox_1.setFont(font)
        self.groupBox_1.setStyleSheet('background-color: rgb(238, 236, 234);\n'
                                    'border-radius: 10px;')
        self.groupBox_1.setFlat(True)
        self.groupBox_1.setCheckable(False)
        self.groupBox_1.setObjectName('groupBox')
        widthBox_1 = self.groupBox_1.frameGeometry().width()
        heightBox_1 = self.groupBox_1.frameGeometry().height()

        self.solve_1 = QtWidgets.QPushButton(self.groupBox_1, text='Solve 1')
        self.solve_1.setGeometry(QtCore.QRect(30, 480, 113, 32))
        self.solve_1.setStyleSheet(styleButton)
        self.solve_1.setFlat(False)
        self.solve_1.setObjectName('Solve 1')
        self.solve_1.clicked.connect(lambda: self.solve(0))

        self.solve_2 = QtWidgets.QPushButton(self.groupBox_1, text='Solve 2')
        self.solve_2.setGeometry(QtCore.QRect(widthBox_1 * 0.4, 480, 113, 32))
        self.solve_2.setStyleSheet(styleButton)
        self.solve_2.setFlat(False)
        self.solve_2.setObjectName('Solve 2')
        self.solve_2.clicked.connect(lambda: self.solve(1))
        
        self.solve_3 = QtWidgets.QPushButton(self.groupBox_1, text='Solve 3')
        self.solve_3.setGeometry(QtCore.QRect(widthBox_1 * 0.75, 480, 113, 32))
        self.solve_3.setStyleSheet(styleButton)
        self.solve_3.setFlat(False)
        self.solve_3.setObjectName('Solve 3')
        self.solve_3.clicked.connect(lambda: self.solve(2))

        self.randomButton = QtWidgets.QPushButton(self.groupBox_1, text='Random')
        self.randomButton.setGeometry(QtCore.QRect(widthBox_1 * 0.2, 20, 113, 32))
        self.randomButton.setStyleSheet(styleButton)
        self.randomButton.setFlat(False)
        self.randomButton.setObjectName('Random')
        self.randomButton.clicked.connect(self.randomFace)

        self.resetButton = QtWidgets.QPushButton(self.groupBox_1, text='Reset')
        self.resetButton.setGeometry(QtCore.QRect(widthBox_1 * 0.6, 20, 113, 32))
        self.resetButton.setStyleSheet(styleButton)
        self.resetButton.setFlat(False)
        self.resetButton.setObjectName('Reset')
        self.resetButton.clicked.connect(self.reset)

        self.inputColor = QtWidgets.QPushButton(self.groupBox_1, text='Input Colors')
        self.inputColor.setGeometry(QtCore.QRect(widthBox_1 * 0.2, 45, 113, 32))
        self.inputColor.setStyleSheet(styleButton)
        self.inputColor.setFlat(False)
        self.inputColor.setObjectName('Input Colors')
        self.inputColor.clicked.connect(lambda: self.showInput(0))

        self.inputStep = QtWidgets.QPushButton(self.groupBox_1, text='Input Steps')
        self.inputStep.setGeometry(QtCore.QRect(widthBox_1 * 0.6, 45, 113, 32))
        self.inputStep.setStyleSheet(styleButton)
        self.inputStep.setFlat(False)
        self.inputStep.setObjectName('Input Steps')
        self.inputStep.clicked.connect(lambda: self.showInput(1))

        # Group box choose color

        self.groupBox_choosecolor = QtWidgets.QGroupBox(self.groupBox_1, title="Choose Colors")
        self.groupBox_choosecolor.setGeometry(QtCore.QRect(widthBox_1 * 0.75, heightBox_1 * 0.2, widthBox_1 * 0.2, heightBox_1 * 0.6))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_choosecolor.setFont(font)
        self.groupBox_choosecolor.setStyleSheet("background-color: rgb(170, 255, 255);")
        self.groupBox_choosecolor.setObjectName("groupBox_choosecolor")

        #TODO: Choose one in six colors to Rubik
        self.orangeButton = QtWidgets.QRadioButton(self.groupBox_choosecolor, text="Orange")
        self.orangeButton.setGeometry(QtCore.QRect(10, 250, 95, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.orangeButton.setFont(font)
        self.orangeButton.setStyleSheet("color: rgb(255, 170, 0);")
        self.orangeButton.setCheckable(True)
        self.orangeButton.setChecked(False)
        self.orangeButton.setObjectName("orangeButton")

        self.whiteButton = QtWidgets.QRadioButton(self.groupBox_choosecolor, text="White")
        self.whiteButton.setGeometry(QtCore.QRect(10, 210, 95, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.whiteButton.setFont(font)
        self.whiteButton.setStyleSheet("color: rgb(255, 255, 255);")
        self.whiteButton.setCheckable(True)
        self.whiteButton.setChecked(True)
        self.whiteButton.setObjectName("whiteButton")

        self.greenButton = QtWidgets.QRadioButton(self.groupBox_choosecolor, text="Green")
        self.greenButton.setGeometry(QtCore.QRect(10, 170, 95, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.greenButton.setFont(font)
        self.greenButton.setStyleSheet("color: rgb(0, 170, 0);")
        self.greenButton.setCheckable(True)
        self.greenButton.setChecked(False)
        self.greenButton.setObjectName("greenButton")

        self.blueButton = QtWidgets.QRadioButton(self.groupBox_choosecolor, text="Blue")
        self.blueButton.setGeometry(QtCore.QRect(10, 130, 95, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.blueButton.setFont(font)
        self.blueButton.setStyleSheet("color: rgb(0, 85, 255);")
        self.blueButton.setCheckable(True)
        self.blueButton.setChecked(False)
        self.blueButton.setObjectName("blueButton")

        self.yellowButton = QtWidgets.QRadioButton(self.groupBox_choosecolor, text="Yellow")
        self.yellowButton.setGeometry(QtCore.QRect(10, 90, 95, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.yellowButton.setFont(font)
        self.yellowButton.setStyleSheet("color: rgb(255, 255, 0);")
        self.yellowButton.setCheckable(True)
        self.yellowButton.setChecked(False)
        self.yellowButton.setObjectName("yellowButton")

        self.redButton = QtWidgets.QRadioButton(self.groupBox_choosecolor, text="Red")
        self.redButton.setGeometry(QtCore.QRect(10, 50, 95, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.redButton.setFont(font)
        self.redButton.setStyleSheet("color: rgb(255, 0, 0);")
        self.redButton.setCheckable(True)
        self.redButton.setChecked(False)
        self.redButton.setObjectName("redButton")

        self.loadButton = QtWidgets.QPushButton(self.groupBox_choosecolor, text="Load")
        self.loadButton.setGeometry(QtCore.QRect(0, 280, 113, 32))
        self.loadButton.setStyleSheet(styleButton)
        self.loadButton.setFlat(False)
        self.loadButton.clicked.connect(self.loadInputColor)
        self.loadButton.setObjectName("loadButton")
        
        #TODO: Group Rubik 2D (input)
        self.rubik_2D = QtWidgets.QGroupBox(self.groupBox_1)
        self.rubik_2D.setGeometry(QtCore.QRect(30, heightBox_1 * 0.2, widthBox_1 * 0.65, heightBox_1 * 0.6))
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.rubik_2D.setFont(font)
        self.rubik_2D.setStyleSheet("background-color: rgb(170, 255, 255);")
        self.rubik_2D.setObjectName("Rubik_2D")
        
        #TODO: 24 faces of Rubik
        self.button_F = QtWidgets.QPushButton(self.rubik_2D)
        self.button_F.setGeometry(QtCore.QRect(130, 110, 40, 40))
        self.button_F.clicked.connect(lambda: self.applyColor(self.button_F, 2, 2))
        self.button_F.setObjectName("button_F")

        self.button_Z = QtWidgets.QPushButton(self.rubik_2D)
        self.button_Z.setGeometry(QtCore.QRect(90, 230, 40, 40))
        self.button_Z.clicked.connect(lambda: self.applyColor(self.button_Z, 7, 0))
        self.button_Z.setObjectName("button_Z")

        self.button_V = QtWidgets.QPushButton(self.rubik_2D)
        self.button_V.setGeometry(QtCore.QRect(130, 190, 40, 40))
        self.button_V.clicked.connect(lambda: self.applyColor(self.button_V, 5, 0))
        self.button_V.setObjectName("button_V")

        self.button_A = QtWidgets.QPushButton(self.rubik_2D)
        self.button_A.setGeometry(QtCore.QRect(90, 30, 40, 40))
        self.button_A.clicked.connect(lambda: self.applyColor(self.button_A, 0, 0))
        self.button_A.setObjectName("button_A")

        self.button_M = QtWidgets.QPushButton(self.rubik_2D)
        self.button_M.setGeometry(QtCore.QRect(250, 110, 40, 40))
        self.button_M.clicked.connect(lambda: self.applyColor(self.button_M, 1, 1))
        self.button_M.setObjectName("button_M")

        self.button_B = QtWidgets.QPushButton(self.rubik_2D)
        self.button_B.setGeometry(QtCore.QRect(130, 30, 40, 40))
        self.button_B.clicked.connect(lambda: self.applyColor(self.button_B, 1, 0))
        self.button_B.setObjectName("button_B")

        self.button_K = QtWidgets.QPushButton(self.rubik_2D)
        self.button_K.setGeometry(QtCore.QRect(210, 150, 40, 40))
        self.button_K.clicked.connect(lambda: self.applyColor(self.button_K, 6, 1))
        self.button_K.setObjectName("button_K")

        self.button_O = QtWidgets.QPushButton(self.rubik_2D)
        self.button_O.setGeometry(QtCore.QRect(290, 150, 40, 40))
        self.button_O.clicked.connect(lambda: self.applyColor(self.button_O, 7, 1))
        self.button_O.setObjectName("button_O")

        self.button_Q = QtWidgets.QPushButton(self.rubik_2D)
        self.button_Q.setGeometry(QtCore.QRect(10, 110, 40, 40))
        self.button_Q.clicked.connect(lambda: self.applyColor(self.button_Q, 0, 1))
        self.button_Q.setObjectName("button_Q")

        self.button_G = QtWidgets.QPushButton(self.rubik_2D)
        self.button_G.setGeometry(QtCore.QRect(130, 150, 40, 40))
        self.button_G.clicked.connect(lambda: self.applyColor(self.button_G, 5, 1))
        self.button_G.setObjectName("button_G")

        self.button_L = QtWidgets.QPushButton(self.rubik_2D)
        self.button_L.setGeometry(QtCore.QRect(170, 150, 40, 40))
        self.button_L.clicked.connect(lambda: self.applyColor(self.button_L, 5, 2))
        self.button_L.setObjectName("button_L")

        self.button_N = QtWidgets.QPushButton(self.rubik_2D)
        self.button_N.setGeometry(QtCore.QRect(290, 110, 40, 40))
        self.button_N.clicked.connect(lambda: self.applyColor(self.button_N, 0, 2))
        self.button_N.setObjectName("button_N")

        self.button_E = QtWidgets.QPushButton(self.rubik_2D)
        self.button_E.setGeometry(QtCore.QRect(90, 110, 40, 40))
        self.button_E.clicked.connect(lambda: self.applyColor(self.button_E, 3, 1))
        self.button_E.setObjectName("button_E")

        self.button_J = QtWidgets.QPushButton(self.rubik_2D)
        self.button_J.setGeometry(QtCore.QRect(210, 110, 40, 40))
        self.button_J.clicked.connect(lambda: self.applyColor(self.button_J, 1, 2))
        self.button_J.setObjectName("button_J")

        self.button_T = QtWidgets.QPushButton(self.rubik_2D)
        self.button_T.setGeometry(QtCore.QRect(10, 150, 40, 40))
        self.button_T.clicked.connect(lambda: self.applyColor(self.button_T, 7, 2))
        self.button_T.setObjectName("button_T")

        self.button_H = QtWidgets.QPushButton(self.rubik_2D)
        self.button_H.setGeometry(QtCore.QRect(90, 150, 40, 40))
        self.button_H.clicked.connect(lambda: self.applyColor(self.button_H, 4, 2))
        self.button_H.setObjectName("button_H")

        self.button_W = QtWidgets.QPushButton(self.rubik_2D)
        self.button_W.setGeometry(QtCore.QRect(130, 230, 40, 40))
        self.button_W.clicked.connect(lambda: self.applyColor(self.button_W, 6, 0))
        self.button_W.setObjectName("button_W")

        self.button_U = QtWidgets.QPushButton(self.rubik_2D)
        self.button_U.setGeometry(QtCore.QRect(90, 190, 40, 40))
        self.button_U.clicked.connect(lambda: self.applyColor(self.button_U, 4, 0))
        self.button_U.setObjectName("button_U")

        self.button_D = QtWidgets.QPushButton(self.rubik_2D)
        self.button_D.setGeometry(QtCore.QRect(90, 70, 40, 40))
        self.button_D.clicked.connect(lambda: self.applyColor(self.button_D, 3, 0))
        self.button_D.setObjectName("button_D")

        self.button_I = QtWidgets.QPushButton(self.rubik_2D)
        self.button_I.setGeometry(QtCore.QRect(170, 110, 40, 40))
        self.button_I.clicked.connect(lambda: self.applyColor(self.button_I, 2, 1))
        self.button_I.setObjectName("button_I")

        self.button_R = QtWidgets.QPushButton(self.rubik_2D)
        self.button_R.setGeometry(QtCore.QRect(50, 110, 40, 40))
        self.button_R.clicked.connect(lambda: self.applyColor(self.button_R, 3, 2))
        self.button_R.setObjectName("button_R")

        self.button_C = QtWidgets.QPushButton(self.rubik_2D)
        self.button_C.setGeometry(QtCore.QRect(130, 70, 40, 40))
        self.button_C.clicked.connect(lambda: self.applyColor(self.button_C, 2, 0))
        self.button_C.setObjectName("button_C")

        self.button_P = QtWidgets.QPushButton(self.rubik_2D)
        self.button_P.setGeometry(QtCore.QRect(250, 150, 40, 40))
        self.button_P.clicked.connect(lambda: self.applyColor(self.button_P, 6, 2))
        self.button_P.setObjectName("button_P")

        self.button_S = QtWidgets.QPushButton(self.rubik_2D)
        self.button_S.setGeometry(QtCore.QRect(50, 150, 40, 40))
        self.button_S.clicked.connect(lambda: self.applyColor(self.button_S, 4, 1))
        self.button_S.setObjectName("button_S")

        # Add buttons to list rubik buttons
        self.listRubikButton = [self.button_A, self.button_B, self.button_C, self.button_D,
                            self.button_E, self.button_F, self.button_G, self.button_H,
                            self.button_I, self.button_J, self.button_K, self.button_L,
                            self.button_M, self.button_N, self.button_O, self.button_P,
                            self.button_Q, self.button_R, self.button_S, self.button_T,
                            self.button_U, self.button_V, self.button_W, self.button_Z]

        # Hide input colors
        self.hideInputColors()

        # Button in input steps
        self.pushButton_F = QtWidgets.QPushButton(self.groupBox_1, text='F')
        self.pushButton_F.setGeometry(QtCore.QRect(35, heightBox_1 * 0.2, 32, 32))
        self.pushButton_F.setStyleSheet(styleButton)
        self.pushButton_F.setFlat(False)
        self.pushButton_F.setObjectName('pushButton_F')
        self.pushButton_F.clicked.connect(lambda: self.inputStr('F'))

        self.pushButton_Fi = QtWidgets.QPushButton(self.groupBox_1, text='F\'')
        self.pushButton_Fi.setGeometry(QtCore.QRect(80, heightBox_1 * 0.2, 32, 32))
        self.pushButton_Fi.setStyleSheet(styleButton)
        self.pushButton_Fi.setFlat(False)
        self.pushButton_Fi.setObjectName('pushButton_Fi')
        self.pushButton_Fi.clicked.connect(lambda: self.inputStr('F\''))

        self.pushButton_B = QtWidgets.QPushButton(self.groupBox_1, text='B')
        self.pushButton_B.setGeometry(QtCore.QRect(125, heightBox_1 * 0.2, 32, 32))
        self.pushButton_B.setStyleSheet(styleButton)
        self.pushButton_B.setFlat(False)
        self.pushButton_B.setObjectName('pushButton_B')
        self.pushButton_B.clicked.connect(lambda: self.inputStr('B'))

        self.pushButton_Bi = QtWidgets.QPushButton(self.groupBox_1, text='B\'')
        self.pushButton_Bi.setGeometry(QtCore.QRect(170, heightBox_1 * 0.2, 32, 32))
        self.pushButton_Bi.setStyleSheet(styleButton)
        self.pushButton_Bi.setFlat(False)
        self.pushButton_Bi.setObjectName('pushButton_Bi')
        self.pushButton_Bi.clicked.connect(lambda: self.inputStr('B\''))

        self.pushButton_L = QtWidgets.QPushButton(self.groupBox_1, text='L')
        self.pushButton_L.setGeometry(QtCore.QRect(215, heightBox_1 * 0.2, 32, 32))
        self.pushButton_L.setStyleSheet(styleButton)
        self.pushButton_L.setFlat(False)
        self.pushButton_L.setObjectName('pushButton_L')
        self.pushButton_L.clicked.connect(lambda: self.inputStr('L'))

        self.pushButton_Li = QtWidgets.QPushButton(self.groupBox_1, text='L\'')
        self.pushButton_Li.setGeometry(QtCore.QRect(260, heightBox_1 * 0.2, 32, 32))
        self.pushButton_Li.setStyleSheet(styleButton)
        self.pushButton_Li.setFlat(False)
        self.pushButton_Li.setObjectName('pushButton_Li')
        self.pushButton_Li.clicked.connect(lambda: self.inputStr('L\''))

        self.pushButton_R = QtWidgets.QPushButton(self.groupBox_1, text='R')
        self.pushButton_R.setGeometry(QtCore.QRect(305, heightBox_1 * 0.2, 32, 32))
        self.pushButton_R.setStyleSheet(styleButton)
        self.pushButton_R.setFlat(False)
        self.pushButton_R.setObjectName('pushButton_R')
        self.pushButton_R.clicked.connect(lambda: self.inputStr('R'))

        self.pushButton_Ri = QtWidgets.QPushButton(self.groupBox_1, text='R\'')
        self.pushButton_Ri.setGeometry(QtCore.QRect(350, heightBox_1 * 0.2, 32, 32))
        self.pushButton_Ri.setStyleSheet(styleButton)
        self.pushButton_Ri.setFlat(False)
        self.pushButton_Ri.setObjectName('pushButton_Ri')
        self.pushButton_Ri.clicked.connect(lambda: self.inputStr('R\''))

        self.pushButton_U = QtWidgets.QPushButton(self.groupBox_1, text='U')
        self.pushButton_U.setGeometry(QtCore.QRect(395, heightBox_1 * 0.2, 32, 32))
        self.pushButton_U.setStyleSheet(styleButton)
        self.pushButton_U.setFlat(False)
        self.pushButton_U.setObjectName('pushButton_U')
        self.pushButton_U.clicked.connect(lambda: self.inputStr('U'))

        self.pushButton_Ui = QtWidgets.QPushButton(self.groupBox_1, text='U\'')
        self.pushButton_Ui.setGeometry(QtCore.QRect(440, heightBox_1 * 0.2, 32, 32))
        self.pushButton_Ui.setStyleSheet(styleButton)
        self.pushButton_Ui.setFlat(False)
        self.pushButton_Ui.setObjectName('pushButton_Ui')
        self.pushButton_Ui.clicked.connect(lambda: self.inputStr('U\''))

        self.pushButton_D = QtWidgets.QPushButton(self.groupBox_1, text='D')
        self.pushButton_D.setGeometry(QtCore.QRect(485, heightBox_1 * 0.2, 32, 32))
        self.pushButton_D.setStyleSheet(styleButton)
        self.pushButton_D.setFlat(False)
        self.pushButton_D.setObjectName('pushButton_D')
        self.pushButton_D.clicked.connect(lambda: self.inputStr('D'))

        self.pushButton_Di = QtWidgets.QPushButton(self.groupBox_1, text='D\'')
        self.pushButton_Di.setGeometry(QtCore.QRect(530, heightBox_1 * 0.2, 30, 32))
        self.pushButton_Di.setStyleSheet(styleButton)
        self.pushButton_Di.setFlat(False)
        self.pushButton_Di.setObjectName('pushButton_Di')
        self.pushButton_Di.clicked.connect(lambda: self.inputStr('D\''))

        # Add buttons to list
        self.listStepButton = [self.pushButton_B, self.pushButton_Bi, self.pushButton_D,
                                self.pushButton_Di, self.pushButton_F, self.pushButton_Fi,
                                self.pushButton_L, self.pushButton_Li, self.pushButton_R,
                                self.pushButton_Ri, self.pushButton_U, self.pushButton_Ui]

        # Text box in input steps
        self.textBox = QtWidgets.QTextEdit(self.groupBox_1)
        self.textBox.setGeometry(QtCore.QRect(30, heightBox_1 * 0.3, widthBox_1 * 0.9, heightBox_1 * 0.5))
        self.textBox.setStyleSheet('background-color: rgb(255, 255, 255);\n'
                                    'border-radius: 10px;')
        self.textBox.textChanged.connect(self.handleStrChange)
        font = QtGui.QFont()
        font.setFamily('Apple SD Gothic Neo')
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(50)
        font.setPointSize(20)
        self.textBox.setFont(font)
        self.textBox.setObjectName('Text Box')
        
        # Hide input steps
        self.hideInputSteps()

        # Group 2: Rubik

        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(width * 0.5 + 30, 50, width * 0.45, height * 0.6))
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
        widthBox_2 = self.groupBox_2.frameGeometry().width()
        heightBox_2 = self.groupBox_2.frameGeometry().height()

        self.frame = QtWidgets.QFrame(self.groupBox_2)
        self.frame.setGeometry(QtCore.QRect(40, 40, widthBox_2 * 0.85, heightBox_2 * 0.8))
        self.frame.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName('frame')

        self.myMplCanvas = my3DCanvas(self.cube, self.frame, width=4.5, height=4.5)

        self.horizontalSlider = QtWidgets.QSlider(self.groupBox_2)
        self.horizontalSlider.setGeometry(QtCore.QRect(40, 40 + heightBox_2 * 0.8, widthBox_2 * 0.9, 22))
        self.horizontalSlider.setRange(0, np.pi*20)
        self.horizontalSlider.setValue(0)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setInvertedAppearance(False)
        self.horizontalSlider.setInvertedControls(False)
        self.horizontalSlider.setObjectName('horizontalSlider')
        self.horizontalSlider.valueChanged.connect(self.rotateCube)

        self.verticalSlider = QtWidgets.QSlider(self.groupBox_2)
        self.verticalSlider.setGeometry(QtCore.QRect(15 + widthBox_2 * 0.9, 40, 22, heightBox_2 * 0.8))
        self.verticalSlider.setRange(0, np.pi*20)
        self.verticalSlider.setValue(0)
        self.verticalSlider.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider.setObjectName('verticalSlider')
        self.verticalSlider.valueChanged.connect(self.rotateCube)

        self.verticalSlider_2 = QtWidgets.QSlider(self.groupBox_2)
        self.verticalSlider_2.setGeometry(QtCore.QRect(15, 40, 22, heightBox_2 * 0.8))
        self.verticalSlider_2.setRange(0, np.pi*20)
        self.verticalSlider_2.setValue(0)
        self.verticalSlider_2.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_2.setObjectName('verticalSlider')
        self.verticalSlider_2.valueChanged.connect(self.rotateCube)

        # Group 3: Solution

        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(30, height * 0.6 + 50, width * 0.95, height * 0.32))
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
        widthBox_3 = self.groupBox_3.frameGeometry().width()
        heightBox_3 = self.groupBox_3.frameGeometry().height()

        self.scrollArea = QtWidgets.QScrollArea(self.groupBox_3)
        self.scrollArea.setGeometry(QtCore.QRect(30, 30, widthBox_3 * 0.95, heightBox_3 * 0.7))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName('scrollArea')
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, widthBox_3 * 0.95, heightBox_3 * 0.7))
        self.scrollAreaWidgetContents.setObjectName('scrollAreaWidgetContents')
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.my2DCanvas = my2DCanvas(
                                parent=self.scrollAreaWidgetContents,
                                width=11,
                                height=1.5)

        self.nextButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents, text='Next Step')
        self.nextButton.setGeometry(QtCore.QRect(widthBox_3 * 0.8, heightBox_3 * 0.55, 113, 32))
        self.nextButton.clicked.connect(self.nextStep)
        self.nextButton.setStyleSheet(styleButton)
        self.nextButton.setObjectName('Next Step')

        styleStepButton = 'border-radius: 10px; \
                        background-color: rgb(255, 0, 0);' 

        self.step_1 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.step_1.setGeometry(QtCore.QRect(140, heightBox_3 * 0.45, 57, 5))
        self.step_1.setStyleSheet(styleStepButton)
        self.step_1.setObjectName('Step 1')

        self.step_2 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.step_2.setGeometry(QtCore.QRect(201, heightBox_3 * 0.45, 57, 5))
        self.step_2.setStyleSheet(styleStepButton)
        self.step_2.setObjectName('Step 2')

        self.step_3 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.step_3.setGeometry(QtCore.QRect(262, heightBox_3 * 0.45, 57, 5))
        self.step_3.setStyleSheet(styleStepButton)
        self.step_3.setObjectName('Step 3')

        self.step_4 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.step_4.setGeometry(QtCore.QRect(323, heightBox_3 * 0.45, 57, 5))
        self.step_4.setStyleSheet(styleStepButton)
        self.step_4.setObjectName('Step 4')

        self.step_5 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.step_5.setGeometry(QtCore.QRect(384, heightBox_3 * 0.45, 57, 5))
        self.step_5.setStyleSheet(styleStepButton)
        self.step_5.setObjectName('Step 5')

        self.step_6 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.step_6.setGeometry(QtCore.QRect(445, heightBox_3 * 0.45, 57, 5))
        self.step_6.setStyleSheet(styleStepButton)
        self.step_6.setObjectName('Step 6')

        self.step_7 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.step_7.setGeometry(QtCore.QRect(506, heightBox_3 * 0.45, 57, 5))
        self.step_7.setStyleSheet(styleStepButton)
        self.step_7.setObjectName('Step 7')

        self.step_8 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.step_8.setGeometry(QtCore.QRect(567, heightBox_3 * 0.45, 57, 5))
        self.step_8.setStyleSheet(styleStepButton)
        self.step_8.setObjectName('Step 8')

        self.step_9 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.step_9.setGeometry(QtCore.QRect(628, heightBox_3 * 0.45, 57, 5))
        self.step_9.setStyleSheet(styleStepButton)
        self.step_9.setObjectName('Step 9')

        self.step_10 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.step_10.setGeometry(QtCore.QRect(689, heightBox_3 * 0.45, 57, 5))
        self.step_10.setStyleSheet(styleStepButton)
        self.step_10.setObjectName('Step 10')

        self.step_11 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.step_11.setGeometry(QtCore.QRect(750, heightBox_3 * 0.45, 57, 5))
        self.step_11.setStyleSheet(styleStepButton)
        self.step_11.setObjectName('Step 11')

        self.step_12 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.step_12.setGeometry(QtCore.QRect(811, heightBox_3 * 0.45, 57, 5))
        self.step_12.setStyleSheet(styleStepButton)
        self.step_12.setObjectName('Step 12')

        self.listNextStepButton = [self.step_1, self.step_2, self.step_3, self.step_4,
                                    self.step_5, self.step_6, self.step_7, self.step_8,
                                    self.step_9, self.step_10, self.step_11, self.step_12]

        self.groupBox_statistic = QtWidgets.QGroupBox(self.groupBox_3)
        self.groupBox_statistic.setGeometry(QtCore.QRect(30, heightBox_3 * 0.6 + 30, widthBox_3 * 0.5, heightBox_3 * 0.2))
        font = QtGui.QFont()
        font.setFamily('Apple SD Gothic Neo')
        font.setWeight(75)
        self.groupBox_statistic.setFont(font)
        self.groupBox_statistic.setStyleSheet(  'background-color: rgb(170, 255, 255);\n'
                                        'border-radius: 10px;')
        self.groupBox_statistic.setFlat(True)
        self.groupBox_statistic.setObjectName('groupBox_statistic')
        self.label = QtWidgets.QLabel(self.groupBox_statistic)
        self.label.setGeometry(QtCore.QRect(10, 0, widthBox_3 * 0.5 - 10, heightBox_3 * 0.2))
        self.label.setObjectName('Label')


        self.cube.rotate(1.5, 0, 0)

        #FIXME: NameProject - Title
        self.NameProject = QtWidgets.QLabel(self.centralwidget)
        self.NameProject.setGeometry(QtCore.QRect(width * 0.35, 0, width * 0.3, height * 0.05))
        font = QtGui.QFont()
        font.setFamily("Apple SD Gothic Neo")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.NameProject.setFont(font)
        self.NameProject.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.NameProject.setAutoFillBackground(False)
        self.NameProject.setStyleSheet("color: rgb(255, 0, 0);")
        self.NameProject.setTextFormat(QtCore.Qt.RichText)
        self.NameProject.setAlignment(QtCore.Qt.AlignCenter)
        self.NameProject.setObjectName("NameProject")

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName('statusbar')
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.reset()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate('MainWindow', 'MainWindow'))
        self.groupBox_1.setTitle(_translate('MainWindow', 'Configuration'))
        self.groupBox_2.setTitle(_translate('MainWindow', 'Visualization'))
        self.groupBox_3.setTitle(_translate('MainWindow', 'Solution'))
        self.NameProject.setText(_translate("MainWindow", "Rubic\'s Cube Solver"))

    def rotateCube(self):
        yaw = self.horizontalSlider.value()/10
        pitch = self.verticalSlider.value()/10
        roll = self.verticalSlider_2.value()/10
        self.cube.rotate(yaw, pitch, roll)
        self.myMplCanvas.updateMpl(self.cube)

    def reset(self):
        self.cube.resetFace()
        self.myMplCanvas.updateMpl(self.cube)
        self.my2DCanvas.textOutput("")
        self.label.setText("")
        self.hideStepButton()
        self.hideInputSteps()
        self.hideInputColors()
    
    def solve(self, mode):
        textRoute = ""
        self.solution = []
        self.currentStep = 0
        self.hideStepButton()
        result = self.cube.solve(mode)
        if result is None:
            print("WRONG COLOR")
            self.label.setText("WRONG COLOR")
            self.label.setAlignment(QtCore.Qt.AlignCenter)
        goalState, self.generated, self.visited, self.time = result
        for c in goalState.route:
            if c.islower():
                textRoute += c.upper() + '\''
            else:
                textRoute += c
            textRoute += ' '
            self.solution.append(c)
        self.label.setText("Number of generated states: " + str(self.generated) + "\n" +
                        "Number of visited states: " + str(self.visited) + "\n" +
                        "Time: " + str(round(self.time, 4)) + " s")
        self.my2DCanvas.updateMpl(self.solution)
        self.myMplCanvas.updateMpl(self.cube)

    def randomFace(self):
        self.cube.randomFace()
        self.myMplCanvas.updateMpl(self.cube)

    def nextStep(self):
        if self.currentStep < len(self.solution):
            self.cube.nextStep(self.solution[self.currentStep])
            self.nextStepButton(self.currentStep)
            self.currentStep += 1
            self.myMplCanvas.updateMpl(self.cube)

    def loadInputColor(self):
        if (not self.cube.loadColor(self.posColor)):
            self.alert = QtWidgets.QMessageBox.critical(QtWidgets.QMainWindow(), "Alert", "You chose wrong colors!",
                                                        buttons=QtWidgets.QMessageBox.Ok)
        self.myMplCanvas.updateMpl(self.cube)

    #TODO: Add Color 2D Rubik
    def applyColor(self, button_pos, x, y):
        if self.orangeButton.isChecked():
            button_pos.setStyleSheet("background-color: rgb(255, 170, 0);"
            "border-style: solid;\n"
            "border-radius: 0px;\n"
            "border-width: 1px;\n"
            "border-color: black;")
            self.posColor[x][y] = 'o'
        elif self.yellowButton.isChecked():
            button_pos.setStyleSheet("background-color: rgb(255, 255, 0);"
            "border-style: solid;\n"
            "border-radius: 0px;\n"
            "border-width: 1px;\n"
            "border-color: black;")
            self.posColor[x][y] = 'y'
        elif self.redButton.isChecked():
            button_pos.setStyleSheet("background-color: rgb(255, 0, 0);"
            "border-style: solid;\n"
            "border-radius: 0px;\n"
            "border-width: 1px;\n"
            "border-color: black;")
            self.posColor[x][y] = 'r'
        elif self.blueButton.isChecked():
            button_pos.setStyleSheet("background-color: rgb(0, 85, 255);"
            "border-style: solid;\n"
            "border-radius: 0px;\n"
            "border-width: 1px;\n"
            "border-color: black;")
            self.posColor[x][y] = 'b'
        elif self.greenButton.isChecked():
            button_pos.setStyleSheet("background-color: rgb(0, 170, 0);"
            "border-style: solid;\n"
            "border-radius: 0px;\n"
            "border-width: 1px;\n"
            "border-color: black;")
            self.posColor[x][y] = 'g'
        elif self.whiteButton.isChecked():
            button_pos.setStyleSheet("background-color: rgb(255, 255, 255);"
            "border-style: solid;\n"
            "border-radius: 0px;\n"
            "border-width: 1px;\n"
            "border-color: black;")
            self.posColor[x][y] = 'w'
        else:
            print('Not Found')

    def nextStepButton(self, mode):
        if mode == 0:
            self.step_1.show()
        elif mode == 1:
            self.step_2.show()
        elif mode == 2:
            self.step_3.show()
        elif mode == 3:
            self.step_4.show()
        elif mode == 4:
            self.step_5.show()
        elif mode == 5:
            self.step_6.show()
        elif mode == 6:
            self.step_7.show()
        elif mode == 7:
            self.step_8.show()
        elif mode == 8:
            self.step_9.show()
        elif mode == 9:
            self.step_10.show()
        elif mode == 10:
            self.step_11.show()
        else:
            self.step_12.show()

    def hideStepButton(self):
        for button in self.listNextStepButton:
            button.hide()

    def setDefaultInputColors(self):
        for button in self.listRubikButton:
            button.setStyleSheet("background-color: rgb(255, 255, 255);"
                                "border-style: solid;\n"
                                "border-radius: 0px;\n"
                                "border-width: 1px;\n"
                                "border-color: black;")
            button.setText("")
        self.whiteButton.setChecked(True)
        self.posColor = [['w' for i in range(3)] for j in range(8)]
    
    def setDefaultInputSteps(self):
        self.textBox.setText("")

    def inputStr(self, char):
        self.textBox.setText(self.textBox.toPlainText() + char)
    
    def handleStrChange(self):
        def removeRedundantCharacters(str):
            result = ""
            flag = False
            for c in str[::-1]:
                if c == '\'': flag = True
                elif c in 'UDFBRLudfbrl':
                    result += ('\'' if flag else '') + c.upper()
                    flag = False
            return result[::-1]

        def translateStr(str: str):
            result = ""
            i = len(str) - 1
            while i >= 0:
                if str[i] == '\'':
                    i -= 1
                    result += str[i].lower()
                else:
                    result += str[i]
                i -= 1
            return result[::-1]

        text = self.textBox.toPlainText()
        reduce = removeRedundantCharacters(text)
        if text != reduce:
            self.textBox.setText(reduce)
            self.textBox.moveCursor(QtGui.QTextCursor.End)

        self.cube.moveByStep(translateStr(self.textBox.toPlainText()))
        self.myMplCanvas.updateMpl(self.cube)

    def showInputColors(self):
        self.groupBox_choosecolor.show()
        self.rubik_2D.show()

    def hideInputColors(self):
        self.groupBox_choosecolor.hide()
        self.rubik_2D.hide()

    def showInputSteps(self):
        for button in self.listStepButton:
            button.show()
        self.textBox.show()

    def hideInputSteps(self):
        for button in self.listStepButton:
            button.hide()
        self.textBox.hide()    
    
    def showInput(self, mode):
        if (mode == 0):
            self.hideInputSteps()
            self.setDefaultInputColors()
            self.showInputColors()
        else:
            self.hideInputColors()
            self.setDefaultInputSteps()
            self.showInputSteps()