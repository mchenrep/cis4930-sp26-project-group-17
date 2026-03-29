
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from functions import ensure_dirs, save_figure

sns.set_theme(style="whitegrid")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(ROOT, "data", "raw")
PROCESSED_DIR = os.path.join(ROOT, "data", "processed")
FIG_DIR = os.path.join(ROOT, "figures")

ensure_dirs(PROCESSED_DIR, FIG_DIR)

DATA_PATH = os.path.join(RAW_DIR, "nba_advanced_stats_2000_2009.csv")

if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(
        f"Could not find dataset at {DATA_PATH}. Put the Kaggle CSV in data/raw/ "
        "and rename it or update DATA_PATH in src/nba_analysis.py."
    )

df = pd.read_csv(DATA_PATH)

# Hand-made pandas objects
example_series = pd.Series({"PER_threshold": 15, "High_TS_threshold": 0.55, "Min_MP": 500})
example_frame = pd.DataFrame({
    "metric": ["PER", "TS%", "USG%"],
    "description": ["efficiency", "shooting efficiency", "usage rate"]
})

# Cleaning
df.columns = [c.strip() for c in df.columns]
if "Unnamed: 0" in df.columns:
    df = df.drop(columns=["Unnamed: 0"])

# Keep years in project range if a broader file is used
if "Year" in df.columns:
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df = df[df["Year"].between(2000, 2009, inclusive="both")].copy()

numeric_candidates = [
    "Age", "G", "GS", "MP", "PER", "TS%", "3PAr", "FTr", "ORB%", "DRB%", "TRB%",
    "AST%", "STL%", "BLK%", "TOV%", "USG%", "OWS", "DWS", "WS", "WS/48",
    "OBPM", "DBPM", "BPM", "VORP", "FG", "FGA", "FG%", "3P", "3PA", "3P%",
    "2P", "2PA", "2P%", "eFG%", "FT", "FTA", "FT%", "ORB", "DRB", "TRB",
    "AST", "STL", "BLK", "TOV", "PF", "PTS"
]
numeric_cols = [c for c in numeric_candidates if c in df.columns]

for c in numeric_cols:
    df[c] = pd.to_numeric(df[c], errors="coerce")

if "Pos" in df.columns:
    df["Pos"] = df["Pos"].astype("category")
if "Tm" in df.columns:
    df["Tm"] = df["Tm"].astype("category")

# Build a datetime column from season year to satisfy date conversion requirement
df["season_end_date"] = pd.to_datetime(df["Year"].astype("Int64").astype(str) + "-06-30", errors="coerce")

# Missing values: strategy 1 = drop rows missing critical identifiers
critical_cols = [c for c in ["Player", "Pos", "Tm", "Year"] if c in df.columns]
df = df.dropna(subset=critical_cols)

# Missing values: strategy 2 = fill selected metrics with median
for c in [col for col in ["PER", "TS%", "USG%", "WS", "BPM", "VORP", "MP"] if col in df.columns]:
    df[c] = df[c].fillna(df[c].median())

# Feature engineering with np.where / apply
if "MP" in df.columns:
    df["minutes_bucket"] = np.where(df["MP"] >= 2000, "heavy_minutes",
                             np.where(df["MP"] >= 1000, "rotation", "limited"))
if "PER" in df.columns:
    df["efficiency_tier"] = df["PER"].apply(
        lambda x: "elite" if x >= 20 else ("above_average" if x >= 15 else "below_average")
    )

# loc / iloc / boolean filtering examples
example_loc = df.loc[df["Pos"].astype(str).str.contains("G", na=False), ["Player", "Year", "Pos", "PER"]].head()
example_iloc = df.iloc[:5, :5]
high_usage = df[df["USG%"] > df["USG%"].median()].copy() if "USG%" in df.columns else df.copy()

# Descriptive stats
desc = df[numeric_cols].describe().round(3)
league_avg_by_year = df.groupby("Year")[["PER", "TS%", "USG%", "WS", "BPM", "VORP"]].mean().round(3)
position_summary = df.groupby("Pos")[["PER", "TS%", "USG%", "WS", "BPM", "VORP"]].agg(["count", "mean", "median"]).round(3)

# Groupby with multi-column aggregation
team_year_summary = (
    df[df["MP"] >= 500]
    .groupby(["Tm", "Year"])
    .agg(
        player_count=("Player", "count"),
        mean_PER=("PER", "mean"),
        mean_TS=("TS%", "mean"),
        mean_WS=("WS", "mean"),
        mean_BPM=("BPM", "mean"),
    )
    .reset_index()
    .sort_values(["Year", "mean_PER"], ascending=[True, False])
)

# Pivot table reshape
position_per_pivot = df.pivot_table(index="Pos", columns="Year", values="PER", aggfunc="mean")

# Save processed outputs
df.to_csv(os.path.join(PROCESSED_DIR, "nba_advanced_stats_2000_2009_cleaned.csv"), index=False)
league_avg_by_year.to_csv(os.path.join(PROCESSED_DIR, "league_avg_by_year.csv"))
team_year_summary.to_csv(os.path.join(PROCESSED_DIR, "team_year_summary.csv"), index=False)
position_per_pivot.to_csv(os.path.join(PROCESSED_DIR, "position_per_by_year_pivot.csv"))

# Figures
fig, ax = plt.subplots(figsize=(10, 5))
league_avg_by_year[["PER", "TS%", "USG%"]].plot(ax=ax, marker="o")
ax.set_title("League Average Advanced Metrics by Season")
ax.set_xlabel("Season End Year")
ax.set_ylabel("Average Metric Value")
save_figure(fig, os.path.join(FIG_DIR, "line_league_metrics_over_time.png"))
plt.close(fig)

fig, ax = plt.subplots(figsize=(9, 5))
pos_order = df.groupby("Pos")["PER"].mean().sort_values(ascending=False).index
sns.barplot(data=df[df["MP"] >= 500], x="Pos", y="PER", order=pos_order, estimator="mean", errorbar=None, ax=ax)
ax.set_title("Average PER by Position (Players with at Least 500 Minutes)")
ax.set_xlabel("Position")
ax.set_ylabel("Average PER")
save_figure(fig, os.path.join(FIG_DIR, "bar_average_per_by_position.png"))
plt.close(fig)

fig, ax = plt.subplots(figsize=(9, 5))
ax.hist(df["PER"].dropna(), bins=30)
ax.set_title("Distribution of Player Efficiency Rating (PER)")
ax.set_xlabel("PER")
ax.set_ylabel("Frequency")
save_figure(fig, os.path.join(FIG_DIR, "hist_per_distribution.png"))
plt.close(fig)

fig, ax = plt.subplots(figsize=(9, 5))
sns.scatterplot(data=df[df["MP"] >= 500], x="USG%", y="WS", hue="Pos", alpha=0.7, ax=ax)
ax.set_title("Usage Rate vs Win Shares")
ax.set_xlabel("USG%")
ax.set_ylabel("WS")
save_figure(fig, os.path.join(FIG_DIR, "scatter_usage_vs_win_shares.png"))
plt.close(fig)

corr_cols = [c for c in ["PER", "TS%", "USG%", "WS", "BPM", "VORP", "AST%", "TRB%", "TOV%"] if c in df.columns]
corr = df[corr_cols].corr()

fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
ax.set_title("Correlation Heatmap of Key Advanced Metrics")
save_figure(fig, os.path.join(FIG_DIR, "heatmap_correlation_key_metrics.png"))
plt.close(fig)

print("Analysis complete. Outputs written to data/processed and figures.")
