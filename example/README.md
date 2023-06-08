# Example usage of GMWI2

GMWI2 is ...

Below is a mini-tutorial on how to download a metagenome sample (run accession x) from the Sequence Read Archive (SRA) and use GMWI2 on the downloaded .fastq files.

## Download and uncompress fastq files using [sra-tools](https://github.com/ncbi/sra-tools/wiki/)

```bash
prefetch x
cd x
fasterq-dump x.sra --skip-technical --split-files
```

Output:
```bash
.
├── x.sra
├── x_1.fastq
└── x_2.fastq
```

## Run GMWI2 on the extracted paired-end metagenome reads
```bash
gmwi2 -n 8 -f x_1.fastq,x_2.fastq -o x
```

Output:
```bash
.
├── SRR6915153.sra
├── SRR6915153_1.fastq
├── SRR6915153_2.fastq
├── SRR6915153_BGC_FINAL_RESULT.txt
├── SRR6915153_BGC_metsp.txt
└── SRR6915153_coverage_stats_taxibgc2022.txt
```

## Verify that your output files are identical to those shown below
Note: Slight differences in the output may occur due to updates to the marker databases or differences in versions of dependencies.

```bash
head *.txt
```

Output:
```bash
```
