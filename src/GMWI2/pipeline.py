import subprocess
from . import utils
import os

def run(args):

  # run metaphlan
  subprocess.call([
    "metaphlan",
    args.input,
    "--nproc",
    args.num_threads,
    "--input_type",
    "fastq",
    "-o",
    args.output + "_metaphlan.txt",
    "--add_viruses",
    "--unknown_estimation",
  ])

  # compute gmwi2