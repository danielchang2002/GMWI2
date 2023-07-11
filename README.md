# GMWI2: Gut Microbiome Wellness Index 2

### Description
GMWI2 (Gut Microbiome Wellness Index 2) for Enhanced Health Status Prediction 
from Gut Microbiome Taxonomic Signatures

On a metagenome sample, GMWI2 performs two steps:
1. Taxonomic profiling using MetaPhlAn3 (v3.0.13)
2. 

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

