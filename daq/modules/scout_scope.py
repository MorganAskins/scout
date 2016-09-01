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

class scope_tab(QtGui.QWidget):
    def __init__(self, connection):
        QtGui.QWidget.__init__(self)
        self.connection = connection
        self.layout = QtGui.QVBoxLayout()
        self._start_()
        self._settings_table_init_()
        self._plot_spot_()
        self.setLayout(self.layout)

    def _plot_spot_(self):
        self.fig = Figure((5.0, 4.0), dpi=100)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self)
        self.canvas.setFocusPolicy(Qt.StrongFocus)
        self.canvas.setFocus()

        self.mpl_toolbar = NavigationToolbar(self.canvas, self)

        #self.canvas.mpl_connect('key_press_event', self.on_key_press)
        self.layout.addWidget(self.canvas)
        self.layout.addWidget(self.mpl_toolbar)

    def _start_(self):
        run_button = QtGui.QPushButton("Start")
        run_button.clicked.connect(self._begin_)
        self.layout.addWidget(run_button)

    def _settings_table_init_(self):
        self.stable_dict = {}
        self.runlength, self.events = 2, 1
        headers = [ 'runlength', 'events' ]
        self.stable = QtGui.QTableWidget(1, 2)
        # Runlength
        newitem = QtGui.QTableWidgetItem( str(self.runlength) )
        self.stable.setItem(0, 0, newitem)
        self.stable_dict['runlength'] = newitem
        newitem = QtGui.QTableWidgetItem( str(self.events) )
        self.stable.setItem(0, 1, newitem)
        self.stable_dict['events'] = newitem
        self.stable.setHorizontalHeaderLabels(headers)
        self.stable.itemChanged.connect(self._settings_table_update_)
        self.stable.resizeColumnsToContents()
        self.stable.resizeRowsToContents()
        self._settings_table_update_()
        self.layout.addWidget(self.stable)

    def _settings_table_update_(self):
        self.runlength = int(self.stable_dict['runlength'].text())
        self.events = int(self.stable_dict['events'].text())

    def _begin_(self):
        fname = 'temp_file_scope.dat'
        rname = 'temp_file_scope.root'
        try:
            os.remove(fname)
        except OSError:
            pass
        runlength = self.runlength
        # Move last temp_file to ready file
        cookie = scout(self.connection, fname)
        proc = cookie.__run__(runlength, fname)
        proc.join()
        try:
            self.sroot = scoutroot(rname)
            self.plot()
        except IOError:
            pass # No events this time around, keep going

    def plot(self):
        waves = self.sroot.get_waves(0)
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

    def get_waves(self, event):
        # This is a test of functionality
        self.tree.GetEvent(event)
        wflist = []
        wflist.append(list(self.tree.waveform0))
        wflist.append(list(self.tree.waveform1))
        wflist.append(list(self.tree.waveform2))
        wflist.append(list(self.tree.waveform3))
        return wflist
