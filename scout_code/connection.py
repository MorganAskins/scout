#!/usr/bin/env python2

import subprocess
import os, sys
import argparse
import errno
import time

class sis_connection():
    '''
    Monitors the connection through ethernet with the sis3316
    '''
    def __init__(self, interface, host):
        # Check to see if the card is already connected
        self.sis_ip = self.sis_address()
        # If not make a connection
        if self.sis_ip is None:
            self.connect(interface, host)

    def connect(self, iface, host):
        self.ifconfig('%s down' % iname)
        self.ifconfig('%s %s' % (iname, host))
        self.ifconfig('%s up' % iname)
        self.dhcpd(2, quiet=True)
        self.sis_ip = self.sis_address()
        return sis_ip

    def ifconfig(self, args):
        cmd = ('ifconfig %s' % args).split()
        output_kw = {'stdout': subprocess.PIPE, 'stderr': subprocess.PIPE}
        sp = subprocess.Popen(cmd, **output_kw)
        status = sp.wait()
        error = sp.stderr.read().lower()
        if status and 'operation not permitted' in error:
            raise OSError(errno.EACCES, 'Permision denied, run as root')

    def dhcpd(self, sleep, quiet):
        cmd = 'dhcpd'.split()
        output_kw = {'stdout': subprocess.PIPE, 'stderr': subprocess.PIPE}
        # stop dhcpd
        clear_cmd = 'sudo pkill dhcpd'.split()
        sp = subprocess.Popen(clear_cmd, **output_kw)
        sp.wait()
        # clear dhcpd leases
        fname = '/var/lib/dhcpd/dhcpd.leases'
        os.remove(fname)
        os.remove(fname+'~')
        with open(fname, 'a'):
            os.utime(fname, None)
        # continue
        sp = subprocess.Popen(cmd, **output_kw)
        status = sp.wait()
        error = sp.stderr.read().lower()
        if status and 'exiting' in error:
            raise OSError(errno.EACCES, 'Permision denied, run as root')
        for t in range(sleep):
            if not quiet:
                sys.stderr.write('%i\r' % (sleep-t))
            time.sleep(1)

    def sis_address(self):
        '''
        Check the dhcp leases file to find out if there
        is a card that has been given an IP address in
        the past. Then ping the card and see if it is
        connected
        '''
        fname = '/var/lib/dhcpd/dhcpd.leases'
        pairs = {}
        lease = ''
        host = ''
        address = None
        with open(fname, 'r') as f:
            for line in f:
                line = line.strip(' ')
                if line.startswith('lease'):
                    lease = line.split()[1]
                if line.startswith('client-hostname'):
                    host = line.split()[1].strip(';').strip('"')
                    pairs[host] = lease
        for k,v in pairs.iteritems():
            if 'sis3316' in k:
              address = v
        if address:
            try: 
                output = subprocess.check_output('ping -c 1 %s' % address, shell=True)
                return address
            except Exception, e:
                pass
        return None
        
def main(args):
  # User likely needs root permissions to configure the network card
  # this is unless the interface is already configured
  connection = sis_connection(args.interface, args.address)
  print 'SIS3316 connect at IP: %s' % connection.sis_ip

def get_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('-i', '--interface', type=str, default='eno1',
      help="Ethernet interface to SIS3316")
  parser.add_argument('-a', '--address', type=str, default='192.168.1.1',
      help="IP Address of this machine")
  return parser.parse_args()

if __name__ == '__main__':
  main(get_args())
