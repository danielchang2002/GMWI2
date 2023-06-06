# Figure data for GMWI2 analysis

## 1b

1b_age.csv and 1b_bmi.csv are (new line delimited) lists of age and bmi metadata for the subjects that have this data. (less than half of the subjects have these data)

1b_country.csv and 1b_sex.csv contain country of origin counts and sex counts for the metadataset. N/a columns detail the number of samples that do not have country or sex data.

## 1c

1c_health_status.csv contains health status for all subjects (true = healthy, false = nonhealthy). 

1c_relative_abundance.csv contains taxonomic relative abundances values for all samples. 

I used PCA with binarized presence/absence features in my figure sketch.

## 1d

1d_coefficients.csv contain coefficient values for each taxonomic feature, after training lasso logistic regression on the dataset.

## 1e

1e_violin.csv contain GMWI2, GMWI, and alpha diversity metrics for all samples, along with their health status.

## 1f

1f_phenotypes.csv contains GMWI2 scores for all samples, along with their specific phenotype.

## 1g

For figure 1g, I used the GMWI2 and health status columns from 1e_violin.csv.

## 1h

1h_training_set_performances.csv contains the # of samples retained and the balanced accuracy for varying GMWI2 cutoff values on the training set

## 1i, j, k

Please refer to my slides here:
https://docs.google.com/presentation/d/1PtCsg4VeulQ8FUBEN01onODwC49qm9fE9PjRS_WW5J0/edit#slide=id.p

## 2a

2a_isv_performances.csv contains the # of samples retained and the balanced accuracy for varying GMWI2 cutoff values on inter study validation

## 2b

2b_study_performance.csv contains the balanced accuracy, num healthy, and num nonhealthy for each held out stuyd in interstudy validation.

## 2c

2c_effect.csv contains the species richness, GMWI2 score, and timepoint for the effect group in the Goll et al study: https://www.tandfonline.com/doi/full/10.1080/19490976.2020.1794263

2c_noeffect.csv contains the same, excpet for the no effect group.

Note: the p values in this figure were obtained via the one-sided Wilcoxon signed rank test (instead of two-sided one, like for the rest of the longitudinal analyses)

## 2d

2d_abx_intervention.csv contains GMWI2 scores, species richness, and shannon diversity for all samples and timepoints from Palleja et al: https://www.nature.com/articles/s41564-018-0257-9

## 2e

2e_diet.csv contains GMWI2 scores for samples in all dietary groups during the dietary phase of tanes et al https://www.cell.com/cell-host-microbe/pdfExtended/S1931-3128(20)30674-0
