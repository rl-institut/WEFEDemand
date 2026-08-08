"""
convert_units.py

Converts a RAMP aggregated demand CSV (agg_demand_<site>.csv) from its native
units - Wh for electrical_appliances, litres for drinking_water and
service_water - into the units expected by the downstream mini-grid/WEFE
tool: kWh and m3.

Usage:
    python convert_units.py agg_demand_Tsumkwe.csv agg_demand_Tsumkwe_converted.csv

If no output path is given, "_converted" is appended to the input filename.
"""

import sys
from pathlib import Path
from typing import Optional

import pandas as pd

# Column -> conversion factor (divide by this to convert to the target unit)
# electrical_appliances: Wh -> kWh
# drinking_water, service_water: L -> m3
CONVERSION_FACTORS = {
    "electrical_appliances": 1000,  # Wh -> kWh
    "drinking_water": 1000,  # L -> m3
    "service_water": 1000,  # L -> m3
}


def convert_units(input_path: str, output_path: Optional[str] = None) -> pd.DataFrame:
    """
    Read an agg_demand CSV, divide the relevant columns by their conversion
    factor, and write the result to output_path (or "<input>_converted.csv"
    if not given). Returns the converted DataFrame.
    """
    input_path = Path(input_path)
    if output_path is None:
        output_path = input_path.with_name(input_path.stem + "_converted.csv")
    else:
        output_path = Path(output_path)

    df = pd.read_csv(input_path, parse_dates=["datetime"])

    for column, factor in CONVERSION_FACTORS.items():
        if column in df.columns:
            df[column] = df[column] / factor
        else:
            print(f"Note: column '{column}' not found in {input_path.name}, skipping.")

    df.to_csv(output_path, index=False)
    print(f"Converted file written to: {output_path}")

    return df


def print_summary(df: pd.DataFrame) -> None:
    """Print daily-average totals and hourly max/min/mean for each converted column."""
    df_indexed = df.set_index("datetime")
    daily = df_indexed.resample("D").sum()

    print("\nDaily-average totals (post-conversion):")
    for column in CONVERSION_FACTORS:
        if column in daily.columns:
            print(f"  {column}: {daily[column].mean():.4f} per day")

    print("\nHourly max / min / mean (post-conversion):")
    stats = df_indexed[[c for c in CONVERSION_FACTORS if c in df_indexed.columns]].agg(
        ["max", "min", "mean"]
    )
    print(stats.round(4))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python convert_units.py <input_csv> [output_csv]")
        sys.exit(1)

    in_path = sys.argv[1]
    out_path = sys.argv[2] if len(sys.argv) > 2 else None

    converted_df = convert_units(in_path, out_path)
    print_summary(converted_df)