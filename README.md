# E-Commerce Customer Retention & Growth Analysis

## 🎯 1. Ask
**Business Problem:** The business observed an overall decline in month-over-month transactional sales volume and feared a massive customer retention crisis. 
**Objective:** Analyze historical retail transaction data to determine if revenue drops are caused by poor customer retention or a shrinking pipeline of new user acquisitions.

## 🗄️ 2. Prepare & Process
* **Dataset:** 541,909 raw transactional records from a UK-based online retail store.
* **Data Cleaning (SQL):** Handled data quality issues by dropping 135,080 records with missing `CustomerID` attributes, eliminating exact row duplicates using `DISTINCT`, and filtering out negative values in `Quantity` and `UnitPrice` representing system test errors or cancellations. 
* **Final Pristine Dataset:** 392,692 high-quality analytical rows.

## 📈 3. Analyze & Share
Using advanced SQL Window Functions (cohort partitioning) and Google BigQuery, I isolated the exact month each customer made their first purchase to split the consumer base into "New" vs. "Returning" cohorts.

* **Interactive Dashboard:** [👉 Click here to view my interactive Tableau Dashboard](https://public.tableau.com/views/E-CommerceCustomerRetentionAnalysis/Sheet1?:language=en-US&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)
* * **Executive Presentation:** [📊 Click here to view the Google Slides Deck](https://docs.google.com/presentation/d/1ChNI6ouefXILf5Mp1zrqnRgyvR56voNWBn8Elvog9Lg/edit?usp=sharing)


**Key Finding:** The analysis disproved the initial retention panic. In peak operational months like June 2011, returning customers accounted for over 75% of the total active shopping audience (749 returning vs. 242 new). The real revenue driver is seasonal holiday surges, masking a steady drop in new user acquisition during off-peak seasons.

## 🚀 4. Act (Business Recommendations)
1. **Pivot Marketing Budget:** Shift capital away from retention campaigns and heavily target top-of-funnel *New Customer Acquisition* during slow mid-year periods (Q2/Q3).
2. **First-Purchase Incentives:** Introduce introductory discounts or welcome bundles to increase the shrinking baseline cohort sizes observed mid-year.
3. **Reward VIP Cohorts:** Design an automated loyalty tier targeting the high-performing 75% returning customer base to increase their average order value (AOV).

