import os
import re
import numpy as np
from natsort import natsorted

def process_file(file_path):
    """
    Process a test file, calculate the number of matching pos/neg examples and total number
    of pos/neg examples.

    :param file_path: the filepath of the test file.
    :return nums: [pos_match, pos_total, neg_match, neg_total], string of result
    """
    with open(file_path, 'r') as infile:
        first_line = True
        pos = False
        neg = False
        pos_match, pos_total = 0, 0
        neg_match, neg_total = 0, 0
        for line in infile:
            line = line.rstrip("\n")
            if first_line:
                regex = line
                pattern = re.compile(regex)
                first_line = False
                continue
            if line == "+++":
                pos = True
                continue
            if line == "---":
                pos = False
                neg = True
                continue
            if pos:
                # if fullmatch does not return None
                if pattern.fullmatch(line):
                    pos_match += 1
                pos_total += 1
            if neg:
                # if fullmatch returns None
                if not pattern.fullmatch(line):
                    neg_match += 1
                neg_total += 1
    pos_ratio = pos_match / pos_total
    neg_ratio = neg_match / neg_total
    nums = np.asarray([pos_match, pos_total, neg_match, neg_total])
    string = f"Pos: {pos_match}/{pos_total}: {pos_ratio:.2f}, \t Neg: {neg_match}/{neg_total}: {neg_ratio:.2f}\n"
    return nums, string


def cal_f1(nums):
    """
    Calculate precision, recall, F1_score, F_score from given numbers.

    :param nums: the matching information: [pos_match, pos_total, neg_nonmatch, neg_total]
    :return precision, recall, F1_score, F_score
    """
    TP = nums[0]            # positive match
    TN = nums[2]            # negative mismatch
    FP = nums[3] - nums[2]  # negative match
    FN = nums[1] - nums[0]  # positive mismatch

    recall = TP / (TP + FN)
    precision = TP / (TP + FP)
    F1_score = 2 * precision * recall / ( precision + recall )
    F_score = (TP - FN + TN - FP) / (nums[1] + nums[3])

    return precision, recall, F1_score, F_score


def main():
    folder_paths = ["tests/dataset_20", "tests/dataset_40", "tests/dataset_80", "tests/dataset_160", "tests/dataset_200"]

    for i in range(len(folder_paths)):
        # output to baseline/ folder
        out_path = folder_paths[i].split("/")
        out_path.insert(1, "baseline")
        out_path = "/".join(out_path) + ".txt"

        files = os.listdir(folder_paths[i])
        files = natsorted(files)                # process files in sorted order

        total_nums = np.zeros(4)

        with open(out_path, "w") as outfile:
            for file_name in files:
                nums, string = process_file(os.path.join(folder_paths[i], file_name))
                total_nums += nums
                outfile.write(file_name + ":   " + string)

            pos_ratio = total_nums[0] / total_nums[1]
            neg_ratio = total_nums[2] / total_nums[3]
            outfile.write(f"\nTotal Pos: {total_nums[0]}/{total_nums[1]}: {pos_ratio:.2f}, \
                Total Neg: {total_nums[2]}/{total_nums[3]}: {neg_ratio:.2f}\n")
            precision, recall, F1_score, F_score = cal_f1(total_nums)
            string = f"{folder_paths[i]}: precision: {precision:.4f}, recall: {recall:.4f}, \
                      F1 score: {F1_score:.4f}, F score: {F_score:.4f}"
            outfile.write(string)
            print(string)


if __name__ == "__main__":
    main()
