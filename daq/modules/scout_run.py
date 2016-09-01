from PyQt4 import QtCore, QtGui
import sys, os, time
import ctypes
import traceback, types
from functools import wraps
from scout_configure import scout_configure
from cStringIO import StringIO
import json

from readout import main as readout
from pycaen import pycaen
from multiprocessing import Process, Lock, Pool, Queue, Pipe

'''
When scout is running it has taken posession of the
interface with the struck sis3316, which means nothing
else can communicate with it. Since we don't want the
gui to own this process we will spawn another process
to run the daq
'''

''' Decorator to catch c++ exceptions '''
def PyQtSlot(*args):
    if len(args) == 0 or isinstance(args[0], types.FunctionType):
        args = []
    @QtCore.pyqtSlot(*args)
    def slotdecorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                func(*args)
            except:
                print "Uncaught Exception in slot"
                traceback.print_exc()
        return wrapper
    return slotdecorator

class run_tab(QtGui.QWidget):
    def __init__(self, connection):
        QtGui.QWidget.__init__(self)
        self.connection = connection
        fbox = run_form(connection)
        self.setLayout(fbox)

class run_form(QtGui.QFormLayout):
    def __init__(self, connection):
        # Get scout
        self.connection = connection
        QtGui.QFormLayout.__init__(self)
        self.__private_methods__()
        self.run_proc = Process()

    def __private_methods__(self):
        self.__build_form__()
        self.data_string = ''
        try:
            os.remove('.logfile_gui')
        except OSError:
            pass
        self.logfile = open('.logfile_gui', 'wb')
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.__refresh__)
        self.timer.start(1000)
        self.motherdatadir = os.path.abspath(
                os.path.join(os.path.dirname(__file__), '../data'))

    def __refresh__(self):
        old_text = self.data_string
        self.logread = open('.logfile_gui', 'r')
        data_list = self.logread.readlines()
        prune_list = [ item.split('\r')[-2] if len(item.split('\r')) > 1
                else item.split('\r')[0] for item in data_list]
        prune_list = [item.strip('\n') for item in prune_list]
        self.data_string = '\n'.join(prune_list)
        if self.data_string != old_text:
            self.tblock.setText(self.data_string)
            self.tblock.moveCursor(QtGui.QTextCursor.End)

    def __set_names__(self):
        daughterdatadir = time.strftime('%d_%b_%y_%H_%M')
        full_dir = os.path.join(self.motherdatadir, daughterdatadir)
        counter, make_dir = 0, full_dir
        while True:
            try:
                os.mkdir(make_dir)
                break
            except OSError:
                counter += 1
                make_dir = '%s-%i' % (full_dir, counter)
                continue
        self.full_dir = full_dir
        self.full_name = os.path.join(make_dir,str(self.fname.text()))

    def __build_form__(self):
        self.fname = QtGui.QLineEdit('data.dat')
        self.runlength = QtGui.QLineEdit('60')
        self.runcount= QtGui.QLineEdit('1')
        self.addRow(QtGui.QLabel("File name"), self.fname)
        self.addRow(QtGui.QLabel("Individual Run Length"), self.runlength)
        self.addRow(QtGui.QLabel("Total Runs"), self.runcount)
        # Start the run
        run_button = QtGui.QPushButton("Start")
        run_button.clicked.connect(self.__run__)
        stop_button = QtGui.QPushButton("Stop")
        stop_button.clicked.connect(self.__stop__)
        self.addRow(run_button, stop_button)
        self.notes_block()
        self.text_block()

    def text_block(self):
        self.tblock = QtGui.QTextEdit()
        self.tblock.setReadOnly(True)
        self.addRow(self.tblock)

    def notes_block(self):
        self.notesblock = QtGui.QTextEdit()
        label = QtGui.QLabel("Run Notes")
        self.addRow(label)
        self.addRow(self.notesblock)

    def __save_notes__(self):
        note_name = os.path.join(self.full_dir, 'notes.txt')
        with open(note_name, 'w') as fw:
            fw.write(self.notesblock.toPlainText())


    @PyQtSlot("bool")
    def __run__(self, checked):
        self.__set_names__()
        self.__save_notes__()
        msg = 'Begin DAQ run at %s for %s seconds\n' % \
                (time.strftime('%d %b %y %H:%M:%S'), self.runlength.text())
        self.logfile.write(msg)
        self.logfile.flush()
        cookie = scout(self.connection, self.full_name, self.logfile)
        try:
            runlength = int(self.runlength.text())
        except ValueError:
            self.runlength.setText('Enter an integer!!')
            return
        try:
            runcount = int(self.runcount.text())
        except ValueError:
            self.runcount.setText('Enter an integer!!')
            return
        if not self.run_proc.is_alive():
            self.run_proc = Process(target=cookie.batchrun, 
                    args=(runlength, runcount,))
            self.run_proc.start()
        else:
            print 'Can only run one instance of the DAQ'

    def __stop__(self):
        self.run_proc.terminate()

class scout():
    def __init__(self, connection, fname='data.dat', stderr=sys.stderr):
        self.stderr=stderr
        self.connection = connection
        self.configure = scout_configure(self.connection.sis_address(), 3333)
        self.configure.push_to_struck()
        self.__scout_info__()
        if not fname.endswith('.dat'):
            fname = ''.join([fname, '.dat'])
        if len(fname.split('.'))>2:
            raise NameError('Either give .dat or no extension')
        self.fname = fname
        self.__save_struck_state__()

    def __save_struck_state__(self):
        # Save the json config file with the scout run files
        json_name = os.path.dirname(self.fname)+'/scout.config'
        self.configure.write_to_json(json_name)

    def __save_hv_state__(self):
        # Run this at beginning and end of each run
        json_name = os.path.dirname(self.fname)+'/scout.hv'
        params = ['VMon', 'IMonH', 'Pw', 'VSet']
        this_run_d = {ch: {} for ch in range(self.hv_chan)}
        for item in params:
            if item in self.hv.param_list:
                for ch in range(self.hv_chan):
                    this_run_d[ch][item] = \
                            self.hv.GetParameter(ch, item)
        self.__hvinfo__[self.run_num]=this_run_d
        with open(json_name, 'wb') as fp:
            json.dump(self.__hvinfo__, fp, sort_keys=True, indent=2)


    def __scout_info__(self):
        # Collect: samples, header_size, enabled channels
        self.__info__ = {} 
        self.hv_chan = 4
        self.__hvinfo__={}
        self.hv = pycaen()
        self.run_num = 0
        chan_count = 0
        for ch in range(16):
            idx = 'ch_%i_enable' % ch
            if self.configure.toggle_data[idx]:
                chan_count += 1
        self.__info__['channels'] = chan_count
        format = self.configure.ranged_data['ch_format']['setpoint']
        match = lambda a, b: 1 if a & b else 0
        headsize = 4*( 3+match(format, 0b1)*7+match(format, 0b10)*2+\
                match(format, 0b100)*3+match(format, 0b1000)*2 )
        samplesize = 2*self.configure.ranged_data['gate_window']['setpoint']
        self.__info__['event_size'] = headsize+samplesize

    def __run__(self, length, fname=None):
        if not fname:
            fname = self.fname
        self.__save_hv_state__()
        readout(self.connection.sis_address(), 3333, 
                fname, range(0,16), length, self.stderr, self.__info__ )
        self.run_num += 1
        myargv = ctypes.c_char_p*2
        argv = myargv('python', fname)
        libpath = os.path.abspath( os.path.join( 
                os.path.dirname(__file__), '../lib/libscout.so'))
        proc = Process(target=ctypes.CDLL(libpath).main,
                args=(2,argv))
        proc.start()
        return proc

    def batchrun(self, length, run_count):
        for i in range(run_count):
            counter = ''.join(['_', str(i), '.'])
            seq = self.fname.split('.')
            seq.insert(-1, counter)
            newname = ''.join(seq)
            self.__run__(length, fname=newname)
