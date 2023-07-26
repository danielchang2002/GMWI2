# Example usage of GMWI2

GMWI2 (Gut Microbiome Wellness Index 2) is a robust and biologically interpretable predictor of health status based on gut microbiome taxonomic profiles.

Below is a mini-tutorial on how to download a metagenome sample (run accession SRR1761667, a healthy sample belonging to the pooled dataset of 8,069 stool metagenomes used to trained GMWI2) from the Sequence Read Archive (SRA) and use this command-line tool on the downloaded .fastq files to compute the GMWI2 score.

## Download and uncompress fastq files using [sra-tools](https://github.com/ncbi/sra-tools/wiki/)

```bash
prefetch SRR1761667
cd SRR1761667
fasterq-dump SRR1761667.sra --skip-technical --split-files
```

Output:
```bash
.
├── SRR1761667.sra
├── SRR1761667_1.fastq
└── SRR1761667_2.fastq
```

## Run GMWI2 on the extracted paired-end metagenome reads using 16 threads
```bash
gmwi2 -f SRR1761667_1.fastq -r SRR1761667_2.fastq -n 16 -o SRR1761667
```

Output:
```bash
.
├── SRR1761667.sra
├── SRR1761667_1.fastq
├── SRR1761667_2.fastq
├── SRR1761667_GMWI2.txt
├── SRR1761667_GMWI2_taxa.txt
└── SRR1761667_metaphlan.txt
```

## Verify that your output files are identical to those in this directory and shown below

Note: Slight differences in the output may occur due to updates to the marker databases or differences in versions of dependencies.

```bash
head *.txt
```

Output:
```bash
==> SRR1761667_GMWI2.txt <==
1.4017773651306447

==> SRR1761667_GMWI2_taxa.txt <==
taxa_name       coefficient
k__Bacteria|p__Actinobacteria|c__Actinobacteria|o__Bifidobacteriales|f__Bifidobacteriaceae|g__Bifidobacterium|s__Bifidobacterium_adolescentis       0.184438966271142
k__Bacteria|p__Actinobacteria|c__Coriobacteriia|o__Eggerthellales       0.10985985383440176
k__Bacteria|p__Actinobacteria|c__Coriobacteriia|o__Eggerthellales|f__Eggerthellaceae    0.058580915614315394
k__Bacteria|p__Bacteroidetes|c__Bacteroidia|o__Bacteroidales|f__Bacteroidaceae|g__Bacteroides|s__Bacteroides_vulgatus   -0.07104784193156662
k__Bacteria|p__Bacteroidetes|c__Bacteroidia|o__Bacteroidales|f__Prevotellaceae|g__Prevotella|s__Prevotella_copri        0.019327473574940728
k__Bacteria|p__Bacteroidetes|c__Bacteroidia|o__Bacteroidales|f__Prevotellaceae|g__Prevotella|s__Prevotella_sp_AM42_24   0.20713868303104763
k__Bacteria|p__Firmicutes|c__Clostridia|o__Clostridiales|f__Clostridiaceae      -0.016769603426408927
k__Bacteria|p__Firmicutes|c__Clostridia|o__Clostridiales|f__Eubacteriaceae|g__Eubacterium|s__Eubacterium_hallii 0.05692133949999932
k__Bacteria|p__Firmicutes|c__Clostridia|o__Clostridiales|f__Eubacteriaceae|g__Eubacterium|s__Eubacterium_sp_CAG_180     -0.284991033861398

==> SRR1761667_metaphlan.txt <==
#mpa_v30_CHOCOPhlAn_201901
#/Users/daniel/opt/anaconda3/envs/gmwi2_env/bin/metaphlan SRR1761667_QC_1P.fastq.gz,SRR1761667_QC_2P.fastq.gz --index mpa_v30_CHOCOPhlAn_201901 --force --no_map --nproc 16 --input_type fastq -o SRR1761667_metaphlan.txt --add_viruses --unknown_estimation
#SampleID       Metaphlan_Analysis
#clade_name     NCBI_tax_id     relative_abundance      additional_species
UNKNOWN -1      70.84224
k__Bacteria     2       29.031894900524044
k__Archaea      2157    0.1258623750557678
k__Bacteria|p__Firmicutes       2|1239  11.989174109844733
k__Bacteria|p__Proteobacteria   2|1224  11.783008355476293
k__Bacteria|p__Bacteroidetes    2|976   4.101251412438412
```
