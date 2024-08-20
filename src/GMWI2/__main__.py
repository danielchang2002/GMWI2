import os
import sys
from . import utils
import argparse
from . import pipeline
import argparse
import subprocess
from argparse import RawTextHelpFormatter

__author__ = "Daniel Chang, Vinod Gupta, Jaeyun Sung"
__version__ = "1.6"

def main():
    parser = argparse.ArgumentParser(
        description="\n" + utils.logo() + 
        "\n\nDESCRIPTION:\n"
        "GMWI2 version " + __version__ + " \n"
        "GMWI2 (Gut Microbiome Wellness Index 2) is a a robust and biologically interpretable "
        "predictor of health status based on the gut microbiome.\n\n" 
        "AUTHORS: \n" + __author__ + "\n\n"
        "USAGE: \n"
        "GMWI2 takes as input raw fastq (or fastq.gz) files generated "
        "from a paired-end stool metagenome, "
        "performs quality control, "
        "estimates microbial abundances, "
        "and using these microbial estimates, "
        "returns as output the GMWI2 score. \n\n"
        "* Example usage:\n\n"
        "$ ls\n"
        ".\n"
        "├── forward.fastq\n"
        "└── reverse.fastq\n\n"
        "$ gmwi2 -f forward.fastq -r reverse.fastq -n 8 -o output_prefix\n\n"
        "$ ls\n"
        ".\n"
        "├── forward.fastq\n"
        "├── reverse.fastq\n"
        "├── output_prefix_GMWI2.txt\n"
        "├── output_prefix_GMWI2_taxa.txt\n"
        "└── output_prefix_metaphlan.txt\n\n"
        "The three output files are: \n"
        "(i) output_prefix_GMWI2.txt: GMWI2 score\n"
        "(ii) output_prefix_GMWI2_taxa.txt: A list of the taxa present in the sample used to compute GMWI2\n"
        "(iii) output_prefix_metaphlan.txt: Raw MetaPhlAn3 taxonomic profiling output",
        formatter_class=RawTextHelpFormatter,
    )
    requiredNamed = parser.add_argument_group("required named arguments")
    requiredNamed.add_argument(
        "-n", "--num_threads", required=True, help="number of threads", type=int
    )
    requiredNamed.add_argument(
        "-f", "--forward", required=True, help="forward-read of metagenome (.fastq/.fastq.gz)", type=str
    )
    requiredNamed.add_argument(
        "-r", "--reverse", required=True, help="reverse-read of metagenome (.fastq/.fastq.gz)", type=str
    )
    requiredNamed.add_argument(
        "-o", "--output_prefix", required=True, help="prefix to designate output file names", type=str
    )

    parser.add_argument("-v", '--version', action='version', version=f"GMWI2 version {__version__}")

    if len(sys.argv) == 1:
        parser.print_help()
        return

    args = parser.parse_args()
    forward, reverse = args.forward, args.reverse
    if not os.path.exists(forward) or not os.path.exists(reverse):
        print("input file(s) do not exist")
        return

    if not os.path.dirname(args.output_prefix) == "" and not os.path.exists(os.path.dirname(args.output_prefix)):
        print("output prefix is invalid")

    # check forward file
    if not forward.endswith(".fastq") and not forward.endswith(".fastq.gz"):
        print("invalid input file extensions")
        return

    # check reverse file
    if not reverse.endswith(".fastq") and not reverse.endswith(".fastq.gz"):
        print("invalid input file extensions")
        return

    print(utils.logo())
    print()
    
    pipeline.run(args)

if __name__ == "__main__":
    main()