import subprocess
from . import utils
import os
import pandas as pd
from joblib import load
import numpy as np
from time import sleep
import traceback
from halo import Halo
import gzip
import zipfile
import shutil
import sys

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

def rm_r(path):
  if os.path.isdir(path) and not os.path.islink(path):
      shutil.rmtree(path)
  elif os.path.exists(path):
      os.remove(path)

def check_GRCh38():
  database_dir = os.path.join(utils.DEFAULT_DB_FOLDER, "GRCh38_noalt_as")
  hash_dir = os.path.join(utils.DEFAULT_DB_FOLDER, "GRCh38_md5sum.txt")
  if not os.path.exists(database_dir):
    return False

  cur = os.getcwd()
  os.chdir(database_dir)

  proc = subprocess.Popen(
      ["md5sum", "-c", hash_dir], stdout=subprocess.PIPE, stderr=subprocess.PIPE
  )
  os.chdir(cur)
  proc.communicate()
  return proc.returncode == 0

def dependency_checks():
  print(
        "-" * 11,
        "Dependency checks",
        "-" * 11,
  )

  # -----------------------check metaphlan-------------------------------------
  spinner = Halo(text="MetaPhlAn v3.0.13", spinner=spin)
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
    spinner.fail()
    if correct:
          printw(output.split("\n")[0])
          printw("Incorrect version of MetaPhlAn")
    else:
          printw("MetaPhlAn not found on path")
    printw('Please run: "mamba install -c bioconda metaphlan=3.0.13"')
    printr("GMWI2 aborted " + poop)
    sys.exit()
  else:
    spinner.succeed()
  # -----------------------check metaphlan-------------------------------------



  # -----------------------check other dependencies----------------------------
  dependencies = ["repair.sh", "fastqc", "bowtie2", "samtools", "bedtools", "trimmomatic"]
  for d in dependencies:
    spinner = Halo(text=d, spinner=spin)
    spinner.start()

    try:
        proc = subprocess.Popen(
            [d, "--version" if d != "trimmomatic" else "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        output = proc.stdout.read().decode("ASCII")
        proc.communicate()
        correct = proc.returncode == 0
    except:
        correct = False

    if not correct:
      spinner.fail()
      printw(f"{d} not found on path")
      install = d if d != "repair.sh" else "bbmap"
      printw(f'Please run: "mamba install -c bioconda {install}"')
      printr("GMWI2 aborted " + poop)
      sys.exit()
    else:
      spinner.succeed()

  print(
        "-" * 41,
        "\n"
  )

def database_installation():
  print(
        "-" * 9,
        "Database installation",
        "-" * 9,
  )
  spinner = Halo(text="Installing MetaPhlAn marker database", spinner=spin)
  spinner.start()

  command = [
    "metaphlan",
    "--install",
    "--index", 
    "mpa_v30_CHOCOPhlAn_201901",
  ]
  proc = subprocess.Popen(command, stderr=subprocess.PIPE)

  stderr = proc.stderr.read().decode("utf-8") 

  proc.communicate()
  incorrect = proc.returncode != 0

  if "MD5 checksums do not correspond!" in stderr or incorrect:
    spinner.fail()
    printw(stderr)
    printr("GMWI2 aborted " + poop)
    sys.exit()
  else:
    spinner.succeed()


  spinner = Halo(text="Downloading GRCh38/hg38", spinner=spin)
  spinner.start()

  if not check_GRCh38():
    target_dir = os.path.join(utils.DEFAULT_DB_FOLDER)
    zip_location = os.path.join(target_dir, "GRCh38_noalt_as.zip")

    rm_r(os.path.join(target_dir, "GRCh38_noalt_as"))
    rm_r(zip_location)

    url = "https://genome-idx.s3.amazonaws.com/bt/GRCh38_noalt_as.zip"
    proc = subprocess.Popen(f"wget -q -P {target_dir} {url}", shell=True, stderr=subprocess.PIPE)

    stderr = proc.stderr.read().decode("utf-8") 

    proc.communicate()
    incorrect = proc.returncode != 0

    if incorrect:
      spinner.fail()
      printw(stderr)
      printr("GMWI2 aborted " + poop)
      sys.exit()

    zip_location = os.path.join(target_dir, "GRCh38_noalt_as.zip")

    error = None
    try:
      with zipfile.ZipFile(zip_location, 'r') as zip_ref:
        zip_ref.extractall(target_dir)
    except Exception as e:
       error = traceback.format_exc()

    if error:
      spinner.fail()
      printw(error)
      printr("GMWI2 aborted " + poop)
      sys.exit()

    rm_r(zip_location)

  spinner.succeed()
  print(
        "-" * 41,
        "\n"
  )

def copy_input(args):
  spinner = Halo(text="Extracting/copying fastq files", spinner=spin)
  spinner.start()

  # copy and optionally extract input files
  forward = f"{args.output_prefix}_in1.fastq"
  reverse = f"{args.output_prefix}_in2.fastq"

  try:
    for user_input, target in [(args.forward, forward), (args.reverse, reverse)]:
      if user_input.endswith(".fastq.gz"):
        with gzip.open(user_input, 'rb') as f_in:
            with open(target, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
      else:
        shutil.copy(user_input, target)
  except Exception as e:
    error = traceback.format_exc()
    spinner.fail()
    printw(error)
    printr("GMWI2 aborted " + poop)
    sys.exit()

  spinner.succeed()

def repair_reads(args):
  spinner = Halo(text="Re-pairing reads", spinner=spin)
  spinner.start()
  command = [
    "repair.sh",
    f"in1={args.output_prefix}_in1.fastq",
    f"in2={args.output_prefix}_in2.fastq",
    f"out1={args.output_prefix}_repaired1.fastq",
    f"out2={args.output_prefix}_repaired2.fastq",
    "outs=/dev/null"
  ]
  proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  stderr = proc.stderr.read().decode("utf-8") 
  proc.communicate()

  if proc.returncode != 0:
    spinner.fail()
    printw(stderr)
    printr("GMWI2 aborted " + poop)
    sys.exit()

  spinner.succeed()

  # remove input
  rm_r(f"{args.output_prefix}_in1.fastq")
  rm_r(f"{args.output_prefix}_in2.fastq")

def overrepresented(args):
  spinner = Halo(text="Extracting overrepresented sequences", spinner=spin)
  spinner.start()

  output_dir = os.path.dirname(args.output_prefix)

  command = [
    "fastqc",
    f"{args.output_prefix}_repaired1.fastq",
    "--extract",
    "--delete",
    "-o",
    output_dir
  ]
  proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  stderr = proc.stderr.read().decode("utf-8") 
  proc.communicate()

  if proc.returncode != 0:
    spinner.fail()
    printw(stderr)
    printr("GMWI2 aborted " + poop)
    sys.exit()

  command = [
    "fastqc",
    f"{args.output_prefix}_repaired2.fastq",
    "--extract",
    "--delete",
    "-o",
    output_dir
  ]
  proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  stderr = proc.stderr.read().decode("utf-8") 
  proc.communicate()

  if proc.returncode != 0:
    spinner.fail()
    printw(stderr)
    printr("GMWI2 aborted " + poop)
    sys.exit()

  command = """
    for f in """ + args.output_prefix + """_repaired1_fastqc/fastqc_data.txt; do
        echo $f `grep -A100 ">>Overrepresented sequences" $f | \
        grep -m1 -B100 ">>END_MODULE" | \
        grep -P "Adapter|PCR" | awk '{print ">overrepresented_sequences" "_" ++c "/1" $1}'` | \
        awk '{gsub(/\/1/,"/1\n")}1' | \
        awk '{gsub(/>/,"\n>")}1' | \
        awk '{gsub(/fastqc_data.txt/,"")}1' | \
        awk 'NF > 0';
    done > """ + args.output_prefix + """_adapter1.txt

    for f in """ + args.output_prefix + """_repaired2_fastqc/fastqc_data.txt; do
        echo $f `grep -A100 ">>Overrepresented sequences" $f | \
        grep -m1 -B100 ">>END_MODULE" | \
        grep -P "Adapter|PCR" | awk '{print ">overrepresented_sequences" "_" ++c "/1" $1}'` | \
        awk '{gsub(/\/1/,"/1\n")}1' | \
        awk '{gsub(/>/,"\n>")}1' | \
        awk '{gsub(/fastqc_data.txt/,"")}1' | \
        awk 'NF > 0';
    done > """ + args.output_prefix + """_adapter2.txt
  """

  proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

  stderr = proc.stderr.read().decode("utf-8") 
  proc.communicate()

  if proc.returncode != 0:
    spinner.fail()
    printw(stderr)
    printr("GMWI2 aborted " + poop)
    sys.exit()

  spinner.succeed()

  intermediate = [
    "repaired1_fastqc",
    "repaired1_fastqc.html",
    "repaired2_fastqc",
    "repaired2_fastqc.html",
  ]

  intermediate = [f"{args.output_prefix}_{i}" for i in intermediate]

  for f in intermediate:
    rm_r(f)

def open_shell(command, spinner):
  proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

  stderr = proc.stderr.read().decode("utf-8") 
  proc.communicate()

  if proc.returncode != 0:
    spinner.fail()
    printw(stderr)
    printr("GMWI2 aborted " + poop)
    sys.exit()

def human(args):
  spinner = Halo(text="Removing human reads", spinner=spin)
  spinner.start()

  # input: repaired1.fastq, repaired2.fastq
  # output: mapped.sam
  command = f"bowtie2 -p {args.num_threads} -x {os.path.join(utils.DEFAULT_DB_FOLDER, 'GRCh38_noalt_as/GRCh38_noalt_as')} -1 {args.output_prefix}_repaired1.fastq -2 {args.output_prefix}_repaired2.fastq -S {args.output_prefix}_mapped.sam"
  open_shell(command, spinner)
  rm_r(f"{args.output_prefix}_repaired1.fastq")
  rm_r(f"{args.output_prefix}_repaired2.fastq")

  # input: mapped.sam
  # output: mapped.bam
  command = f"samtools view -bS {args.output_prefix}_mapped.sam > {args.output_prefix}_mapped.bam"
  open_shell(command, spinner)
  rm_r(f"{args.output_prefix}_mapped.sam")

  # input: mapped.bam
  # output: human.bam
  command = f"samtools view -b -f 12 -F 256 {args.output_prefix}_mapped.bam > {args.output_prefix}_human.bam"
  open_shell(command, spinner)
  rm_r(f"{args.output_prefix}_mapped.bam")

  # input: human.bam
  # output: human_sorted.bam
  command = f"samtools sort -n {args.output_prefix}_human.bam -o {args.output_prefix}_human_sorted.bam -@ {args.num_threads}"
  open_shell(command, spinner)
  rm_r(f"{args.output_prefix}_human.bam")

  # input: human_sorted.bam
  # output: human1.fastq, human2.fastq
  command = f"bedtools bamtofastq -i {args.output_prefix}_human_sorted.bam -fq {args.output_prefix}_human1.fastq -fq2 {args.output_prefix}_human2.fastq"
  open_shell(command, spinner)
  rm_r(f"{args.output_prefix}_human_sorted.bam")

  spinner.succeed()

def trim(args):
  spinner = Halo(text="Removing adapters and low quality reads", spinner=spin)
  spinner.start()
  
  # input: adapter1.txt, adapter2.txt
  # output: adapters.txt
  truseq = os.path.join(utils.DEFAULT_DB_FOLDER, "TruSeq3-PE.fa")
  open_shell(f"cat {args.output_prefix}_adapter1.txt {args.output_prefix}_adapter2.txt {truseq} > {args.output_prefix}_adapters.txt", spinner)
  rm_r(f"{args.output_prefix}_adapter1.txt")
  rm_r(f"{args.output_prefix}_adapter2.txt")

  # input: adapters.txt, human1.fastq, human2.fastq
  # output: QC_xx.fastq.gz, 
  command = f"trimmomatic PE -threads {args.num_threads} {args.output_prefix}_human1.fastq {args.output_prefix}_human2.fastq "
  command += f"-baseout {args.output_prefix}_QC.fastq.gz ILLUMINACLIP:{args.output_prefix}_adapters.txt:2:30:10:2:keepBothReads LEADING:3 TRAILING:3 MINLEN:60"
  open_shell(command, spinner)
  rm_r(f"{args.output_prefix}_adapters.txt")
  rm_r(f"{args.output_prefix}_human1.fastq")
  rm_r(f"{args.output_prefix}_human2.fastq")

  spinner.succeed()

  rm_r(f"{args.output_prefix}_QC_1U.fastq.gz")
  rm_r(f"{args.output_prefix}_QC_2U.fastq.gz")

def quality_control(args):
  print(
        "-" * 12,
        "Quality control",
        "-" * 12,
  )

  copy_input(args)
  repair_reads(args)
  overrepresented(args)
  human(args)
  trim(args)

  print(
        "-" * 41,
        "\n"
  )

def profile(args):
  spinner = Halo(text='Profiling metagenome', spinner=spin)
  spinner.start()

  command = [
    "metaphlan",
    f"{args.output_prefix}_QC_1P.fastq.gz,{args.output_prefix}_QC_2P.fastq.gz",
    "--index", 
    "mpa_v30_CHOCOPhlAn_201901",
    "--force",
    "--no_map",
    "--nproc",
    str(args.num_threads),
    "--input_type",
    "fastq",
    "-o",
    args.output_prefix + "_metaphlan.txt",
    "--add_viruses",
    "--unknown_estimation",
  ]
  proc = subprocess.Popen(command, stderr=subprocess.PIPE)
  stderr = proc.stderr.read().decode("utf-8") 
  proc.communicate()

  if proc.returncode == 0:
    spinner.succeed()
  else:
    spinner.fail()
    printw(stderr)
    printr("GMWI2 aborted " + poop)
    sys.exit()

  rm_r(f"{args.output_prefix}_QC_1P.fastq.gz")
  rm_r(f"{args.output_prefix}_QC_2P.fastq.gz")

def microbiome_analysis(args):
  print(
        "-" * 10,
        "Microbiome analysis",
        "-" * 10,
  )
  profile(args)

  spinner = Halo(text='Computing GMWI2', spinner=spin)
  spinner.start()

  gmwi2_error = None
  try:
    compute_gmwi2(args)
  except Exception as e:
    gmwi2_error = traceback.format_exc()

  if gmwi2_error:
    spinner.fail()
    printw(gmwi2_error)
    printr("GMWI2 aborted " + poop)
    sys.exit()
  else:
    spinner.succeed()

  print(
        "-" * 41,
        "\n"
  )

def compute_gmwi2(args):
    # load in taxonomic profile
    df = pd.read_csv(args.output_prefix + "_metaphlan.txt", sep="\t", skiprows=3, usecols=[0, 2], index_col=0).T

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
    with open(args.output_prefix + "_GMWI2.txt", "w") as f:
      f.write(f"{score}\n")
    
    # Record relative taxa that are present and have nonzero coef in model
    coefficient_df = pd.DataFrame(gmwi2.coef_, columns=gmwi2.feature_names_in_, index=["coefficient"]).T
    coefficient_df["relative_abundance"] = df.values.flatten()
    coefficient_df = coefficient_df[(coefficient_df["coefficient"] != 0) & (coefficient_df["relative_abundance"] > presence_cutoff)]
    coefficient_df.index.name = "taxa_name"
    coefficient_df = coefficient_df[["coefficient"]]

    coefficient_df.to_csv(args.output_prefix + "_GMWI2_taxa.txt", sep="\t")

def cleanup(args):
  intermediate = [
    # "QC_1P.fastq.gz",
    # "QC_1U.fastq.gz",
    # "QC_2P.fastq.gz",
    # "QC_2U.fastq.gz",
    # "adapter1.txt",
    # "adapter2.txt",
    # "adapters.txt",
    # "human.bam",
    # "human1.fastq",
    # "human2.fastq",
    # "human_sorted.bam",
    # "in1.fastq",
    # "in2.fastq",
    # "mapped.bam",
    # "mapped.sam",
    # "repaired1.fastq",
    # "repaired1_fastqc",
    # "repaired1_fastqc.html",
    # "repaired2.fastq",
    # "repaired2_fastqc",
    # "repaired2_fastqc.html",
  ]

  intermediate = [f"{args.output_prefix}_{i}" for i in intermediate]

  for f in intermediate:
    # don't accidentally delete input files! 
    # For the case where an intermediate file has the same name as an input file
    if f == args.forward or f == args.reverse:
      continue

    rm_r(f)

def run(args):
  dependency_checks()
  database_installation()
  quality_control(args)
  microbiome_analysis(args)
  # cleanup(args)

  printg("GMWI2 great success!" + poop + party1 + party2)
