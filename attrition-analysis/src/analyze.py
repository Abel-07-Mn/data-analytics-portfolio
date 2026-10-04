#!/usr/bin/env python3
"""Reproduce descriptive attrition rates and replacement-cost scenarios."""

from __future__ import annotations

import argparse
import csv
import html
from collections import defaultdict
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, required=True, help="IBM HR CSV file.")
    parser.add_argument(
        "--output-dir", type=Path, default=PROJECT_ROOT / "outputs"
    )
    parser.add_argument("--assets-dir", type=Path, default=PROJECT_ROOT / "assets")
    return parser.parse_args()


def read_employees(path: Path) -> list[dict[str, str]]:
    required = {
        "Attrition",
        "Department",
        "OverTime",
        "MonthlyIncome",
        "YearsAtCompany",
    }
    with path.open("r", encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        missing = required - set(reader.fieldnames or ())
        if missing:
            raise ValueError("Missing required columns: " + ", ".join(sorted(missing)))
        rows = list(reader)
    if not rows:
        raise ValueError("The employee dataset is empty.")
    if any(row["Attrition"] not in {"Yes", "No"} for row in rows):
        raise ValueError("Attrition must contain only Yes or No.")
    return rows


def pct(numerator: int, denominator: int) -> float | None:
    return numerator * 100.0 / denominator if denominator else None


def segment(rows: list[dict[str, str]], field: str) -> list[dict[str, object]]:
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        groups[row[field] or "Unknown"].append(row)
    result = []
    for key, members in groups.items():
        leavers = sum(row["Attrition"] == "Yes" for row in members)
        rate = pct(leavers, len(members))
        result.append(
            {
                "segment": key,
                "employees": len(members),
                "leavers": leavers,
                "attrition_rate_pct": round(rate, 2) if rate is not None else "",
            }
        )
    return sorted(result, key=lambda row: str(row["segment"]))


def write_csv(path: Path, rows: list[dict[str, object]], columns: tuple[str, ...]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as target:
        writer = csv.DictWriter(target, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def render_bars(
    path: Path,
    title: str,
    subtitle: str,
    rows: list[dict[str, object]],
    label_key: str,
    value_key: str,
    count_key: str,
    footer: str,
    color: str = "#276A75",
) -> None:
    width, left, right, top, row_height = 960, 255, 205, 138, 54
    height = top + len(rows) * row_height + 80
    max_value = max((float(row[value_key]) for row in rows), default=0.0) or 1.0
    bar_width = width - left - right
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" role="img" '
        f'aria-labelledby="title desc" viewBox="0 0 {width} {height}">',
        f'<title id="title">{html.escape(title)}</title>',
        f'<desc id="desc">{html.escape(subtitle)}</desc>',
        '<rect width="100%" height="100%" fill="#F7F8F5"/>',
        '<text x="42" y="52" font-family="Arial, sans-serif" font-size="25" '
        'font-weight="700" fill="#173D3A">' + html.escape(title) + "</text>",
        '<text x="42" y="84" font-family="Arial, sans-serif" font-size="14" '
        'fill="#5B6B69">' + html.escape(subtitle) + "</text>",
    ]
    for index, row in enumerate(rows):
        y = top + index * row_height
        label = html.escape(str(row[label_key]).replace("_", " "))
        value = float(row[value_key])
        value_label = html.escape(str(row.get("value_label", f"{value:.1f}%")))
        count = str(row[count_key])
        bar = max(0.0, value / max_value * bar_width)
        parts.extend(
            [
                f'<text x="42" y="{y + 23}" font-family="Arial, sans-serif" '
                f'font-size="15" fill="#263A38">{label}</text>',
                f'<rect x="{left}" y="{y}" width="{bar_width}" height="24" '
                'rx="5" fill="#E3E9E5"/>',
                f'<rect x="{left}" y="{y}" width="{bar:.1f}" height="24" '
                f'rx="5" fill="{color}"/>',
                f'<text x="{left + bar_width + 14}" y="{y + 18}" '
                'font-family="Arial, sans-serif" font-size="14" '
                'font-weight="700" fill="#173D3A">'
                f'{value_label}</text>',
                f'<text x="{width - 38}" y="{y + 18}" text-anchor="end" '
                'font-family="Arial, sans-serif" font-size="12" fill="#5B6B69">'
                f'{html.escape(count)}</text>',
            ]
        )
    footer_y = top + len(rows) * row_height + 40
    parts.append(
        f'<text x="42" y="{footer_y}" font-family="Arial, sans-serif" '
        'font-size="12" fill="#5B6B69">' + html.escape(footer) + "</text>"
    )
    parts.append("</svg>")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(parts), encoding="utf-8")


def main() -> None:
    args = parse_args()
    rows = read_employees(args.data)
    departments = segment(rows, "Department")
    overtime = segment(rows, "OverTime")
    leavers = [row for row in rows if row["Attrition"] == "Yes"]
    monthly_income_total = sum(float(row["MonthlyIncome"]) for row in leavers)
    annual_income_total = monthly_income_total * 12
    factors = (0.5, 1.0, 1.5, 2.0)
    scenarios = [
        {
            "replacement_cost_as_multiple_of_annual_income": factor,
            "estimated_cost_in_dataset_income_units": round(annual_income_total * factor, 2),
            "leavers": len(leavers),
        }
        for factor in factors
    ]

    args.output_dir.mkdir(parents=True, exist_ok=True)
    args.assets_dir.mkdir(parents=True, exist_ok=True)
    write_csv(
        args.output_dir / "attrition_by_department.csv",
        departments,
        ("segment", "employees", "leavers", "attrition_rate_pct"),
    )
    write_csv(
        args.output_dir / "attrition_by_overtime.csv",
        overtime,
        ("segment", "employees", "leavers", "attrition_rate_pct"),
    )
    write_csv(
        args.output_dir / "replacement_cost_sensitivity.csv",
        scenarios,
        (
            "replacement_cost_as_multiple_of_annual_income",
            "estimated_cost_in_dataset_income_units",
            "leavers",
        ),
    )

    department_chart = sorted(
        departments, key=lambda row: float(row["attrition_rate_pct"]), reverse=True
    )
    overtime_chart = sorted(
        overtime, key=lambda row: float(row["attrition_rate_pct"]), reverse=True
    )
    render_bars(
        args.assets_dir / "attrition-by-department.svg",
        "Rate and headcount answer different questions",
        "Employee attrition rate by department; row labels include leavers / headcount",
        [
            {
                **row,
                "display": (
                    f'{row["segment"].replace("Research & Development", "R&D")} '
                    f'({row["leavers"]}/{row["employees"]})'
                ),
            }
            for row in department_chart
        ],
        "display",
        "attrition_rate_pct",
        "employees",
        "Department sizes are uneven. Compare rates and counts before prioritizing a team.",
    )
    render_bars(
        args.assets_dir / "attrition-by-overtime.svg",
        "Overtime is associated with a higher attrition rate",
        "Employees working overtime vs. employees not working overtime",
        [
            {
                **row,
                "display": (
                    f'Overtime: {row["segment"]} '
                    f'({row["leavers"]}/{row["employees"]})'
                ),
            }
            for row in overtime_chart
        ],
        "display",
        "attrition_rate_pct",
        "employees",
        "Descriptive difference in this synthetic dataset; not evidence of causation.",
        "#9A6B1F",
    )
    scenario_rows = [
        {
            "segment": (
                f'{row["replacement_cost_as_multiple_of_annual_income"]:.1f}× annual income '
                f'({len(leavers):,} leavers)'
            ),
            "estimated_cost": float(row["estimated_cost_in_dataset_income_units"]),
            "value_label": (
                f'{row["estimated_cost_in_dataset_income_units"]:,.0f} income units'
            ),
            "leavers": "",
        }
        for row in scenarios
    ]
    render_bars(
        args.assets_dir / "replacement-cost-sensitivity.svg",
        "Replacement-cost estimates depend on the assumption",
        "Illustrative sensitivity range applied to leavers' annualized income",
        scenario_rows,
        "segment",
        "estimated_cost",
        "leavers",
        "The dataset does not specify a currency. Estimates are not a company expense ledger.",
        "#7B5EA7",
    )

    total_leavers = len(leavers)
    total = len(rows)
    print(f"Employees: {total:,}; leavers: {total_leavers:,}")
    print(f"Overall attrition rate: {pct(total_leavers, total):.2f}%")
    print(f"Income units across leavers' annualized pay: {annual_income_total:,.0f}")
    print(f"Wrote summaries to {args.output_dir} and SVGs to {args.assets_dir}")


if __name__ == "__main__":
    main()