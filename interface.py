from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import pyqtgraph as pg
import random
import threading
import time
import sqlite3

lst_ac_x = [0] * 100
lst_ac_y = [0] * 100
lst_ac_z = [0] * 100

lst_tt = [0] * 100
lst_vel_z = [0] * 100

lst_pos_x = [0] * 100
lst_pos_y = [0] * 100
lst_pos_z = [0] * 100

lst_rot = [0] * 100
lst_temp = [0] * 100

ac_max = 400
tt_max = 50
vel_max = 360
rot_max = 360
temp_max = 360
pos_max = 1000

def data_simulator_ac(signal_ac):
    global lst_ac_z
    random.seed(time.time())
    while (True):
        lst_ac_z= lst_ac_z[1:] + [random.randint(1, ac_max)]
        signal_ac.emit()
        time.sleep(0.75)


def data_simulator_rot(signal_rot):
    global lst_rot
    random.seed(time.time())
    while (True):
        lst_rot = lst_rot[1:] + [random.randint(1, rot_max)]
        signal_rot.emit()
        time.sleep(0.33)


def data_simulator_vel(signal_vel):
    global lst_vel_z
    random.seed(time.time())
    while (True):
        lst_vel_z = lst_vel_z[1:] + [random.randint(1, vel_max)]
        signal_vel.emit()
        time.sleep(0.47)


def data_simulator_tt(signal_tt):
    global lst_tt
    random.seed(time.time())
    while (True):
        lst_tt = lst_tt[1:] + [random.randint(1, tt_max)]
        signal_tt.emit()
        time.sleep(0.71)


def data_simulator_pos(signal_pos):
    global lst_pos_x, lst_pos_y, lst_pos_z
    count_old, count_new = 0, 0
    conn = sqlite3.connect('dados_cube.db')
    c = conn.cursor()
    while (True):
        rows = c.execute("SELECT COUNT(*) FROM posicao")
        aux = c.fetchall()
        count_new = aux[0][0]
        if count_new > count_old:
            rows = c.execute("SELECT * FROM posicao")
            data = c.fetchall()[-1]
            lst_pos_z = lst_pos_z[1:] + [data[2]]
            signal_pos.emit()
            count_old = count_new
    conn.close()

def data_simulator_temp(signal_temp):
    global lst_temp
    random.seed(time.time())
    while (True):
        lst_temp = lst_temp[1:] + [random.randint(1, temp_max)]
        signal_temp.emit()
        time.sleep(1.5)

class Ui_TabWidget(QtCore.QObject):

    ac_signal = QtCore.pyqtSignal()
    rot_signal = QtCore.pyqtSignal()
    vel_signal = QtCore.pyqtSignal()
    tt_signal = QtCore.pyqtSignal()
    pos_signal = QtCore.pyqtSignal()
    temp_signal = QtCore.pyqtSignal()

    def setupUi(self, TabWidget):
        TabWidget.setObjectName("TabWidget")
        TabWidget.setEnabled(True)
        TabWidget.resize(1278, 587)
        font = QtGui.QFont()
        font.setFamily("Arial")
        TabWidget.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("asabranca.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        TabWidget.setWindowIcon(icon)
        TabWidget.setUsesScrollButtons(False)
        TabWidget.setTabBarAutoHide(True)
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

        self.ac_signal.connect(self.Ac_signal)
        self.rot_signal.connect(self.Rot_signal)
        self.vel_signal.connect(self.Vel_signal)
        self.tt_signal.connect(self.TT_signal)
        self.pos_signal.connect(self.Pos_signal)
        self.temp_signal.connect(self.Temp_signal)

        #Aba Principal
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")

        self.gridLayout = QtWidgets.QGridLayout(self.tab)
        self.gridLayout.setObjectName("gridLayout")

        self.graphicsView_pac = pg.PlotWidget(self.tab)
        self.graphicsView_pac.setObjectName("graphicsView_pac")
        self.gridLayout.addWidget(self.graphicsView_pac, 0, 0, 1, 1)

        self.graphicsView_prot = pg.PlotWidget(self.tab)
        self.graphicsView_prot.setObjectName("graphicsView_prot")
        self.gridLayout.addWidget(self.graphicsView_prot, 0, 1, 1, 1)

        self.graphicsView_ptt = pg.PlotWidget(self.tab)
        self.graphicsView_ptt.setObjectName("graphicsView_ptt")
        self.gridLayout.addWidget(self.graphicsView_ptt, 1, 0, 1, 1)

        self.graphicsView_pvel = pg.PlotWidget(self.tab)
        self.graphicsView_pvel.setObjectName("graphicsView_pvel")
        self.gridLayout.addWidget(self.graphicsView_pvel, 1, 1, 1, 1)

        self.line = QtWidgets.QFrame(self.tab)
        self.line.setMinimumSize(QtCore.QSize(0, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 2, 0, 1, 2)

        self.label_ppos = QtWidgets.QLabel(self.tab)
        self.label_ppos.setObjectName("label_ppos")
        self.gridLayout.addWidget(self.label_ppos, 3, 0, 1, 1)
        self.label_ptemp = QtWidgets.QLabel(self.tab)
        self.label_ptemp.setObjectName("label_ptemp")
        self.gridLayout.addWidget(self.label_ptemp, 3, 1, 1, 1)
        self.label_prot = QtWidgets.QLabel(self.tab)
        self.label_prot.setObjectName("label_prot")
        self.gridLayout.addWidget(self.label_prot, 4, 0, 1, 1)
        self.label_pac = QtWidgets.QLabel(self.tab)
        self.label_pac.setObjectName("label_pac")
        self.gridLayout.addWidget(self.label_pac, 4, 1, 1, 1)
        self.label_ptt = QtWidgets.QLabel(self.tab)
        self.label_ptt.setObjectName("label_ptt")
        self.gridLayout.addWidget(self.label_ptt, 5, 0, 1, 1)
        self.label_pvel = QtWidgets.QLabel(self.tab)
        self.label_pvel.setObjectName("label_pvel")
        self.gridLayout.addWidget(self.label_pvel, 5, 1, 1, 1)

        self.line_2 = QtWidgets.QFrame(self.tab)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout.addWidget(self.line_2, 6, 0, 1, 2)
        TabWidget.addTab(self.tab, "")

        #Aba Temperatura
        self.tab1 = QtWidgets.QWidget()
        self.tab1.setObjectName("tab1")

        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab1)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.graphicsView_temp = pg.PlotWidget(self.tab1)
        self.graphicsView_temp.setObjectName("graphicsView_temp")
        self.gridLayout_2.addWidget(self.graphicsView_temp, 0, 0, 1, 1)

        self.line_3 = QtWidgets.QFrame(self.tab1)
        self.line_3.setMinimumSize(QtCore.QSize(0, 16))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.gridLayout_2.addWidget(self.line_3, 1, 0, 1, 1)

        self.label_temp = QtWidgets.QLabel(self.tab1)
        self.label_temp.setObjectName("label_temp")
        self.gridLayout_2.addWidget(self.label_temp, 2, 0, 1, 1)
        TabWidget.addTab(self.tab1, "")

        #Aba Aceleração
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")

        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_3.setObjectName("gridLayout_3")

        self.graphicsView_ac = pg.PlotWidget(self.tab_2)
        self.graphicsView_ac.setObjectName("graphicsView_ac")
        self.gridLayout_3.addWidget(self.graphicsView_ac, 0, 0, 1, 1)

        self.line_4 = QtWidgets.QFrame(self.tab_2)
        self.line_4.setMinimumSize(QtCore.QSize(0, 16))
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.gridLayout_3.addWidget(self.line_4, 1, 0, 1, 1)

        self.label_ac = QtWidgets.QLabel(self.tab_2)
        self.label_ac.setObjectName("label_ac")
        self.gridLayout_3.addWidget(self.label_ac, 2, 0, 1, 1)
        TabWidget.addTab(self.tab_2, "")

        #Aba Velocidade
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")

        self.gridLayout_4 = QtWidgets.QGridLayout(self.tab_3)
        self.gridLayout_4.setObjectName("gridLayout_4")

        self.graphicsView_vel = pg.PlotWidget(self.tab_3)
        self.graphicsView_vel.setObjectName("graphicsView_vel")
        self.gridLayout_4.addWidget(self.graphicsView_vel, 0, 0, 1, 1)

        self.line_5 = QtWidgets.QFrame(self.tab_3)
        self.line_5.setMinimumSize(QtCore.QSize(0, 16))
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.gridLayout_4.addWidget(self.line_5, 1, 0, 1, 1)

        self.label_vel = QtWidgets.QLabel(self.tab_3)
        self.label_vel.setObjectName("label_vel")
        self.gridLayout_4.addWidget(self.label_vel, 2, 0, 1, 1)
        TabWidget.addTab(self.tab_3, "")

        #Aba Rotação
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")

        self.gridLayout_5 = QtWidgets.QGridLayout(self.tab_4)
        self.gridLayout_5.setObjectName("gridLayout_5")

        self.graphicsView_rot = pg.PlotWidget(self.tab_4)
        self.graphicsView_rot.setObjectName("graphicsView_rot")
        self.gridLayout_5.addWidget(self.graphicsView_rot, 0, 0, 1, 1)

        self.line_6 = QtWidgets.QFrame(self.tab_4)
        self.line_6.setMinimumSize(QtCore.QSize(0, 16))
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.gridLayout_5.addWidget(self.line_6, 1, 0, 1, 1)

        self.label_rot = QtWidgets.QLabel(self.tab_4)
        self.label_rot.setObjectName("label_rot")
        self.gridLayout_5.addWidget(self.label_rot, 2, 0, 1, 1)
        TabWidget.addTab(self.tab_4, "")

        #Aba Posição
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")

        self.gridLayout_6 = QtWidgets.QGridLayout(self.tab_5)
        self.gridLayout_6.setObjectName("gridLayout_6")

        self.graphicsView_pos = pg.PlotWidget(self.tab_5)
        self.graphicsView_pos.setObjectName("graphicsView_pos")
        self.gridLayout_6.addWidget(self.graphicsView_pos, 0, 0, 1, 1)

        self.line_7 = QtWidgets.QFrame(self.tab_5)
        self.line_7.setMinimumSize(QtCore.QSize(0, 16))
        self.line_7.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.gridLayout_6.addWidget(self.line_7, 1, 0, 1, 1)

        self.label_pos = QtWidgets.QLabel(self.tab_5)
        self.label_pos.setObjectName("label_pos")
        self.gridLayout_6.addWidget(self.label_pos, 2, 0, 1, 1)
        TabWidget.addTab(self.tab_5, "")

        #Aba Taxa de Transmissão
        self.tab_6 = QtWidgets.QWidget()
        self.tab_6.setObjectName("tab_6")

        self.gridLayout_7 = QtWidgets.QGridLayout(self.tab_6)
        self.gridLayout_7.setObjectName("gridLayout_7")

        self.graphicsView_tt = pg.PlotWidget(self.tab_6)
        self.graphicsView_tt.setObjectName("graphicsView_tt")
        self.gridLayout_7.addWidget(self.graphicsView_tt, 0, 0, 1, 1)

        self.line_8 = QtWidgets.QFrame(self.tab_6)
        self.line_8.setMinimumSize(QtCore.QSize(0, 16))
        self.line_8.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_8.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_8.setObjectName("line_8")
        self.gridLayout_7.addWidget(self.line_8, 1, 0, 1, 1)

        self.label_tt = QtWidgets.QLabel(self.tab_6)
        self.label_tt.setObjectName("label_tt")
        self.gridLayout_7.addWidget(self.label_tt, 2, 0, 1, 1)
        TabWidget.addTab(self.tab_6, "")

        #Aba Mapa
        self.tab_7 = QtWidgets.QWidget()
        self.tab_7.setObjectName("tab_7")

        self.gridLayout_8 = QtWidgets.QGridLayout(self.tab_7)
        self.gridLayout_8.setObjectName("gridLayout_8")

        self.line_9 = QtWidgets.QFrame(self.tab_7)
        self.line_9.setMinimumSize(QtCore.QSize(0, 16))
        self.line_9.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_9.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_9.setObjectName("line_9")
        self.gridLayout_8.addWidget(self.line_9, 1, 0, 1, 2)

        self.label_lat = QtWidgets.QLabel(self.tab_7)
        self.label_lat.setObjectName("label_lat")
        self.gridLayout_8.addWidget(self.label_lat, 2, 0, 1, 1)

        self.graphicsView_11 = QtWidgets.QGraphicsView(self.tab_7)
        self.graphicsView_11.setObjectName("graphicsView_11")
        self.gridLayout_8.addWidget(self.graphicsView_11, 0, 0, 1, 1)

        self.label_long = QtWidgets.QLabel(self.tab_7)
        self.label_long.setObjectName("label_long")
        self.gridLayout_8.addWidget(self.label_long, 3, 0, 1, 1)
        TabWidget.addTab(self.tab_7, "")

        self.retranslateUi(TabWidget)
        TabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(TabWidget)

    def retranslateUi(self, TabWidget):
        _translate = QtCore.QCoreApplication.translate
        TabWidget.setWindowTitle(_translate("TabWidget", "Interface Gráfica"))
        TabWidget.setTabText(TabWidget.indexOf(self.tab), _translate("TabWidget", "Principal"))
        TabWidget.setTabText(TabWidget.indexOf(self.tab1), _translate("TabWidget", "Temperatura"))
        TabWidget.setTabText(TabWidget.indexOf(self.tab_2), _translate("TabWidget", "Aceleração"))
        TabWidget.setTabText(TabWidget.indexOf(self.tab_3), _translate("TabWidget", "Velocidade"))
        TabWidget.setTabText(TabWidget.indexOf(self.tab_4), _translate("TabWidget", "Rotação"))
        TabWidget.setTabText(TabWidget.indexOf(self.tab_5), _translate("TabWidget", "Posição"))
        TabWidget.setTabText(TabWidget.indexOf(self.tab_6), _translate("TabWidget", "Taxa de Transmissão"))
        self.label_lat.setText(_translate("TabWidget", "Latitude"))
        self.label_long.setText(_translate("TabWidget", "Longitude"))
        TabWidget.setTabText(TabWidget.indexOf(self.tab_7), _translate("TabWidget", "Mapa"))

    def Ac_signal(self):
        self.label_pac.setText("Aceleração: " + str(lst_ac_z[-1]) + " m/s²")
        self.label_ac.setText("Aceleração: " + str(lst_ac_z[-1]) + " m/s²")

        self.graphicsView_pac.clear()
        self.graphicsView_pac.plot(lst_ac_z, pen='r')
        self.graphicsView_pac.showGrid(x=True, y=True)
        self.graphicsView_pac.setLabel('left', 'Aceleração', units='m/s²')
        self.graphicsView_pac.setLabel('bottom', 'Tempo', units='s')

        self.graphicsView_ac.clear()
        self.graphicsView_ac.plot(lst_ac_z, pen='r')
        self.graphicsView_ac.showGrid(x=True, y=True)
        self.graphicsView_ac.setLabel('left', 'Aceleração', units='m/s²')
        self.graphicsView_ac.setLabel('bottom', 'Tempo', units='s')

    def Rot_signal(self):
        self.label_prot.setText("Rotação: " + str(lst_rot[-1]) + " rad/s")
        self.label_rot.setText("Rotação: " + str(lst_rot[-1]) + " rad/s")

        self.graphicsView_prot.clear()
        self.graphicsView_prot.plot(lst_rot, pen='r')
        self.graphicsView_prot.showGrid(x=True, y=True)
        self.graphicsView_prot.setLabel('left', 'Rotação', units='rad/s')
        self.graphicsView_prot.setLabel('bottom', 'Tempo', units='s')

        self.graphicsView_rot.clear()
        self.graphicsView_rot.plot(lst_rot, pen='r')
        self.graphicsView_rot.showGrid(x=True, y=True)
        self.graphicsView_rot.setLabel('left', 'Rotação', units='rad/s')
        self.graphicsView_rot.setLabel('bottom', 'Tempo', units='s')

    def Vel_signal(self):
        self.label_pvel.setText("Velocidade: " + str(lst_vel_z[-1]) + " m/s")
        self.label_vel.setText("Velocidade: " + str(lst_vel_z[-1]) + " m/s")

        self.graphicsView_pvel.clear()
        self.graphicsView_pvel.plot(lst_vel_z, pen='r')
        self.graphicsView_pvel.showGrid(x=True, y=True)
        self.graphicsView_pvel.setLabel('left', 'Velocidade', units='m/s')
        self.graphicsView_pvel.setLabel('bottom', 'Tempo', units='s')

        self.graphicsView_vel.clear()
        self.graphicsView_vel.plot(lst_vel_z, pen='r')
        self.graphicsView_vel.showGrid(x=True, y=True)
        self.graphicsView_vel.setLabel('left', 'Velocidade', units='m/s')
        self.graphicsView_vel.setLabel('bottom', 'Tempo', units='s')

    def TT_signal(self):
        self.label_ptt.setText("Taxa de Transmissão: " + str(lst_tt[-1]) + " kbps")
        self.label_tt.setText("Taxa de Transmissão: " + str(lst_tt[-1]) + " kbps")

        self.graphicsView_ptt.clear()
        self.graphicsView_ptt.plot(lst_tt, pen='r')
        self.graphicsView_ptt.showGrid(x=True, y=True)
        self.graphicsView_ptt.setLabel('left', 'Taxa de Transmissão', units='kbps/s')
        self.graphicsView_ptt.setLabel('bottom', 'Tempo', units='s')

        self.graphicsView_tt.clear()
        self.graphicsView_tt.plot(lst_tt, pen='r')
        self.graphicsView_tt.showGrid(x=True, y=True)
        self.graphicsView_tt.setLabel('left', 'Taxa de Transmissão', units='kbps/s')
        self.graphicsView_tt.setLabel('bottom', 'Tempo', units='s')

    def Pos_signal(self):
        self.label_ppos.setText("Posição: " + str(lst_pos_z[-1]) + " m")
        self.label_pos.setText("Posição: " + str(lst_pos_z[-1]) + " m")

        self.graphicsView_pos.clear()
        self.graphicsView_pos.plot(lst_pos_z, pen='r')
        self.graphicsView_pos.showGrid(x=True, y=True)
        self.graphicsView_pos.setLabel('left', 'Posição', units='m')
        self.graphicsView_pos.setLabel('bottom', 'Tempo', units='s')

    def Temp_signal(self):
        self.label_ptemp.setText("Temperatura: " + str(lst_temp[-1]) + " ºC")
        self.label_temp.setText("Temperatura: " + str(lst_temp[-1]) + " ºC")

        self.graphicsView_temp.clear()
        self.graphicsView_temp.plot(lst_temp, pen='r')
        self.graphicsView_temp.showGrid(x=True, y=True)
        self.graphicsView_temp.setLabel('left', 'temperatura', units='ºC')
        self.graphicsView_temp.setLabel('bottom', 'Tempo', units='s')

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    TabWidget = QtWidgets.QTabWidget()
    ui = Ui_TabWidget()
    ui.setupUi(TabWidget)
    TabWidget.show()

    conn = sqlite3.connect('dados_cube.db')
#    cursor = conn.cursor()

    t_temp = threading.Thread(target=data_simulator_temp, args=(ui.temp_signal,))
    t_pos = threading.Thread(target=data_simulator_pos, args=(ui.pos_signal,))
    t_rot = threading.Thread(target=data_simulator_rot, args=(ui.rot_signal,))
    t_ac = threading.Thread(target=data_simulator_ac, args=(ui.ac_signal,))
    t_tt = threading.Thread(target=data_simulator_tt, args=(ui.tt_signal,))
    t_vel = threading.Thread(target=data_simulator_vel, args=(ui.vel_signal,))


#    count_old, count_new = 0, 0


    t_temp.start()
    t_pos.start()
    t_rot.start()
    t_ac.start()
    t_tt.start()
    t_vel.start()
    
#    rows = cursor.execute("SELECT * FROM posicao")
#    while (True):
#        for x, y, z, t in rows:
#            ui.pos_signal.emit()
#            print("{}, {}, {}, {}".format(x, y, z, t))
#            time.sleep(0.2)
#    conn.close()
    sys.exit(app.exec_())
