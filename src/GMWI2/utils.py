import os
from time import sleep
import threading
import sys

# get the directory that contains this script
gmwi2_script_install_folder = os.path.dirname(os.path.abspath(__file__))

# get the default database folder
DEFAULT_DB_FOLDER = os.path.join(gmwi2_script_install_folder, "GMWI2_databases")

class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

string = """
 ██████╗ ███╗   ███╗██╗    ██╗██╗██████╗ 
██╔════╝ ████╗ ████║██║    ██║██║╚════██╗
██║  ███╗██╔████╔██║██║ █╗ ██║██║ █████╔╝
██║   ██║██║╚██╔╝██║██║███╗██║██║██╔═══╝ 
╚██████╔╝██║ ╚═╝ ██║╚███╔███╔╝██║███████╗
 ╚═════╝ ╚═╝     ╚═╝ ╚══╝╚══╝ ╚═╝╚══════╝
"""

dna = """
-. .-.   .-. .-.   .-. .-.   .-. .-.   .-. .-.   .-. .-.   .
||\|||\ /|||\|||\ /|||\|||\ /|||\|||\ /|||\|||\ /|||\|||\ /|
|/ \|||\|||/ \|||\|||/ \|||\|||/ \|||\|||/ \|||\|||/ \|||\||
~   `-~ `-`   `-~ `-`   `-~ `-~   `-~ `-`   `-~ `-`   `-~ `-
"""

def color_dna(d):
  dna_colors = [
     [
      bcolors.OKGREEN,
      bcolors.HEADER,
      bcolors.OKBLUE,
      bcolors.WARNING,
    ],
    [
      bcolors.HEADER,
      bcolors.OKGREEN,
      bcolors.WARNING,
      bcolors.OKBLUE,
    ]
  ]

  splitted = d.split("\n")
  has_nucleotide = [False] * len(splitted[3])

  for line in splitted:
    for i, c in enumerate(line):
      if c == "|":
        has_nucleotide[i] = True


  color_index = 0

  for i, line in enumerate(splitted):
    if "|" not in line: continue

    color_ind = 0

    new_line = []
    for j, c in enumerate(line):
      if has_nucleotide[j] and c == "|":
        new_line.append(dna_colors[color_index][color_ind] + "|" + bcolors.ENDC)
      else:
        new_line.append(c)

      if has_nucleotide[j]:
        color_ind = (color_ind + 1) % 4

    splitted[i] = "".join(new_line)
    color_index += 1

  return "\n".join(splitted)


def logo(rotation=0):
  splits = [(0, 9), (9, 20), (20, 30), (30, 33), (33, 41)]

  colors = [
    bcolors.HEADER,
    bcolors.OKBLUE,
    bcolors.OKCYAN,
    bcolors.OKGREEN,
    bcolors.WARNING,
    bcolors.FAIL,
    bcolors.HEADER,
    ]

  # left_space = " " * ((len(dna.split("\n")[1]) - len(string.split("\n")[1])) // 2 - 1)
  left_space = ""

  text = left_space + ("\n" + left_space).join([
  "".join([color + st[split[0]:split[1]] + bcolors.ENDC for color, split in zip(colors, splits)])
  for st in string.split("\n")[1:-1]])

  # top_dna = "\n".join([line[rotation:] + line[:rotation] for line in dna.split("\n")])
  # bot_dna = "\n".join([line[len(line) - rotation:] + line[:len(line) - rotation] for line in dna.split("\n")])

  # top_dna = color_dna(top_dna)
  # bot_dna = color_dna(bot_dna)

  gmwi2_logo = text

  return gmwi2_logo


def print_logo():
  print(logo())
  # num_iters = 15

  # for i in range(num_iters):
  #   s = logo(rotation=i)
  #   n = len(s.split("\n"))
  #   print(s)

  #   LINE_UP = f'\033[{n}A'
  #   LINE_CLEAR = '\x1b[2K'

  #   if i < num_iters - 1:
  #     print(LINE_UP, end=LINE_CLEAR)

  #   sleep(0.1)

class Spinner:
    busy = False
    delay = 0.1

    @staticmethod
    def spinning_cursor():
        while 1: 
            for cursor in '|/-\\': yield cursor

    def __init__(self, delay=None):
        self.spinner_generator = self.spinning_cursor()
        if delay and float(delay): self.delay = delay

    def spinner_task(self):
        while self.busy:
            sys.stdout.write(next(self.spinner_generator) + " ")
            sys.stdout.flush()
            sleep(self.delay)
            sys.stdout.write('\b\b')
            sys.stdout.flush()

    def __enter__(self):
        self.busy = True
        threading.Thread(target=self.spinner_task).start()

    def __exit__(self, exception, value, tb):
        self.busy = False
        sleep(self.delay)
        if exception is not None:
            return False