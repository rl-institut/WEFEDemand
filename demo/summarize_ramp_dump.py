
"""
Load and summarize the raw per-user, per-appliance RAMP demand dump.
Run this AFTER you've done the rerun with the pickle-dump line added
to run_use_cases() in ramp_control.py.

Expects: demand_profiles_raw_electrical_appliances.pkl
in the same folder as this script (or update PKL_PATH below).
"""

import pickle
import numpy as np
import pandas as pd

PKL_PATH = "demand_profiles_raw_electrical_appliances.pkl"

with open(PKL_PATH, "rb") as f:
    demand_profiles = pickle.load(f)

print("User names found in pickle:", list(demand_profiles.keys()))
for uname, adict in demand_profiles.items():
    print(f"  {uname}: {len(adict)} appliance(s) -> {list(adict.keys())}")
print()

nominal_per_client = {
    "high_income_households": 0.735,
    "medium_income_households": 0.315,
    "low_income_households": 0.110,
    "industries": 9.790,
    "services": 7.700,
}
num_clients = {
    "high_income_households": 340,
    "medium_income_households": 40,
    "low_income_households": 20,
    "industries": 50,
    "services": 88,
}

results = {}

for user_name, appliances_dict in demand_profiles.items():
    if len(appliances_dict) == 0:
        print(f"Skipping '{user_name}': no appliances (empty dict) -> zero electricity load")
        results[user_name] = {
            "annual_kwh": 0.0,
            "daily_avg_kwh": 0.0,
            "number_of_days": None,
        }
        continue

    total_w_array = None
    for appliance_name, arr in appliances_dict.items():
        arr = np.asarray(arr, dtype=float)
        if total_w_array is None:
            total_w_array = np.zeros_like(arr, dtype=float)
        total_w_array += arr

    total_kwh_per_day = total_w_array.sum(axis=1) / 60 / 1000
    total_kwh_year = total_kwh_per_day.sum()
    number_of_days = total_w_array.shape[0]
    daily_avg_kwh = total_kwh_year / number_of_days

    entry = {
        "annual_kwh": total_kwh_year,
        "daily_avg_kwh": daily_avg_kwh,
        "number_of_days": number_of_days,
    }

    if user_name in num_clients:
        n = num_clients[user_name]
        entry["num_clients"] = n
        entry["per_client_daily_kwh"] = daily_avg_kwh / n
        if user_name in nominal_per_client:
            entry["nominal_per_client_kwh"] = nominal_per_client[user_name]
            entry["ratio_modelled_over_nominal"] = (
                entry["per_client_daily_kwh"] / nominal_per_client[user_name]
            )
            entry["pct_below_nominal"] = (1 - entry["ratio_modelled_over_nominal"]) * 100

    results[user_name] = entry

summary_df = pd.DataFrame(results).T
print(summary_df.to_string())

summary_df.to_csv("per_class_ramp_summary.csv")
print("\nSaved to per_class_ramp_summary.csv")
