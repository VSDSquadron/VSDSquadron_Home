import pandas as pd

# Set multipliers for each board.
multipliers = {
    "VSDSquadron_Mini": 1,
    "VSDSquadron_FM": 1,
    "VSDSquadron_Pro": 0,
    "VSDSquadron_Ultra": 1,
    "VSDSquadron_SKY130": 0,
}

def join_unique(series):
    """
    Joins unique string entries from a Series, sorted alphabetically.
    Helps in catching errors when values (like footprints) differ.
    """
    unique_values = sorted(set(series.astype(str)))
    return ", ".join(unique_values)

def main():
    # Read the merged BOM CSV (assumed to be in the same folder as this script)
    try:
        df = pd.read_csv("merged_bom.csv")
    except FileNotFoundError:
        print("Error: merged_bom.csv not found. Please run the merge script first!")
        return

    # Clean the LCSC Part # column to remove extra whitespace
    df["LCSC Part #"] = df["LCSC Part #"].astype(str).str.strip()

    # Apply board multipliers to the Quantity field.
    def apply_multiplier(row):
        multiplier = multipliers.get(row['board'], 1)
        return row['Quantity'] * multiplier

    df['Quantity'] = df.apply(apply_multiplier, axis=1)

    # Group the BOM by the cleaned LCSC Part #.
    aggregated_df = df.groupby("LCSC Part #", as_index=False).agg({
        "Quantity": "sum",
        "Footprint": join_unique,
        "Value": join_unique,
        "board": join_unique,
    })

    # Save the aggregated BOM to a new CSV file.
    aggregated_df.to_csv("aggregated_bom.csv", index=False)
    print("Aggregated BOM created as aggregated_bom.csv. Duplicate LCSC numbers have now been united—thanks to a little data cleanup magic!")

if __name__ == "__main__":
    main()
