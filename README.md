# GMWI2: Gut Microbiome Wellness Index 2
![poop computer chip](https://raw.githubusercontent.com/danielchang2002/GMWI2/main/poop.jpeg)
(Image generated via OpenAI DALL·E 2 with prompt: "3D render of GPU chip in the form of a poop emoji, digital art")

### Description

GMWI2 (Gut Microbiome Wellness Index 2) is a robust and biologically interpretable predictor of health status based on the gut microbiome.

On a stool metagenome sample, GMWI2 performs three major steps:
1. Taxonomic profiling using MetaPhlAn3 (v3.0.13)
2. Transformation of taxonomic relative abundances into a binary presence/absence profile
3. Computation of the GMWI2 score using a Lasso-penalized logistic regression model trained on a meta-dataset of 8,069 health status labeled stool shotgun metagenomes

If you use GMWI2, please cite:

TODO

### Installation

To avoid dependency conflicts, please create an isolated conda environment and 
install GMWI2. Installation via conda/mamba automatically installs GMWI2 and 
its dependencies (MetaPhlAn3).

1. Create new conda environment and install mamba
```bash
conda create --name gmwi2_env mamba python=3.8
```

2. Activate environment
```bash
conda activate gmwi2_env
```

3. Install GMWI2 package with mamba
```bash
mamba install -c danielchang2002 -c bioconda -c conda-forge gmwi2
```

### Usage

Try downloading and running GMWI2 on an example metagenome.

