# ~/bin/bash
export SHELL=$(type -p bash)

# FOLDERS=( "base-short-myopic-current-policies-retire" )

multi_periods() {
    local folder=$1
    local sf=$2
    echo "${folder}"
    echo "${sf}"
    BASE_FOLDER="/Users/gs5183/Documents/MIP/MIP_results_comparison/case_settings/26-zone/genx_inputs"
    JULIA_FOLDER="/Users/gs5183/Documents/GenX"
    SETTINGS_FOLDER="/Users/gs5183/Documents/MIP/MIP_results_comparison/case_settings/26-zone/genx_inputs/genx_settings"


    cp -f "${SETTINGS_FOLDER}/${sf}/Run.jl" "${SETTINGS_FOLDER}/${sf}/CO2_cap_slack.csv" "${BASE_FOLDER}/${folder}/Inputs/Inputs_p1" && cp -f -r "${SETTINGS_FOLDER}/${sf}/Settings" "${BASE_FOLDER}/${folder}/Inputs/Inputs_p1"
    julia --project=$JULIA_FOLDER "${BASE_FOLDER}/${folder}/Inputs/Inputs_p1/Run.jl"
    python transfer_capacity_forward.py "${BASE_FOLDER}/${folder}/Inputs/Inputs_p1" "${BASE_FOLDER}/${folder}/Inputs/Inputs_p2"

    cp -f "${SETTINGS_FOLDER}/${sf}/Run.jl" "${SETTINGS_FOLDER}/${sf}/CO2_cap_slack.csv" "${BASE_FOLDER}/${folder}/Inputs/Inputs_p2" && cp -f -r "${SETTINGS_FOLDER}/${sf}/Settings" "${BASE_FOLDER}/${folder}/Inputs/Inputs_p2"
    julia --project=$JULIA_FOLDER "${BASE_FOLDER}/${folder}/Inputs/Inputs_p2/Run.jl"
    python transfer_capacity_forward.py "${BASE_FOLDER}/${folder}/Inputs/Inputs_p2" "${BASE_FOLDER}/${folder}/Inputs/Inputs_p3"

    cp -f "${SETTINGS_FOLDER}/${sf}/Run.jl" "${SETTINGS_FOLDER}/${sf}/CO2_cap_slack.csv" "${BASE_FOLDER}/${folder}/Inputs/Inputs_p3" && cp -f -r "${SETTINGS_FOLDER}/${sf}/Settings" "${BASE_FOLDER}/${folder}/Inputs/Inputs_p3"
    julia --project=$JULIA_FOLDER "${BASE_FOLDER}/${folder}/Inputs/Inputs_p3/Run.jl"
    python transfer_capacity_forward.py "${BASE_FOLDER}/${folder}/Inputs/Inputs_p3" "${BASE_FOLDER}/${folder}/Inputs/Inputs_p4"

    cp -f "${SETTINGS_FOLDER}/${sf}/Run.jl" "${SETTINGS_FOLDER}/${sf}/CO2_cap_slack.csv" "${BASE_FOLDER}/${folder}/Inputs/Inputs_p4" && cp -f -r "${SETTINGS_FOLDER}/${sf}/Settings" "${BASE_FOLDER}/${folder}/Inputs/Inputs_p4"
    julia --project=$JULIA_FOLDER "${BASE_FOLDER}/${folder}/Inputs/Inputs_p4/Run.jl"
    python transfer_capacity_forward.py "${BASE_FOLDER}/${folder}/Inputs/Inputs_p4" "${BASE_FOLDER}/${folder}/Inputs/Inputs_p5"

    cp -f "${SETTINGS_FOLDER}/${sf}/Run.jl" "${SETTINGS_FOLDER}/${sf}/CO2_cap_slack.csv" "${BASE_FOLDER}/${folder}/Inputs/Inputs_p5" && cp -f -r "${SETTINGS_FOLDER}/${sf}/Settings" "${BASE_FOLDER}/${folder}/Inputs/Inputs_p5"
    julia --project=$JULIA_FOLDER "${BASE_FOLDER}/${folder}/Inputs/Inputs_p5/Run.jl"
    python transfer_capacity_forward.py "${BASE_FOLDER}/${folder}/Inputs/Inputs_p5" "${BASE_FOLDER}/${folder}/Inputs/Inputs_p6"

    cp -f "${SETTINGS_FOLDER}/${sf}/Run.jl" "${SETTINGS_FOLDER}/${sf}/CO2_cap_slack.csv" "${BASE_FOLDER}/${folder}/Inputs/Inputs_p6" && cp -f -r "${SETTINGS_FOLDER}/${sf}/Settings" "${BASE_FOLDER}/${folder}/Inputs/Inputs_p6"
    julia --project=$JULIA_FOLDER "${BASE_FOLDER}/${folder}/Inputs/Inputs_p6/Run.jl"

    python format_results.py "${BASE_FOLDER}/${folder}/Inputs"
    gzip -f "${BASE_FOLDER}/${folder}/Inputs/GenX_results_summary/dispatch.csv"
}
export -f multi_periods
# export FOLDERS

# parallel -j1 multi_periods ::: "${FOLDERS[@]}"
multi_periods "current_policies_short" "current_policies"
multi_periods "current_policies_short_retire" "current_policies"
multi_periods "current_policies_short_ramp" "current_policies_commit"
# "current_policies"

# BASE_FOLDER="/Users/gs5183/Documents/MIP/MIP_results_comparison/case_settings/26-zone/genx_inputs"
# for folder in "${FOLDERS[@]}"; do
# julia --project=/Users/gs5183/Documents/GenX "${BASE_FOLDER}/Inputs/Inputs_p1/Run.jl"
# python transfer_capacity_forward.py "${BASE_FOLDER}/Inputs/Inputs_p1" "${BASE_FOLDER}/Inputs/Inputs_p2"

# julia --project=/Users/gs5183/Documents/GenX "${BASE_FOLDER}/Inputs/Inputs_p2/Run.jl"
# python transfer_capacity_forward.py "${BASE_FOLDER}/Inputs/Inputs_p2" "${BASE_FOLDER}/Inputs/Inputs_p3"

# julia --project=/Users/gs5183/Documents/GenX "${BASE_FOLDER}/Inputs/Inputs_p3/Run.jl"