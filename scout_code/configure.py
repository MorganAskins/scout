#!/usr/bin/env python2
import sys, os
sys.path.append(
        os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import sis3316
import argparse
import json

'''
Certain parameters will be always fixed for scout (ie trigger conditions)
but things like high-voltage and triggers should be stored and written into
the files. Scout.py will keep track of this and add it to file headers at some
point.
'''

def parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('host', type=str,
            help="SIS3316 IP Address")
    parser.add_argument('-p', '--port', type=int, default=3333,
            help="SIS3316 Host port, default 3333")
    parser.add_argument('--debug', action='store_true',
            help="Turn debug verbosity on")
    return parser.parse_args()

class bugger():
    def __init__(self, debug):
        self._debug = debug
    def bprint(self, txt):
        if self._debug:
            print(txt)

def setup(host, port, debug):
    bug = bugger(debug)
    bug.bprint( 'Connecting to %s:%i' % (host,port) )
    dev = sis3316.Sis3316_udp(host, port)
    dev.open()
    dev.reset()
    dev.configure()
    dev.flags = ['nim_ti_as_te', 'extern_ts_clr_ena', 'extern_trig_ena']
    #active_channels = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    active_channels = [0,1,2,3]
    chflags = ['extern_trig', 'invert']
    # 0x74 LEMO TI to TE
    dev.write(0x74, 0x10000)
    #dev.write(0x7c,0xF0000)
    ### IMPORTANT VARIABLES HERE ###
    # The following 0x800 0000 is a 1 in the 28th bit amounting to a 
    # trigger on, followed by a 27-bit running sum to trigger on
    threshold = 200 + 0x8000000
    high_threshold = 120000 + 0x8000000
    # Turn on sample saving for group 1
    gate_window = 512 
    sample_size = gate_window & 0xFFFE
    sample_value = 0x0 + (sample_size << 16)
    dev.write(0x1020, sample_value)
    ################################

    for ch in dev.channels:
        if ch.idx in active_channels:
            ch.gain = 0 # 0->2V input range at 14-bits
            ch.dac_offset = 0 
            ch.flags = chflags
            ch.event_format_mask = 0b0001
            ch.trig.cfd_ena = 3
            ch.trig.threshold = threshold 
            ch.trig.high_threshold = 120000
            ch.trig.out_pulse_length = 4
    for gr in dev.groups:
        if (gr.idx == 0):
            gr.clear_link_error_latch_bits()
            gr.enable = True 
            gr.addr_threshold = 6092
            gr.accum1_start = 0 
            gr.accum2_start = 16 
            gr.accum3_start = 16 
            gr.accum4_start = 64 
            gr.accum5_start = 128 
            gr.accum6_start = 256 
            gr.accum1_window = 16 
            gr.accum2_window = 32 
            gr.accum3_window = 48 
            gr.accum4_window = 64 
            gr.accum5_window = 128 
            gr.accum6_window = 256 
            gr.gate_window = gate_window
            gr.gate_coinc_window = 0
            gr.delay = 90 
            gr.sum_trig.enable = 1
            gr.sum_trig.cfd_ena = 3
            gr.sum_trig.threshold = threshold 
            gr.sum_trig.high_suppress_ena = 1
            gr.sum_trig.high_threshold = high_threshold 
            gr.sum_trig.out_pulse_length = 4
            gr.sum_trig.maw_gap_time = 4
            gr.sum_trig.maw_peaking_time = 8
            gr.raw_window = gate_window 
            #gr.maw_delay = 0
            #gr.maw_window = 128

    ### STORE IN HEADER ###
    with open('scout.config', 'w') as sc:
        sc.write('threshold %i\n' % threshold)
        sc.write('gate1_start %i\n' % gr.accum1_start)
        sc.write('gate2_start %i\n' % gr.accum2_start)
        sc.write('gate3_start %i\n' % gr.accum3_start)
        sc.write('gate4_start %i\n' % gr.accum4_start)
        sc.write('gate5_start %i\n' % gr.accum5_start)
        sc.write('gate6_start %i\n' % gr.accum6_start)
        sc.write('gate1_window %i\n' % gr.accum1_window)
        sc.write('gate2_window %i\n' % gr.accum2_window)
        sc.write('gate3_window %i\n' % gr.accum3_window)
        sc.write('gate4_window %i\n' % gr.accum4_window)
        sc.write('gate5_window %i\n' % gr.accum5_window)
        sc.write('gate6_window %i\n' % gr.accum6_window)
    #######################

    # All finished
    dev.close()
    dev.__del__()
    
if __name__ == '__main__':
    args=parser()
    setup(args.host, args.port, args.debug)
