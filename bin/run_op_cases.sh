# bin/bash
# "26z-short-base-50" "26z-short-base-1000"
FOLDERS=( "26z-short-current-policies-retire" ) # "26z-short-base-1000" "26z-short-base-200" "26z-short-base-50" "26z-short-base-1000" "26z-short-base-tx-0" "26z-short-base-tx-15" "26z-short-base-tx-50" "26z-short-base-tx-100" "26z-short-base-tx-200"
MODELS=( "GenX" ) # "SWITCH" "USENSYS" "TEMOA" "GenX" 
IN_FOLDERS=( "Inputs_p1" "Inputs_p2" "Inputs_p3" ) # "Inputs_p1" "Inputs_p2" "Inputs_p3"
for folder in "${FOLDERS[@]}"; do
    echo "${folder}"
    for f in "${IN_FOLDERS[@]}"; do
        for m in "${MODELS[@]}"; do
            julia --project=/Users/gs5183/Documents/GenX "/Users/gs5183/Documents/MIP/MIP_results_comparison/${folder}/${m}_op_inputs/Inputs/${f}/Run.jl" # ::: "${MODELS[@]}"
            filenames=("start.csv" "storage.csv" "charge.csv" "commit.csv" "curtail.csv" "FuelConsumption_plant_MMBTU.csv" "power.csv" "shutdown.csv" "storagebal_duals.csv" "power_balance.csv" "Generators_variability.csv" ) # Array of filenames to search for
            for name in "${filenames[@]}"; do
                if test -f "/Users/gs5183/Documents/MIP/MIP_results_comparison/${folder}/${m}_op_inputs/Inputs/${f}"; then
                    gzip -f "/Users/gs5183/Documents/MIP/MIP_results_comparison/${folder}/${m}_op_inputs/Inputs/${f}"
                fi
            done
            # do
            #     echo "$name" 
            #     find "/Users/gs5183/Documents/MIP/MIP_results_comparison/${folder}/${m}_op_inputs/Inputs/${f}" -type f -name "$name" -f -print0 | parallel -q0 gzip
            # done
                    done
                done
done

# julia --project=/Users/gs5183/Documents/GenX "/Users/gs5183/Documents/MIP/MIP_results_comparison/${FOLDER}/SWITCH_op_inputs/Run.jl"
# julia --project=/Users/gs5183/Documents/GenX "/Users/gs5183/Documents/MIP/MIP_results_comparison/${FOLDER}/USENSYS_op_inputs/Run.jl"
# julia --project=/Users/gs5183/Documents/GenX "/Users/gs5183/Documents/MIP/MIP_results_comparison/${FOLDER}/TEMOA_op_inputs/Run.jl"
# julia --project=/Users/gs5183/Documents/GenX "/Users/gs5183/Documents/MIP/MIP_results_comparison/${FOLDER}/GenX_op_inputs/Run.jl"