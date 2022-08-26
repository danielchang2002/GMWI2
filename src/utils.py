import numpy as np
from scipy.stats import wilcoxon
import matplotlib.pyplot as plt
import os
import config

def plot_longitudinal(meta, index, timepoints_sorted, study):
    """
    meta is a df that has columns: ["timepoint", "timepoint_plot", index]
    """
    subjects = np.unique(meta.index)
    plt.figure(figsize=(10, 10), dpi=200)
    for subject in subjects:
        df = meta.loc[subject].copy()
        df = df.sort_values("timepoint_plot")
        plt.plot(df["timepoint_plot"], df[index], c="gray", zorder=0)
    plt.ylabel(index, fontsize=18)
    plt.xlabel("Time point", fontsize=18)

    for i, time in enumerate(timepoints_sorted):
        data = meta[meta["timepoint"] == time][index]
        sc = plt.scatter(np.ones(data.shape[0]) * i, data)
        c = sc.get_facecolors()[0].tolist()
        width = 3.0
        bp = plt.boxplot(data, positions=[i], patch_artist=True, widths=[0.5],
            boxprops=dict(facecolor=[0, 0, 0, 0], color=c, linewidth=width),
            capprops=dict(color=c, linewidth=0),
            whiskerprops=dict(color=c, linewidth=width),
            flierprops=dict(color=c, markeredgecolor=c, linewidth=width),
            medianprops=dict(color=c, linewidth=width),
                        )
    baseline = timepoints_sorted[0]
    baseline_df = meta[meta["timepoint"] == baseline]
    for i, timepoint in enumerate(timepoints_sorted):
        if i == 0: continue
        timepoint_df = meta[meta["timepoint"] == timepoint]
        subjects_in_both = set(baseline_df.index) & set(timepoint_df.index)
        timepoint_df = timepoint_df.loc[subjects_in_both]
        baseline_df = baseline_df.loc[subjects_in_both]
        stat = wilcoxon(baseline_df[index], timepoint_df[index])
        x = i
        y = meta[index].max() * 1.05
        text = "$P = " + '%.2g' % stat.pvalue + "$" if stat.pvalue < 0.05 else "n.s."
        plt.text(x, y, text, ha="center", fontsize=12)

    plt.xticks(ticks=list(range(len(timepoints_sorted))), labels=timepoints_sorted, fontsize=14)
    plt.yticks(fontsize=14)
    bottom, top = plt.ylim()
    plt.ylim(bottom, top * 1.05)
    plt.savefig(os.path.join(config.FIGURE_DIR, study + "_" + index.replace(" ", "_") + ".svg"))
    plt.show()