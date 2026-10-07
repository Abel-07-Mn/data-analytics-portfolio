# Global Superstore: SQL Profitability Analysis

## Business Question

A global retailer wants to understand: **Where is the business making money, where is it losing money, and why?**

This was broken down into five specific questions, each answered using SQL queries against the company's order data:

1. Which regions/countries are most and least profitable?
2. Which product categories/sub-categories drive the most profit — and which lose money?
3. Does discounting hurt profit?
4. Does shipping cost or order priority eat into profit margins?
5. Which customer segment is most profitable, and does that differ by region?

## Dataset

**Global Superstore** — a public retail dataset (51,290 orders, 24 columns) covering sales across multiple countries, markets, and product categories, including Sales, Profit, Discount, Shipping Cost, and Order Priority for each order.

Source: [Kaggle – Global Super Store Dataset](https://www.kaggle.com/datasets/apoorvaappz/global-super-store-dataset)

## Key Findings

**1. Profitability varies significantly by region — and "biggest" isn't "best."**
The Central region generates the most total profit ($311K), but Canada is the most *efficient* market, with a 26.6% profit margin on far smaller sales volume. Southeast Asia and EMEA stand out as underperformers, with sales in the hundreds of thousands but margins near break-even (2.0% and 5.5% respectively).

| Region | Total Sales | Total Profit | Margin |
|---|---|---|---|
| Central | $2,822,303 | $311,404 | 11.0% |
| Canada | $66,928 | $17,817 | **26.6%** |
| Southeast Asia | $884,423 | $17,852 | **2.0%** |
| EMEA | $806,161 | $43,898 | 5.5% |

**2. Every product sub-category is profitable — except one: Tables.**
Tables is the only sub-category losing money company-wide, at a **-8.46% margin** (-$64,083 on $757K in sales). Every other Furniture, Office Supplies, and Technology sub-category is solidly profitable.

**3. The Tables problem is caused almost entirely by heavy discounting.**
When Tables are sold at full price, they're actually a healthy product (23.1% margin — above the company average). But profitability collapses as discounts increase:

| Discount Band | Orders | Avg Discount | Profit Margin |
|---|---|---|---|
| 0% (no discount) | 208 | 0% | **+23.1%** |
| 1–20% | 186 | 19.8% | +5.0% |
| 21–40% | 246 | 34.4% | -18.1% |
| 41%+ | 221 | 58.3% | **-76.7%** |

Nearly half of all Tables orders are discounted above 20%, directly driving the category's overall loss.

**4. Shipping cost and order priority are not a significant driver of lost profit.**
Margins stay within a narrow 10.3%–12.6% band across all order priority levels. Critical-priority orders have the highest shipping cost ($59.72 avg) but also the *best* margin (12.6%), suggesting rush shipping is already priced appropriately and isn't eroding profitability.

**5. Customer segment doesn't change the pattern — region does.**
Consumer, Corporate, and Home Office segments all follow the same regional profitability pattern (Canada strongest, Southeast Asia/EMEA weakest). This rules out "wrong customer segment" as an explanation and confirms that regional and discounting dynamics are the real drivers of profit performance.

## Recommendation

**Primary: Cap discounts on Tables at 20%.** Data shows a clear, almost linear relationship between discount depth and losses on this specific sub-category. Restricting discounts above 20% on Tables alone could eliminate the bulk of this -$64K loss without affecting any other healthy product line.

**Secondary: Investigate Southeast Asia and EMEA's thin margins.** These regions post substantial sales volume but very weak profitability (2.0% and 5.5% margins). Since this pattern holds across all customer segments, the cause is likely regional — possibly pricing strategy, higher local discounting norms, or cost structure — and warrants a focused follow-up analysis before any broader pricing decisions are made.

## Limitations

- This is historical, static data (no date range filtering applied) — trends over time were not analyzed in this pass.
- Currency is assumed to be a single unit (likely USD) across all countries; true multi-currency effects (exchange rates) are not modeled.
- "Discount" reflects price reduction only; underlying cost-of-goods data isn't available, so margin figures reflect Sales minus Profit as reported in the dataset, not a full cost breakdown.

## Tools Used

SQL (SQLite), Python (pandas, for loading data into the database), Kaggle Notebooks

## Live Notebook

[View the full notebook with all SQL queries on Kaggle](https://www.kaggle.com/code/abelmaina/global-superstore-sql-profitability-analysis)

## Files in This Repo

- `README.md` — this write-up
- `global_superstore_sql_analysis.ipynb` — the Kaggle notebook with all SQL queries and results
- `Global_Superstore2.csv` — the dataset used
