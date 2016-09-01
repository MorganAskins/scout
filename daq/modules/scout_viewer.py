from PyQt4 import QtCore, QtGui
import sys, os, time
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_qt4agg import (
        FigureCanvasQTAgg as FigureCanvas,
        NavigationToolbar2QT as NavigationToolbar)
from matplotlib.backends import qt4_compat
use_pyside = qt4_compat.QT_API == qt4_compat.QT_API_PYSIDE
if use_pyside:
    from PySide.QtCore import *
    from PySide.QtGui import *
else:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
import ROOT as cern
from scout_run import scout

def pid_alive(pid):
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True

class viewer_tab(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.layout = QtGui.QFormLayout()
        self.__loader__()
        self.__chooser__()
        self.__plot_spot__()
        self.setLayout(self.layout)


    def __plot_spot__(self):
        self.fig = Figure((5.0, 4.0), dpi=100)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self)
        self.canvas.setFocusPolicy(Qt.StrongFocus)
        self.canvas.setFocus()

        self.mpl_toolbar = NavigationToolbar(self.canvas, self)

        self.layout.addRow(self.canvas)
        self.layout.addRow(self.mpl_toolbar)

    def __loader__(self):
        load_button = QtGui.QPushButton("Load File")
        self.fname = QtGui.QLineEdit()
        self.fname.setReadOnly(True)
        self.total_events_line = QtGui.QLineEdit("0")
        self.total_events_line.setReadOnly(True)
        load_button.clicked.connect(self.__load_file__)
        self.layout.addRow(load_button, self.fname )
        self.layout.addRow(QLabel("Total Events"), self.total_events_line)

    def __chooser__(self):
        left_button = QtGui.QPushButton("<")
        left_button.clicked.connect(self.__left_event__)
        right_button = QtGui.QPushButton(">")
        right_button.clicked.connect(self.__right_event__)
        self.event = QtGui.QLineEdit("0")
        self.event.textChanged.connect(self.__new_event__)
        self.hboxchooser = QtGui.QHBoxLayout()
        self.hboxchooser.addWidget(left_button)
        self.hboxchooser.addWidget(right_button)
        self.hboxchooser.addWidget(self.event)
        self.layout.addRow(self.hboxchooser)

    def __new_event__(self):
        min_event, max_event = 0, int(self.total_events_line.text())
        try:
            cur_event = int(self.event.text())
        except ValueError:
            self.event.setText("0")
            cur_event = int(self.event.text())
        if (cur_event >= min_event) and (cur_event < max_event):
            self.plot()
        else:
            self.event.setText("0")


    def __left_event__(self):
        min_event = 0
        cur_event = int(self.event.text())
        if cur_event > (min_event):
            cur_event -= 1
        self.event.setText(str(cur_event))

    def __right_event__(self):
        max_event = int(self.total_events_line.text())
        cur_event = int(self.event.text())
        if cur_event < (max_event-1):
            cur_event += 1
        self.event.setText(str(cur_event))

    def __load_file__(self):
        open_me = QtGui.QFileDialog.getOpenFileName()
        if str(open_me).endswith('.root'):
            self.fname.setText(open_me)
            self.sroot = scoutroot(str(open_me))
            self.total_events_line.setText(str(self.sroot.events))
            self.plot() #plot the first event in the file
        else:
            self.fname.setText('Please choose a valid root file')

    def plot(self):
        event = int(self.event.text())
        waves = self.sroot.get_waves(event)
        timeaxis = [i for i in range(len(waves[0]))] 
        self.fig.clear()
        self.axes = self.fig.add_subplot(111)
        for wave in waves:
            self.axes.plot(timeaxis, wave)
        self.canvas.draw()


class scoutroot():
    def __init__(self, tfname):
        self.tfile = cern.TFile(tfname)
        if self.tfile.IsZombie():
            raise IOError("TFile not valid")
        self.tree = self.tfile.Get("Data")
        self.__setup__()

    def __setup__(self):
        self.events = self.tree.GetEntries()

    def get_waves(self, event):
        # This is a test of functionality
        self.tree.GetEvent(event)
        wflist= [list(self.tree.__getattr__(it.GetName())) for it
                in self.tree.GetListOfLeaves()
                if not it.GetName().find('waveform')]
        return wflist
