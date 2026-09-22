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

---

# Global Health Longevity Drivers Analysis (Social Good Case Study)

## 🎯 1. Ask
**Business/Social Problem:** Determining what socioeconomic factors actually drive human longevity to help global health organizations allocate resources effectively.
**Objective:** Analyze World Health Organization (WHO) historical records using advanced statistical scripting to identify variables with the highest correlation to life expectancy.

## 🗄️ 2. Prepare & Process
* **Dataset:** Historical global health metrics compiled by the WHO across 193 countries.
* **Data Engineering (Python):** 
  * Cleaned hidden trailing whitespace characters from columns using `.str.strip()`.
  * Preserved data integrity by handling missing metrics via **Median Imputation** (`.fillna()`) across 448 rows of missing GDP data and 10 rows of missing Life Expectancy metrics.

## 📈 3. Analyze & Share
Using **Python (Pandas, NumPy, Seaborn, and Matplotlib)**, I calculated a Pearson Correlation Matrix and engineered an automated linear regression scatter model.

* **Interactive Code Workspace:** [🐍 Click here to view my Python Jupyter Notebook on Kaggle](https://www.kaggle.com/code/abelmaina/the-global-health-analytics-case-study?inquiry-id=inq_A7UTz9kAJpoqdx8RJonV8jYiMAZktn&reference-id=35676035&subject=35676035&status=approved&fields%5Bname-first%5D%5Btype%5D=string&fields%5Bname-first%5D%5Bvalue%5D=&fields%5Bname-middle%5D%5Btype%5D=string&fields%5Bname-middle%5D%5Bvalue%5D=&fields%5Bname-last%5D%5Btype%5D=string&fields%5Bname-last%5D%5Bvalue%5D=&fields%5Baddress-street-1%5D%5Btype%5D=string&fields%5Baddress-street-1%5D%5Bvalue%5D=&fields%5Baddress-street-2%5D%5Btype%5D=string&fields%5Baddress-street-2%5D%5Bvalue%5D=&fields%5Baddress-city%5D%5Btype%5D=string&fields%5Baddress-city%5D%5Bvalue%5D=&fields%5Baddress-subdivision%5D%5Btype%5D=string&fields%5Baddress-subdivision%5D%5Bvalue%5D=&fields%5Baddress-postal-code%5D%5Btype%5D=string&fields%5Baddress-postal-code%5D%5Bvalue%5D=&fields%5Baddress-country-code%5D%5Btype%5D=string&fields%5Baddress-country-code%5D%5Bvalue%5D=&fields%5Bbirthdate%5D%5Btype%5D=date&fields%5Bbirthdate%5D%5Bvalue%5D=&fields%5Bemail-address%5D%5Btype%5D=string&fields%5Bemail-address%5D%5Bvalue%5D=&fields%5Bphone-number%5D%5Btype%5D=string&fields%5Bphone-number%5D%5Bvalue%5D=%2B254769244650&fields%5Bidentification-number%5D%5Btype%5D=string&fields%5Bidentification-number%5D%5Bvalue%5D=&fields%5Bidentification-class%5D%5Btype%5D=string&fields%5Bidentification-class%5D%5Bvalue%5D=&fields%5Bselected-country-code%5D%5Btype%5D=string&fields%5Bselected-country-code%5D%5Bvalue%5D=KE&fields%5Bphone%5D%5Btype%5D=string&fields%5Bphone%5D%5Bvalue%5D=&fields%5Bhashed-identification-number%5D%5Btype%5D=string&fields%5Bhashed-identification-number%5D%5Bvalue%5D=)

**Key Finding:** The analysis uncovered a powerful positive correlation of **0.75 between years of Schooling and Life Expectancy**, vastly outperforming raw economic indicators like GDP. This visually and mathematically proves that educational infrastructure is a superior long-term predictor of public health outcomes compared to isolated national wealth.

## 🚀 4. Act (Strategic Policy Recommendations)
1. **Prioritize Educational Capital:** Advise international development funds to heavily tie health grants to national schooling attendance infrastructure.
2. **Targeted Off-Peak Health Interventions:** Allocate specific preventative medical resources to regions displaying declining schooling metrics before adult mortality rates begin to spike.
