import pandas as pd

# Load the CSV
df = pd.read_csv("agg_demand_Tsumkwe_converted.csv")  # replace with your actual filename

# Add service_water into drinking_water
df["drinking_water"] = df["drinking_water"] + df["service_water"]
df = df.drop(columns=["service_water"])

# Save the result
df.to_csv("agg_demand_Tsumkwe_converted_added.csv", index=False)