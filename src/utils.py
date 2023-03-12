import numpy as np
from scipy.stats import wilcoxon, kendalltau
from sklearn.metrics import confusion_matrix
import pandas as pd
import matplotlib.pyplot as plt
import os
import config

def plot_longitudinal(meta, indices, timepoints_sorted, study, stars=False, show_tau=False, alternative="two-sided"):
    """
    meta is a df that has columns: ["timepoint", "timepoint_plot", index]
    """
    fig, axs = plt.subplots(ncols=len(indices), figsize=(10 * len(indices), 10), dpi=200)
    for index, ax in zip(indices, axs):
        # plot each subject's longitudinal line
        subjects = np.unique(meta.index)
        for subject in subjects:
            df = meta.loc[[subject]].copy()
            df = df.sort_values("timepoint_plot")
            ax.plot(df["timepoint_plot"], df[index], c="gray", zorder=0)
        ax.set_ylabel(index, fontsize=18)
        ax.set_xlabel("Time point", fontsize=18)

        # compute significance from baseline for each timepoint
        for i, time in enumerate(timepoints_sorted):
            data = meta[meta["timepoint"] == time][index]
            sc = ax.scatter(np.ones(data.shape[0]) * i, data)
            c = sc.get_facecolors()[0].tolist()
            width = 3.0
            bp = ax.boxplot(data, positions=[i], patch_artist=True, widths=[0.5],
                boxprops=dict(facecolor=[0, 0, 0, 0], color=c, linewidth=width),
                capprops=dict(color=c, linewidth=0),
                whiskerprops=dict(color=c, linewidth=width),
                flierprops=dict(color=c, markeredgecolor=c, linewidth=width),
                medianprops=dict(color=c, linewidth=width),
                            )

        ran = meta[index].max() - meta[index].min()

        y = meta[index].max() + ran * 0.05
        y2 = meta[index].max() + ran * 0.1

        baseline = timepoints_sorted[0]
        baseline_df = meta[meta["timepoint"] == baseline]
        for i, timepoint in enumerate(timepoints_sorted):
            if i == 0: continue
            timepoint_df = meta[meta["timepoint"] == timepoint]
            subjects_in_both = set(baseline_df.index) & set(timepoint_df.index)
            timepoint_df = timepoint_df.loc[subjects_in_both]
            baseline_df_curr = baseline_df.loc[subjects_in_both]
            if timepoint_df.shape[0] == 0 or baseline_df_curr.shape[0] == 0:
                wilcoxon_p = 1
                tau_p = 1
            else:
                stat = wilcoxon(baseline_df_curr[index], timepoint_df[index], alternative=alternative)
                wilcoxon_p = stat.pvalue
                stat = kendalltau(baseline_df_curr[index], timepoint_df[index])
                tau, tau_p = stat
                
            x = i
            
            if stars:
                text = "****" if wilcoxon_p <= 0.0001 else "***" if wilcoxon_p <= 0.001 else "**" if wilcoxon_p <= 0.01 else "*" if wilcoxon_p <= 0.05 else "n.s."
            else:
#                 text = "$P = " + '%.2g' % wilcoxon_p + "$" if wilcoxon_p < 0.05 else "n.s."
                text = "$P = " + '%.2g' % wilcoxon_p + "$"
            ax.text(x, y, text, ha="center", fontsize=10)
            
            if show_tau and tau_p < 0.05:
                ax.text(x, y2, r"$\tau$ = " + '%.2g' % tau, ha="center", fontsize=14)

        ax.set_xticks(ticks=list(range(len(timepoints_sorted))))
        ax.set_xticklabels(labels=timepoints_sorted, fontsize=14)
        ax.tick_params(axis="y", labelsize=14)
        bottom, top = ax.get_ylim()
        ax.set_ylim(bottom, ran * 0.05 + (y2 if show_tau else y))

    plt.savefig(os.path.join(config.FIGURE_DIR, study + ".svg"))


def get_diversity(meta, X):
    X_species = X[[col for col in X.columns if "s__" in col and "virus" not in col and "unclassified" not in col]]
    meta = meta.copy()
    meta["Species Richness"] = np.sum(X_species > config.PRESENCE_CUTOFF, axis=1).values
    meta["Shannon Diversity"] = np.sum(-1 * (X_species * np.log(X_species)).fillna(0).values, axis=1)
    meta["Simpson Diversity"] = np.sum((X_species ** 2).values, axis=1)
    return meta

def confusion(logit, y, cutoff):
    idx = (abs(logit) >= cutoff).values
    y_curr = y[idx]
    logit_curr = logit[idx]
    mat = confusion_matrix(y_curr, logit_curr > 0)
    tn, fp, fn, tp = mat.ravel()
    df = pd.DataFrame(np.array([
            [fp, tn, tn / (tn + fp)], 
            [tp, fn, tp / (tp + fn)]
        ]), 
        columns=["Predicted Healthy", "Predicted Nonhealthy", "Accuracy"], 
        index=["Actual Nonhealthy", "Actual healthy"])
    return df