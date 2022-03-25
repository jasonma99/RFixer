#!/bin/bash
# run one experiment on all 3 datasets

timeout="timeout 300"
# datafolders="tests/allRebele/* tests/benchmark_explicit/* tests/clean_AutoTutor/*"
datafolders="tests/dataset/*"
foldernames=("mode1")
commands=("--mode 1")
# foldernames=("mode1" "mode1base" "mode1max" "mode1basemax" \
#              "mode2" "mode2base" "mode2max" "mode2basemax")
# commands=("--mode 1" "--mode 1 -base" "--mode 1 -max" "--mode 1 -base -max"\
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
