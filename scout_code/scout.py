#!/usr/bin/env python2

from scout_configure import setup
from connection import sis_connection
from readout import main as readout
import readout
import time
import argparse
import ctypes
from multiprocessing import Process, Lock, Pool

class scout():
    '''
    Management class that runs different parts of
    the detector in parallel.
    1. Setup ethernet connection
    2. Configure SIS3316
    3. Ramp up high voltage to PMT
    4. Readout from SIS3316
    5. Clean data and output .root file
    '''

    def __init__(self, interface, host, fname='data.dat'):
        if not fname.endswith('.dat'):
            fname = ''.join([fname,'.dat'])
        if len(fname.split('.'))>2:
            raise NameError('Either give .dat extension or no extension')
        self.connection = sis_connection(interface, host)
        self.address = self.connection.sis_ip
        self.fname = fname

    def __run__(self, length, fname=None):
        if not fname:
            fname = self.fname
        setup(self.address, 3333, False)
        readout.main(self.address, 3333, fname, range(0,16), length)
        myargv = ctypes.c_char_p*2
        argv = myargv('python', fname)
        proc = Process(target=ctypes.CDLL('./scout_builder.so').main, args=(2, argv))
        proc.start()

    def batchrun(self, length, run_count):
        for i in range(run_count):
            counter = ''.join(['_', str(i), '.'])
            seq = self.fname.split('.')
            seq.insert(-1, counter)
            newname = ''.join(seq)
            self.__run__(length, fname=newname)

def main():
    args = aparse()
    detector = scout(args.interface, args.address, fname=args.fname)
    detector.batchrun(args.time, args.runs)

def aparse():
    parser = argparse.ArgumentParser()
    parser.add_argument('fname', type=str, default='data.dat',
            help="Output data file")
    parser.add_argument('-t', '--time', type=int, default=0,
            help="Runtime")
    parser.add_argument('-n', '--runs', type=int, default=1,
            help="Number of times to run")
    parser.add_argument('-i', '--interface', type=str, default='eno1',
            help="Ethernet interface to SIS3316")
    parser.add_argument('-a', '--address', type=str, default='192.168.1.1',
            help="IP Address of this machine")
    return parser.parse_args()

if __name__ == '__main__':
    main()


