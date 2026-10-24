import numpy as np

from app.utils.input_assessment import assess_input


# ----------------------------------------
# HELPER
# ----------------------------------------

def create_classification_result(
    probabilities
):

    class_names = [
        "Melanoma",
        "Melanocytic Nevus",
        "Basal Cell Carcinoma",
        "Actinic Keratosis",
        "Benign Keratosis",
        "Dermatofibroma",
        "Vascular Lesion"
    ]

    probability_dict = {}

    for index, class_name in enumerate(
        class_names
    ):
        probability_dict[class_name] = (
            probabilities[index]
        )

    predicted_index = int(
        np.argmax(probabilities)
    )

    return {
        "predicted_class": class_names[
            predicted_index
        ],
        "confidence": float(
            probabilities[predicted_index]
        ),
        "probabilities": probability_dict
    }


# ----------------------------------------
# GENUINE ISIC TEST DATA
# ----------------------------------------
#
# These are representative values from
# the validation experiments we already ran.
#
# We are testing the current assessment
# logic, not retraining the model.
# ----------------------------------------

genuine_isic_cases = [

    {
        "name": "ISIC_01",
        "ood_distance": 17.0,
        "lesion_area": 5.0,
        "fill_ratio": 0.29,
        "border_touch": 0,
        "confidence": 0.85,
        "second": 0.08
    },

    {
        "name": "ISIC_02",
        "ood_distance": 20.0,
        "lesion_area": 4.5,
        "fill_ratio": 0.32,
        "border_touch": 0,
        "confidence": 0.78,
        "second": 0.10
    },

    {
        "name": "ISIC_03",
        "ood_distance": 22.0,
        "lesion_area": 6.0,
        "fill_ratio": 0.30,
        "border_touch": 0,
        "confidence": 0.72,
        "second": 0.14
    },

    {
        "name": "ISIC_04",
        "ood_distance": 15.0,
        "lesion_area": 3.8,
        "fill_ratio": 0.27,
        "border_touch": 0,
        "confidence": 0.91,
        "second": 0.04
    },

    {
        "name": "ISIC_05",
        "ood_distance": 25.0,
        "lesion_area": 7.0,
        "fill_ratio": 0.35,
        "border_touch": 0,
        "confidence": 0.67,
        "second": 0.18
    },

    {
        "name": "ISIC_06_LOW_CONFIDENCE",
        "ood_distance": 24.0,
        "lesion_area": 5.0,
        "fill_ratio": 0.29,
        "border_touch": 0,
        "confidence": 0.4579,
        "second": 0.2071
    }
]


# ----------------------------------------
# WRONG IMAGE
# ----------------------------------------

wrong_image = {
    "name": "WRONG_SCREENSHOT",
    "ood_distance": 28.8481,
    "lesion_area": 1.2222,
    "fill_ratio": 0.2853,
    "border_touch": 0,
    "confidence": 0.51088,
    "second": 0.17698
}


# ----------------------------------------
# BIKE IMAGE
# ----------------------------------------

bike_image = {
    "name": "BIKE_IMAGE",
    "ood_distance": 35.2405,
    "lesion_area": 5.0,
    "fill_ratio": 0.30,
    "border_touch": 0,
    "confidence": 0.8583,
    "second": 0.0594
}


# ----------------------------------------
# TEST FUNCTION
# ----------------------------------------

def run_case(case):

    confidence = case["confidence"]
    second = case["second"]

    remaining_probability = (
        1.0
        - confidence
        - second
    )

    remaining_probability = max(
        remaining_probability,
        0.0
    )

    third_probability = (
        remaining_probability / 5
    )

    probabilities = np.array([
        confidence,
        second,
        third_probability,
        third_probability,
        third_probability,
        third_probability,
        third_probability
    ])

    probabilities = (
        probabilities
        / probabilities.sum()
    )

    ood_result = {
        "distance": case["ood_distance"],
        "safe": case["ood_distance"] <= 32.0
    }

    segmentation_result = {
        "lesion_area_percentage":
            case["lesion_area"],
        "fill_ratio":
            case["fill_ratio"],
        "border_touch_count":
            case["border_touch"]
    }

    classification_result = (
        create_classification_result(
            probabilities
        )
    )

    result = assess_input(
        ood_result,
        segmentation_result,
        classification_result
    )

    return result


# ----------------------------------------
# RUN TESTS
# ----------------------------------------

print("\n" + "=" * 40)
print("INPUT ASSESSMENT BATCH TEST")
print("=" * 40)


accepted = 0
needs_review = 0
rejected = 0


# Genuine ISIC

print("\n" + "=" * 40)
print("GENUINE ISIC CASES")
print("=" * 40)

for case in genuine_isic_cases:

    result = run_case(case)

    print(
        f"\n{case['name']}"
    )

    print(
        "Status:",
        result["status"]
    )

    print(
        "Needs review:",
        result["needs_review"]
    )

    print(
        "Reasons:",
        result["reasons"]
    )

    if result["status"] == "accepted":
        accepted += 1

    elif result["status"] == "needs_review":
        needs_review += 1

    elif result["status"] == "rejected":
        rejected += 1


# Wrong image

print("\n" + "=" * 40)
print("WRONG IMAGE")
print("=" * 40)

result = run_case(
    wrong_image
)

print(
    "Status:",
    result["status"]
)

print(
    "Needs review:",
    result["needs_review"]
)

print(
    "Reasons:",
    result["reasons"]
)

if result["status"] == "accepted":
    accepted += 1

elif result["status"] == "needs_review":
    needs_review += 1

elif result["status"] == "rejected":
    rejected += 1


# Bike

print("\n" + "=" * 40)
print("BIKE IMAGE")
print("=" * 40)

result = run_case(
    bike_image
)

print(
    "Status:",
    result["status"]
)

print(
    "Needs review:",
    result["needs_review"]
)

print(
    "Reasons:",
    result["reasons"]
)

if result["status"] == "accepted":
    accepted += 1

elif result["status"] == "needs_review":
    needs_review += 1

elif result["status"] == "rejected":
    rejected += 1


# ----------------------------------------
# SUMMARY
# ----------------------------------------

print("\n" + "=" * 40)
print("FINAL SUMMARY")
print("=" * 40)

print(
    "Accepted:",
    accepted
)

print(
    "Needs review:",
    needs_review
)

print(
    "Rejected:",
    rejected
)

print("\n" + "=" * 40)
print("BATCH TEST COMPLETE")
print("=" * 40)