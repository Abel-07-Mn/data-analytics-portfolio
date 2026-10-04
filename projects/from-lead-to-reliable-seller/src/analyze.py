#!/usr/bin/env python3
"""Reproduce the seller-acquisition and early-activation case study.

Only Python's standard library is required. Raw Olist CSVs are intentionally
not committed; see the project README for download and attribution instructions.
"""

from __future__ import annotations

import argparse
import csv
import html
import sqlite3
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = {
    "olist_marketing_qualified_leads_dataset.csv": (
        "mql_id",
        "first_contact_date",
        "origin",
    ),
    "olist_closed_deals_dataset.csv": ("mql_id", "seller_id", "won_date"),
    "olist_orders_dataset.csv": (
        "order_id",
        "order_status",
        "order_purchase_timestamp",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ),
    "olist_order_items_dataset.csv": ("order_id", "seller_id", "price"),
    "olist_order_reviews_dataset.csv": ("order_id", "review_score"),
}
TABLES = {
    "olist_marketing_qualified_leads_dataset.csv": (
        "marketing_qualified_leads",
        ("mql_id", "first_contact_date", "origin"),
    ),
    "olist_closed_deals_dataset.csv": (
        "closed_deals",
        ("mql_id", "seller_id", "won_date"),
    ),
    "olist_orders_dataset.csv": (
        "orders",
        (
            "order_id",
            "order_status",
            "order_purchase_timestamp",
            "order_delivered_customer_date",
            "order_estimated_delivery_date",
        ),
    ),
    "olist_order_items_dataset.csv": (
        "order_items",
        ("order_id", "seller_id", "price"),
    ),
    "olist_order_reviews_dataset.csv": (
        "order_reviews",
        ("order_id", "review_score"),
    ),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data-dir",
        type=Path,
        required=True,
        help="Directory containing the five required Olist CSV files.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PROJECT_ROOT / "outputs",
        help="Directory for CSV summaries (default: project outputs/).",
    )
    parser.add_argument(
        "--assets-dir",
        type=Path,
        default=PROJECT_ROOT / "assets",
        help="Directory for SVG charts (default: project assets/).",
    )
    return parser.parse_args()


def check_inputs(data_dir: Path) -> None:
    missing = [name for name in REQUIRED_FILES if not (data_dir / name).is_file()]
    if missing:
        raise FileNotFoundError(
            "Missing required CSV file(s): "
            + ", ".join(missing)
            + f"\nExpected them inside: {data_dir}"
        )


def load_csv(
    connection: sqlite3.Connection,
    data_dir: Path,
    filename: str,
    table: str,
    columns: tuple[str, ...],
) -> int:
    path = data_dir / filename
    with path.open("r", encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        found = set(reader.fieldnames or ())
        missing_columns = set(columns) - found
        if missing_columns:
            raise ValueError(
                f"{filename} is missing column(s): "
                + ", ".join(sorted(missing_columns))
            )

        placeholders = ", ".join("?" for _ in columns)
        names = ", ".join(columns)
        statement = f"INSERT INTO {table} ({names}) VALUES ({placeholders})"
        batch: list[tuple[Any, ...]] = []
        count = 0
        for row in reader:
            values: list[Any] = []
            for column in columns:
                value = (row.get(column) or "").strip()
                if not value:
                    values.append(None)
                elif column == "price":
                    values.append(float(value))
                elif column == "review_score":
                    values.append(int(value))
                else:
                    values.append(value)
            batch.append(tuple(values))
            if len(batch) >= 5000:
                connection.executemany(statement, batch)
                count += len(batch)
                batch.clear()
        if batch:
            connection.executemany(statement, batch)
            count += len(batch)
    return count


def validate_grains(connection: sqlite3.Connection) -> None:
    checks = (
        ("marketing_qualified_leads", "mql_id"),
        ("closed_deals", "mql_id"),
        ("orders", "order_id"),
    )
    for table, key in checks:
        total, distinct = connection.execute(
            f"SELECT COUNT(*), COUNT(DISTINCT {key}) FROM {table}"
        ).fetchone()
        if total != distinct:
            raise ValueError(
                f"{table} has duplicate {key} values ({total} rows, "
                f"{distinct} distinct). Resolve the grain before analysis."
            )

    unmatched_leads = connection.execute(
        """
        SELECT COUNT(*)
        FROM closed_deals AS d
        LEFT JOIN marketing_qualified_leads AS m ON m.mql_id = d.mql_id
        WHERE m.mql_id IS NULL
        """
    ).fetchone()[0]
    if unmatched_leads:
        raise ValueError(
            f"{unmatched_leads} closed deal(s) do not match a qualified lead."
        )


def write_csv(path: Path, rows: list[dict[str, Any]], columns: tuple[str, ...]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as target:
        writer = csv.DictWriter(target, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def pct(numerator: int, denominator: int) -> float | None:
    if denominator == 0:
        return None
    return numerator * 100.0 / denominator


def format_pct(value: float | None) -> str:
    return "—" if value is None else f"{value:.1f}%"


def render_bar_chart(
    path: Path,
    title: str,
    subtitle: str,
    rows: list[dict[str, Any]],
    value_field: str,
    count_field: str,
    count_label: str,
    footer: str,
    color: str = "#176B67",
) -> None:
    width = 1000
    left = 250
    right = 170
    top = 150
    row_height = 48
    bottom = 88
    height = top + len(rows) * row_height + bottom
    max_value = max((float(row[value_field]) for row in rows), default=0.0)
    max_value = max(max_value, 1.0)
    bar_width = width - left - right
    escaped_title = html.escape(title)
    escaped_subtitle = html.escape(subtitle)
    pieces = [
        f'<svg xmlns="http://www.w3.org/2000/svg" role="img" '
        f'aria-labelledby="title desc" viewBox="0 0 {width} {height}">',
        '<title id="title">' + escaped_title + "</title>",
        '<desc id="desc">' + escaped_subtitle + "</desc>",
        '<rect width="100%" height="100%" fill="#F7F8F5"/>',
        '<text x="48" y="55" font-family="Arial, sans-serif" font-size="28" '
        'font-weight="700" fill="#173D3A">' + escaped_title + "</text>",
        '<text x="48" y="88" font-family="Arial, sans-serif" font-size="15" '
        'fill="#5B6B69">' + escaped_subtitle + "</text>",
    ]
    for index, row in enumerate(rows):
        y = top + index * row_height
        label = html.escape(str(row["origin"]).replace("_", " ").title())
        value = float(row[value_field])
        count = int(row[count_field])
        bar = max(0.0, value / max_value * bar_width)
        pieces.extend(
            [
                f'<text x="48" y="{y + 22}" font-family="Arial, sans-serif" '
                f'font-size="15" fill="#263A38">{label}</text>',
                f'<rect x="{left}" y="{y}" width="{bar_width}" height="22" '
                'rx="5" fill="#E3E9E5"/>',
                f'<rect x="{left}" y="{y}" width="{bar:.1f}" height="22" '
                f'rx="5" fill="{color}"/>',
                f'<text x="{left + bar_width + 16}" y="{y + 17}" '
                'font-family="Arial, sans-serif" font-size="15" '
                'font-weight="700" fill="#173D3A">'
                f'{value:.1f}%</text>',
                f'<text x="{width - 48}" y="{y + 17}" text-anchor="end" '
                'font-family="Arial, sans-serif" font-size="12" fill="#5B6B69">'
                f'n = {count:,} {html.escape(count_label)}</text>',
            ]
        )
    footer_y = top + len(rows) * row_height + 42
    pieces.append(
        f'<text x="48" y="{footer_y}" font-family="Arial, sans-serif" '
        'font-size="12" fill="#5B6B69">' + html.escape(footer) + "</text>"
    )
    pieces.append("</svg>")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(pieces), encoding="utf-8")


def main() -> None:
    args = parse_args()
    check_inputs(args.data_dir)
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    connection.executescript(
        (PROJECT_ROOT / "sql" / "schema.sql").read_text(encoding="utf-8")
    )

    loaded_rows: dict[str, int] = {}
    for filename, (table, columns) in TABLES.items():
        loaded_rows[table] = load_csv(
            connection, args.data_dir, filename, table, columns
        )
    validate_grains(connection)
    connection.executescript(
        (PROJECT_ROOT / "sql" / "analysis.sql").read_text(encoding="utf-8")
    )

    source_rows = [
        dict(row)
        for row in connection.execute(
            """
            SELECT origin, qualified_leads, closed_deals
            FROM source_funnel
            ORDER BY qualified_leads DESC
            """
        )
    ]
    mature_rows = [
        dict(row)
        for row in connection.execute(
            "SELECT mql_id, seller_id, origin FROM mature_closed_sellers"
        )
    ]
    activated_rows = [
        dict(row)
        for row in connection.execute(
            """
            SELECT origin, mql_id, days_to_first_delivered_order,
                   delivered_orders_90d, delivered_item_value_90d
            FROM activated_sellers_90d
            """
        )
    ]
    quality_rows = [
        dict(row)
        for row in connection.execute(
            """
            SELECT origin, on_time, mean_review_score
            FROM early_fulfillment_orders_90d
            """
        )
    ]
    latest_delivery = connection.execute(
        "SELECT MAX(order_delivered_customer_date) FROM orders"
    ).fetchone()[0]
    source_to_mature: dict[str, int] = defaultdict(int)
    for row in mature_rows:
        source_to_mature[row["origin"]] += 1
    source_to_active: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in activated_rows:
        source_to_active[row["origin"]].append(row)
    source_to_quality: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in quality_rows:
        source_to_quality[row["origin"]].append(row)

    performance: list[dict[str, Any]] = []
    quality_summary: list[dict[str, Any]] = []
    for source in source_rows:
        origin = source["origin"]
        mature_n = source_to_mature[origin]
        active = source_to_active[origin]
        quality = source_to_quality[origin]
        active_n = len(active)
        days = [float(row["days_to_first_delivered_order"]) for row in active]
        scores = [
            float(row["mean_review_score"])
            for row in quality
            if row["mean_review_score"] is not None
        ]
        on_time_n = sum(int(row["on_time"]) for row in quality)
        on_time_rate = pct(on_time_n, len(quality))
        mean_review = statistics.mean(scores) if scores else None
        lead_to_won = pct(source["closed_deals"], source["qualified_leads"])
        activation = pct(active_n, mature_n)
        qualified_to_activation = pct(active_n, source["qualified_leads"])
        median_days = statistics.median(days) if days else None
        performance.append(
            {
                "origin": origin,
                "qualified_leads": source["qualified_leads"],
                "closed_deals": source["closed_deals"],
                "lead_to_won_pct": (
                    round(lead_to_won, 2) if lead_to_won is not None else ""
                ),
                "mature_closed_deals": mature_n,
                "activated_sellers_90d": active_n,
                "activation_rate_90d_pct": (
                    round(activation, 2) if activation is not None else ""
                ),
                "qualified_to_activated_pct": (
                    round(qualified_to_activation, 2)
                    if qualified_to_activation is not None
                    else ""
                ),
                "median_days_to_first_delivered_order": (
                    round(median_days, 1) if median_days is not None else ""
                ),
                "single_seller_delivered_orders_90d": len(quality),
                "on_time_delivery_rate_pct": (
                    round(on_time_rate, 2) if on_time_rate is not None else ""
                ),
                "mean_review_score": round(mean_review, 2) if mean_review else "",
            }
        )
        quality_summary.append(
            {
                "origin": origin,
                "mature_closed_deals": mature_n,
                "single_seller_delivered_orders_90d": len(quality),
                "on_time_orders": on_time_n,
                "on_time_delivery_rate_pct": (
                    round(on_time_rate, 2) if on_time_rate is not None else ""
                ),
                "orders_with_review": len(scores),
                "mean_review_score": round(mean_review, 2) if mean_review else "",
            }
        )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    args.assets_dir.mkdir(parents=True, exist_ok=True)
    performance_columns = (
        "origin",
        "qualified_leads",
        "closed_deals",
        "lead_to_won_pct",
        "mature_closed_deals",
        "activated_sellers_90d",
        "activation_rate_90d_pct",
        "qualified_to_activated_pct",
        "median_days_to_first_delivered_order",
        "single_seller_delivered_orders_90d",
        "on_time_delivery_rate_pct",
        "mean_review_score",
    )
    quality_columns = (
        "origin",
        "mature_closed_deals",
        "single_seller_delivered_orders_90d",
        "on_time_orders",
        "on_time_delivery_rate_pct",
        "orders_with_review",
        "mean_review_score",
    )
    write_csv(
        args.output_dir / "source_performance.csv",
        performance,
        performance_columns,
    )
    write_csv(
        args.output_dir / "early_fulfillment_quality.csv",
        quality_summary,
        quality_columns,
    )

    lead_chart_rows = [
        {
            "origin": row["origin"],
            "value": pct(row["closed_deals"], row["qualified_leads"]) or 0,
            "count": row["qualified_leads"],
        }
        for row in source_rows
        if row["qualified_leads"] >= 50
    ]
    activation_chart_rows = [
        {
            "origin": row["origin"],
            "value": float(row["activation_rate_90d_pct"] or 0),
            "count": row["mature_closed_deals"],
        }
        for row in performance
        if int(row["mature_closed_deals"]) >= 20
    ]
    quality_chart_rows = [
        {
            "origin": row["origin"],
            "value": float(row["on_time_delivery_rate_pct"] or 0),
            "count": row["single_seller_delivered_orders_90d"],
        }
        for row in performance
        if int(row["mature_closed_deals"]) >= 20
        and int(row["single_seller_delivered_orders_90d"]) > 0
    ]
    lead_chart_rows.sort(key=lambda row: float(row["value"]), reverse=True)
    activation_chart_rows.sort(key=lambda row: float(row["value"]), reverse=True)
    quality_chart_rows.sort(key=lambda row: float(row["value"]), reverse=True)
    render_bar_chart(
        args.assets_dir / "lead-to-won-rate.svg",
        "Lead volume is not the same as closed-won conversion",
        "Qualified leads converted to a closed seller deal, by recorded source",
        lead_chart_rows,
        "value",
        "count",
        "leads",
        "All displayed sources have at least 50 qualified leads. Unknown attribution is retained.",
        "#2D7181",
    )
    render_bar_chart(
        args.assets_dir / "seller-activation-90d.svg",
        "Paid search leads activated more often, but later",
        "Share of mature closed deals with a delivered order within 90 days of the win date",
        activation_chart_rows,
        "value",
        "count",
        "mature deals",
        "Only sources with at least 20 mature closed deals are shown; a complete 90-day window is required.",
        "#176B67",
    )
    render_bar_chart(
        args.assets_dir / "early-delivery-quality.svg",
        "Early on-time delivery varies by acquisition source",
        "On-time share among single-seller delivered orders in the first 90 days",
        quality_chart_rows,
        "value",
        "count",
        "orders",
        "Only sources with at least 20 mature closed deals are shown; rates are descriptive, not causal.",
        "#9A6B1F",
    )

    totals = connection.execute(
        "SELECT COUNT(*) AS leads FROM marketing_qualified_leads"
    ).fetchone()["leads"]
    closed = connection.execute("SELECT COUNT(*) FROM closed_deals").fetchone()[0]
    mature = len(mature_rows)
    activated = len(activated_rows)
    print(f"Loaded rows: {loaded_rows}")
    print(f"Latest observed customer delivery: {latest_delivery}")
    print(f"Qualified leads: {totals:,}; closed deals: {closed:,}")
    print(f"Mature closed deals: {mature:,}; 90-day activated: {activated:,}")
    print(
        "Lead-to-won conversion: "
        + format_pct(pct(closed, totals))
        + "; mature-deal activation: "
        + format_pct(pct(activated, mature))
    )
    print(f"Wrote CSV summaries to {args.output_dir}")
    print(f"Wrote SVG charts to {args.assets_dir}")
    connection.close()


if __name__ == "__main__":
    main()