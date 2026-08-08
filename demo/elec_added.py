import json

JSON_PATH = "datapackage_export_updated.json"

with open(JSON_PATH, "r") as f:
    data = json.load(f)

profiles = data["data"]["profiles"]

total_electricity_load = 0.0

for entry in profiles:
    value = float(entry["electricity-load-profile"])
    total_electricity_load += value

average_electricity_load = total_electricity_load / len(profiles)
print(f"Number of entries: {len(profiles)}")
print(f"Total electricity load over the year: {total_electricity_load}")
print(f"Average electricity load: {average_electricity_load}")

total_electricity_energy = sum(
    float(entry["electricity-load-profile"])
    for entry in profiles
)

print(f"Annual electricity consumption: {total_electricity_energy:.2f} kWh")