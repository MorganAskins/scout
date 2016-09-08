#!/usr/bin/env python2
from PyQt4 import QtCore, QtGui 
import sys, os, traceback
import json, time
import argparse

from modules.scout_run import run_tab
from modules.scout_settings import settings_tab
try:
    from modules.scout_viewer import viewer_tab
except ImportError:
    print 'problem with PyRoot'
from modules.scout_connection import sis_connection
from modules.scout_hv import hv_tab

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--nodaq', action='store_true', default=False)
    return parser.parse_args()

'''
Plan: Build test app here, then break up and move
into individual modules
'''

class Login(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.textPass = QtGui.QLineEdit()
        self.textPass.setEchoMode(QtGui.QLineEdit.Password)
        self.buttonLogin = QtGui.QPushButton('Confirm')
        self.buttonLogin.clicked.connect(self.handleLogin)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.textPass)
        layout.addWidget(self.buttonLogin)
        self.setLayout(layout)
        self.show()

    def handleLogin(self):
        self.password = self.textPass.text()
        self.accept()

class scout_gui(QtGui.QMainWindow):
    def __init__(self, args):
        QtGui.QMainWindow.__init__(self)
        self.args = args
        if not self.args.nodaq:
            self.connection = sis_connection('eno1', '192.168.1.1')
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Scout-QT')
        #self.tabs.resize(800,600)
        #self.tabs.move(300,300)
        self.resize(1000, 700)
        self.move(200, 0)
        self.tabs = QtGui.QTabWidget()
        if not self.args.nodaq:
            if self.connection.sis_address() is not None:
                self.tabs.addTab( run_tab(self.connection), "Run" )
                self.tabs.addTab( settings_tab(self.connection), "Settings" )
        try:
            self.tabs.addTab( viewer_tab(), "Event Viewer" )
        except NameError:
            pass
        self.tabs.addTab( hv_tab(), "High Voltage" )
        self.setCentralWidget(self.tabs)
        self.show()
        #self.tabs.show()

    def exit(self):
        QtGui.QApplication.exit()

    def closeEvent(self, event):
        clip = QtGui.QApplication.clipboard()
        clip.clear()
        event.accept()

class MyApp(QtGui.QApplication):
    def notify(self, obj, event):
        try:
            return QtGui.QApplication.notify(self, obj, event)
        except Exception:
            print "fix me!"
            print traceback.format_exception(*sys.exc_info())
            return False


def main():
    #app = QtGui.QApplication(sys.argv)
    args = get_args()
    app = MyApp(sys.argv)
    #login = Login()
    #if login.exec_() == QtGui.QDialog.Accepted:
    #    args.password = login.password
    sgui = scout_gui(args)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

