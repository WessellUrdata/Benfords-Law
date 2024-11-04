import pickle as pkl
import numpy as np
from icecream import ic
import matplotlib.pyplot as plt
import scipy.stats as stats

filename = "output.pkl"
with open(filename, "rb") as f:
    t = pkl.load(f)

features = t["data"]
labels = t["label"]
N = t["N"]

# Benford's Law for the first digit
digits = np.arange(1, 10)
benford = np.log10(1 + 1 / digits)

# Get first digit of each value
extract_first_digit = lambda x: int(str(x)[0])
for arrays in features:
    for i in range(len(arrays)):
        arrays[i] = extract_first_digit(arrays[i])

# Count the occurrences of each first digit
first_digits_counts = [
    np.histogram(array, bins=np.arange(1, 11))[0] for array in features
]

# # plot the distribution of first digits
# for first_digits_count in first_digits_counts:
#     plt.plot(
#         digits, first_digits_count / N, color="blue", label="First digit distribution"
#     )
#     plt.plot(
#         digits,
#         benford,
#         color="red",
#         label="Benford's Law distribution",
#     )
#     plt.xlabel("First digit")
#     plt.ylabel("Frequency")
#     plt.legend()
#     plt.show()


goodness_of_fit = [
    stats.pearsonr(first_digits_count, benford)
    for first_digits_count in first_digits_counts
]

ALPHA = 0.01

# calculate True Positive, False Positive, True Negative, False Negative
results = [
    (1 - ALPHA >= p_value, labels[i]) for i, (p_value, _) in enumerate(goodness_of_fit)
]

# fake is 0, real is 1
TP = sum(is_legitimate and (label == 1) for is_legitimate, label in results)
FP = sum(is_legitimate and (label == 0) for is_legitimate, label in results)
TN = sum(not is_legitimate and (label == 0) for is_legitimate, label in results)
FN = sum(not is_legitimate and (label == 1) for is_legitimate, label in results)

ic(TP, FP, TN, FN)

precision = TP / (TP + FP)
recall = TP / (TP + FN)
f1 = 2 * (precision * recall) / (precision + recall)
accuracy = (TP + TN) / (TP + TN + FP + FN)

ic(precision, recall, f1, accuracy)


# # Check if the goodness of fit is within 0.05 significance level
# for i, (p_value, _) in enumerate(goodness_of_fit):
#     if 1 - 0.05 > p_value:
#         if labels[i] == 1:
#             print("Guess was correct")
#         else:
#             print("Guess was incorrect")
#     else:
#         if labels[i] == 0:
#             print("Guess was correct")
#         else:
#             print("Guess was incorrect")
