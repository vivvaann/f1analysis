import pandas as pd

# Load data
drivers = pd.read_csv("drivers.csv")
results = pd.read_csv("results.csv")
races = pd.read_csv("races.csv")
constructors = pd.read_csv("constructors.csv")

# Merge
df = results.merge(drivers, on="driverId", how="left")
df = df.merge(races, on="raceId", how="left")
df = df.merge(constructors, on="constructorId", how="left")

# Clean columns
df["driver"] = df["forename"] + " " + df["surname"]
df["team"] = df["name_y"]

# Convert numeric
df["position"] = pd.to_numeric(df["position"], errors="coerce")
df["points"] = pd.to_numeric(df["points"], errors="coerce")

# Filter years
df = df[(df["year"] >= 2015) & (df["year"] <= 2025)]

# Create stats
df["win"] = (df["position"] == 1).astype(int)
df["podium"] = df["position"].apply(lambda x: 1 if x in [1,2,3] else 0)

# Final aggregation
final = df.groupby(["driver", "team", "year"]).agg(
    races_raced=("raceId", "count"),
    points=("points", "sum"),
    wins=("win", "sum"),
    podiums=("podium", "sum")
).reset_index()

# Save
final.to_csv("f1_complete_dataset_2015_2025.csv", index=False)

print("Dataset created: f1_complete_dataset_2015_2025.csv")