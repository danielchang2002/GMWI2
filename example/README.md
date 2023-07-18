# Example usage of GMWI2

GMWI2 (Gut Microbiome Wellness Index 2) is a robust and biologically interpretable predictor of health status based on gut microbiome taxonomic profiles.

Below is a mini-tutorial on how to download a metagenome sample (run accession SRR1761666, a healthy sample belonging to the pooled dataset of 8,069 stool metagenomes used to trained GMWI2) from the Sequence Read Archive (SRA) and use this command-line tool on the downloaded .fastq files to compute the GMWI2 score.

## Download and uncompress fastq files using [sra-tools](https://github.com/ncbi/sra-tools/wiki/)

```bash
prefetch SRR1761666
cd SRR1761666
fasterq-dump SRR1761666.sra --skip-technical --split-files
```

Output:
```bash
.
├── SRR1761666.sra
├── SRR1761666_1.fastq
└── SRR1761666_2.fastq
```

## Run GMWI2 on the extracted paired-end metagenome reads using 16 threads
```bash
gmwi2 -i SRR1761666_1.fastq,SRR1761666_2.fastq -n 16 -o SRR1761666
```

Output:
```bash
.
├── SRR1761666.sra
├── SRR1761666_1.fastq
├── SRR1761666_2.fastq
├── SRR1761666_GMWI2.txt
├── SRR1761666_GMWI2_taxa.txt
└── SRR1761666_metaphlan.txt
```

## Verify that your output files are identical to those in this directory and shown below

```bash
head *.txt
```

Output:
```bash
==> SRR1761666_GMWI2.txt <==
1.8352371587787006

==> SRR1761666_GMWI2_taxa.txt <==
taxa_name	coefficient
k__Bacteria|p__Actinobacteria|c__Actinobacteria|o__Actinomycetales|f__Actinomycetaceae|g__Actinomyces	-0.002971706718511846
k__Bacteria|p__Actinobacteria|c__Coriobacteriia|o__Eggerthellales	0.10985985383440176
k__Bacteria|p__Actinobacteria|c__Coriobacteriia|o__Eggerthellales|f__Eggerthellaceae	0.058580915614315394
k__Bacteria|p__Bacteroidetes|c__Bacteroidia|o__Bacteroidales|f__Prevotellaceae|g__Prevotella|s__Prevotella_copri	0.019327473574940728
k__Bacteria|p__Bacteroidetes|c__Bacteroidia|o__Bacteroidales|f__Prevotellaceae|g__Prevotella|s__Prevotella_sp_AM42_24	0.20713868303104763
k__Bacteria|p__Firmicutes|c__Clostridia|o__Clostridiales|f__Clostridiaceae	-0.016769603426408927
k__Bacteria|p__Firmicutes|c__Clostridia|o__Clostridiales|f__Eubacteriaceae|g__Eubacterium|s__Eubacterium_eligens	0.15173013105151076
k__Bacteria|p__Firmicutes|c__Clostridia|o__Clostridiales|f__Eubacteriaceae|g__Eubacterium|s__Eubacterium_hallii	0.05692133949999932
k__Bacteria|p__Firmicutes|c__Clostridia|o__Clostridiales|f__Lachnospiraceae|g__Blautia|s__Ruminococcus_torques	0.14658685040674785

==> SRR1761666_metaphlan.txt <==
#mpa_v30_CHOCOPhlAn_201901
#/Users/daniel/opt/anaconda3/envs/gmwi2_env/bin/metaphlan SRR1761666_1.fastq,SRR1761666_2.fastq --index mpa_v30_CHOCOPhlAn_201901 --bowtie2out bowtie2out.bowtie2.bz2 --nproc 16 --input_type fastq -o SRR1761666_metaphlan.txt --add_viruses --unknown_estimation
#SampleID	Metaphlan_Analysis
#clade_name	NCBI_tax_id	relative_abundance	additional_species
UNKNOWN	-1	61.19317	
k__Bacteria	2	38.73979484943826	
k__Viruses	10239	0.0670310303421447	
k__Bacteria|p__Bacteroidetes	2|976	20.26310443428757	
k__Bacteria|p__Firmicutes	2|1239	15.384543125636853	
k__Bacteria|p__Actinobacteria	2|201174	3.067314801633372	
```
