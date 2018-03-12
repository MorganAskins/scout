from PyQt4 import QtCore, QtGui
import sys, os
import time
import copy
from pycaen import pycaen

def sditer(dic):
    return iter(sorted(dic.iteritems()))

class hv_tab(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.hv = pycaen()
        self.layout = QtGui.QVBoxLayout()
        self.hvGetTable = hv_table(self.hv)
        self.hvSetTable = hv_table2(self.hv)
        self.layout.addWidget(self.hvGetTable)
        self.layout.addWidget(self.hvSetTable)
        self._onoffswitch_()
        self.setLayout(self.layout)

    def _onoffswitch_(self):
        on_switch = QtGui.QPushButton("All Channels Power ON")
        on_switch.clicked.connect(self.hvSetTable.poweron)
        self.layout.addWidget(on_switch)
        off_switch = QtGui.QPushButton("All Channels Power OFF")
        off_switch.clicked.connect(self.hvSetTable.poweroff)
        self.layout.addWidget(off_switch)

class hv_table(QtGui.QTableWidget):
    def __init__(self, hvcaen):
        self.hv = hvcaen
        self.num_chan = 4 #todo ask caen for this number
        # One row for setting, one row for getting, if contains Mon cant set
        self._setup_dicts()
        QtGui.QTableWidget.__init__(self, self.num_chan, len(self.getdata))
        # self._make_table()
        # Add a refresh timer which redraws the table values (ie _make_table)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._refresh_)
        self.timer.start(1000)

    def _refresh_(self):
        self._make_table()

    def _setup_dicts(self):
        # This table is non-editable, here is a list of the params to show
        self.getdata = {}
        params = ['VMon', 'IMonL', 'IMonH', 'Pw']
        for item in self.hv.param_list:
            if item in params:
                self.getdata[item] = [0]*self.num_chan
        self._retrievedata()

    def _retrievedata(self):
        for item in self.getdata:
            for ch in range(self.num_chan):
                self.getdata[item][ch] = self.hv.GetParameter(ch, item)

    def _make_table(self):
        '''
        Block out anything that starts with Mon, and throw away Status (for now)
        '''
        skip = 'Status'
        self._retrievedata()
        horHeaders = []
        faded = QtGui.QColor(150,210,230)
        for col, (param, val_list) in enumerate(sditer(self.getdata)):
            horHeaders.append(param)
            for ch in range(self.num_chan):
                getvalue = val_list[ch]
                if type(getvalue) is float:
                    vstring = '%.2f' % getvalue
                else:
                    vstring = str(getvalue)
                newitem = QtGui.QTableWidgetItem(vstring)
                newitem.setFlags(QtCore.Qt.ItemIsEnabled)
                newitem.setBackground(faded)
                self.setItem(ch, col, newitem)
        self.setHorizontalHeaderLabels(horHeaders)

class hv_table2(QtGui.QTableWidget):
    def __init__(self, hvcaen):
        self.hv = hvcaen
        self.num_chan = 4 #todo ask caen for this number
        # One row for setting, one row for getting, if contains Mon cant set
        self._setup_dicts()
        QtGui.QTableWidget.__init__(self, self.num_chan, len(self.setdata))
        self._make_table()
        self.itemChanged.connect(self._senddata)
        # self._make_table()
        # Add a refresh timer which redraws the table values (ie _make_table)
        #self.timer = QtCore.QTimer()
        #self.timer.timeout.connect(self._refresh_)
        #self.timer.start(1000)

    def poweron(self):
        for ch in range(self.num_chan):
            self.data_dict['Pw'][ch].setText("1")

    def poweroff(self):
        for ch in range(self.num_chan):
            self.data_dict['Pw'][ch].setText("0")

    def _setup_dicts(self):
        # This table is non-editable, here is a list of the params to show
        self.setdata = {}
        notparams = ['VMon', 'IMonL', 'IMonH', 'Status']
        for item in self.hv.param_list:
            if item not in notparams:
                self.setdata[item] = [0]*self.num_chan
        self._retrievedata()

    def _update_dict(self):
        for item in self.setdata:
            for ch in range(self.num_chan):
                mytype = type(self.setdata[item][ch])
                self.setdata[item][ch] = mytype(self.data_dict[item][ch].text())

    def _senddata(self):
        self._update_dict()
        for item, val_list in sditer(self.setdata):
            for ch in range(self.num_chan):
                self.hv.SetParameter(ch, item, val_list[ch])

    def _retrievedata(self):
        for item in self.setdata:
            for ch in range(self.num_chan):
                self.setdata[item][ch] = self.hv.GetParameter(ch, item)

    def _make_table(self):
        self.data_dict = copy.deepcopy(self.setdata)
        horHeaders = []
        faded = QtGui.QColor(150,210,230)
        for col, (param, val_list) in enumerate(sditer(self.setdata)):
            horHeaders.append(param)
            for ch in range(self.num_chan):
                getvalue = val_list[ch]
                if type(getvalue) is float:
                    vstring = '%.2f' % getvalue
                else:
                    vstring = str(getvalue)
                ''' Format is set (get) '''
                newitem = QtGui.QTableWidgetItem(vstring)
                self.data_dict[param][ch] = newitem
                self.setItem(ch, col, newitem)
        self.setHorizontalHeaderLabels(horHeaders)
