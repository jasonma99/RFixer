import os
import sys
import glob

def main():
    """
    A short program to compare the duplicate rate of examples from training datasets with testing dataset.
    """
    datasets = ["tests/dataset20", "tests/dataset40", "tests/dataset80", "tests/dataset160"]
    dataset_test = "tests/dataset200"
    test_list = os.listdir(dataset_test)
    test_list.sort()

    for dataset in datasets:
        train_list = os.listdir(dataset)
        train_list.sort()
        pos_dup_total, neg_dup_total = 0, 0
        total_examples = 0
        out_path = dataset + "_duplicate.txt"
        with open(out_path, "w") as outfile:
            for i in range(len(train_list)):
                assert train_list[i] == test_list[i]

                train_lines = [line.strip() for line in open(os.path.join(dataset, train_list[i]))]
                train_minus = train_lines.index("---")
                train_pos = set(train_lines[2:train_minus])
                train_neg = set(train_lines[train_minus+1:])

                test_lines = [line.strip() for line in open(os.path.join(dataset_test, test_list[i]))]
                test_minus = test_lines.index("---")
                test_pos = set(test_lines[2:test_minus])
                test_neg = set(test_lines[test_minus+1:])

                pos_intersection = len(train_pos.intersection(test_pos))
                neg_intersection = len(train_neg.intersection(test_neg))

                train_test = len(train_pos) + len(test_pos)
                pos_ratio = pos_intersection / train_test
                neg_ratio = neg_intersection / train_test

                pos_dup_total += pos_intersection
                neg_dup_total += neg_intersection
                total_examples += train_test

                outfile.write(f"{train_list[i]}: pos {pos_intersection}/{train_test}={pos_ratio:.3f}, \
                                neg {neg_intersection}/{train_test}={neg_ratio:.3f}\n")

            pos_ratio = pos_dup_total / total_examples
            neg_ratio = neg_dup_total / total_examples
            outfile.write(f"Average: pos {pos_dup_total}/{total_examples}={pos_ratio:.3f}, \
                            neg {neg_dup_total}/{total_examples}={pos_ratio:.3f}\n")


if __name__ == "__main__":
    main()