import cv2
import numpy as np
image = cv2.imread("/media/HDD2/VITON/StableVITON_git/StableVITON/test/test/agnostic-v3.2/t55.png")
arr = image.reshape(-1, 3)
unique_rows, counts = np.unique(arr, axis=0, return_counts=True)
most_frequent_index = np.argmax(counts)

most_frequent_row = unique_rows[most_frequent_index]

print("Most frequent row:", most_frequent_row)
print("Frequency:", counts[most_frequent_index])
