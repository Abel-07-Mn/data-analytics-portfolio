# Global Superstore: Profitability & Discount Dashboard

## Business Question

This project turns the findings from the companion [SQL Profitability Analysis](../sql-retail-profitability-analysis/README.md) into an interactive Tableau dashboard — making the same business question explorable visually: **Where is this global retailer making money, where is it losing money, and why?**

## Dataset

Same dataset as the SQL project: **Global Superstore** (51,290 orders, 24 columns), covering sales across multiple countries, markets, and product categories.

Source: [Kaggle – Global Super Store Dataset](https://www.kaggle.com/datasets/apoorvaappz/global-super-store-dataset)

## Dashboard

🔗 **[View the live, interactive dashboard on Tableau Public](https://public.tableau.com/app/profile/abel.maina/viz/GlobalSuperstoreProfitabilityDashboard_17913524628970/Dashboard1?publish=yes)**

The dashboard contains three linked, interactive charts:

1. **Profit by Region** — a bar chart ranking all 13 regions by total profit, confirming Central as the top earner by volume and Canada as the smallest but most efficient market.
2. **Profit by Sub-Category** — a bar chart across all 17 product sub-categories, visually isolating **Tables** as the only sub-category operating at a loss.
3. **Discount vs Profit (Tables)** — a scatter plot of every individual Tables order, plotting discount percentage against profit, with a trend line showing the sharp decline in profitability as discounts increase.

**Interactivity:** Clicking any region bar in the first chart filters the other two charts to that region, letting a viewer explore how the Tables/discount problem shows up differently across markets.

## Key Finding

The dashboard visually confirms the core finding from the SQL analysis: **the Tables sub-category is the only unprofitable product line company-wide, and its losses are driven almost entirely by heavy discounting** (profit collapses from +23% margin at 0% discount to -77% margin at 41%+ discount). Region and shipping cost are not significant factors — the discount pattern holds consistently across markets.

## Recommendation

Cap discounts on Tables at 20%. The scatter plot shows a clear, consistent decline in profitability once discounts exceed this threshold, with minimal additional sales benefit to offset the loss.

## Tools Used

Tableau Public, same Global Superstore dataset used in the SQL project

## Related Project

This dashboard is a visual companion to the [SQL Profitability Analysis](../sql-retail-profitability-analysis/README.md), which contains the full query-by-query breakdown behind these findings.
