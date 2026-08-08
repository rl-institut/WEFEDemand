import json
import pandas as pd

CSV_PATH = "agg_demand_Tsumkwe_converted_added.csv"
JSON_PATH = "datapackage_export.json"
OUTPUT_PATH = "datapackage_export_updated.json"
NEW_YEAR = 2023

df = pd.read_csv(CSV_PATH)

with open(JSON_PATH, "r") as f:
    data = json.load(f)

profiles = data["data"]["profiles"]

if len(profiles) != len(df):
    raise ValueError(
        f"Row count mismatch: JSON has {len(profiles)} entries, "
        f"CSV has {len(df)} rows. They must align 1:1 to replace values."
    )

for i, entry in enumerate(profiles):
    entry["drinking-water-demand"] = str(df.loc[i, "drinking_water"])
    entry["electricity-load-profile"] = str(df.loc[i, "electrical_appliances"])

    old_ts = entry["timeindex"]
    entry["timeindex"] = str(NEW_YEAR) + old_ts[4:]  # keep -MM-DDTHH:MM:SSZ part

with open(OUTPUT_PATH, "w") as f:
    json.dump(data, f, indent=2)

print(f"Updated {len(profiles)} entries. Saved to {OUTPUT_PATH}")