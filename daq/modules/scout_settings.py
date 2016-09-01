from PyQt4 import QtCore, QtGui
import sys, os, json
from scout_configure import scout_configure

# helper function for sorted dictionary iterators
def sditer(dic):
    return iter(sorted(dic.iteritems()))

class settings_tab(QtGui.QWidget):
    ''' Subtabs: Detector, Channels, Groups '''
    def __init__(self, connection):
        QtGui.QWidget.__init__(self)
        ''' Talk to the sis3316 and load in data '''
        self.connection = connection
        self.sc_data = scout_configure(connection.sis_address(), 3333)
        ''' Tabs for various settings '''
        self.tabs = QtGui.QTabWidget()
        self.__refresh_tabs__()
        self.layout = QtGui.QGridLayout()
        self.__savewriteload_box__()
        # self.layout.addWidget(settings_table())
        self.layout.addWidget(self.tabs, 1,0)
        self.setLayout(self.layout)

    def __refresh_tabs__(self):
        self.tabs.clear()
        self.tablist = []
        self.tablist.append(detector_subtab(self.sc_data))
        self.tabs.addTab(self.tablist[0], "Detector" )
        self.tablist.append(gates_subtab(self.sc_data))
        self.tabs.addTab(self.tablist[1], "Gates" )
        self.tablist.append(channel_subtab(self.sc_data))
        self.tabs.addTab(self.tablist[2], "Channels" )
        self.tablist.append(group_subtab(self.sc_data))
        self.tabs.addTab(self.tablist[3], "Groups" )

    def __savewriteload_box__(self):
        self.save_button = QtGui.QPushButton("Save")
        self.save_button.clicked.connect(self.__savefile__)
        self.load_buton = QtGui.QPushButton("Load")
        self.load_buton.clicked.connect(self.__loadfile__)
        self.write_button = QtGui.QPushButton("Write to SIS3316")
        self.write_button.clicked.connect(self.gwrite)
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.write_button)
        hbox.addWidget(self.save_button)
        hbox.addWidget(self.load_buton)
        self.layout.addLayout(hbox, 0, 0)
        #self.layout.addWidget(self.write_button, 0,1)
        #self.layout.addWidget(self.save_button, 1,1)
        #self.layout.addWidget(self.load_buton, 2,1)

    def __savefile__(self):
        self.gwrite()
        save_me = QtGui.QFileDialog.getSaveFileName()
        fname = str(save_me)
        if not fname.endswith('.config'):
            fname += '.config'
        self.sc_data.write_to_json(fname)

    def __loadfile__(self):
        load_me = QtGui.QFileDialog.getOpenFileName()
        fname = str(load_me)
        self.sc_data.load_from_json(fname)
        self.__refresh_tabs__()

    def gwrite(self):
        for tab in self.tablist:
            tab.gwrite()
        # Tell scout_configure to write to json
        self.sc_data.write_to_json()
        # Now push to sis3316
        self.sc_data.push_to_struck()

class channel_subtab(QtGui.QWidget):
    ''' Subtabs of individual channels '''
    def __init__(self, sc_data):
        QtGui.QWidget.__init__(self)
        self.sc_data = sc_data 
        self.tabs = QtGui.QTabWidget()
        self.tablist = []
        for ch in range(16):
            self.tablist.append(channel_subsubtab(self.sc_data, ch))
            self.tabs.addTab(self.tablist[ch], "CH "+str(ch))
        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def gwrite(self):
        for chsst in self.tablist:
            chsst.gwrite()

class group_subtab(QtGui.QWidget):
    ''' Subtabs of individual channels '''
    def __init__(self, sc_data):
        QtGui.QWidget.__init__(self)
        self.sc_data = sc_data 
        self.tabs = QtGui.QTabWidget()
        self.tablist = []
        for gr in range(4):
            self.tablist.append(group_subsubtab(self.sc_data, gr))
            self.tabs.addTab(self.tablist[gr], "GR "+str(gr))
        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        
    def gwrite(self):
        for grsst in self.tablist:
            grsst.gwrite()

class detector_subtab(QtGui.QWidget):
    def __init__(self, data):
        QtGui.QWidget.__init__(self)
        # self.form = QtGui.QFormLayout()
        # self.build_form()
        self.layout = QtGui.QVBoxLayout()
        self.dtable = detector_table(data)
        self.layout.addWidget(self.dtable)
        #self.add_write_button()
        self.setLayout(self.layout)

    def gwrite(self):
        self.dtable.writescoutdata()


class gates_subtab(QtGui.QWidget):
    def __init__(self, data):
        QtGui.QWidget.__init__(self)
        # self.form = QtGui.QFormLayout()
        # self.build_form()
        self.layout = QtGui.QVBoxLayout()
        self.dtable = gate_table(data)
        self.layout.addWidget(self.dtable)
        #self.add_write_button()
        self.setLayout(self.layout)

    def gwrite(self):
        self.dtable.writescoutdata()


class channel_subsubtab(QtGui.QWidget):
    def __init__(self, data, channel):
        QtGui.QWidget.__init__(self)
        # self.form = QtGui.QFormLayout()
        # self.build_form()
        self.layout = QtGui.QVBoxLayout()
        self.dtable = channel_table(data, channel)
        self.layout.addWidget(self.dtable)
        #self.add_write_button()
        self.setLayout(self.layout)

    #def add_write_button(self):
    #    write_button = QtGui.QPushButton("Write")
    #    write_button.clicked.connect(self.dtable.writescoutdata)
    #    self.layout.addWidget(write_button)

    def gwrite(self):
        self.dtable.writescoutdata()


class group_subsubtab(QtGui.QWidget):
    def __init__(self, data, group):
        QtGui.QWidget.__init__(self)
        # self.form = QtGui.QFormLayout()
        # self.build_form()
        self.layout = QtGui.QVBoxLayout()
        self.dtable = group_table(data, group)
        self.layout.addWidget(self.dtable)
        #self.add_write_button()
        self.setLayout(self.layout)

    #def add_write_button(self):
    #    write_button = QtGui.QPushButton("Write")
    #    write_button.clicked.connect(self.dtable.writescoutdata)
    #    self.layout.addWidget(write_button)

    def gwrite(self):
        self.dtable.writescoutdata()

class detector_table(QtGui.QTableWidget):
    def __init__(self, data):
        self.init_data()
        self.scout_data = data
        self.getscoutdata()
        QtGui.QTableWidget.__init__(self, self.rows, 4)
        self.setmydata()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.show()

    def init_data(self):
        ''' List of data hold on this tab '''
        self.data_list = ['nim_ti_as_te', 'extern_ts_clr_ena', 'extern_trig_ena',
                'feedback_int_as_ext', 'ch_format', 'extern_trig', 'invert',
                'coincidence', 'lemo_ti_to_te', 'int_feedback_select_register']
        self.rows = len(self.data_list)

    def getscoutdata(self):
        td = self.scout_data.toggle_data
        rd = self.scout_data.ranged_data
        self.ranged_dict = {}
        self.toggle_dict = {}
        for item in self.data_list:
            try:
                dlist = rd[item]
                #self.ranged_dict[item] = [ dlist['setpoint'], dlist['min'], dlist['max'] ]
                self.ranged_dict[item] = rd[item]
            except KeyError:
                pass
            try:
                self.toggle_dict[item] = td[item]
            except KeyError:
                pass

    def writescoutdata(self):
        ''' Two steps: Table -> local dict, local dict -> scout dict '''
        # Find values in table and place in dict, search col (0) for matching name
        for key, value in self.ranged_dict.iteritems():
            self.ranged_dict[key]['setpoint'] = int(self.col_dict[key].text())
        for key, value in self.toggle_dict.iteritems():
            self.toggle_dict[key]= int(self.col_dict[key].text())
        # Now transfer these values into the scout dict
        for key, value in self.ranged_dict.iteritems():
            self.scout_data.ranged_data[key] = value
        for key, value in self.toggle_dict.iteritems():
            self.scout_data.toggle_data[key] = value
        # Tell scout_configure to write to json
        #self.scout_data.write_to_json()
        # Now push to sis3316
        #self.scout_data.push_to_struck()

    def setmydata(self):
        self.col_dict = {} # dict is name: item(setpoint)
        horHeaders = ['Setting', 'Setpoint', 'Min Value', 'Max Value']
        faded = QtGui.QColor(150,210,230)
        for row, (variable, key) in enumerate(sditer(self.ranged_dict)):
            # Setting
            newitem = QtGui.QTableWidgetItem(variable)
            newitem.setFlags(QtCore.Qt.ItemIsEnabled)
            newitem.setBackground(faded)
            self.setItem(row, 0, newitem)
            # Setpoint
            newitem = QtGui.QTableWidgetItem(str(key['setpoint']))
            self.col_dict[variable] = newitem
            self.setItem(row, 1, newitem)
            # Min
            newitem = QtGui.QTableWidgetItem(str(key['min']))
            newitem.setFlags(QtCore.Qt.ItemIsEnabled)
            newitem.setBackground(faded)
            self.setItem(row, 2, newitem)
            # Max
            newitem = QtGui.QTableWidgetItem(str(key['max']))
            newitem.setFlags(QtCore.Qt.ItemIsEnabled)
            newitem.setBackground(faded)
            self.setItem(row, 3, newitem)
            '''
            for col, value in enumerate(key):
                newitem = QtGui.QTableWidgetItem(str(value))
                if col>0:
                    newitem.setFlags(QtCore.Qt.ItemIsEnabled)
                    newitem.setBackground(faded)
                else: # store setpoint in dict
                    self.col_dict[variable] = newitem
                self.setItem(row, col+1, newitem)
            '''
            tstart = row+1
        for row, (variable, key) in enumerate(sditer(self.toggle_dict)):
            rrow = row+tstart
            newitem = QtGui.QTableWidgetItem(variable)
            newitem.setFlags(QtCore.Qt.ItemIsEnabled)
            newitem.setBackground(faded)
            self.setItem(rrow, 0, newitem)
            newitem = QtGui.QTableWidgetItem(str(key))
            self.col_dict[variable] = newitem
            self.setItem(rrow, 1, newitem)
            newitem = QtGui.QTableWidgetItem('0')
            newitem.setFlags(QtCore.Qt.ItemIsEnabled)
            newitem.setBackground(faded)
            self.setItem(rrow, 2, newitem)
            newitem = QtGui.QTableWidgetItem('1')
            newitem.setFlags(QtCore.Qt.ItemIsEnabled)
            newitem.setBackground(faded)
            self.setItem(rrow, 3, newitem)

        self.setHorizontalHeaderLabels(horHeaders)

class gate_table(QtGui.QTableWidget):
    def __init__(self, data):
        self.init_data()
        self.scout_data = data
        self.getscoutdata()
        QtGui.QTableWidget.__init__(self, self.rows, 4)
        self.setmydata()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.show()

    def init_data(self):
        ''' List of data hold on this tab '''
        self.data_list = ['gate_window', 'gate_coinc_window', 'gate_intern_window',
                'gate_delay', 'gr_accum1_start', 'gr_accum2_start', 'gr_accum3_start',
                'gr_accum4_start', 'gr_accum5_start', 'gr_accum6_start', 
                'gr_accum1_window', 'gr_accum2_window', 'gr_accum3_window', 
                'gr_accum4_window', 'gr_accum5_window', 'gr_accum6_window' ] 
        self.rows = len(self.data_list)

    def getscoutdata(self):
        td = self.scout_data.toggle_data
        rd = self.scout_data.ranged_data
        self.ranged_dict = {}
        self.toggle_dict = {}
        for item in self.data_list:
            try:
                dlist = rd[item]
                #self.ranged_dict[item] = [ dlist['setpoint'], dlist['min'], dlist['max'] ]
                self.ranged_dict[item] = rd[item]
            except KeyError:
                pass
            try:
                self.toggle_dict[item] = td[item]
            except KeyError:
                pass

    def writescoutdata(self):
        ''' Two steps: Table -> local dict, local dict -> scout dict '''
        # Find values in table and place in dict, search col (0) for matching name
        for key, value in self.ranged_dict.iteritems():
            self.ranged_dict[key]['setpoint'] = int(self.col_dict[key].text())
        for key, value in self.toggle_dict.iteritems():
            self.toggle_dict[key]= int(self.col_dict[key].text())
        # Now transfer these values into the scout dict
        for key, value in self.ranged_dict.iteritems():
            self.scout_data.ranged_data[key] = value
        for key, value in self.toggle_dict.iteritems():
            self.scout_data.toggle_data[key] = value
        # Tell scout_configure to write to json
        #self.scout_data.write_to_json()
        # Now push to sis3316
        #self.scout_data.push_to_struck()

    def setmydata(self):
        self.col_dict = {} # dict is name: item(setpoint)
        horHeaders = ['Setting', 'Setpoint', 'Min Value', 'Max Value']
        faded = QtGui.QColor(150,210,230)
        for row, (variable, key) in enumerate(sditer(self.ranged_dict)):
            # Setting
            newitem = QtGui.QTableWidgetItem(variable)
            newitem.setFlags(QtCore.Qt.ItemIsEnabled)
            newitem.setBackground(faded)
            self.setItem(row, 0, newitem)
            # Setpoint
            newitem = QtGui.QTableWidgetItem(str(key['setpoint']))
            self.col_dict[variable] = newitem
            self.setItem(row, 1, newitem)
            # Min
            newitem = QtGui.QTableWidgetItem(str(key['min']))
            newitem.setFlags(QtCore.Qt.ItemIsEnabled)
            newitem.setBackground(faded)
            self.setItem(row, 2, newitem)
            # Max
            newitem = QtGui.QTableWidgetItem(str(key['max']))
            newitem.setFlags(QtCore.Qt.ItemIsEnabled)
            newitem.setBackground(faded)
            self.setItem(row, 3, newitem)
            '''
            for col, value in enumerate(key):
                newitem = QtGui.QTableWidgetItem(str(value))
                if col>0:
                    newitem.setFlags(QtCore.Qt.ItemIsEnabled)
                    newitem.setBackground(faded)
                else: # store setpoint in dict
                    self.col_dict[variable] = newitem
                self.setItem(row, col+1, newitem)
            '''
            tstart = row+1
        for row, (variable, key) in enumerate(sditer(self.toggle_dict)):
            rrow = row+tstart
            newitem = QtGui.QTableWidgetItem(variable)
            newitem.setFlags(QtCore.Qt.ItemIsEnabled)
            newitem.setBackground(faded)
            self.setItem(rrow, 0, newitem)
            newitem = QtGui.QTableWidgetItem(str(key))
            self.col_dict[variable] = newitem
            self.setItem(rrow, 1, newitem)
            newitem = QtGui.QTableWidgetItem('0')
            newitem.setFlags(QtCore.Qt.ItemIsEnabled)
            newitem.setBackground(faded)
            self.setItem(rrow, 2, newitem)
            newitem = QtGui.QTableWidgetItem('1')
            newitem.setFlags(QtCore.Qt.ItemIsEnabled)
            newitem.setBackground(faded)
            self.setItem(rrow, 3, newitem)

        self.setHorizontalHeaderLabels(horHeaders)


class channel_table(QtGui.QTableWidget):
    def __init__(self, data, channel):
        self.channel = channel
        self.init_data()
        self.scout_data = data
        self.getscoutdata()
        QtGui.QTableWidget.__init__(self, self.rows, 4)
        self.setmydata()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.show()

    def init_data(self):
        ''' List of data hold on this tab '''
        def chstr(item):
            return 'ch_'+str(self.channel)+item
        self.data_list = [ chstr('_enable'), chstr('_threshold'),
                chstr('_hithreshold'), chstr('_gain'), chstr('_dacoffset'),
                chstr('_triggerdelay'), chstr('_cfd_ena'), chstr('_trig_enable'), 
                chstr('_hisuppress_enable'), chstr('_mawgap'), chstr('_mawpeak'),
                chstr('_out_pulse') ]
        self.rows = len(self.data_list)

    def getscoutdata(self):
        td = self.scout_data.toggle_data
        rd = self.scout_data.ranged_data
        self.ranged_dict = {}
        self.toggle_dict = {}
        for item in self.data_list:
            try:
                dlist = rd[item]
                #self.ranged_dict[item] = [ dlist['setpoint'], dlist['min'], dlist['max'] ]
                self.ranged_dict[item] = rd[item]
            except KeyError:
                pass
            try:
                self.toggle_dict[item] = td[item]
            except KeyError:
                pass

    def writescoutdata(self):
        ''' Two steps: Table -> local dict, local dict -> scout dict '''
        # Find values in table and place in dict, search col (0) for matching name
        for key, value in self.ranged_dict.iteritems():
            self.ranged_dict[key]['setpoint'] = int(self.col_dict[key].text())
        for key, value in self.toggle_dict.iteritems():
            self.toggle_dict[key]= int(self.col_dict[key].text())
        # Now transfer these values into the scout dict
        for key, value in self.ranged_dict.iteritems():
            self.scout_data.ranged_data[key] = value
        for key, value in self.toggle_dict.iteritems():
            self.scout_data.toggle_data[key] = value
        # Tell scout_configure to write to json
        #self.scout_data.write_to_json()
        # Now push to sis3316
        #self.scout_data.push_to_struck()

    def setmydata(self):
        self.col_dict = {} # dict is name: item(setpoint)
        horHeaders = ['Setting', 'Setpoint', 'Min Value', 'Max Value']
        faded = QtGui.QColor(150,210,230)
        for row, (variable, key) in enumerate(sditer(self.ranged_dict)):
            # Setting
            newitem = QtGui.QTableWidgetItem(variable)
            newitem.setFlags(QtCore.Qt.ItemIsEnabled)
            newitem.setBackground(faded)
            self.setItem(row, 0, newitem)
            # Setpoint
            newitem = QtGui.QTableWidgetItem(str(key['setpoint']))
            self.col_dict[variable] = newitem
            self.setItem(row, 1, newitem)
            # Min
            newitem = QtGui.QTableWidgetItem(str(key['min']))
            newitem.setFlags(QtCore.Qt.ItemIsEnabled)
            newitem.setBackground(faded)
            self.setItem(row, 2, newitem)
            # Max
            newitem = QtGui.QTableWidgetItem(str(key['max']))
            newitem.setFlags(QtCore.Qt.ItemIsEnabled)
            newitem.setBackground(faded)
            self.setItem(row, 3, newitem)
            '''
            for col, value in enumerate(key):
                newitem = QtGui.QTableWidgetItem(str(value))
                if col>0:
                    newitem.setFlags(QtCore.Qt.ItemIsEnabled)
                    newitem.setBackground(faded)
                else: # store setpoint in dict
                    self.col_dict[variable] = newitem
                self.setItem(row, col+1, newitem)
            '''
            tstart = row+1
        for row, (variable, key) in enumerate(sditer(self.toggle_dict)):
            rrow = row+tstart
            newitem = QtGui.QTableWidgetItem(variable)
            newitem.setFlags(QtCore.Qt.ItemIsEnabled)
            newitem.setBackground(faded)
            self.setItem(rrow, 0, newitem)
            newitem = QtGui.QTableWidgetItem(str(key))
            self.col_dict[variable] = newitem
            self.setItem(rrow, 1, newitem)
            newitem = QtGui.QTableWidgetItem('0')
            newitem.setFlags(QtCore.Qt.ItemIsEnabled)
            newitem.setBackground(faded)
            self.setItem(rrow, 2, newitem)
            newitem = QtGui.QTableWidgetItem('1')
            newitem.setFlags(QtCore.Qt.ItemIsEnabled)
            newitem.setBackground(faded)
            self.setItem(rrow, 3, newitem)

        self.setHorizontalHeaderLabels(horHeaders)


class group_table(QtGui.QTableWidget):
    def __init__(self, data, group):
        self.group = group 
        self.init_data()
        self.scout_data = data
        self.getscoutdata()
        QtGui.QTableWidget.__init__(self, self.rows, 4)
        self.setmydata()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.show()

    def init_data(self):
        ''' List of data hold on this tab '''
        def gstr(item):
            return 'gr_'+str(self.group)+item
        self.data_list = [ gstr('_enable'), gstr('_threshold'), gstr('_hithreshold'), 
                gstr('_cfd_ena'), gstr('_sumtrigger'), gstr('_hisuppress_enable'), 
                gstr('_mawgap'), gstr('_mawpeak'), gstr('_out_pulse') ]
        self.rows = len(self.data_list)

    def getscoutdata(self):
        td = self.scout_data.toggle_data
        rd = self.scout_data.ranged_data
        self.ranged_dict = {}
        self.toggle_dict = {}
        for item in self.data_list:
            try:
                dlist = rd[item]
                #self.ranged_dict[item] = [ dlist['setpoint'], dlist['min'], dlist['max'] ]
                self.ranged_dict[item] = rd[item]
            except KeyError:
                pass
            try:
                self.toggle_dict[item] = td[item]
            except KeyError:
                pass

    def writescoutdata(self):
        ''' Two steps: Table -> local dict, local dict -> scout dict '''
        # Find values in table and place in dict, search col (0) for matching name
        for key, value in self.ranged_dict.iteritems():
            self.ranged_dict[key]['setpoint'] = int(self.col_dict[key].text())
        for key, value in self.toggle_dict.iteritems():
            self.toggle_dict[key]= int(self.col_dict[key].text())
        # Now transfer these values into the scout dict
        for key, value in self.ranged_dict.iteritems():
            self.scout_data.ranged_data[key] = value
        for key, value in self.toggle_dict.iteritems():
            self.scout_data.toggle_data[key] = value
        # Tell scout_configure to write to json
        #self.scout_data.write_to_json()
        # Now push to sis3316
        #self.scout_data.push_to_struck()

    def setmydata(self):
        self.col_dict = {} # dict is name: item(setpoint)
        horHeaders = ['Setting', 'Setpoint', 'Min Value', 'Max Value']
        faded = QtGui.QColor(150,210,230)
        for row, (variable, key) in enumerate(sditer(self.ranged_dict)):
            # Setting
            newitem = QtGui.QTableWidgetItem(variable)
            newitem.setFlags(QtCore.Qt.ItemIsEnabled)
            newitem.setBackground(faded)
            self.setItem(row, 0, newitem)
            # Setpoint
            newitem = QtGui.QTableWidgetItem(str(key['setpoint']))
            self.col_dict[variable] = newitem
            self.setItem(row, 1, newitem)
            # Min
            newitem = QtGui.QTableWidgetItem(str(key['min']))
            newitem.setFlags(QtCore.Qt.ItemIsEnabled)
            newitem.setBackground(faded)
            self.setItem(row, 2, newitem)
            # Max
            newitem = QtGui.QTableWidgetItem(str(key['max']))
            newitem.setFlags(QtCore.Qt.ItemIsEnabled)
            newitem.setBackground(faded)
            self.setItem(row, 3, newitem)
            '''
            for col, value in enumerate(key):
                newitem = QtGui.QTableWidgetItem(str(value))
                if col>0:
                    newitem.setFlags(QtCore.Qt.ItemIsEnabled)
                    newitem.setBackground(faded)
                else: # store setpoint in dict
                    self.col_dict[variable] = newitem
                self.setItem(row, col+1, newitem)
            '''
            tstart = row+1
        for row, (variable, key) in enumerate(sditer(self.toggle_dict)):
            rrow = row+tstart
            newitem = QtGui.QTableWidgetItem(variable)
            newitem.setFlags(QtCore.Qt.ItemIsEnabled)
            newitem.setBackground(faded)
            self.setItem(rrow, 0, newitem)
            newitem = QtGui.QTableWidgetItem(str(key))
            self.col_dict[variable] = newitem
            self.setItem(rrow, 1, newitem)
            newitem = QtGui.QTableWidgetItem('0')
            newitem.setFlags(QtCore.Qt.ItemIsEnabled)
            newitem.setBackground(faded)
            self.setItem(rrow, 2, newitem)
            newitem = QtGui.QTableWidgetItem('1')
            newitem.setFlags(QtCore.Qt.ItemIsEnabled)
            newitem.setBackground(faded)
            self.setItem(rrow, 3, newitem)

        self.setHorizontalHeaderLabels(horHeaders)
