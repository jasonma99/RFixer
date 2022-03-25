"""
A short program to calculate metrics from the 4 number.
"""
# pos_match, pos_total, neg_match, neg_total
nums = [815, 36200, 34258, 36201]

TP = nums[0]            # positive match
TN = nums[2]            # negative mismatch
FP = nums[3] - nums[2]  # negative match
FN = nums[1] - nums[0]  # positive mismatch

recall = TP / (TP + FN)
precision = TP / (TP + FP)
F1_score = 2 * precision * recall / ( precision + recall )
F_score = (TP - FN + TN - FP) / (nums[1] + nums[3])

print(f"precision: {precision}, recall: {recall}, F1 score: {F1_score}, F score: {F_score}")