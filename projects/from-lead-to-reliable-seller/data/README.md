# Data source and setup

This project uses two public Olist datasets:

1. [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
2. [Marketing Funnel by Olist](https://www.kaggle.com/datasets/olistbr/marketing-funnel-olist)

Download and extract both datasets. Place these five files together in `data/raw/`:

- `olist_marketing_qualified_leads_dataset.csv`
- `olist_closed_deals_dataset.csv`
- `olist_orders_dataset.csv`
- `olist_order_items_dataset.csv`
- `olist_order_reviews_dataset.csv`

The pipeline reads only the fields required for this case study. It does not upload or commit raw data, and it writes only grouped summaries to `outputs/`.

Olist describes the marketplace data as anonymized historical data from 2016–2018. The lead funnel can be linked to marketplace activity through `mql_id` and `seller_id`. The marketplace dataset is published under **CC BY-NC-SA 4.0**. Review each dataset's current Kaggle data card and license before redistributing any source data or using it commercially. This repository links to the original sources and does not redistribute the raw CSVs.