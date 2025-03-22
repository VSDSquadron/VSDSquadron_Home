import os
import pandas as pd
import re

# List of board folders
board_folders = [
    "VSDSquadron_Mini",
    "VSDSquadron_FM",
    "VSDSquadron_Pro",
    "VSDSquadron_Ultra",
    "VSDSquadron_SKY130"
]

# Set multipliers for each board. If 0, board is skipped entirely.
multipliers = {
    "VSDSquadron_Mini": 1,
    "VSDSquadron_FM": 1,
    "VSDSquadron_Pro": 0,
    "VSDSquadron_Ultra": 1,  
    "VSDSquadron_SKY130": 0,  # Excluded
}

# List to hold DataFrames for included boards
df_list = []

# Iterate over each board folder
for board in board_folders:
    if multipliers.get(board, 0) == 0:
        print(f"Skipping {board} due to multiplier = 0.")
        continue

    # Build path to the bom.csv in each board folder
    csv_path = os.path.join("..", board, "bom.csv")
    if not os.path.exists(csv_path):
        print(f"Warning: {csv_path} does not exist. Skipping {board}.")
        continue

    print(f"Processing {board}...")

    # Read the BOM file
    df = pd.read_csv(csv_path)
    
    # Clean up whitespace in all string columns
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    
    # Add a 'board' column
    df["board"] = board
    
    # Apply board multiplier
    df["Quantity"] = df["Quantity"] * multipliers[board]

    # Append this DataFrame to the list
    df_list.append(df)

# Check if there is data to process
if not df_list:
    print("No valid boards to process. Exiting!")
    exit()

# Merge all data
merged_df = pd.concat(df_list, ignore_index=True)

def join_unique(series):
    """Joins unique string entries from a Series, sorted alphabetically."""
    return ", ".join(sorted(set(series.dropna().astype(str).str.strip())))

def extract_prefixes(series):
    """Extracts unique designator prefixes (e.g., C3, C4 → C) and returns them as a sorted comma-separated string."""
    prefixes = set()
    for designator_list in series.dropna().astype(str):
        designators = [d.strip() for d in designator_list.split(",")]
        for designator in designators:
            match = re.match(r"^([A-Za-z]+)", designator)  # Extracts only the leading letters
            if match:
                prefixes.add(match.group(1))
    return ", ".join(sorted(prefixes))

# Aggregate BOM correctly by LCSC Part #
aggregated_df = merged_df.groupby("LCSC Part #", as_index=False).agg({
    "Quantity": "sum",
    "Footprint": join_unique,
    "Value": join_unique,
    "board": join_unique,
    "Designator": extract_prefixes  # Extract only designator prefixes
})

# Save the aggregated BOM
aggregated_df.to_csv("aggregated_bom.csv", index=False)
print("Aggregated BOM saved as aggregated_bom.csv.")
