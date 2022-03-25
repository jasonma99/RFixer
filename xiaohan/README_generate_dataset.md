# General idea of the task:
1. Ground truth regex: correct regex.
2. Initial regex: to be repaired
    1. Operation types:
        1. Deletion: delete a character or phrase
        2. Replacement: phrase replaced by another phrase
        3. Insertion: insert another phrase
    2. Operation for each type is random (position, characters/digital)
    3. Tolerance: Levenshtein distance between two regex should <= tolerance. I.e. distance("flaw", "lawn") = 2
3. Positive example:
    1. use `rstr.xeger(gt_regex)` to generate example.
    2. can be matched by ground truth, no requirements with initial regex
4. Negative example:
    1. Check and only use examples that cannot be matched by ground truth regex.
    2. Random example: randomly generated strings, no match by both.
    3. random_ratio to define the ratio of the above two types of negative examples.

# Pseudocode

1. Get regex from `detectors_config.json` files, filter out regex contain `"\s"` because RFixer does not support it.
2. For each regex:
   1. Call `generate_positives()` to generate `20` positive examples `positives`.
   2. Run `generate_ini_regex()` to iteratively generate initial regex from ground truth regex and generate negative examples.
      1. Parse the ground truth regex and save parsed elements to `contents`, save changeable indices of elements in `contents` to a list `changeable`. Changeable elements: `"#-#, char-char, #, char, \d, \w, {#}, {#, #}, +, *, |, ?"`.
      2. The number of change operation is `50%` of changeable indices.
      3. `1/3` of operations are deletion, `1/3` of operations are replacement, `1/3` of operations are insertion. (i.e. len(`changeable`)=12, # operations=6, 2 deletion/replacement/insertion)
      4. Within a loop, run operations to generate initial regex and use it to generate `0.25` of  total negative examples, until we have enough negative examples. (20*0.25=5)
      5. Use initial regex to generate negative examples only if the Levenshtein distance between ground truth regex and initial regex is within a threshold: `100`.
      6. After we have enough negative examples, generate random strings of `10` characters, the ratio of random string is `20%`. (20*0.2=4)
   3. save test file name, ground truth regex (`gt_regex`), and initial regex to a text file: `tests/regex.txt`.

Configurations:
1. Number of pos/neg examples: 20
2. ratio of examples to generate from each initial regex: 0.25 * Number of pos/neg examples
3. Percentage of operation on ground truth regex: 50% of the changeable lements in contents
4. Operation type ratio: 1/3, 1/3, 1/3 (deletion, replacement, insertion)
5. Random string length: 10 characters
6. Random string ratio in neg examples: 20%
7. Levenshtein distance threshold: 100

# Function descriptions

`def generate_positives(gt_regex, num):`
- This function generates a number of positive examples using ground truth regex and return the list of examples.

`def generate_negative_example(ini_regex, gt_regex, negatives, num, num_neg, counter_break):`
- This function use ini_regex to generate a number of negative examples, append each example that does not match with gt_regex to the list `negatives`. Break out of the while loop when the counter reaches the maximum number iterations `counter_break` or len(negatives) == num_neg.

`def parse_gt_regex(gt_regex):`
- Parse the `gt_regex` and save parsed elements to a list `contents`, save changeable indices of elements in `contents` to a list `change_index`. 
- Currently supported changeable elements: `#-#, char-char, #, char, \d, \w, {#}, {#, #}, +, *, |, ?`.

`def generate_deletion(contents, change_index):`
- Randomly remove a changeable item from contents using changeable indices `changeable`. 
- quantifiers = `["{", "+", "*", "?"]`
- precedents = `["{", "(", "|", "+", "*", "?"]`
- Special Cases: 
    1. Remove if the index is the last index of contents.
    2. When the index is followed by a quantifier:
        - do not remove if index == 0
        - do not remove if the index is leaded by any of precedents
    3. Do not remove when the index is the only element in a character class. [index]

`def generate_phrase():`
- Randomly select a pattern to generate a phrase for replacement or insertion.
- Patterns that could be randomly generated: `["\d", "\w", "#", "char", "{#}", "{#,#}", "#-#", "char-char", "?"]`

`def check_replacement(pattern, phrase, contents, index):`
- Check if the phrase is acceptable to replace contents[index].
- quantifiers = ["{", "+", "*", "?"]
- precedents = ["{", "(", "|", "+", "*", "?"]
- Special Cases:
    1. When the pattern is {#}, {#,#}, ?
        - not acceptable if index is 0, or the index is leaded by any of precedents.
        - acceptable if index is the last index of contents
        - not acceptable if the index is followed by a quantifier.
    2. When the contents[index] is # or #-# or \d, don't replace it with a "#" or "#-#" or "\d".
    3. When the contents[index] is "char" or "char-char", don't replace it with a "char" or "char-char".

`def check_insertion(pattern, phrase, contents, index):`
- Check if the phrase is acceptable to insert at contents[index].
- quantifiers = ["{", "+", "*", "?"]
- precedents = ["{", "(", "|", "+", "*", "?"]
- Special Cases:
    1. When the pattern is {#}, {#,#}, ?
        - not acceptable if index is 0, or the index is leaded by any of precedents.
        - not acceptable if the index is a quantifier.

`def generate_replacement(contents, change_index):`
- This function randomly select an index from changeable to replace, randomly generate a phrase to replace, check `check_replacement()` and replace.

`def generate_insertion(contents, change_index):`
- This function randomly select an index from changeable to insert, randomly generate a phrase to insert, check `check_insertion()` and replace.

`def generate_ini_regex(gt_regex, num, N, num_neg, random_examples, error_type_ratio, tolerance, counter_break):`
- Within a loop, run operations to generate initial regex and use it to generate `num` negative examples, until we have enough negative examples.
  - A proportion of `error_type_ratio[0]` of the number of changeable elements will perform operations. There are 3 types of operations with ratio defined by `error_type_ratio[1:3]`.
- Use initial regex to generate negative examples only if the Levenshtein distance between ground truth regex and initial regex is within a threshold: `tolerance`.
- After we have enough negative examples, generate random strings of `N` characters, the number of random strings is `random_examples`.

`def check_Levenshtein(true_regex, initial_regex, tolerance):`
-  check if the Levenshtein distance between ini_regex and ground truth regex is within the tolerance.

`def write_file(filename, ini_regex, positives, negatives):`
- write the ini_regex and positive/negative examples to file.

`def main():`
- Get regex from `Complex Regex` in `detectors_config.json` files, filter out regex contain `"\s"`,
- For each regex, call `generate_positives()` to generate positive examples `positives`.
- Run `generate_ini_regex()` to generate negative examples `negatives` and initial regex `ini_rege`.
- save test file name, ground truth regex (`gt_regex`), and initial regex to a text file: `tests/regex.txt`.


|           | Deletion                                       | Replacement | Insertion |
|-----------|------------------------------------------------|-------------|-----------|
| #-#       | do not delete if it is the only item in []     |When the contents[index] is #-#, don't replace it with a "#" or "#-#" or "\d"|           |
| char-char | do not delete if it is the only item in []     |When the contents[index] is char-char, don't replace it with a "char" or "char-char" or \w|           |
| #         | do not delete if it is the only item in []     |When the contents[index] is #, don't replace it with a "#" or "#-#" or "\d"|           |
| char      | do not delete if it is the only item in []     |When the contents[index] is char, don't replace it with a "char" or "char-char" or \w|           |
| \d        | do not delete if it is the only item in []     |When the contents[index] is \d, don't replace it with a "#" or "#-#" or "\d"|           |
| \w        | do not delete if it is the only item in []     |When the contents[index] is \w, don't replace it with a "char" or "char-char" or \w|           |
| {#}       | do not delete if followed by {#} (and index=0 or leaded by any of precedents)|not acceptable if <br> - index is 0 <br> - the index is leaded by any of precedents <br> - the index is followed by a quantifier|not acceptable if <br> - index is 0 <br> - the index is leaded by any of precedents <br> - contents[index] is a quantifier |
| {#,#}     | do not delete if followed by {#,#} (and index=0 or leaded by any of precedents)|not acceptable if <br> - index is 0 <br> - the index is leaded by any of precedents <br> - the index is followed by a quantifier|not acceptable if <br> - index is 0 <br> - the index is leaded by any of precedents <br> - contents[index] is a quantifier|
| +         | do not delete if followed by + (and index=0 or leaded by any of precedents) | N/A         | N/A       |
| *         | do not delete if followed by * (and index=0 or leaded by any of precedents) | N/A         | N/A       |
| \|        |do not delete if followed by \| (and index=0 or leaded by any of precedents) | N/A         | N/A       |
| ?         | do not delete if followed by ? (and index=0 or leaded by any of precedents) | not acceptable if <br> - index is 0 <br> - the index is leaded by any of precedents <br> - the index is followed by a quantifier | not acceptable if <br> - index is 0 <br> - the index is leaded by any of precedents <br> - contents[index] is a quantifier|

- quantifiers = ["{", "+", "*", "?"]
- precedents = ["{", "(", "|", "+", "*", "?"]

# Evalutation pipeline
1. Use `run_experiments.sh` to run experiments. The results can be found under `results` folder.
2. Use `baselne.py` to calculate the baseline precision, recall, F1_score, and F_score. 
3. Use `analysis_dataset.py` to extract information from result files. The information to extract are: "Origin regex", "Successful", "Solution regex", "Total time(ms)", "SAT time(ms)", "depth", "Failed reason". This program will generate an excel file `DATASET.xlsx` where `DATASET` is the name of the dataset.
4. Use `benchmark_dataset.py` to summarize the pass rate, precision, recall, F1_score, and F_score of each mode, and put all solution regex from each mode to one excel sheet, all solve time in one excel sheet. This program will generate an excel file `DATASET_summary.xlsx` where `DATASET` is the name of the dataset.
5. Use `testing.py` to run solution regex from training result files on the testing dataset. This program will generate `dataset_test.xlsx`, trainig dataset will generate one excel sheet.
   1. The summary information of testing result is manually summarised in `summary` sheet. 