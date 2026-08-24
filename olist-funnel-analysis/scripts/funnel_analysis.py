"""
Olist Seller Acquisition Funnel Analysis
==========================================
Tracks 8,000 marketing-qualified leads (MQLs) from first contact through
deal closure, and breaks the resulting funnel down by channel, time-to-close,
and monthly cohort to find where and why leads drop off.

Input:
    data/olist_marketing_qualified_leads_dataset.csv
    data/olist_closed_deals_dataset.csv
    (Download from: https://www.kaggle.com/datasets/olistbr/marketing-funnel-olist)

Output:
    charts/chart1_overall_funnel.png
    charts/chart2_channel_conversion.png
    charts/chart3_monthly_trend.png
    charts/chart4_time_to_close.png
    data/merged_funnel_data.csv

Usage:
    python scripts/funnel_analysis.py
"""

import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
CHART_DIR = os.path.join(BASE_DIR, "charts")

NAVY = "#1a2b4c"
TEAL = "#1f9e8f"
CORAL = "#e8604c"
GREY = "#8a94a3"
LIGHT = "#eef1f5"

plt.rcParams["font.family"] = "DejaVu Sans"


def load_and_merge():
    """Load leads + closed deals and merge into one funnel-ready table."""
    leads = pd.read_csv(
        os.path.join(DATA_DIR, "olist_marketing_qualified_leads_dataset.csv"),
        parse_dates=["first_contact_date"],
    )
    deals = pd.read_csv(
        os.path.join(DATA_DIR, "olist_closed_deals_dataset.csv"),
        parse_dates=["won_date"],
    )

    df = leads.merge(deals, on="mql_id", how="left")
    df["won"] = df["won_date"].notna()
    df["days_to_close"] = (df["won_date"] - df["first_contact_date"]).dt.days
    df["origin_clean"] = df["origin"].fillna("unknown")
    return df


def print_summary(df):
    total_leads = len(df)
    total_won = df["won"].sum()
    print(f"TOTAL LEADS: {total_leads}")
    print(f"TOTAL WON:   {total_won}")
    print(f"OVERALL CONVERSION: {total_won / total_leads * 100:.2f}%\n")

    print("=== FUNNEL BY ORIGIN ===")
    origin_funnel = (
        df.groupby("origin_clean")
        .agg(leads=("mql_id", "count"), won=("won", "sum"))
        .reset_index()
    )
    origin_funnel["conv_rate"] = origin_funnel["won"] / origin_funnel["leads"] * 100
    print(origin_funnel.sort_values("leads", ascending=False).to_string(index=False))

    print("\n=== DAYS TO CLOSE (won leads only) ===")
    print(df.loc[df["won"], "days_to_close"].describe())


def chart_overall_funnel(df):
    total_leads = len(df)
    total_won = int(df["won"].sum())
    conv_rate = total_won / total_leads * 100

    fig, ax = plt.subplots(figsize=(7, 5))
    stages = ["Leads Generated (MQLs)", "Deals Won"]
    values = [total_leads, total_won]
    colors = [NAVY, TEAL]
    bar_widths = [1, values[1] / values[0]]
    y_pos = [1, 0]

    for i, (s, v, c, w) in enumerate(zip(stages, values, colors, bar_widths)):
        left = (1 - w) / 2
        ax.barh(y_pos[i], w, left=left, height=0.5, color=c)
        ax.text(0.5, y_pos[i] + 0.35, s, ha="center", va="bottom",
                 color=NAVY, fontsize=12, fontweight="bold")
        ax.text(0.5, y_pos[i], f"{v:,}", ha="center", va="center",
                 color="white", fontsize=13, fontweight="bold")

    ax.set_xlim(0, 1)
    ax.set_ylim(-0.6, 1.9)
    ax.axis("off")
    ax.text(0.5, -0.45, f"Overall conversion: {conv_rate:.1f}%",
             ha="center", fontsize=13, color=CORAL, fontweight="bold")
    plt.title("Lead-to-Close Funnel", fontsize=15, fontweight="bold", color=NAVY, pad=10)
    plt.tight_layout()
    plt.savefig(os.path.join(CHART_DIR, "chart1_overall_funnel.png"), dpi=150, facecolor="white")
    plt.close()


def chart_channel_conversion(df):
    overall_conv = df["won"].mean() * 100
    origin_funnel = (
        df.groupby("origin_clean")
        .agg(leads=("mql_id", "count"), won=("won", "sum"))
        .reset_index()
    )
    origin_funnel["conv_rate"] = origin_funnel["won"] / origin_funnel["leads"] * 100
    origin_funnel = origin_funnel.sort_values("conv_rate", ascending=True)

    fig, ax = plt.subplots(figsize=(8, 6))
    colors_bar = [CORAL if x < overall_conv else TEAL for x in origin_funnel["conv_rate"]]
    bars = ax.barh(origin_funnel["origin_clean"], origin_funnel["conv_rate"], color=colors_bar)
    ax.axvline(overall_conv, color=NAVY, linestyle="--", linewidth=1.2,
               label=f"Overall avg ({overall_conv:.1f}%)")
    for bar, leads in zip(bars, origin_funnel["leads"]):
        ax.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height() / 2,
                 f"{bar.get_width():.1f}%  (n={leads})", va="center", fontsize=9, color=NAVY)
    ax.set_xlabel("Conversion Rate (%)")
    ax.set_title("Conversion Rate by Lead Source", fontsize=14, fontweight="bold", color=NAVY)
    ax.legend(loc="lower right", fontsize=9)
    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()
    plt.savefig(os.path.join(CHART_DIR, "chart2_channel_conversion.png"), dpi=150, facecolor="white")
    plt.close()


def chart_monthly_trend(df):
    df = df.copy()
    df["lead_month"] = df["first_contact_date"].dt.to_period("M").dt.to_timestamp()
    monthly = (
        df.groupby("lead_month")
        .agg(leads=("mql_id", "count"), won=("won", "sum"))
        .reset_index()
    )
    monthly["conv_rate"] = monthly["won"] / monthly["leads"] * 100

    fig, ax1 = plt.subplots(figsize=(10, 5.5))
    ax1.bar(monthly["lead_month"], monthly["leads"], width=20, color=LIGHT,
            edgecolor=GREY, label="Leads generated")
    ax1.set_ylabel("Leads Generated", color=GREY)
    ax1.tick_params(axis="x", rotation=45)
    ax2 = ax1.twinx()
    ax2.plot(monthly["lead_month"], monthly["conv_rate"], color=CORAL,
             marker="o", linewidth=2.5, label="Conversion rate")
    ax2.set_ylabel("Conversion Rate (%)", color=CORAL)
    ax2.tick_params(axis="y", labelcolor=CORAL)
    ax1.set_title("Lead Volume vs. Conversion Rate Over Time", fontsize=14,
                  fontweight="bold", color=NAVY)
    ax1.spines[["top"]].set_visible(False)
    ax2.spines[["top"]].set_visible(False)
    fig.legend(loc="upper left", bbox_to_anchor=(0.1, 0.88), fontsize=9)
    plt.tight_layout()
    plt.savefig(os.path.join(CHART_DIR, "chart3_monthly_trend.png"), dpi=150, facecolor="white")
    plt.close()


def chart_time_to_close(df):
    won_df = df[df["won"]].copy()
    won_df = won_df[won_df["days_to_close"] >= 0]

    bins = [0, 7, 14, 30, 60, 90, 180, 430]
    labels = ["0-7", "8-14", "15-30", "31-60", "61-90", "91-180", "181+"]
    won_df["bucket"] = pd.cut(won_df["days_to_close"], bins=bins, labels=labels,
                                right=True, include_lowest=True)
    bucket_counts = won_df["bucket"].value_counts().reindex(labels)

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(labels, bucket_counts.values, color=TEAL)
    ax.axvline(x=1.5, color=CORAL, linestyle="--", linewidth=1.2)
    ax.text(1.6, max(bucket_counts.values) * 0.92, "Median: 14 days",
             color=CORAL, fontsize=10, fontweight="bold")
    for bar, val in zip(bars, bucket_counts.values):
        ax.text(bar.get_x() + bar.get_width() / 2, val + 3, str(val),
                 ha="center", fontsize=9, color=NAVY)
    ax.set_xlabel("Days from First Contact to Won")
    ax.set_ylabel("Number of Deals")
    ax.set_title("Time-to-Close Distribution", fontsize=14, fontweight="bold", color=NAVY)
    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()
    plt.savefig(os.path.join(CHART_DIR, "chart4_time_to_close.png"), dpi=150, facecolor="white")
    plt.close()


def main():
    os.makedirs(CHART_DIR, exist_ok=True)
    df = load_and_merge()
    print_summary(df)

    chart_overall_funnel(df)
    chart_channel_conversion(df)
    chart_monthly_trend(df)
    chart_time_to_close(df)

    df.to_csv(os.path.join(DATA_DIR, "merged_funnel_data.csv"), index=False)
    print(f"\nCharts written to {CHART_DIR}/")
    print(f"Merged dataset written to {DATA_DIR}/merged_funnel_data.csv")


if __name__ == "__main__":
    main()
