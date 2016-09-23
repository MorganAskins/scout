from PyQt4 import QtCore, QtGui
import sys, os
import time
import copy
from duepulser.duepulser_comms import PulserCommunication


class pulser_tab(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        fbox = pulser_form()
        self.setLayout(fbox)

class pulser_form(QtGui.QFormLayout):
    def __init__(self):
        QtGui.QFormLayout.__init__(self)
        self.duepulser = PulserCommunication()
        self.__build_form__()

    def __build_form__(self):
        # Find serial button
        self.find_serial_bt = QtGui.QPushButton("Find Arduino")
        self.find_serial_bt.clicked.connect(self.__find_serial__)
        self.serialname = QtGui.QLineEdit()
        self.serialname.setReadOnly(True)
        self.addRow(self.find_serial_bt, self.serialname)
        # Serial connect button
        self.connect_serial_bt = QtGui.QPushButton("Connect")
        self.connect_serial_bt.clicked.connect(self.__connect__)
        self.connectstatus = QtGui.QLineEdit()
        self.connectstatus.setReadOnly(True)
        self.addRow(self.connect_serial_bt, self.connectstatus)
        # Set Frequency
        self.set_freq_bt = QtGui.QPushButton("Set Frequency")
        self.set_freq_bt.clicked.connect(self.__set_frequency__)
        self.freqvalue = QtGui.QLineEdit()
        self.addRow(self.set_freq_bt, self.freqvalue)
        # Set Cycles
        self.set_cycle_bt = QtGui.QPushButton("Set Cycles")
        self.set_cycle_bt.clicked.connect(self.__set_cycles__)
        self.cyclevalue = QtGui.QLineEdit()
        self.addRow(self.set_cycle_bt, self.cyclevalue)
        # On button / Off button
        self.on_bt = QtGui.QPushButton("Pulser ON")
        self.on_bt.clicked.connect(self.__pulser_on__)
        self.off_bt = QtGui.QPushButton("Pulser OFF")
        self.off_bt.clicked.connect(self.__pulser_off__)
        self.addRow(self.on_bt, self.off_bt)

    def __find_serial__(self):
        self.duepulser.findSerial()
        self.serialname.setText(str(self.duepulser.port))

    def __connect__(self):
        self.ret = self.duepulser.connectSerial()
        self.connectstatus.setText(str(self.duepulser.connected))

    def __set_frequency__(self):
        freq = int(self.freqvalue.text())
        self.ret = self.duepulser.setFrequency(freq)
        self.status_update()

    def __set_cycles__(self):
        cycles = int(self.cyclevalue.text())
        self.ret = self.duepulser.setCycles(cycles)
        self.status_update()

    def __pulser_on__(self):
        self.ret = self.duepulser.pulserOn()
        self.status_update()

    def __pulser_off__(self):
        self.ret = self.duepulser.pulserOff()
        self.status_update()

    def status_update(self):
        self.connectstatus.setText(str(self.ret))
