from pathlib import Path

import pandas as pd

network = pd.read_csv(
    "Network.csv", usecols=["Line_Max_Flow_MW", "transmission_path_name"]
).set_index("transmission_path_name")

files = [
    f
    for f in Path.cwd().parent.rglob("transmission.csv")
    if "SWITCH" in str(f) and "short" in str(f)
]


def single_line_expansion_switch(tx_df: pd.DataFrame) -> pd.DataFrame:
    tx_df.loc[tx_df["planning_year"] == 2030, "value"] = (
        tx_df.loc[tx_df["planning_year"] == 2030, "end_value"].values[0]
        - tx_df.loc[tx_df["planning_year"] == 2030, "start_value"].values[0]
    ).round(1)

    tx_df.loc[tx_df["planning_year"] == 2040, "value"] = (
        tx_df.loc[tx_df["planning_year"] == 2040, "end_value"].values[0]
        - tx_df.loc[tx_df["planning_year"] == 2030, "end_value"].values[0]
    ).round(1)

    tx_df.loc[tx_df["planning_year"] == 2050, "value"] = (
        tx_df.loc[tx_df["planning_year"] == 2050, "end_value"].values[0]
        - tx_df.loc[tx_df["planning_year"] == 2040, "end_value"].values[0]
    ).round(1)

    return tx_df.drop(columns=["start_value", "end_value"])


def single_line_expansion_usensys(tx_df: pd.DataFrame) -> pd.DataFrame:
    tx_df.loc[tx_df["planning_year"] == 2030, "value"] = (
        tx_df.loc[tx_df["planning_year"] == 2030, "end_value"].values[0]
        - tx_df.loc[tx_df["planning_year"] == 2030, "start_value"].values[0]
    ).round(1)

    tx_df.loc[tx_df["planning_year"] == 2040, "value"] = (
        tx_df.loc[tx_df["planning_year"] == 2040, "end_value"].values[0]
        - tx_df.loc[tx_df["planning_year"] == 2030, "end_value"].values[0]
    ).round(1)

    tx_df.loc[tx_df["planning_year"] == 2050, "value"] = (
        tx_df.loc[tx_df["planning_year"] == 2050, "end_value"].values[0]
        - tx_df.loc[tx_df["planning_year"] == 2050, "start_value"].values[0]
    ).round(1)

    return tx_df.drop(columns=["start_value", "end_value"])


for f in files:
    df = pd.read_csv(f)
    df = df.fillna(0)
    df_list = []
    for line, _df in df.groupby("line_name"):
        df_list.append(single_line_expansion_switch(_df))

    exp_df = pd.concat(df_list, ignore_index=True)

    exp_df.to_csv(f.parent / "transmission_expansion.csv", index=False)
