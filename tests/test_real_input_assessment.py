import os
import numpy as np
from PIL import Image

from app.services.classification_service import ClassificationService
from app.services.segmentation_service import SegmentationService
from app.utils.ood_check import OODChecker
from app.utils.input_safety import check_segmentation_quality
from app.utils.input_assessment import assess_input


# ----------------------------------------
# PATHS
# ----------------------------------------

ISIC_FOLDER = (
    r"C:\D Drive Folder\Major Project"
    r"\ISIC2018_Task3_Training_Input"
)

WRONG_IMAGE = (
    r"C:\Users\vedan\Pictures\Screenshots"
    r"\Screenshot 2026-04-29 114902.png"
)

BIKE_IMAGE = (
    r"C:\Users\vedan\Downloads\bike.jpg"
)

# ----------------------------------------
# LOAD SERVICES
# ----------------------------------------

print("\n" + "=" * 40)
print("LOADING ANALYSIS SERVICES")
print("=" * 40)

classification_service = (
    ClassificationService()
)

segmentation_service = (
    SegmentationService()
)

ood_checker = (
    OODChecker()
)


# ----------------------------------------
# ANALYZE ONE IMAGE
# ----------------------------------------

def analyze_image(image_path):

    image = Image.open(
        image_path
    ).convert("RGB")

    # ------------------------------------
    # OOD
    # ------------------------------------

    ood_result = (
        ood_checker.check(image)
    )

    # ------------------------------------
    # SEGMENTATION
    # ------------------------------------

    segmentation_result = (
        segmentation_service.segment(
            image
        )
    )

    # ------------------------------------
    # SEGMENTATION SAFETY
    # ------------------------------------

    safety_result = (
        check_segmentation_quality(
            segmentation_result
        )
    )

    # ------------------------------------
    # CLASSIFICATION
    # ------------------------------------

    classification_result = (
        classification_service.predict(
            image
        )
    )

    # ------------------------------------
    # INPUT ASSESSMENT
    # ------------------------------------

    assessment_result = assess_input(
        ood_result,
        safety_result,
        classification_result
    )

    return (
        ood_result,
        segmentation_result,
        safety_result,
        classification_result,
        assessment_result
    )


# ----------------------------------------
# PRINT RESULT
# ----------------------------------------

def print_result(
    name,
    result
):

    (
        ood_result,
        segmentation_result,
        safety_result,
        classification_result,
        assessment_result
    ) = result

    print("\n" + "=" * 40)
    print(name)
    print("=" * 40)

    print(
        "OOD distance:",
        round(
            ood_result["distance"],
            4
        )
    )

    print(
        "OOD safe:",
        ood_result["safe"]
    )

    print(
        "Lesion area:",
        round(
            safety_result[
                "lesion_area_percentage"
            ],
            4
        ),
        "%"
    )

    print(
        "Fill ratio:",
        round(
            safety_result[
                "fill_ratio"
            ],
            4
        )
    )

    print(
        "Border touches:",
        safety_result[
            "border_touch_count"
        ]
    )

    print(
        "Predicted class:",
        classification_result[
            "predicted_class"
        ]
    )

    print(
        "Confidence:",
        round(
            classification_result[
                "confidence"
            ],
            4
        )
    )

    probabilities = np.array(
        list(
            classification_result[
                "probabilities"
            ].values()
        )
    )

    sorted_probabilities = (
        np.sort(
            probabilities
        )[::-1]
    )

    confidence_gap = (
        sorted_probabilities[0]
        - sorted_probabilities[1]
    )

    entropy = float(
        -np.sum(
            probabilities
            * np.log(
                probabilities + 1e-10
            )
        )
    )

    print(
        "Confidence gap:",
        round(
            confidence_gap,
            4
        )
    )

    print(
        "Entropy:",
        round(
            entropy,
            4
        )
    )

    print(
        "Assessment:",
        assessment_result[
            "status"
        ]
    )

    print(
        "Needs review:",
        assessment_result[
            "needs_review"
        ]
    )

    print(
        "Reasons:",
        assessment_result[
            "reasons"
        ]
    )


# ----------------------------------------
# FIND ISIC IMAGES
# ----------------------------------------

image_files = []

for filename in os.listdir(
    ISIC_FOLDER
):

    if filename.lower().endswith(
        (
            ".jpg",
            ".jpeg",
            ".png",
            ".webp"
        )
    ):

        image_files.append(
            os.path.join(
                ISIC_FOLDER,
                filename
            )
        )


image_files.sort()


# ----------------------------------------
# USE 20 IMAGES
# ----------------------------------------

image_files = image_files[:20]


print("\n" + "=" * 40)
print("REAL ISIC VALIDATION")
print("=" * 40)

print(
    "Images:",
    len(image_files)
)


accepted = 0
needs_review = 0
rejected = 0


# ----------------------------------------
# RUN ISIC TEST
# ----------------------------------------

for index, image_path in enumerate(
    image_files
):

    print(
        f"\nProcessing "
        f"{index + 1}/{len(image_files)}"
    )

    try:

        result = analyze_image(
            image_path
        )

        print_result(
            os.path.basename(
                image_path
            ),
            result
        )

        status = result[4]["status"]

        if status == "accepted":

            accepted += 1

        elif status == "needs_review":

            needs_review += 1

        elif status == "rejected":

            rejected += 1

    except Exception as error:

        print(
            "ERROR:",
            error
        )


# ----------------------------------------
# WRONG IMAGE
# ----------------------------------------

if os.path.exists(
    WRONG_IMAGE
):

    result = analyze_image(
        WRONG_IMAGE
    )

    print_result(
        "WRONG SCREENSHOT",
        result
    )


# ----------------------------------------
# BIKE IMAGE
# ----------------------------------------

if os.path.exists(
    BIKE_IMAGE
):

    result = analyze_image(
        BIKE_IMAGE
    )

    print_result(
        "BIKE IMAGE",
        result
    )


# ----------------------------------------
# SUMMARY
# ----------------------------------------

print("\n" + "=" * 40)
print("REAL VALIDATION SUMMARY")
print("=" * 40)

print(
    "Genuine ISIC accepted:",
    accepted
)

print(
    "Genuine ISIC needs review:",
    needs_review
)

print(
    "Genuine ISIC rejected:",
    rejected
)

print("\n" + "=" * 40)
print("REAL VALIDATION COMPLETE")
print("=" * 40)