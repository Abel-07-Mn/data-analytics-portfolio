# Employee Attrition & Retention Cost Analysis

A case study on why employees leave, what it's costing the business, and who the company should prioritize retaining — using SQL-style data analysis in Python (pandas) on IBM's HR Analytics dataset.

## The Business Question

A company comes to you with a vague worry: *"We feel like we're losing good people."*
That's not something you can analyze directly, so I scoped it into three answerable questions:

1. Which departments have the highest attrition rates?
2. What factors are associated with employees leaving (pay, tenure, overtime, satisfaction)?
3. What is attrition actually costing the business, and who should they prioritize retaining?

## Live Notebook

View the full interactive analysis on Kaggle: [Employee Attrition & Retention Cost Analysis](https://www.kaggle.com/code/abelmaina/employee-attrition-retention-cost-analysis)

## Dataset

[IBM HR Analytics Employee Attrition & Performance](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset) — 1,470 employees, 35 attributes, no missing values. A synthetic but realistic dataset created by IBM data scientists for HR analytics practice.

## Key Findings

**1. Attrition rate vs. headcount tell different stories.**
Sales has the highest attrition *rate* (20.6%), but R&D loses the most people in *absolute* terms (133 people vs. 92) simply because it's a much bigger team (961 vs. 446 employees). A recommendation based on percentage alone would have missed this.

| Department | Attrition Rate | Employees | Est. People Lost |
|---|---|---|---|
| Sales | 20.6% | 446 | ~92 |
| R&D | 13.8% | 961 | ~133 |
| HR | 19.0% | 63 | ~12 |

**2. Overtime is the strongest predictor of attrition — by far.**
Employees working overtime are **nearly 3x more likely to leave** (30.5% vs. 10.4%). This was a stronger signal than any other factor tested.

**3. Pay and career stage matter more than reported satisfaction.**
Employees who left earned **~30% less** on average and had **~31% less tenure/experience** than those who stayed. Surprisingly, self-reported Job Satisfaction and Work-Life Balance scores were nearly identical between the two groups — meaning survey-based "happiness" metrics weren't the real story here.

**4. Estimated cost of attrition: ~$6.8 million.**
Using the standard HR industry estimate that replacing an employee costs 50–200% of their annual salary (I used a conservative 50%), the 237 employees who left cost the business an estimated **$6,807,246** in recruiting, lost productivity, and training.

## Recommendation

Prioritize retention efforts on **early-career, below-average-earning employees working overtime**, particularly in Sales. Overtime reduction and targeted pay adjustments are likely to be more effective levers than generic engagement or satisfaction initiatives, since satisfaction scores showed little difference between leavers and stayers.

## Limitations

This analysis shows correlation, not proven causation — a statistical test (e.g. logistic regression) would be needed to confirm overtime and income *cause* attrition rather than simply co-occurring with it. The 50% replacement-cost assumption is an industry rule of thumb, not a figure specific to this company.

## Tools Used

Python, pandas, Jupyter/Kaggle Notebooks

## Files in This Repo

- `attrition_analysis.ipynb` — full notebook with code and outputs
- `WA_Fn-UseC_-HR-Employee-Attrition.csv` — dataset
- `README.md` — this file
