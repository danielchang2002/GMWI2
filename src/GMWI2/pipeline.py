import subprocess
from . import utils
import os
import pandas as pd
from joblib import load
import numpy as np
from time import sleep
import traceback
from halo import Halo

success = u"\u2705"
fail = u"\u274C"
poop = u"\U0001F4A9"
spin = "line"
party1 = u"\U0001F973"
party2 = u"\U0001F389"

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

def printw(s):
   print(bcolors.WARNING + s + bcolors.ENDC)

def printg(s):
   print(bcolors.BOLD + bcolors.OKGREEN + s + bcolors.ENDC)
   
def printr(s):
   print(bcolors.BOLD + bcolors.FAIL + s + bcolors.ENDC)

def run(args):
  # -----------------------check metaphlan-------------------------------------
  spinner = Halo(text="Checking for MetaPhlAn v3.0.13 on path", spinner=spin)
  spinner.start()

  try:
      proc = subprocess.Popen(
          ["metaphlan", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
      )
      output = proc.stdout.read().decode("ASCII")
      correct = "MetaPhlAn" in output
      correct_version = "3.0.13" in output
  except:
      correct = False

  if not correct or not correct_version:
    # spinner.stop_and_persist(symbol=fail)
    spinner.fail()
    if correct:
          printw(output.split("\n")[0])
          printw("Incorrect version of MetaPhlAn")
    else:
          printw("MetaPhlAn not found on path")
    printw('Please run: "mamba install -c bioconda metaphlan=3.0.13"')
    printr("GMWI2 aborted " + poop)
    return
  else:
    #  spinner.stop_and_persist(symbol=success)
    spinner.succeed()
  # -----------------------check metaphlan-------------------------------------

  # -----------------------install database -----------------------------------
  spinner = Halo(text='Installing MetaPhlAn database (this may take a while)', spinner=spin)
  spinner.start()

  command = [
    "metaphlan",
    "--install",
    "--index", 
    "mpa_v30_CHOCOPhlAn_201901",
  ]
  proc = subprocess.Popen(command, stderr=subprocess.PIPE)

  stderr = proc.stderr.read().decode("utf-8") 

  if "MD5 checksums do not correspond!" in stderr:
    # spinner.stop_and_persist(symbol=fail)
    spinner.fail()
    printw(stderr)
    printr("GMWI2 aborted " + poop)
    return
  else:
    # spinner.stop_and_persist(symbol=success)
    spinner.succeed()
  # -----------------------install database -----------------------------------




  # -----------------------run metaphlan-----------------------------------
  spinner = Halo(text='Profiling metagenome', spinner=spin)
  spinner.start()

  command = [
    "metaphlan",
    str(args.input),
    # "bowtie2out.bowtie2.bz2",
    "--index", 
    "mpa_v30_CHOCOPhlAn_201901",
    "--bowtie2out",
    "bowtie2out.bowtie2.bz2",
    "--nproc",
    str(args.num_threads),
    "--input_type",
    "fastq",
    # "--input_type",
    # "bowtie2out",
    "-o",
    args.output + "_metaphlan.txt",
    "--add_viruses",
    "--unknown_estimation",
  ]
  proc = subprocess.Popen(command, stderr=subprocess.PIPE)
  stderr = proc.stderr.read().decode("utf-8") 

  if "An additional column listing the merged species is added to the MetaPhlAn output." in stderr:
    # spinner.stop_and_persist(symbol=success)
    spinner.succeed()
  else:
    # spinner.stop_and_persist(symbol=fail)
    spinner.fail()
    printw(stderr)
    printr("GMWI2 aborted " + poop)
    return
  # -----------------------run metaphlan-----------------------------------




  # -----------------------compute gmwi2-----------------------------------
  gmwi2_error = None
  spinner = Halo(text='Computing GMWI2', spinner=spin)
  spinner.start()

  try:
    compute_gmwi2(args)
  except Exception as e:
    gmwi2_error = traceback.format_exc()

  if gmwi2_error:
    # spinner.stop_and_persist(symbol=fail)
    spinner.fail()
    printw(gmwi2_error)
    printr("GMWI2 aborted " + poop)
    return
  else:
    # spinner.stop_and_persist(symbol=success)
    spinner.succeed()
  # -----------------------compute gmwi2-----------------------------------

  # cleanup
  subprocess.call(["rm", "bowtie2out.bowtie2.bz2"])

  printg("GMWI2 great success!" + poop + party1 + party2)

def compute_gmwi2(args):
    # load in taxonomic profile
    df = pd.read_csv(args.output + "_metaphlan.txt", sep="\t", skiprows=3, usecols=[0, 2], index_col=0).T

    # load model
    gmwi2 = load(os.path.join(utils.DEFAULT_DB_FOLDER, "GMWI2_model.joblib"))

    # add dummy columns
    dummy_cols = list(set(gmwi2.feature_names_in_) - set(df.columns))
    dummy_df = pd.DataFrame(np.zeros((1, len(dummy_cols))), columns=dummy_cols, index=["relative_abundance"])
    df = pd.concat([dummy_df, df], axis=1)
    df = df.copy()[["UNKNOWN"] + list(gmwi2.feature_names_in_)]

    # normalize relative abundances
    df = df.divide((100 - df["UNKNOWN"]), axis="rows")
    df = df.drop(labels=["UNKNOWN"], axis=1)

    # compute gmwi2
    presence_cutoff = 0.00001
    score = gmwi2.decision_function(df > presence_cutoff)[0]

    # write results to file
    with open(args.output + "_GMWI2.txt", "w") as f:
      f.write(f"{score}\n")
    
    # Record relative abundances of taxa that are present and have nonzero coef in model
    coefficient_df = pd.DataFrame(gmwi2.coef_, columns=gmwi2.feature_names_in_, index=["coefficient"]).T
    coefficient_df["relative_abundance"] = df.values.flatten()
    coefficient_df = coefficient_df[(coefficient_df["coefficient"] != 0) & (coefficient_df["relative_abundance"] > presence_cutoff)]
    coefficient_df.index.name = "taxa_name"

    coefficient_df.to_csv(args.output + "_GMWI2_taxa.txt", sep="\t")
