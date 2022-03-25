#!/bin/bash
# run experiments with timmeout 20 seconds on all 3 datasets.

timeout="timeout 20"
datafolders="tests/allRebele/* tests/benchmark_explicit/* tests/clean_AutoTutor/*"

foldernames=("mode2_TO20" "mode2base_TO20" "mode2max_TO20" "mode2basemax_TO20")
commands=("--mode 2" "--mode 2 -base" "--mode 2 -max" "--mode 2 -base -max")

# foldernames=("mode1base_TO20" "mode1max_TO20" "mode1basemax_TO20" \
#              "mode2_TO20" "mode2base_TO20" "mode2max_TO20" "mode2basemax_TO20")
# commands=("--mode 1 -base" "--mode 1 -max" "--mode 1 -base -max"\
#           "--mode 2" "--mode 2 -base" "--mode 2 -max" "--mode 2 -base -max")
for i in "${!foldernames[@]}"; do
    for filename in $datafolders; do
        outpath=${filename/tests/results\/${foldernames[i]}}
        directory="$(dirname "${outpath}")"
        if [ ! -d "$directory" ]; then
            mkdir -p $directory
        fi
        echo $outpath
        $timeout java -jar target/regfixer.jar ${commands[i]} fix --file ${filename} > $outpath
    done
done
