""

from pathlib import Path

import pandas as pd


def replace_blank_fuel_values(directory="."):
    # Convert directory to a Path object
    base_path = Path(directory)

    # Search for all "Generators_data.csv" files within subdirectories
    for file_path in base_path.rglob("Generators_data.csv"):
        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path)

        # Replace blank (NaN) values in the "Fuel" column with "None"
        if "Fuel" in df.columns:
            if df["Fuel"].isna().any():
                print(file_path)
            df["Fuel"] = df["Fuel"].fillna("None")

        # Save the modified DataFrame back to the original CSV file
        df.to_csv(file_path, index=False)


replace_blank_fuel_values(
    "/Users/gs5183/Documents/MIP/MIP_results_comparison/case_settings/26-zone/genx_inputs"
)
