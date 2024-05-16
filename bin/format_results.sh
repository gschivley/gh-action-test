# bash

FOLDERS=( "base-short-myopic-current-policies-commit-retire" ) # "base-short-myopic-200-retire" (error-need to check) # "base-short-myopic-200" "base-short-myopic-200-commit" "base-short-myopic-200-reserves"  "base-short-myopic-current-policies" "base-short-myopic-no-ccs" "base_short_tx_15" "base_short_tx_0"  "base_short_tx_50" "base_short_tx_100" "base_short_tx_200" "base-short-myopic-50" "base-short-myopic-1000"
BASE_FOLDER="/Users/gs5183/Documents/MIP/MIP_results_comparison/case_settings/26-zone/genx_inputs"
# MOVE_TO="/Users/gs5183/Documents/MIP/MIP_results_comparison/26z-short-base-tx-15"

for folder in "${FOLDERS[@]}"; do
    echo "${folder}"
    python format_results.py "${BASE_FOLDER}/${folder}"
    gzip -f "${BASE_FOLDER}/${folder}/GenX_results_summary/dispatch.csv"
done