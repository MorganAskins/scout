#!/usr/bin/env python2
import sys, os
from __sislib__ import sis3316
import argparse
import json, time
import numpy as np

'''
Certain parameters will be always fixed for scout (ie trigger conditions)
but things like high-voltage and triggers should be stored and written into
the files. Scout.py will keep track of this and add it to file headers at some
point.
'''

debug = False


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

class scout_configure():
    '''
    The following parameters adjust the sis3316 settings for a given
    run. The state of the detector is then stored in a json config
    file. Order of operations:
    1) Data structure from json file (or build one if not available)
    '''
    def __init__(self, host, port):

        self.host, self.port = host, port
        self.build_data_structure()

    def build_data_structure(self):
        ''' Types of flags: on/off, value(min, max) '''
        self.config_file_name = '.scout.config' #hidden file
        self.toggle_data = {}
        self.ranged_data = {}
        self.load_from_json()

    def add_toggle_data(self, name, default):
        self.toggle_data[name] = default

    def add_ranged_data(self, name, default, minV, maxV):
        self.ranged_data[name] = { 'setpoint':default, 'min':minV, 'max':maxV }

    def load_from_json(self, fname=None):
        if fname is None:
            fname = self.config_file_name
        #if fname is not None:
        #    self.config_file_name = fname
        try:
            with open(fname, 'rb') as fp:
                data = json.load(fp)
            self.toggle_data = data['toggle']
            self.ranged_data = data['ranged']
            self.write_to_json()
        except IOError:
            self.setup_data() # Loads in defaults
            self.write_to_json() # Then saves the defaults

    def write_to_json(self, fname=None):
        big_dict = {'toggle':self.toggle_data, 'ranged':self.ranged_data}
        #if fname is not None:
        #    self.config_file_name = fname
        if fname is None:
            fname = self.config_file_name
        with open(fname, 'wb') as fp:
            json.dump(big_dict, fp, sort_keys=True, indent=2)

    def setup_data(self):
        ''' Manual input of data components '''
        self.add_toggle_data('nim_ti_as_te', 1)
        self.add_toggle_data('extern_ts_clr_ena', 1)
        self.add_toggle_data('extern_trig_ena', 1)
        self.add_toggle_data('feedback_int_as_ext', 1)
        self.add_toggle_data('record_waveforms', 1)
        for ch in range(16):
            self.add_toggle_data('ch_'+str(ch)+'_enable', 0)
            self.add_ranged_data('ch_'+str(ch)+'_threshold', 500, 0, 65535) # don't know max
            self.add_ranged_data('ch_'+str(ch)+'_hithreshold', 120000, 0, 200000)
            self.add_ranged_data('ch_'+str(ch)+'_gain', 1, 0, 3)
            self.add_ranged_data('ch_'+str(ch)+'_dacoffset', 52000, 0, 65535)
            self.add_ranged_data('ch_'+str(ch)+'_triggerdelay', 20, 0, 1024)
            self.add_ranged_data('ch_'+str(ch)+'_cfd_ena', 3, 0, 3)
            self.add_toggle_data('ch_'+str(ch)+'_trig_enable', 0)
            self.add_toggle_data('ch_'+str(ch)+'_hisuppress_enable', 1)
            self.add_ranged_data('ch_'+str(ch)+'_mawgap', 4, 0, 32)
            self.add_ranged_data('ch_'+str(ch)+'_mawpeak', 8, 0, 32)
            self.add_ranged_data('ch_'+str(ch)+'_out_pulse', 4, 0, 32)
            self.add_toggle_data('ch_'+str(ch)+'_invert', 0 )

        for gr in range(4):
            self.add_toggle_data('gr_'+str(gr)+'_enable', 1)
            self.add_toggle_data('gr_'+str(gr)+'_sumtrigger', 0)
            self.add_ranged_data('gr_'+str(gr)+'_cfd_ena', 3, 0, 3)
            self.add_ranged_data('gr_'+str(gr)+'_threshold', 100, 0, 100000) 
            self.add_ranged_data('gr_'+str(gr)+'_hithreshold', 120000, 0, 200000)
            self.add_toggle_data('gr_'+str(gr)+'_hisuppress_enable', 1)
            self.add_ranged_data('gr_'+str(gr)+'_mawgap', 4, 0, 32)
            self.add_ranged_data('gr_'+str(gr)+'_mawpeak', 8, 0, 32)
            self.add_ranged_data('gr_'+str(gr)+'_out_pulse', 4, 0, 32)

        self.add_ranged_data('gr_accum1_start', 0, 0, 1024)
        self.add_ranged_data('gr_accum2_start', 16, 0, 1024)
        self.add_ranged_data('gr_accum3_start', 16, 0, 1024)
        self.add_ranged_data('gr_accum4_start', 64, 0, 1024)
        self.add_ranged_data('gr_accum5_start', 128, 0, 1024)
        self.add_ranged_data('gr_accum6_start', 256, 0, 1024)
        self.add_ranged_data('gr_accum1_window', 16, 0, 1024)
        self.add_ranged_data('gr_accum2_window', 32, 0, 1024)
        self.add_ranged_data('gr_accum3_window', 48, 0, 1024)
        self.add_ranged_data('gr_accum4_window', 64, 0, 1024)
        self.add_ranged_data('gr_accum5_window', 128, 0, 1024)
        self.add_ranged_data('gr_accum6_window', 256, 0, 1024)
        self.add_ranged_data('gr_accum6_window', 256, 0, 1024)
        self.add_ranged_data('gate_coinc_window', 20, 4, 1024)
        self.add_ranged_data('gate_intern_window', 30, 4, 1024)
        self.add_ranged_data('gate_delay', 90, 4, 1024)

        self.add_ranged_data('ch_format', 1, 0, 16)
        self.add_toggle_data('extern_trig', 1)
        #self.add_toggle_data('invert', 1)
        self.add_ranged_data('coincidence', 2, 1, 16)
        self.add_toggle_data('lemo_ti_to_te', 1)
        self.add_toggle_data('int_feedback_select_register', 1)
        self.add_ranged_data('gate_window', 512, 4, 1024)

    def look_rdata(self, var):
        value = self.ranged_data[var]['setpoint']
        if debug:
            print "set %s to %i with type %s" % (var, value, type(value))
        return value

    def push_to_struck(self):
        td = self.toggle_data
        rd = self.ranged_data
        self.dev = sis3316.Sis3316_udp(self.host, self.port)
        self.dev.open()
        self.dev.reset()
        self.dev.configure()
        ''' Board flags '''
        dev_flags = ['nim_ti_as_te', 'extern_ts_clr_ena', 'extern_trig_ena', 'feedback_int_as_ext']
        self.dev.flags = [ flag for flag in dev_flags if td[flag] == 1]
        allch_flag_options = ['extern_trig']
        allchflags = [ flag for flag in allch_flag_options if td[flag] == 1 ]
        # Coincidence Tables ... n choose k permutations here
        coinc_level = self.look_rdata('coincidence')
        ## Swap hack
        def idx_swapper(idx):
            gid = int(idx/4)
            cid = idx % 4
            swapbox = [1,0,3,2]
            swapcid = swapbox[cid]
            return gid*4 + swapcid
        ##
        ## Swap hack changes channels
        channels = [ ch for ch in range(16) if (td['ch_'+str(ch)+'_enable'] == 1)]
        sw_channels = [ idx_swapper(ch) for ch in range(16) if (td['ch_'+str(ch)+'_enable'] == 1)]
        groups = [ gr for gr in range(4) if td['gr_'+str(gr)+'_enable'] == 1]
        num_channels = len(sw_channels)
        cp_maker = coincidence_permutations(sw_channels, coinc_level)
        coinc_table_address = cp_maker.bitarray
        # Trigger Coincidence Lookup Table Control Register
        self.dev.write(0x64, 0x80000004)
        # This above operation takes 500us to run, so lets wait for it
        time.sleep(0.5)
        for addr in coinc_table_address:
            # Trigger Coincidence Lookup Table Address Register
            self.dev.write(0x68, addr) 
            # Trigger Coincidence Lookup Table Data Register
            self.dev.write(0x6c, 1)
        # Trigger mask
        mask = chan_to_bit(sw_channels)
        self.dev.write(0x68, mask)
        
        # 0x74 LEMO TI to TE
        if td['lemo_ti_to_te']:
            #self.dev.write(0x74, 0x101000f)
            self.dev.write(0x74, 0x10fffff)
        # 0x7C = Internal Feedback Select Register
        #dev.write(0x7C, 0x201000f)
        if td['int_feedback_select_register']:
            self.dev.write(0x7C, 0x1000000)
        # The following 0x800 0000 is a 1 in the 28th bit amounting to a 
        # trigger on, followed by a 27-bit running sum to trigger on

        # Turn on sample saving for group 1
        #gate_window = self.look_rdata('gate_window')
        #sample_size = gate_window & 0xFFFE
        #sample_value = 0x0 + (sample_size << 16)
        #self.dev.write(0x1020, sample_value)

        ###############################

        for ch in self.dev.channels:
            if (ch.idx in sw_channels):
                swidx = 'ch_'+str(idx_swapper(ch.idx))
                # Swap hack, does it work here?
                # Here are the things that need swapping
                # flags
                if td[swidx+'_invert'] == 1:
                    ch.flags = allchflags + ['invert']
                else:
                    ch.flags = allchflags
                ch.event_format_mask = self.look_rdata('ch_format')
                ch.intern_trig_delay = self.look_rdata(swidx+'_triggerdelay')
                ch.trig.cfd_ena = self.look_rdata(swidx+'_cfd_ena') 
                ch.trig.enable = td[swidx+'_trig_enable'] 
                ch.trig.high_suppress_ena = td[swidx+'_hisuppress_enable'] 
                ch.trig.maw_gap_time = self.look_rdata(swidx+'_mawgap') 
                ch.trig.maw_peaking_time = self.look_rdata(swidx+'_mawpeak') 
                ch.trig.threshold = self.look_rdata(swidx+'_threshold') + 0x8000000
                ch.trig.high_threshold = self.look_rdata(swidx+'_hithreshold') + 0x8000000
                ch.trig.out_pulse_length = self.look_rdata(swidx+'_out_pulse')
            if (ch.idx in channels):
                idx = 'ch_'+str(ch.idx)
                ch.gain = self.look_rdata(idx+'_gain')
                ch.dac_offset = self.look_rdata(idx+'_dacoffset')


        for gr in self.dev.groups:
            if gr.idx in groups:
                idx = 'gr_'+str(gr.idx)
                gr.clear_link_error_latch_bits()
                gr.enable = td[idx+'_enable']
                gr.addr_threshold = 6092
                gr.accum1_start = self.look_rdata('gr_accum1_start')
                gr.accum2_start = self.look_rdata('gr_accum2_start')
                gr.accum3_start = self.look_rdata('gr_accum3_start')
                gr.accum4_start = self.look_rdata('gr_accum4_start')
                gr.accum5_start = self.look_rdata('gr_accum5_start')
                gr.accum6_start = self.look_rdata('gr_accum6_start')
                gr.accum1_window = self.look_rdata('gr_accum1_window')
                gr.accum2_window = self.look_rdata('gr_accum2_window')
                gr.accum3_window = self.look_rdata('gr_accum3_window')
                gr.accum4_window = self.look_rdata('gr_accum4_window')
                gr.accum5_window = self.look_rdata('gr_accum5_window')
                gr.accum6_window = self.look_rdata('gr_accum6_window')
                gr.gate_window = self.look_rdata('gate_window')
                gr.gate_coinc_window = self.look_rdata('gate_coinc_window') 
                gr.gate_intern_window = self.look_rdata('gate_intern_window') 
                gr.delay = self.look_rdata('gate_delay') 
                gr.sum_trig.enable = td[idx+'_sumtrigger'] 
                gr.sum_trig.cfd_ena = self.look_rdata(idx+'_cfd_ena') 
                gr.sum_trig.threshold = self.look_rdata(idx+'_threshold')+0x8000000
                gr.sum_trig.high_suppress_ena = td[idx+'_hisuppress_enable'] 
                gr.sum_trig.high_threshold = self.look_rdata(idx+'_hithreshold')+0x8000000
                gr.sum_trig.out_pulse_length = self.look_rdata(idx+'_out_pulse') 
                gr.sum_trig.maw_gap_time = self.look_rdata(idx+'_mawgap') 
                gr.sum_trig.maw_peaking_time = self.look_rdata(idx+'_mawpeak') 
                ## This should be its own parameter and not share with raw_window ... orrr ... make it a toggle and set same??
                ## if td['record_waveforms'] set to gate_window, else 0
                #gr.raw_window = self.look_rdata('gate_window')
                if td['record_waveforms']:
                    gr.raw_window = self.look_rdata('gate_window')
                else:
                    gr.raw_window = 0
        self.dev.close()
        self.dev.__del__()

class unique_element:
    def __init__(self, value, occurrences):
        ''' Data structure to hold coincidence permutations '''
        self.value = value
        self.occurrences = occurrences

class coincidence_permutations:
    def __init__(self, channels, coincidence):
        ''' Should be n choose k permutations '''
        self.channels = channels
        self.ch = len(channels)
        self.co = coincidence
        self.make_array()

    def perm_unique(self, elements):
        eset = set(elements)
        listunique = [unique_element(i, elements.count(i)) for i in eset]
        u=len(elements)
        return self.perm_unique_helper(listunique, [0]*u, u-1)

    def perm_unique_helper(self, listunique, result_list, d):
        if d<0:
            yield tuple(result_list)
        else:
            for i in listunique:
                if i.occurrences > 0:
                    result_list[d]=i.value
                    i.occurrences-=1
                    for g in self.perm_unique_helper(listunique, result_list, d-1):
                        yield g
                    i.occurrences += 1
    
    def list_to_bin(self, ll):
        stringy = [str(int(e)) for e in ll]
        return int(''.join(stringy),2)

    def make_array(self):
        self.bitarray = []
        # include the exact coincidence and all coincidence greater
        # ... also, adjust for the actual list of channels
        for i in range(self.co, self.ch+1):
            fvec = list(np.append( (np.zeros(i)+1), np.zeros(self.ch-i)))
            perms = [list(ele) for ele in list(self.perm_unique(fvec))]
            self.bitarray += [self.list_to_bin(ele) for ele in perms]
        # Now that we have the permutations, fill in the holes
        notbitarray = [ [ int(x) for x in bin(bits)[2:]] for bits in self.bitarray ]
        notbitarray = [ [0]*(len(self.channels) - len(x))+x for x in notbitarray ]
        newthingarray = []
        for ba in notbitarray:
            newthing = [0 for i in range(16)]
            for ele, ch in zip(ba, self.channels):
                newthing[ch] = ele
            newthing.reverse()
            newthingarray.append(newthing)
        realbitarray = [self.list_to_bin(ele) for ele in newthingarray]
        self.bitarray = realbitarray

def chan_to_bit(chan_list):
    bitthing = 0
    for ch in chan_list:
        bitthing += (1 << ch )
    return (bitthing << 16)
    
if __name__ == '__main__':
    args=parser()
    sc = scout_configure(args.host, args.port)
    sc.write_to_json()
    sc.push_to_struck()
