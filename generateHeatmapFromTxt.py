import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.patches import Patch

# Create custom legend patches
legend_elements = [
    Patch(facecolor="#c6e48b", edgecolor="white", label="1–10"),
    Patch(facecolor="#7bc96f", edgecolor="white", label="11–20"),
    Patch(facecolor="#239a3b", edgecolor="white", label="21–30"),
]

# Step 1: Reading and parsing the commit log file
dates = []
with open("ktzan_contributions.txt", "r") as file:
    for line in file:
        parts = [p.strip() for p in line.strip().split("|")]
        if len(parts) >= 3:
            date_str = parts[2]
            try:
                date = datetime.strptime(date_str, "%Y-%m-%d").date()
                dates.append(date)
            except ValueError:
                pass  # Skip malformed dates

# Step 2: DataFrame of commits per date
df = pd.DataFrame(dates, columns=["date"])
commit_counts = df.groupby("date").size().reset_index(name="count")

# Step 3: Filling missing dates
start_date = min(commit_counts["date"])
end_date = max(commit_counts["date"])
all_dates = pd.date_range(start=start_date, end=end_date)

calendar_df = pd.DataFrame({"date": all_dates})
calendar_df["date"] = pd.to_datetime(calendar_df["date"]).dt.date
calendar_df = calendar_df.merge(commit_counts, how="left", on="date").fillna(0)

# Step 4: Aligning weeks to actual Mondays
calendar_df["week_monday"] = pd.to_datetime(calendar_df["date"]) - pd.to_timedelta(pd.to_datetime(calendar_df["date"]).dt.weekday, unit='D')
calendar_df["week"] = (calendar_df["week_monday"] - calendar_df["week_monday"].min()).dt.days // 7
calendar_df["dow"] = pd.to_datetime(calendar_df["date"]).dt.weekday 


# Step 5: Month-Year label only when month changes
calendar_df["month_year"] = pd.to_datetime(calendar_df["date"]).dt.strftime("%b %Y")

# Get the first occurrence of each week
weeks = calendar_df.drop_duplicates("week")[["week", "date"]]
weeks["month"] = pd.to_datetime(weeks["date"]).dt.month
weeks["label"] = pd.to_datetime(weeks["date"]).dt.strftime("%b %Y")

# Creating labels only for the first week of a new month
labels = []
prev_month = -1
for _, row in weeks.iterrows():
    month = row["month"]
    label = row["label"] if month != prev_month else ""
    labels.append(label)
    prev_month = month

week_to_month = pd.Series(labels, index=weeks["week"])

# Step 6: Pivoting to matrix
heatmap_data = calendar_df.pivot(index="dow", columns="week", values="count")

# Step 7: GitLab-style color bins
bins = [0, 1, 10, 20, 30, float("inf")]
colors = ["#ebedf0", "#c6e48b", "#7bc96f", "#239a3b", "#196127"]
cmap = ListedColormap(colors)
norm = BoundaryNorm(bins, cmap.N)

# Step 8: Plotting
fig, ax = plt.subplots(figsize=(len(heatmap_data.columns) * 0.3, 3))

sns.heatmap(
    heatmap_data,
    ax=ax,
    cmap=cmap,
    norm=norm,
    cbar=False,
    linewidths=1,
    linecolor="white",
    square=True,
)

# Labels: Monday first, Saturday and Sunday last two rows
ax.set_yticks(range(7))
ax.set_yticklabels(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], rotation=0)

# Only showing ticks where there is a non-empty label
valid_ticks = week_to_month[week_to_month != ""]
ax.set_xticks(list(valid_ticks.index))
ax.set_xticklabels(valid_ticks.values, rotation=0, fontsize=8)
ax.set_title("GitLab-style Contribution Heatmap for ProteomicsDB - Konstantinos Tzanakis")

# Adding the legend to the plot
ax.legend(
    handles=legend_elements,
    title="Commits per day",
    loc="upper right",
    bbox_to_anchor=(1.1, 1.0),
    frameon=False,
    fontsize=8,
    title_fontsize=9
)
plt.tight_layout()
plt.savefig("gitlab_ktzanakis_heatmap.png")
plt.show()

