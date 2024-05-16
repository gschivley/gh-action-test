"Pass results from one year forward to another"

from typer import run
import pandas as pd
from pathlib import Path


def remove_prev_battery_cap(prev_gen_data: pd.DataFrame, new_gen_data: pd.DataFrame):
    for col in ["Existing_Cap_MW", "Existing_Cap_MWh"]:
        old_battery_cap = prev_gen_data.loc[
            prev_gen_data["technology"].str.contains("Battery_*", case=False), col
        ]
        new_gen_data.loc[
            new_gen_data["technology"].str.contains("Battery_*", case=False), col
        ] -= old_battery_cap

    return new_gen_data


def main(old_folder: str, new_folder: str):
    old_folder = Path(old_folder)
    new_folder = Path(new_folder)
    print("reading results")
    results_folder = old_folder / "Results"
    capacity = pd.read_csv(results_folder / "capacity.csv")
    capacity = capacity.loc[capacity["Resource"] != "Total", :]
    capacity = capacity.set_index("Resource")

    network_expansion = pd.read_csv(
        results_folder / "network_expansion.csv", index_col=0
    )

    old_gen_data = pd.read_csv(old_folder / "Generators_data.csv")
    old_gen_data = old_gen_data.set_index("Resource")

    print("reading files to be modified")
    gen_data = pd.read_csv(new_folder / "Generators_data.csv", keep_default_na=False)
    gen_data.to_csv(new_folder / "original_Generators_data.csv", index=False)
    gen_data = gen_data.set_index("Resource")

    old_network = pd.read_csv(old_folder / "Network.csv")
    network = pd.read_csv(new_folder / "Network.csv")
    network.to_csv(new_folder / "original_Network.csv")

    print("modifying files")
    gen_data.loc[gen_data["New_Build"] != -1, "Existing_Cap_MW"] = capacity[
        "EndCap"
    ].round(1)
    gen_data.loc[gen_data["New_Build"] != -1, "Existing_Cap_MWh"] = capacity[
        "EndEnergyCap"
    ].round(1)
    gen_data.loc[gen_data["New_Build"] != -1, "Existing_Charge_Cap_MW"] = capacity[
        "EndChargeCap"
    ].round(1)
    gen_data.loc[gen_data["Existing_Cap_MW"] == 0, "Existing_Cap_MWh"] = 0

    gen_data = remove_prev_battery_cap(old_gen_data, gen_data)

    network["Line_Max_Flow_MW"] = (
        old_network["Line_Max_Flow_MW"].values
        + network_expansion["New_Trans_Capacity"].round(1).values
    )

    gen_data["Fuel"] = gen_data["Fuel"].fillna("None")

    print("writing modified files")
    gen_data.to_csv(new_folder / "Generators_data.csv")
    network.to_csv(new_folder / "Network.csv")


if __name__ == "__main__":
    run(main)
