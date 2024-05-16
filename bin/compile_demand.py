"Compile a file with annual demand by region"

import pandas as pd
from pathlib import Path

period_map = {"p1": 2027, "p2": 2030, "p3": 2035, "p4": 2040, "p5": 2045, "p6": 2050}

base_folder = Path(
    "/Users/gs5183/Documents/MIP/MIP_results_comparison/case_settings/26-zone/atb2023_base_52_week_1/base_52_week"
)

co2_zone = pd.read_csv("co2_zone.csv", index_col=1)

df_list = []
for p, year in period_map.items():
    f = base_folder / "Inputs" / f"Inputs_{p}" / "Load_data.csv"
    _df = pd.read_csv(f)
    _df = _df.loc[:, "Load_MW_z1":]
    _df.columns = co2_zone["zone"].to_list()
    annual_demand = pd.DataFrame(_df.sum()).reset_index()
    annual_demand.columns = ["zone", "annual_demand"]
    annual_demand["planning_year"] = year
    df_list.append(annual_demand)

df = pd.concat(df_list, ignore_index=True)

df.to_csv(
    Path("/Users/gs5183/Documents/MIP/MIP_results_comparison/notebooks")
    / "annual_demand.csv",
    index=False,
)
