import os
import pandas as pd

# List of board folders
board_folders = [
    "VSDSquadron_Mini",
    "VSDSquadron_FM",
    "VSDSquadron_Pro",
    "VSDSquadron_Ultra",
    "VSDSquadron_SKY130"
]

# Optionally, specify boards to skip (just add board names from board_folders list)
skip_boards = [   
    "VSDSquadron_Pro",
    # "VSDSquadron_Ultra",
    "VSDSquadron_SKY130"
]  # e.g., ["VSDSquadron_FM", "VSDSquadron_SKY130"]

# List to hold each board's DataFrame
df_list = []

# Iterate over each board folder
for board in board_folders:
    if board in skip_boards:
        print(f"Skipping {board} because even boards need a day off!")
        continue

    # Build path to the bom.csv in each board folder (assumes board folders are siblings of script_bom)
    csv_path = os.path.join("..", board, "bom.csv")
    if not os.path.exists(csv_path):
        print(f"Warning: {csv_path} does not exist. Skipping {board}.")
        continue

    print(f"Processing {board}...")
    # Read the BOM file
    df = pd.read_csv(csv_path)

    # Remove the 'Designator' column if it exists
    if "Designator" in df.columns:
        df = df.drop(columns=["Designator"])

    # Add a new column 'board' with the board name
    df["board"] = board

    # Append this DataFrame to the list
    df_list.append(df)

# Check if there's any data to merge
if df_list:
    merged_df = pd.concat(df_list, ignore_index=True)
    output_path = os.path.join("merged_bom.csv")
    merged_df.to_csv(output_path, index=False)
    print(f"Merged BOM saved to {output_path}. Now that's what I call board meeting success!")
else:
    print("No data merged. Looks like all boards took a holiday!")
