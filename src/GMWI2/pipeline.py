import subprocess
from . import utils
import os
import pandas as pd
from joblib import load
import numpy as np
from time import sleep
import traceback

def run(args):

  # -----------------------install database -----------------------------------
  print("Installing MetaPhlAn database (this may take a while): ", end="")

  with utils.Spinner():
    command = [
      "metaphlan",
      "--install",
      "--index", 
      "mpa_v30_CHOCOPhlAn_201901",
    ]
    proc = subprocess.Popen(command, stderr=subprocess.PIPE)

    stderr = proc.stderr.read().decode("utf-8") 

  if "MD5 checksums do not correspond!" in stderr:
    # fail
    print(u"\u274C")

    print(stderr)

    print("GMWI2 aborted", u"\U0001F4A9")
    return
  else:
    # success
    print(u"\u2705")
  # -----------------------install database -----------------------------------




  # -----------------------run metaphlan-----------------------------------
  print("Profiling metagenome: ", end="")

  with utils.Spinner():
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
    # success
    print(u"\u2705")
  else:
    print(u"\u274C")
    print(stderr)
    print("GMWI2 aborted", u"\U0001F4A9")
    return
  # -----------------------run metaphlan-----------------------------------




  # -----------------------compute gmwi2-----------------------------------
  print("Computing GMWI2: ", end="")

  gmwi2_error = None

  with utils.Spinner():
    try:
      compute_gmwi2(args)
    except Exception as e:
      gmwi2_error = traceback.format_exc()

  if gmwi2_error:
    print(u"\u274C")
    print(gmwi2_error)
    print("GMWI2 aborted", u"\U0001F4A9")
    return
  else:
    print(u"\u2705")
  # -----------------------compute gmwi2-----------------------------------

  # cleanup
  subprocess.call(["rm", "bowtie2out.bowtie2.bz2"])

  print("GMWI2 great success!", u"\U0001F4A9")

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
