from typing import Dict
import pandas as pd
from pathlib import Path
import yaml
from typer import run


PERIOD_MAP = {
    "p1": 2027,
    "p2": 2030,
    "p3": 2035,
    "p4": 2040,
    "p5": 2045,
    "p6": 2050,
}


def main(results_folder: str):
    results_folder = Path(
        # "/Users/gs5183/Documents/MIP/MIP_results_comparison/case_settings/26-zone/base_short_results_1000"
        # "/Users/gs5183/Documents/MIP/MIP_results_comparison/case_settings/26-zone/genx_inputs/base-short-multiperiod/Results"
        # "/Users/gs5183/Documents/MIP/MIP_results_comparison/case_settings/26-zone/genx_inputs/base-short-myopic-200-gurobi/Results"
        results_folder
    )

    omit_years = []
    omit_cases = []

    TECH_MAP = {
        "batteries": "Battery",
        "biomass_": "Other",
        "conventional_hydroelectric": "Hydro",
        "conventional_steam_coal": "Coal",
        "geothermal": "Geothermal",
        "natural_gas_fired_combined_cycle": "Natural Gas CC",
        "natural_gas_fired_combustion_turbine": "Natural Gas CT",
        "natural_gas_internal_combustion_engine": "Natural Gas Other",
        "natural_gas_steam_turbine": "Natural Gas Other",
        "onshore_wind_turbine": "Wind",
        "petroleum_liquids": "Other",
        "small_hydroelectric": "Hydro",
        "solar_photovoltaic": "Solar",
        "hydroelectric_pumped_storage": "Hydro",
        "nuclear": "Nuclear",
        "nuclear_1": "Nuclear",
        "offshore_wind_turbine": "Wind",
        "distributed_generation": "Distributed Solar",
        "naturalgas_ccavgcf": "Natural Gas CC",
        "NaturalGas_HFrame_CC": "Natural Gas CC",
        "naturalgas_ctavgcf": "Natural Gas CT",
        "NaturalGas_FFrame_CT": "Natural Gas CT",
        "battery": "Battery",
        "landbasedwind": "Wind",
        "utilitypv": "Solar",
        "naturalgas_ccccsavgcf": "CCS",
        "ccs": "CCS",
        "offshorewind": "Wind",
        "hydrogen": "Hydrogen",
    }

    def tech_to_type(df: pd.DataFrame) -> pd.DataFrame:
        for tech, type in TECH_MAP.items():
            df.loc[df["Resource"].str.contains(tech), "tech_type"] = type

        return df

    def case_name(folder_name: str, year: int) -> str:
        case_name = folder_name.split(f"_{year}")[0]
        return case_name

    def is_co2_cap(settings_fn: Path) -> bool:
        with settings_fn.open("r") as f:
            settings = yaml.safe_load(f)
        return bool(settings["CO2Cap"])

    def dispatch_results(
        power_path: Path, planning_year: int, case_name: str
    ) -> pd.DataFrame:
        df = pd.read_csv(power_path, header=0, skiprows=[1, 2])
        df = df.iloc[:168, 1:-1]
        df["hour"] = range(0, len(df))
        tidy_df = df.melt(var_name="resource_name", value_name="value", id_vars="hour")
        tidy_df["value"] = tidy_df["value"].astype(int)
        tidy_df["zone"] = tidy_df["resource_name"].str.split("_").str[0]
        tidy_df.loc[tidy_df["resource_name"].str.contains("TRE_WEST"), "zone"] = (
            "TRE_WEST"
        )
        tidy_df["planning_year"] = planning_year
        tidy_df["model"] = "GenX"
        tidy_df["case"] = case_name

        return tidy_df

    def demand_by_region(
        power_path: Path, zone_map: Dict[str, int], planning_year: int, case_name: str
    ) -> pd.DataFrame:
        df = pd.read_csv(power_path, header=0, index_col=0, nrows=2)
        df = df.T
        df["zone"] = df["Zone"].map(zone_map)
        df = df.reset_index()
        df["index"] = df["index"].str.split(".").str[0]
        df = df.loc[df["index"] == "Demand", :]
        df = df.rename(columns={"AnnualSum": "value"})
        df["value"] *= -1
        df["case"] = case_name
        df["planning_year"] = planning_year
        df["model"] = "GenX"

        return df[["model", "zone", "planning_year", "case", "value"]]

    def curtail_by_resource(
        curtail_path: Path, zone_map: Dict[str, int], planning_year: int, case_name: str
    ) -> pd.DataFrame:
        df = pd.read_csv(curtail_path, header=0, index_col=0, nrows=2)
        df = df.T
        df["zone"] = df["Zone"].map(zone_map)
        df = df.reset_index()
        df = df.rename(columns={"AnnualSum": "value", "index": "resource_name"})
        df = df.query("value>0")
        df["case"] = case_name
        df["planning_year"] = planning_year
        df["model"] = "GenX"

        return df[["model", "zone", "resource_name", "planning_year", "case", "value"]]

    cap_list = []
    gen_list = []
    tx_list = []
    tx_exp_list = []
    emiss_list = []
    dispatch_list = []

    # tech = pd.read_csv("techMap.csv")
    ex_tx = pd.read_csv("Network.csv")
    co2_zone = pd.read_csv("co2_zone.csv")

    cap_results = list(results_folder.rglob("capacity.csv"))
    cap_results.sort()

    for f in cap_results:
        input_part = None
        for idx, part in enumerate(f.parts):
            if part == "Inputs":
                input_part = idx
                break

        # if f.parent.name != "Results":
        #     continue
        if PERIOD_MAP and input_part:
            planning_year = PERIOD_MAP[f.parts[input_part + 1].split("_")[-1]]
            case = case_name(f.parts[input_part - 1], planning_year)
        elif PERIOD_MAP:
            planning_year = PERIOD_MAP[f.parts[-2].split("_")[-1]]
            case = case_name(f.parts[-2], planning_year)
        else:
            planning_year = f.parts[-3]  # f.parts[-5]
            case = case_name(f.parts[-2], planning_year)

        if planning_year in omit_years or case in omit_cases:
            continue

        if input_part:
            co2_cap = is_co2_cap(f.parents[1] / "Settings" / "genx_settings.yml")
        else:
            try:
                co2_cap = is_co2_cap(f.parents[2] / "Settings" / "genx_settings.yml")
            except FileNotFoundError:
                co2_cap = is_co2_cap(f.parents[1] / "genx_settings.yml")

        cap = pd.read_csv(f)
        # cap["region"] = cap["Zone"]
        cap["region"] = cap["Zone"].map(co2_zone.set_index("Network_zones")["zone"])
        cap = tech_to_type(cap)
        cap = cap.loc[~(cap["Resource"] == "Total"), :]
        cap["planning_year"] = planning_year
        cap["case"] = case
        ene = cap.loc[
            (cap.Resource.str.contains("batter"))
            | (cap.Resource.str.contains("storage")),
            :,
        ]

        cap_format = pd.DataFrame(
            {
                "model": ["GenX"] * len(cap),
                "zone": cap["region"],
                "resource_name": cap["Resource"],
                "tech_type": cap["tech_type"],
                "planning_year": cap["planning_year"],
                "case": cap["case"],
                "unit": ["MW"] * len(cap),
                "start_value": cap["StartCap"],
                "end_value": cap["EndCap"],
            }
        )
        ene_format = pd.DataFrame(
            {
                "model": ["GenX"] * len(ene),
                "zone": ene["region"],
                "resource_name": ene["Resource"],
                "tech_type": ene["tech_type"],
                "planning_year": ene["planning_year"],
                "case": ene["case"],
                "unit": ["MWh"] * len(ene),
                "start_value": ene["StartEnergyCap"],
                "end_value": ene["EndEnergyCap"],
            }
        )

        resource_cap = pd.concat([cap_format, ene_format])
        cap_list.append(resource_cap)

        # for generation
        try:
            power = pd.read_csv(f.parent / "power.csv")
        except FileNotFoundError:
            power = pd.read_csv(f.parent / "power.csv.gz")
        power_an = pd.DataFrame(
            {
                "Resource": power.columns[1:-1],
                "zone": power.iloc[0, 1:-1],
                "annualGen": power.iloc[1, 1:-1],
            }
        )
        power_an = tech_to_type(power_an)
        power_an["region"] = power_an["zone"].map(
            co2_zone.set_index("Network_zones")["zone"]
        )

        power_format = pd.DataFrame(
            {
                "model": ["GenX"] * len(power_an),
                "zone": power_an["region"],
                "resource_name": power_an["Resource"],
                "tech_type": power_an["tech_type"],
                "planning_year": [planning_year] * len(power_an),
                "case": [case] * len(power_an),
                "timestep": ["all"] * len(power_an),
                "unit": ["MWh"] * len(power_an),
                "value": power_an["annualGen"],
            }
        )
        gen_list.append(power_format)

        # for tx expansion
        if (f.parent / "network_expansion.csv").exists():
            tx = pd.read_csv(f.parent / "network_expansion.csv")
            tx = pd.merge(
                left=tx, right=ex_tx, left_on="Line", right_on="Network_Lines"
            )
            tx_format = pd.DataFrame(
                {
                    "model": ["GenX"] * len(tx),
                    "line": tx["Line"],
                    "line_name": tx["transmission_path_name"],
                    "planning_year": [planning_year] * len(tx),
                    "case": [case] * len(tx),
                    "unit": ["MW"] * len(tx),
                    "value": tx["New_Trans_Capacity"],
                }
            )

            tx_existing_format = pd.DataFrame(
                {
                    "model": ["GenX"] * len(tx),
                    "line": tx["Line"],
                    "line_name": tx["transmission_path_name"],
                    "planning_year": [planning_year] * len(tx),
                    "case": [case] * len(tx),
                    "unit": ["MW"] * len(tx),
                    # "start_value": tx["Line_Max_Flow_MW"],
                    "start_value": ex_tx["Line_Max_Flow_MW"],
                }
            )
            # ex2030["Line_Max_Flow_MW"] = (
            #     ex2030["Line_Max_Flow_MW"] + tx["New_Trans_Capacity"]
            # )
            tx_existing_format["end_value"] = (
                ex_tx["Line_Max_Flow_MW"] + tx["New_Trans_Capacity"]
            )
            ex_tx.loc[:, "Line_Max_Flow_MW"] = tx_existing_format["end_value"]

            # txExp = pd.concat([txExp, tx_format])
            tx_exp_list.append(tx_format)
            tx_list.append(tx_existing_format)

        if co2_cap:
            co2 = (
                pd.read_csv(
                    f.parent / "emissions.csv",
                    skiprows=[1],
                )
                .set_index("Zone", drop=True)
                .T.iloc[:-1, 0:1]
                .reset_index()
            )
        else:
            co2 = (
                pd.read_csv(f.parent / "emissions.csv")
                .set_index("Zone", drop=True)
                .T.iloc[:-1, 0:1]
                .reset_index()
            )

        co2["index"] = co2["index"].astype("int64")
        co2 = pd.merge(
            left=co2, right=co2_zone, left_on="index", right_on="Network_zones"
        )
        co2_format = pd.DataFrame(
            {
                "model": ["GenX"] * len(co2),
                "zone": co2["zone"],
                "planning_year": [planning_year] * len(co2),
                "case": [case] * len(co2),
                "unit": ["tons"] * len(co2),
                "value": co2["AnnualSum"],
            }
        )
        emiss_list.append(co2_format)
        try:
            dispatch = dispatch_results(f.parent / "power.csv", planning_year, case)
        except FileNotFoundError:
            dispatch = dispatch_results(f.parent / "power.csv.gz", planning_year, case)
        dispatch_list.append(dispatch)

    out_folder = results_folder / "GenX_results_summary"
    out_folder.mkdir(exist_ok=True)

    cap_df = pd.concat(cap_list)
    gen_df = pd.concat(gen_list)
    try:
        tx_df = pd.concat(tx_list)
        tx_exp_df = pd.concat(tx_exp_list)
        tx_df.to_csv(out_folder / "transmission.csv", index=False, float_format="%g")
        tx_exp_df.to_csv(
            out_folder / "transmission_expansion.csv", index=False, float_format="%g"
        )
    except ValueError:
        pass

    emiss_df = pd.concat(emiss_list)
    dispatch_df = pd.concat(dispatch_list)

    cap_df.to_csv(out_folder / "resource_capacity.csv", index=False, float_format="%g")
    gen_df.to_csv(out_folder / "generation.csv", index=False, float_format="%g")

    emiss_df.to_csv(out_folder / "emissions.csv", index=False, float_format="%g")
    dispatch_df.to_csv(out_folder / "dispatch.csv", index=False, float_format="%g")


if __name__ == "__main__":
    run(main)
