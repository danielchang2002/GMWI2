import pandas as pd
from joblib import load
import sys
import numpy as np

def main():
    assert(len(sys.argv) == 4)

    taxonomic_profile = sys.argv[1]
    linear_model = sys.argv[2]
    output_prefix = sys.argv[1]

    # load in taxonomic profile
    df = pd.read_csv(taxonomic_profile, sep="\t", skiprows=3, usecols=[0, 2], index_col=0).T

    # load model
    gmwi2 = load(linear_model)

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
    with open(output_prefix + "_GMWI2.txt", "w") as f:
      f.write(f"{score}\n")
    
    # Record relative taxa that are present and have nonzero coef in model
    coefficient_df = pd.DataFrame(gmwi2.coef_, columns=gmwi2.feature_names_in_, index=["coefficient"]).T
    coefficient_df["relative_abundance"] = df.values.flatten()
    coefficient_df = coefficient_df[(coefficient_df["coefficient"] != 0) & (coefficient_df["relative_abundance"] > presence_cutoff)]
    coefficient_df.index.name = "taxa_name"
    coefficient_df = coefficient_df[["coefficient"]]

    coefficient_df.to_csv(output_prefix + "_GMWI2_taxa.txt", sep="\t")

if __name__ == "__main__":
    main()