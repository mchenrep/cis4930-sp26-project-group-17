
import os
import pandas as pd
import matplotlib.pyplot as plt

def ensure_dirs(*paths):
    for path in paths:
        os.makedirs(path, exist_ok=True)

def save_figure(fig, output_path):
    fig.tight_layout()
    fig.savefig(output_path, dpi=300, bbox_inches="tight")

def summarize_group(df, group_col, metric_cols):
    return df.groupby(group_col)[metric_cols].agg(["count", "mean", "median"]).round(3)

def top_players_by_metric(df, metric, n=10, min_mp=500):
    subset = df[df["MP"] >= min_mp].copy()
    return subset.sort_values(metric, ascending=False)[[["PLAYER", "year_str", "POS", "TEAM", metric, "MP"]]].head(n)
