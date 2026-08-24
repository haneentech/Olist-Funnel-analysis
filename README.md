[README.md](https://github.com/user-attachments/files/31385430/README.md)
# Olist Seller Acquisition Funnel Analysis

A funnel analysis of 8,000 marketing-qualified leads tracked from first contact through deal closure, using [Olist's public marketing funnel dataset](https://www.kaggle.com/datasets/olistbr/marketing-funnel-olist). The goal isn't just to report a conversion rate — it's to find *where and why* leads drop off, and turn that into concrete recommendations.

## Why a funnel, and not just a summary chart

A funnel isn't a chart type — it's a way of thinking about the business as a *process* rather than a snapshot. Instead of asking "how many sellers did we sign up," the question becomes: **at every step between a lead entering the pipeline and becoming a paying seller, how many people did we lose, and why?**

That reframing turns a static metric (842 sellers signed) into something actionable: an 8,000-lead haystack where 90% of the value walked away, and the data can tell us *where* and *when* it walked.

## The headline funnel

![Overall Funnel](charts/chart1_overall_funnel.png)

- **8,000** leads entered the pipeline
- **842** converted into signed sellers
- **Overall conversion: 10.5%** — roughly 9 out of 10 leads that sales teams spent time on never converted

## Where leads come from, and which sources are worth the spend

![Channel Conversion](charts/chart2_channel_conversion.png)

| Channel | Leads | Won | Conversion |
|---|---|---|---|
| Unknown (untracked) | 1,159 | 193 | **16.7%** |
| Paid search | 1,586 | 195 | **12.3%** |
| Organic search | 2,296 | 271 | **11.8%** |
| Direct traffic | 499 | 56 | 11.2% |
| Referral | 284 | 24 | 8.5% |
| Social | 1,350 | 75 | 5.6% |
| Display | 118 | 6 | 5.1% |
| Other publicities | 65 | 3 | 4.6% |
| Email | 493 | 15 | 3.0% |
| Other | 150 | 4 | 2.7% |

**Key findings:**
- **Search (organic + paid) does the heavy lifting** — ~49% of total volume at conversion rates 15–17% above average.
- **Social is a volume trap** — the 3rd-largest source (1,350 leads) but converts at barely half the overall rate.
- **Email underperforms its cost** — a presumably warm, opted-in channel converting worse (3.0%) than cold social traffic (5.6%).
- **"Unknown" origin converting best (16.7%) is a flag, not a win** — it means ~14.5% of leads have broken attribution, likely hiding a real high-performing channel (probably referral/word-of-mouth) inside a junk-data bucket.

## When leads convert — the funnel has a clock, not just a shape

![Time to Close](charts/chart4_time_to_close.png)

- **Median time-to-close: 14 days**
- **34% of all wins close within the first week** — the highest-leverage window in the funnel
- 18% of wins take longer than 90 days, some over a year — a long tail that likely represents leads losing momentum

## The trend over time — something changed in January 2018

![Monthly Trend](charts/chart3_monthly_trend.png)

From June–December 2017, conversion crept from 0% to 5.5%. Then, starting **January 2018, conversion jumped to 13–14% and held there for four months** — while lead volume *also* grew, which is rare (scaling volume usually dilutes quality). This is a "find out what happened and do it again" moment worth investigating with the sales/marketing ops team.

## Business recommendations

1. **Reallocate paid budget toward search, away from social/display**, or treat social as a separate, lower-cost awareness channel rather than expecting search-level conversion from it.
2. **Audit the email channel end-to-end** — list source, cadence, and follow-up urgency. A 3% conversion rate on an owned channel is a fixable process problem, not a market problem.
3. **Fix attribution tracking.** Closing the "unknown source" gap could reveal an underinvested high-performing channel currently invisible to marketing.
4. **Build a hard SLA around the first 14 days of contact.** Since a third of all wins close in week one, "no engagement by day 14" should trigger a different follow-up motion rather than sitting in the same queue for months.
5. **Investigate and codify whatever changed in January 2018** — confirm whether it's a replicable process win or a seasonal pattern, and act accordingly.
6. **Expand beyond the mid-size-online-seller sweet spot.** `online_medium` sellers dominate wins (39%); it's worth checking whether beginner/small sellers convert poorly because they're a bad fit for the platform, or because the sales process isn't built for their objections and timeline.

## Repo structure

```
.
├── data/
│   ├── olist_marketing_qualified_leads_dataset.csv   # raw leads (source data)
│   ├── olist_closed_deals_dataset.csv                # raw closed deals (source data)
│   └── merged_funnel_data.csv                        # generated: leads + deals joined
├── scripts/
│   └── funnel_analysis.py                            # reproducible analysis + chart generation
├── charts/
│   ├── chart1_overall_funnel.png
│   ├── chart2_channel_conversion.png
│   ├── chart3_monthly_trend.png
│   └── chart4_time_to_close.png
├── requirements.txt
└── README.md
```

## Reproducing this analysis

```bash
pip install -r requirements.txt
python scripts/funnel_analysis.py
```

This regenerates all four charts in `charts/` and the merged dataset in `data/merged_funnel_data.csv` from the two raw CSVs.

## Data source

[Olist Marketing Funnel dataset](https://www.kaggle.com/datasets/olistbr/marketing-funnel-olist) on Kaggle, released under Olist's public dataset license (CC BY-NC-SA 4.0). Data covers June 2017 – May 2018 for `olist_marketing_qualified_leads_dataset.csv`, with deals closing through November 2018.

## Methodology notes

- "Unknown" origin includes both leads with missing UTM/source data and leads explicitly tagged unknown by the tracking system.
- Time-to-close figures exclude one record with a negative value (likely a data entry issue).
- May 2018 conversion figures may be modestly understated due to right-censoring — the dataset's won-deal window extends only to November 2018, so late-month leads had less time to close.
