"""
Fullback Evolution Analysis 

Outputs:
1. Side-by-side heatmaps

2. Structured table with categories

Comparison:
- Traditional fullbacks (2004/05)
- Modern fullbacks (2020/21)
"""

from statsbombpy import sb
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Pitch
from scipy.ndimage import gaussian_filter


# STYLE

PITCH_COLOR = '#22312b'
LINE_COLOR = 'white'


# DATA PROCESSING
def process_dataset(comp_id, season_id):
    """Load and prepare dataset (LB + RB)."""

    matches = sb.matches(competition_id=comp_id, season_id=season_id)
    match_ids = matches['match_id'].tolist()

    events = pd.concat(
        [sb.events(match_id=m) for m in match_ids],
        ignore_index=True
    )

    # BOTH FULLBACKS
    df = events[
        (events['type'] == 'Pass') &
        (events['position'].isin(['Left Back', 'Right Back']))
    ].dropna(subset=['location', 'pass_end_location']).copy()

    # Coordinates
    df['x_start'] = df['location'].str[0]
    df['y_start'] = df['location'].str[1]
    df['x_end'] = df['pass_end_location'].str[0]
    df['y_end'] = df['pass_end_location'].str[1]

    # Position
    df['final_third'] = df['x_start'] > 80
    df['central_distance'] = abs(df['y_start'] - 40)

    # Progression
    df['progression'] = df['x_end'] - df['x_start']
    df['is_progressive'] = df['progression'] > 10

    # Creation
    df['into_box'] = df['pass_end_location'].apply(
        lambda x: x[0] > 102 and 18 < x[1] < 62
    )

    df['is_key_pass'] = (
        df['pass_goal_assist'].fillna(False) |
        df['pass_shot_assist'].fillna(False)
    )

    df['is_cross'] = df['pass_cross'].fillna(False)

    # Build-up
    df['pass_length'] = df['pass_length'].fillna(0)
    df['short_pass'] = df['pass_length'] < 15

    return df

# METRICS

def compute_metrics(df):

    n_matches = df['match_id'].nunique()

    return {
        # POSITION
        "Median position (m)": df['x_start'].median(),
        "Final third (%)": df['final_third'].mean() * 100,
        "Centrality (m)": df['central_distance'].mean(),

        # PROGRESSION
        "Progressive passes / match": df['is_progressive'].sum() / n_matches,
        "Progressive pass (%)": df['is_progressive'].mean() * 100,
        "Avg progression (m)": df['progression'].mean(),

        # CREATION
        "Box entries / match": df['into_box'].sum() / n_matches,
        "Key passes / match": df['is_key_pass'].sum() / n_matches,
        "Crosses / match": df['is_cross'].sum() / n_matches,

        # BUILD-UP
        "Short pass (%)": df['short_pass'].mean() * 100,
        "Avg pass length (m)": df['pass_length'].mean()
    }


# HEATMAP 
def plot_heatmaps(old_df, modern_df):

    pitch = Pitch(pitch_color=PITCH_COLOR, line_color=LINE_COLOR)
    fig, axs = pitch.draw(ncols=2, figsize=(14, 6))

    datasets = [old_df, modern_df]
    titles = ["La Liga 2004/05", "La Liga 2020/21"]

    for i, data in enumerate(datasets):

        # Heatmap
        bin_stat = pitch.bin_statistic(
            data['x_start'],
            data['y_start'],
            statistic='count',
            bins=(30, 30)
        )

        bin_stat['statistic'] /= bin_stat['statistic'].sum()
        bin_stat['statistic'] = gaussian_filter(bin_stat['statistic'], sigma=2)

        pitch.heatmap(
            bin_stat,
            ax=axs[i],
            cmap='inferno',
            edgecolors='none',
            alpha=0.9
        )

        axs[i].set_title(titles[i], fontsize=12, color='black')

    plt.suptitle(
        "Evolution of Fullback Activity Zones",
        fontsize=16,
        fontweight='bold',
        color='black'
    )

    # Legend
    handles, labels = axs[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center', ncol=3)

    plt.subplots_adjust(bottom=0.15)
    plt.show()


# TABLE
def create_structured_table(old, modern):

    categories = {
        "POSITION": [
            "Median position (m)",
            "Final third (%)",
            "Centrality (m)"
        ],
        "PROGRESSION": [
            "Progressive passes / match",
            "Progressive pass (%)",
            "Avg progression (m)"
        ],
        "CREATION": [
            "Box entries / match",
            "Key passes / match",
            "Crosses / match"
        ],
        "BUILD-UP": [
            "Short pass (%)",
            "Avg pass length (m)"
        ]
    }

    rows = []

    for category, metrics in categories.items():
        rows.append([f"--- {category} ---", "", "", ""])

        for metric in metrics:
            old_val = old[metric]
            mod_val = modern[metric]

            change = ((mod_val - old_val) / old_val * 100) if old_val != 0 else 0

            rows.append([
                metric,
                round(old_val, 2),
                round(mod_val, 2),
                f"{change:+.1f}%"
            ])

    return pd.DataFrame(rows, columns=["Metric", "2004/05", "2020/21", "Change"])


# MAIN
if __name__ == "__main__":

    old_df = process_dataset(11, 37)
    modern_df = process_dataset(11, 90)

    old_metrics = compute_metrics(old_df)
    modern_metrics = compute_metrics(modern_df)

    # Heatmap
    plot_heatmaps(old_df, modern_df)

    # Table
    table = create_structured_table(old_metrics, modern_metrics)

    print("\n=== FULLBACK EVOLUTION SUMMARY ===\n")
    print(table.to_string(index=False))