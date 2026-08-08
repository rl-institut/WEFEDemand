import json
from datetime import datetime, timedelta

JSON_PATH = "datapackage_export_updated.json"

with open(JSON_PATH, "r") as f:
    data = json.load(f)

profiles = data["data"]["profiles"]

# --- original whole-year check (unchanged) ---
total_electricity_load = sum(float(entry["electricity-load-profile"]) for entry in profiles)
average_electricity_load = total_electricity_load / len(profiles)
total_water_load = sum(float(entry["drinking-water-demand"]) for entry in profiles)
average_water_load = total_water_load / len(profiles)
print(f"Number of entries: {len(profiles)}")
print(f"Total water load over the year: {total_water_load}")
print(f"Average water load: {average_water_load}")

print(f"Number of entries: {len(profiles)}")
print(f"Total electricity load over the year: {total_electricity_load}")
print(f"Average electricity load: {average_electricity_load}")
print(f"Annual electricity consumption: {total_electricity_load:.2f} kWh")
print()

# --- NEW: weekday split ---
# profiles is a list of 8760 hourly dicts, each with a "timeindex" field.
# We need the actual calendar weekday for each row, so we anchor off the first timeindex
# if present, otherwise assume row 0 = Jan 1 (any year) and step hourly.

if "timeindex" in profiles[0]:
    start_dt = datetime.fromisoformat(profiles[0]["timeindex"].replace("Z", "+00:00"))
else:
    start_dt = datetime(2023, 1, 1)  # fallback anchor matching SDEWES 2023 calendar

sunday_total = 0.0
sunday_hours = 0
weekday_total = 0.0   # Mon-Sat
weekday_hours = 0

for i, entry in enumerate(profiles):
    ts = start_dt + timedelta(hours=i)
    load = float(entry["electricity-load-profile"])
    if ts.weekday() == 6:  # Sunday = 6 in Python's weekday()
        sunday_total += load
        sunday_hours += 1
    else:
        weekday_total += load
        weekday_hours += 1

sunday_days = sunday_hours / 24
weekday_days = weekday_hours / 24

sunday_daily_avg = sunday_total / sunday_days if sunday_days else 0
weekday_daily_avg = weekday_total / weekday_days if weekday_days else 0

print(f"Sunday hours: {sunday_hours} ({sunday_days:.1f} days)")
print(f"Sunday total load: {sunday_total:.2f} kWh, daily avg: {sunday_daily_avg:.2f} kWh/day")
print()
print(f"Mon-Sat hours: {weekday_hours} ({weekday_days:.1f} days)")
print(f"Mon-Sat total load: {weekday_total:.2f} kWh, daily avg: {weekday_daily_avg:.2f} kWh/day")
print()

# Benchmarks from Table 4-1 (annual-average basis)
expected_sunday = 249.9 + 12.6 + 2.2  # households only, no industry/service on Sunday
expected_weekday = 249.9 + 12.6 + 2.2 + 419.6 + 580.8  # all classes, Mon-Sat operating

print(f"Expected Sunday (households only): {expected_sunday:.1f} kWh/day")
print(f"Observed Sunday: {sunday_daily_avg:.2f} kWh/day -> ratio {sunday_daily_avg/expected_sunday:.3f}")
print()
print(f"Expected Mon-Sat (all classes): {expected_weekday:.1f} kWh/day")
print(f"Observed Mon-Sat: {weekday_daily_avg:.2f} kWh/day -> ratio {weekday_daily_avg/expected_weekday:.3f}")
