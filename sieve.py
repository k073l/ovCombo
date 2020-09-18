import os
import logging
import datetime
import re

DEBUG = False

log = logging.getLogger('Sieve-Logger')  # Creating logger
if DEBUG:
    log.setLevel(logging.DEBUG)  # Setting logging level to DEBUG
log.addHandler(logging.StreamHandler())  # Adding StreamHandler


class Sieve:
    """
    Prepare file for further usage
    """
    def __init__(self, date: bool, outfile: str):
        """
        Initialize class, introduce variables
        :type outfile: str
        :type date: bool
        :param date: Is file formatted with date (see README)
        :param outfile: Filename to save outfile as
        """
        for filename in os.listdir(os.getcwd()):
            if filename.endswith('.txt'):
                log.debug(f'Combo: {filename}')
                self.combo_in = filename
        self.outfile = outfile
        self.today = datetime.datetime.now().date()
        log.debug(f'Today\'s date: {self.today}')
        self.date = date
        log.debug(f'Is date used in combo? {date}')
        if self.date:
            self.eligible = []  # List to store lines with dates older than today

    def filter(self):
        """
        Check date if present, add to list for saving
        :return: Nothing
        """
        with open(self.combo_in, 'r') as combo:  # Read combo
            lines = combo.readlines()
            for line in lines:
                if self.date:  # If true, then combo has supported date formatting
                    log.debug(f'Line: {line.strip()}')
                    self.eligible.append(line)
                    unformatted_combo_date = re.search(r' \| (\d+-\d+-\d+) (\d+:\d+:\d+)', line)
                    log.debug(f'Is date present? {unformatted_combo_date}')
                    if unformatted_combo_date:
                        unformatted_combo_date = unformatted_combo_date.group(1)
                        formatted_combo_date = datetime.datetime.strptime(unformatted_combo_date, "%Y-%m-%d").date()
                        if formatted_combo_date > self.today:
                            log.debug(f'Found date older than today: {formatted_combo_date}')
                            self.eligible.append(line)
                    else:
                        self.eligible.append(line)
                else:
                    self.eligible.append(line)  # If false all files are eligible

    def write(self):
        """
        Saves file as filename set earlier, removes dates
        :return: Path to outfile
        """
        try:
            os.mkdir('output')
        except FileExistsError:
            pass
        self.eligible = list(dict.fromkeys(self.eligible))  # Convert list to dict and back to dict to remove duplicates
        with open('output/' + self.outfile, 'w') as output:
            for line in self.eligible:
                if self.date:
                    line = re.sub(r' \| (\d+-\d+-\d+) (\d+:\d+:\d+)', '', line)
                output.write(line)
        return 'output/' + self.outfile


if __name__ == '__main__':
    sv = Sieve(date=True, outfile='out.txt')
    sv.filter()
    sv.write()

