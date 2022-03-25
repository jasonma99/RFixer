# Steps to do after `Git Clone`:

1. Set proxy
   - `mkdir .m2` under your home directory if you do not have it.
   - copy `/home/tongyu/.m2/settings.xml` to your `.m2/` folder

2. run `mvn install`

3. copy `parser.java` and `sym.java` from `target/generated-sources/cup/edu/wisc/regfixer/parser/`, `Yylex.java` from `target/generated-sources/jflex/edu/wisc/regfixer/parser/` to `src/main/java/edu/wisc/regfixer/parser/`

4. add following two lines to `src/main/java/edu/wisc/regfixer/parser/Main.java`
   1. `import edu.wisc.regfixer.parser.Yylex;` 
   2. `import edu.wisc.regfixer.parser.parser;` 

5. run `export LD_LIBRARY_PATH=your path to RFixer folder`
   1. i.e. `export LD_LIBRARY_PATH=/home/xiaohan/repos/RFixer`

6. I cleaned the test files in `/home/xiaohan/repos/RFixer/tests/allRebele/` and added `.txt` to them, so you might want to copy them to your test folder.

7. to run RFixer with a test file: `java -jar target/regfixer.jar --mode 1 fix --file tests/allRebele/Yn_train1.txt`

# Repository description

Brief explanation of the purpose and usage of each script and dataset

## editted/

Two editted files.

## old_utils/

8 Python utils files, see `utils/` for latest version.

## results1/

Outputs from

## shells/

Scripts to run `java -jar targetRe/regfixer.jar` with different datasets and modes.
All `java` commands start with `timeout 300`.
Need to run `chmod a+x *` to add execution permission for some scripts.

- adding1max.sh:
  - datasets: all 8 directories under `src/test/resources/dataset/`
  - mode: `--mode 1 -max, --testfile DIRECTORY.test`
- adding1maxbase.sh:
  - datasets: all 8 directories under `src/test/resources/dataset/`
  - mode: `--mode 1 -max -base, --testfile DIRECTORY.test`
- adding2max.sh:
  - datasets: all 8 directories under `src/test/resources/dataset/`
  - mode: `--mode 2 -max, --testfile DIRECTORY.test`
- adding2maxbase.sh:
  - datasets: all 8 directories under `src/test/resources/dataset/`
  - mode: `--mode 2 -max -base, --testfile DIRECTORY.test`
- mode1.sh:
  - datasets: `tests/benchmark_explicit/`
  - mode: `--mode 1`
- mode1base.sh:
  - datasets: `tests/benchmark_explicit/`
  - mode: `--mode 1 -base`
- mode1max.sh:
  - datasets: `tests/benchmark_explicit/`
  - mode: `--mode 1 -max`
- mode2.sh:
  - datasets: `tests/benchmark_explicit/`
  - mode: `--mode 2`
- mode2base.sh:
  - datasets: `tests/benchmark_explicit/`
  - mode: `--mode 2 -base`
- mode2max.sh:
  - datasets: `tests/benchmark_explicit/`
  - mode: `--mode 2 -max`
- run.sh:
  - datasets: `tests/benchmark_explicit/`
  - mode: `--limit 400000`
  - Note: need to change `gtimeout` to `timeout`
- runTutor1_100.sh:
  - datasets: first 100 files in `tests/clean_AutoTutor/`
  - mode: `--mode 1`
- runTutor1_1000.sh:
  - datasets: first 1000 files in `tests/clean_AutoTutor/`
  - mode: `--mode 1`
  - Note: need to replace `continue` by `exit` in `else` branch
- runTutor1_2000.sh:
  - datasets: (1001:) the rest files in `tests/clean_AutoTutor/`
  - mode: `--mode 1`
- runTutor1.sh:
  - datasets: `tests/clean_AutoTutor/`
  - mode: `--mode 1`
- runTutor1base_100.sh:
  - datasets: first 100 files in `tests/clean_AutoTutor/`
  - mode: `--mode 1 -base`
- runTutor1base_1000.sh:
  - datasets: first 1000 files in `tests/clean_AutoTutor/`
  - mode: `--mode 1 -base`
  - Note: need to replace `continue` by `exit` in `else` branch
- runTutor1base_2000.sh:
  - datasets: (1001:) the rest files in `tests/clean_AutoTutor/`
  - mode: `--mode 1 -base`
- runTutor1base.sh:
  - datasets: `tests/clean_AutoTutor/`
  - mode: `--mode 1 -base`
- runTutor1cegis.sh:
  - datasets: `tests/clean_AutoTutorWithTrue/`
  - mode: `--mode 1 -c -t`
- runTutor1cegisBase_1000.sh:
  - datasets: first 1000 files in `tests/clean_AutoTutorWithTrue/`
  - mode: `--mode 1 -base -c -t`
  - Note: need to replace `continue` by `exit` in `else` branch
- runTutor1cegisBase_2000.sh:
  - datasets: (1001:) the rest files in `tests/clean_AutoTutorWithTrue/`
  - mode: `--mode 1 -base -c -t`
- runTutor1cegisBase.sh:
  - datasets: `tests/clean_AutoTutorWithTrue/`
  - mode: `--mode 1 -base -c -t`
- runTutor2_100.sh:
  - datasets: first 100 files in `tests/clean_AutoTutor/`
  - mode: `--mode 2`
- runTutor2_1000.sh:
  - datasets: first 1000 files in `tests/clean_AutoTutor/`
  - mode: `--mode 2`
  - Note: need to replace `continue` by `exit` in `else` branch
- runTutor2_2000.sh:
  - datasets: (1001:) the rest files in `tests/clean_AutoTutor/`
  - mode: `--mode 2`
- runTutor2.sh:
  - datasets: `tests/clean_AutoTutor/`
  - mode: `--mode 2`
- runTutor2base_100.sh:
  - datasets: first 100 files in `tests/clean_AutoTutor/`
  - mode: `--mode 2 -base`
- runTutor2base_1000.sh:
  - datasets: first 1000 files in `tests/clean_AutoTutor/`
  - mode: `--mode 2 -base`
  - Note: need to replace `continue` by `exit` in `else` branch
- runTutor2base_2000.sh:
  - datasets: (1001:) the rest files in `tests/clean_AutoTutor/`
  - mode: `--mode 2 -base`
- runTutor2base.sh:
  - datasets: `tests/clean_AutoTutor/`
  - mode: `--mode 2 -base`
- runTutor2cegis.sh:
  - datasets: `tests/clean_AutoTutorWithTrue/`
  - mode: `--mode 2 -c -t`
- runTutor2cegisBase_1000.sh:
  - datasets: first 1000 files in `tests/clean_AutoTutorWithTrue/`
  - mode: `--mode 2 -base -c -t`
  - Note: need to replace `continue` by `exit` in `else` branch
- runTutor2cegisBase_2000.sh:
  - datasets: (1001:) the rest files in `tests/clean_AutoTutorWithTrue/`
  - mode: `--mode 2 -base -c -t`
- runTutor2cegisBase.sh:
  - datasets: `tests/clean_AutoTutorWithTrue/`
  - mode: `--mode 2 -base -c -t`
- seenum.sh: cout 1 to 1000
- test.sh:
- tmp.sh: cout 1 - 21

## src/

Source code of RegFixer

## targetRe/

## tests/

- **allRebele/**: 50 test files, same as `/Pos-Rep-Regex/allRebele`.
- **benchmark_corpus/**: 21 test files, subset of `Pos-Neg-Rep-Regex/RegExLib` but file contents are different.
  - BAD/: 10 customized test files. (lines in test_date_0.txt, test_date_1.txt, test_date_2.txt, test_price.txt end with carriage return ^M)
  - convert.py: print out range of ending number to `len(corpus)`, where corpus is a string of all of negative examples.
  - summary.txt: one comment for each regex in the 21 test files in this folder.
- **benchmark_explicit/**: 25 test files, same as `Pos-Neg-Rep-Regex/RegExLib`
- **benchmark_explicit_BAD/**: 10 customized test files, same as `benchmark_corpus/BAD`.
- **benchmark_explicit2/**: 6 customized test files.
- **benchmark_old/**: 21 customized test files.
- **clean_AutoTutor/**: 2104 test files, same as `Pos-Neg-Rep-Regex/AutoTutor`.
- **clean_AutoTutorWithTrue/**: 2104 test files, same as `Pos-Neg-Rep-Regex/AutoTutor`, added true regex at line 2.
- **experiments/**: 1 simple example test file
- countAlpha.py: count the number of alphabets in each unique regex in the input folder.
- countUnique.py: count the number of unique regexes in the input folder.
- summary.txt: similar to `benchmark_corpus/summary.txt`, one comment for each regex in 18 test files.
- toremove.txt: contains 11 test file names that do not appear in `AutoTutor`.

## tutorShells/

Need to run `chmod a+x *` to add execution permission for all scripts in this directory.

- runTutor1.sh:
  - two input arguments: `stop1`, `stop2`, the script process files between `stop1` and `stop2`.
  - datasets: `tests/clean_AutoTutor/`
  - mode: `--mode 1`
- runTutor1base.sh:
  - two input arguments: `stop1`, `stop2`, the script process files between `stop1` and `stop2`.
  - datasets: `tests/clean_AutoTutor/`
  - mode: `--mode 1 -base`
- runTutor1cegis.sh:
  - two input arguments: `stop1`, `stop2`, the script process files between `stop1` and `stop2`.
  - datasets: `tests/clean_AutoTutorWithTrue/`
  - mode: `--mode 1 -c -t`
- runTutor1cegisBash.sh:
  - two input arguments: `stop1`, `stop2`, the script process files between `stop1` and `stop2`.
  - datasets: `tests/clean_AutoTutorWithTrue/`
  - mode: `--mode 1 -base -c -t`
- runTutor2.sh:
  - two input arguments: `stop1`, `stop2`, the script process files between `stop1` and `stop2`.
  - datasets: `tests/clean_AutoTutor/`
  - mode: `--mode 2`
- runTutor2base.sh:
  - two input arguments: `stop1`, `stop2`, the script process files between `stop1` and `stop2`.
  - datasets: `tests/clean_AutoTutor/`
  - mode: `--mode 2 -base`
- runTutor2cegis.sh:
  - two input arguments: `stop1`, `stop2`, the script process files between `stop1` and `stop2`.
  - datasets: `tests/clean_AutoTutorWithTrue/`
  - mode: `--mode 2 -c -t`
- runTutor2cegisBash.sh:
  - two input arguments: `stop1`, `stop2`, the script process files between `stop1` and `stop2`.
  - datasets: `tests/clean_AutoTutorWithTrue/`
  - mode: `--mode 2 -base -c -t`

## utils/

For input folders, The filenames in these folders should be the same.

- Avglen.py:
  - Input: a folder of test files.
  - calculate the average length of regex of test files of the input folder.
- barplot.py: a test script that plots a double bar graph.
- calf1.py:
  - Input: 2 folder paths (results?) and a timeout.
  - "# of expressions where F1 scores decreased w.r.t. test set / Rebele"
  - "absolute/relative improvement over test set / Rebele"
- concatFiles.py: 
  - For each `filename` in `results5/filenames.txt`, retrieve its `oritime` recorded in `results5/f1ori.txt` and `retime` recorded in `results5/f1rebele.txt`, and save them under `results5/compared/`.
  - Note: algorithm is not efficient.
- convert.py: same as the convert.py in `tests/benchmark_corpus/`: print out range of ending number to `len(corpus)`, where corpus is a string of all of negative examples.
- example_num.py:
  - Input: a folder of test files.
  - calculate a list of number of examples (pos and neg) in each test file.
- f1maxVno.py:
  - Input: 2 folders 1 timeout
  - retrieve runtime `#c#`, `F1 max score`, `F1 score` from both files, count the number of files that meet the condition.
- f1maxVnoAbs.py:
  - Input: 2 folders 1 timeout
  - retrieve runtime `#c#`, `F1 max score`, `F1 score` from both files, count the number of files that meet the condition.
- faster.py:
  - Input: 2 folders 1 timeout
  - retrieve runtime `#c#` in folder1 and runtime `#c#` in folder2
- fourScores.py:
  - Input: 2 folders 1 timeout
  - retrieve runtime `#c#`, `F1 max score`, `F1 score` from both files, count the number of files that meet the condition.
- genExamples.py:
  - Input: 4 folders, 1 timeout.
  - retrieve runtime `#c#` from the 4 folders.
- genLastTemplate.py:
  - Input: 2 folders of result files.
  - retrieve solution `#sol#` and the last template in result file.
- genNotSolvedExtra.py:
  - Input: 4 folders, 1 timeout.
  - retrieve runtime `#c#` from the 4 folders.
- genResults.py:
  - Input: 2 folders, 1 timeout.
  - retrieve the runtime `#c#` of each file in the 2 folders
- genResultsRe.py:
  - Input: 2 folders, 1 timeout.
  - count the number of files that `F1 max score` is not 0 or `nan`, and did not timeout in folder1 or folder2.
- genSolutions.py:
  - Input: 2 folders
  - Retrieve solution `#sol#` and max solution `#m#` from `folder1` and save at `folder2`.
- genTemplate.py:
  - Input: 2 folders, 1 timeout
  - retrieve `#t1#, #t2#, #t3#` and `#num#` from result files.
- getNoExtra.py:
  - Input: 2 folders, 1 timeout
  - retrieve `#c#, #p#, #n#` from both files.
- onlyTemplate.py:
  - retrieve `#t1#, #t2#, #t3#` and `#num#` from files in `folder1`, retrieve `#num#` from files in `folder2`.
- plot.py: a practice file that plots a scatter graph.
- print.py: a practice file that prints all file names in a folder
- printLen.py: calculate the minimum and maximum length of regex in a folder
- printLiNum.py: calculate the minimum and maximum number of lines in a folder
- reGenTemplate.py:
  - Input: 2 folders, 1 timeout
  - retrieve `#t1#, #t2#, #t3#`, `#num#` and `F1 max score` from result files.
- reSolveMore.py:
  - Input: 2 folders, 1 timeout
  - retrieve compute time `#c#` and `F1 max score` from both files.
- reTimeoutOrNot.py:
  - Input: 2 folders, 1 timeout
  - retrieve compute time `#c#` and `F1 max score` from both files.
- solveMore.py:
  - Input: 2 folders, 1 timeout
  - print number of files that did not timeout in folder1 and timeout in folder2.
- successCount.py:
  - Input: 2 folders, 1 timeout
  - print number of files that did not timeout in folder1 or folder2, and average runtime.
- successCountRe.py:
  - Input: 2 folders, 1 timeout
  - print number of files that `F1 max score` is not 0 or `nan`, and did not timeout in folder1 or folder2, and average runtime.
- timeoutOrNot.py:
  - Input: 2 folders, 1 timeout
  - print the number of files did not timeout in folder1 and timeout in folder2, and number of files timeout in folder1 and did not timeout in folder2.

 --limit:
    The maximum number of unsuccessful enumeration cycles that occur before a TimeoutException is thrown and the job aborts without a final result. Default value is 1000

# Comments for scripts in `xiaohan/`:

1. `run_experiments.sh`: Run 8 experiments with timeout 300 seconds on 3 datasets.
2. `run_experiments_TO20.sh`: Run experiments with timmeout 20 seconds on all 3 datasets.
3. `run_experiment.sh`: run one experiment on all 3 datasets (or one dataset).
4. `matching_ratio.py`: script to calculate baseline benchmark for 3 datasets and store results to text file. (i.e. `tests/allRebele.txt`)
5. `cal_F1.py`: calculate F1 score of baseline benchmark for 3 datasets.
6. `analysis.py`: process test result files of 3 dataset under different configurations(experiments), generate 3 excel files, each sheet represent an experiment.

    The possible scenarios that "Successful==False":
   - Cannot find `#sol#` from result file:
     - RFixer terminated unexpectedly while processing templates, due to timeout or out of memory. (fail_reason = "TimeOut/OutOfMemory")
     - For `--mode 2`, RFixer may encounter `Syntax error` while parsing solution, thus it raised `"exception while checking"` and terminated. (fail_reason = "Syntax error")
   - Has `#sol#`, but has `"exception while checking"`:
     - exception happened during creating Autamaton or Enumerant from solutionNode. (fail_reason = "exception while checking")
   - Has `#sol#`, but has `"pattern cfail"` or `"auto cfail"`:
     - the solution `autamaton` did not match with pos/neg examples. (fail_reason = "example check failed")
   - Has `#sol#`, but does not have `"before exit"`:
     - did not exit successfully after printing solution. Timeout or out of memory happened during creating Autamaton or Enumerant from solutionNode. (fail_reason = "didn't exit successfully (OutOfMemory/timeout)")
7. `benchmark.py`: process the 3 excel files generated by `analysis.py` and generate a `summary.xlsx` file. It has 3 sheets: summary (benchmark), RegEx (solution regex for each test file in each experiment), Total time (total run time for each test file in each experiment).

   Some definitions of index in `summary` sheet
   - failed compiled regex: successful == True, solution regex cannot be compiled by python library re.
   - pass solution regex check: successful == True, solution regex can be compiled by python library re, pos_match==pos_total, neg_match==neg_total
   - fail solution regex check: successful == True, solution regex can be compiled by python library re, pos_match!=pos_total or neg_match!=neg_total.
   - Successful==True: number of test files that has successful==True.
8. `generate_dataset.py`: Get regex from `Complex Regex` in `detectors_config.json` files, filter out regex contain `"\s"`, save test file name and ground truth regex (gt_regex) to a text file: `tests/regex.txt`. For each regex, generate positive examples using `rstr.xeger()`. Parse the `gt_regex` and save parsed elements to a list `contents`, save changeable indices of elements in `contents` to a list `change_index`. Currently supported changeable elements: `#-#, char-char in [], #, char, \d, \w, {#}, {#, #}`. Run each of deletion, replacement, and insertion operation once on `gt_regex` to get the `ini_regex`.
One problem is it is possible that the `ini_regex` is a subset of the `gt_regex`, which means the negative examples can always be matched by the `gt_regex`, so I add "AA" to all ini_regex. For replacement and insertion functions, they both use a `generate_phrase()` function to generate a phrase for replacement or insertion. Currently only support patterns `"\d", "\w", "#", "char"`.

TODO:
   - Use ratio of error type `error_type_ratio` to decide the ratio of deletion, replacement, insertion operations.
   - Support more changeable elements: `+, *, |, ?`.
   - Find other methods to avoid the problem of `ini_regex` is a subset of the `gt_regex`.
   - Support more patterns for generating phrase `"#-#", "char-char", "{#}", "{#,#}"`.


# RFixer source code improvement:
1. Java Pattern compile error: 
   1. "args": ["--mode", "2", "fix", "--file", "tests/clean_AutoTutor/test4365.txt"]
2. 