import os
from sieve import Sieve
from connector import Connector
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Connect to OpenVPN server using combolist')
    parser.add_argument('-ovpn', '--openvpn-path', action='store', dest='ovpn_path', default='ovpn/openvpn.exe',
                        help='Path to openvpn.exe')
    parser.add_argument('-c', '--config', action='store', dest='config_path', help='Path to .ovpn server config file')
    parser.add_argument('-f', '--outfile', action='store', dest='outfile', required=True, help='Filename of combolist '
                                                                                               'with removed '
                                                                                               'outdated combos or '
                                                                                               'filename to be '
                                                                                               'used to convert '
                                                                                               'combolist with dates '
                                                                                               'to one without')
    parser.add_argument('-d', '--date', action='store_true', dest='date', default=True, help='Add this parameter, '
                                                                                             'if your combolist '
                                                                                             'has dates in supported '
                                                                                             'format')
    parser.add_argument('-t', '--timeout', action='store', dest='timeout', default=20,
                        help='Timeout in seconds for OpenVPN to '
                             'connect before proceeding to next combo')

    results = parser.parse_args()
    ovpn_path = results.ovpn_path
    config_path = results.config_path
    outfile = results.outfile
    date = results.date
    timeout = results.timeout

    if any(os.listdir('output/')) == outfile:  # Check if file is existent, if not, remove dates and proceed
        combos = outfile
    else:
        sv = Sieve(date=date, outfile=outfile)
        sv.filter()
        combos = sv.write()

    if config_path is None:
        for filename in os.listdir('ovpn/'):
            if filename.endswith('.ovpn'):
                config_path = filename
                break
    cn = Connector(ovpn_path=ovpn_path, config_path=config_path, combos=combos,
                   timeout=timeout)
    cn.unpack()
    cn.connect()
