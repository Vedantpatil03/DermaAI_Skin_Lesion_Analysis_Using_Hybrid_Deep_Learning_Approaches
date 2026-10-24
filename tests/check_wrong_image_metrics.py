import numpy as np


probabilities = {
    "Melanoma": 0.023617446422576904,
    "Melanocytic Nevus": 0.5108802914619446,
    "Basal Cell Carcinoma": 0.06574033200740814,
    "Actinic Keratosis": 0.1769767701625824,
    "Benign Keratosis": 0.028061889111995697,
    "Dermatofibroma": 0.09805040806531906,
    "Vascular Lesion": 0.09667297452688217
}


probabilities = np.array(
    list(probabilities.values())
)


# ----------------------------------------
# CONFIDENCE
# ----------------------------------------

sorted_probabilities = np.sort(
    probabilities
)[::-1]

confidence = float(
    sorted_probabilities[0]
)

second_probability = float(
    sorted_probabilities[1]
)

confidence_gap = (
    confidence - second_probability
)


# ----------------------------------------
# ENTROPY
# ----------------------------------------

entropy = float(
    -np.sum(
        probabilities
        * np.log(
            probabilities + 1e-10
        )
    )
)


# ----------------------------------------
# PRINT RESULTS
# ----------------------------------------

print("\n" + "=" * 40)
print("WRONG IMAGE METRICS")
print("=" * 40)

print(
    "Confidence:",
    confidence
)

print(
    "Second probability:",
    second_probability
)

print(
    "Confidence gap:",
    confidence_gap
)

print(
    "Entropy:",
    entropy
)

print("\n" + "=" * 40)
print("TEST COMPLETE")
print("=" * 40)