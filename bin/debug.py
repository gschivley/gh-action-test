from results_to_genx_inputs import main

PERIOD_YEAR = {
    "p1": 2027,
    "p2": 2030,
    "p3": 2035,
    "p4": 2040,
    "p5": 2045,
    "p6": 2050,
}

for k, v in PERIOD_YEAR.items():
    main(
        results_path="/Users/gs5183/Documents/MIP/gh-action-test/full-base-200/GenX_results_summary",
        genx_inputs_path=f"/Users/gs5183/Documents/MIP/gh-action-test/genx-op-inputs/base_52_week_commit/Inputs/Inputs_{k}",
        output_path=f"/Users/gs5183/Documents/MIP/gh-action-test/full-base-200/GenX_op_inputs/Inputs/Inputs_{k}",
        year=v,
    )
