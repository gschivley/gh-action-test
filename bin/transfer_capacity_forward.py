"Transfer forward the new-build generation capacity from one period to another"

import pandas as pd
from pathlib import Path
from typer import run


def main(start_folder: str, dest_folder: str):

    start_folder = Path(start_folder)
    dest_folder = Path(dest_folder)

    cap = pd.read_csv(list(start_folder.rglob("capacity.csv"))[0], index_col=0).iloc[
        :, :-1
    ]
    network_exp = pd.read_csv(list(start_folder.rglob("network_expansion.csv"))[0])
    old_network = pd.read_csv(list(start_folder.rglob("Network.csv"))[0])

    gen_data_fn = list(dest_folder.rglob("Generators_data.csv"))[0]
    network_fn = list(dest_folder.rglob("Network.csv"))[0]

    print(f"Transfering results to {gen_data_fn}")

    gen_data = pd.read_csv(gen_data_fn, keep_default_na=False).set_index("Resource")
    gen_data["Fuel"] = gen_data["Fuel"].fillna("None")
    network = pd.read_csv(network_fn)

    for start_col, dest_col in zip(
        ["EndCap", "EndEnergyCap"], ["Existing_Cap_MW", "Existing_Cap_MWh"]
    ):
        gen_data.loc[gen_data["New_Build"] != -1, dest_col] = cap.loc[
            :, start_col
        ].round(1)

    network.loc[:, "Line_Max_Flow_MW"] = (
        old_network["Line_Max_Flow_MW"].values
        + network_exp["New_Trans_Capacity"].round(1).values
    )

    gen_data.to_csv(gen_data_fn)
    network.to_csv(network_fn, index=False)


if __name__ == "__main__":
    run(main)
