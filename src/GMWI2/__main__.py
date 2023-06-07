import os
import sys
from . import utils
import argparse
from . import prerun
from . import pipeline
import argparse
import subprocess
from argparse import RawTextHelpFormatter

__author__ = "Daniel Chang, Vinod Gupta, Jaeyun Sung"
__version__ = "1.0"

def main():
    parser = argparse.ArgumentParser(
        description="\n" + utils.logo() + 
        "\n\nDESCRIPTION:\n"
        "GMWI2 version " + __version__ + " \n"
        "GMWI2 (Gut Microbiome Wellness Index 2) is a [insert description].\n\n" 
        "AUTHORS: \n" + __author__ + "\n\n"
        "USAGE: \n"
        "GMWI2 is a pipeline that takes as input raw fastq (or fastq.gz) files generated "
        "from a metagenome, "
        "estimates microbial abundances, "
        "and using these microbial estimates, "
        "returns as output the GMWI2 score \n\n"
        "* Example usage (single end):\n\n"
        "$ ls\n"
        ".\n"
        "└── metagenome.fastq\n\n"
        "$ gmwi2 -i metagenome.fastq -n 8 -o output_prefix\n\n"
        "$ ls\n"
        ".\n"
        "├── metagenome.fastq\n"
        "├── output_prefix_GMWI2.txt\n"
        "└── output_prefix_metaphlan.txt\n\n"
        "* Example usage (paired end):\n\n"
        "$ ls\n"
        ".\n"
        "├── forward.fastq\n"
        "└── reverse.fastq\n\n"
        "$ gmwi2 -i forward.fastq,reverse.fastq -n 8 -o output_prefix\n\n"
        "$ ls\n"
        ".\n"
        "├── forward.fastq\n"
        "├── reverse.fastq\n\n"
        "├── output_prefix_GMWI2.txt\n"
        "└── output_prefix_metaphlan.txt\n\n"
        "The two output files are: \n"
        "(i) output_prefix_GMWI2.txt: GMWI2 score\n"
        "(ii) output_prefix_metaphlan.txt: MetaPhlAn3 taxonomic profiling output",
        formatter_class=RawTextHelpFormatter,
    )
    requiredNamed = parser.add_argument_group("required named arguments")
    requiredNamed.add_argument(
        "-n", "--num_threads", required=True, help="number of threads", type=int
    )
    requiredNamed.add_argument(
        "-i", "--input", required=True, help="metagenome (.fastq) file(s)", type=str
    )
    requiredNamed.add_argument(
        "-o", "--output", required=True, help="prefix to designate output file names", type=str
    )

    parser.add_argument("-v", '--version', action='version', version=f"GMWI2 version {__version__}")

    if len(sys.argv) == 1:
        parser.print_help()
        return

    args = parser.parse_args()

    input_files = args.input.split(",")

    for f in input_files:
      if not os.path.exists(f):
        print("input file(s) do not exist")
        return

    utils.print_logo()
    print()
    
    up_to_date = prerun.check_dependencies()
    if not up_to_date:
        print("GMWI2 aborted", u"\U0001F4A9")
        return
        
    pipeline.run(args)

if __name__ == "__main__":
    main()