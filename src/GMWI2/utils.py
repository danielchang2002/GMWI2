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

def logo():
  splits = [(0, 9), (9, 20), (20, 30), (30, 33), (33, 41)]

  colors = [
    bcolors.HEADER,
    bcolors.OKBLUE,
    bcolors.OKCYAN,
    bcolors.OKGREEN,
    bcolors.WARNING,
  ]

  text = "\n".join([
  "".join([color + st[split[0]:split[1]] + bcolors.ENDC for color, split in zip(colors, splits)])
  for st in string.split("\n")[1:-1]])
  gmwi2_logo = text

  return gmwi2_logo