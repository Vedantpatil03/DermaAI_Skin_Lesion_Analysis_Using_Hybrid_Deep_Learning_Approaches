import numpy as np


def assess_input(
    ood_result,
    segmentation_result,
    classification_result
):

    reasons = []

    # ----------------------------------------
    # OOD SIGNAL
    # ----------------------------------------

    ood_distance = ood_result["distance"]

    OOD_REVIEW_THRESHOLD = 30.0
    OOD_REJECT_THRESHOLD = 32.0

    # ----------------------------------------
    # SEGMENTATION SIGNAL
    # ----------------------------------------

    lesion_area = (
        segmentation_result[
            "lesion_area_percentage"
        ]
    )

    fill_ratio = (
        segmentation_result[
            "fill_ratio"
        ]
    )

    border_touch_count = (
        segmentation_result[
            "border_touch_count"
        ]
    )

    bounding_box = (
        segmentation_result.get(
            "bounding_box",
            {}
        )
    )

    # ----------------------------------------
    # CLASSIFICATION SIGNAL
    # ----------------------------------------

    probabilities = np.array(
        list(
            classification_result[
                "probabilities"
            ].values()
        )
    )

    confidence = float(
        np.max(probabilities)
    )

    sorted_probabilities = np.sort(
        probabilities
    )[::-1]

    second_probability = float(
        sorted_probabilities[1]
    )

    confidence_gap = (
        confidence - second_probability
    )

    entropy = float(
        -np.sum(
            probabilities
            * np.log(
                probabilities + 1e-10
            )
        )
    )

    # ----------------------------------------
    # HARD OOD REJECTION
    # ----------------------------------------

    if ood_distance > OOD_REJECT_THRESHOLD:

        reasons.append(
            "Image is outside the supported "
            "ISIC feature distribution."
        )

        return {
            "status": "rejected",
            "needs_review": False,
            "reasons": reasons
        }

    # ----------------------------------------
    # CALCULATE LESION LOCATION
    # ----------------------------------------

    image_size = 256

    x_min = bounding_box.get(
        "x_min",
        0
    )

    y_min = bounding_box.get(
        "y_min",
        0
    )

    x_max = bounding_box.get(
        "x_max",
        image_size - 1
    )

    y_max = bounding_box.get(
        "y_max",
        image_size - 1
    )

    lesion_center_x = (
        (x_min + x_max) / 2
    )

    lesion_center_y = (
        (y_min + y_max) / 2
    )

    # Distance from image center
    center_distance = (
        (
            (
                lesion_center_x
                - image_size / 2
            ) ** 2
            +
            (
                lesion_center_y
                - image_size / 2
            ) ** 2
        ) ** 0.5
    )

    # ----------------------------------------
    # WRONG-INPUT COMBINATION CHECK
    # ----------------------------------------
    #
    # We do NOT reject based on classification
    # uncertainty alone.
    #
    # Several independent signals must agree:
    #
    # 1. OOD is close to the boundary
    # 2. detected lesion is relatively small
    # 3. segmentation is very compact
    # 4. lesion is far from image center
    # 5. classifier is highly uncertain
    #
    # This is an engineering safeguard for
    # unsuitable/non-lesion images.
    # ----------------------------------------

    suspicious_ood = (
        ood_distance > 27.5
    )

    suspicious_small_lesion = (
        lesion_area < 10.0
    )

    suspicious_compact_region = (
        fill_ratio > 0.75
    )

    suspicious_location = (
        center_distance > 105.0
    )

    suspicious_classification = (
        confidence < 0.40
        and confidence_gap < 0.15
        and entropy > 1.50
    )

    if (
        suspicious_ood
        and suspicious_small_lesion
        and suspicious_compact_region
        and suspicious_location
        and suspicious_classification
    ):

        reasons.append(
            "The uploaded image could not be "
            "reliably validated as a suitable "
            "skin-lesion image."
        )

        reasons.append(
            "Multiple image-quality and model "
            "signals indicate that the image "
            "is outside reliable analysis "
            "conditions."
        )

        return {
            "status": "rejected",
            "needs_review": False,
            "reasons": reasons
        }

    # ----------------------------------------
    # OOD REVIEW SIGNAL
    # ----------------------------------------

    if (
        ood_distance
        > OOD_REVIEW_THRESHOLD
    ):

        reasons.append(
            "Image is close to the boundary "
            "of the supported ISIC distribution."
        )

    # ----------------------------------------
    # SEGMENTATION REVIEW SIGNALS
    # ----------------------------------------

    if lesion_area < 1.0:

        reasons.append(
            "The detected region is very small."
        )

    if lesion_area > 50.0:

        reasons.append(
            "The detected region covers an "
            "unusually large portion of the image."
        )

    if fill_ratio < 0.15:

        reasons.append(
            "The detected region has a "
            "low fill ratio."
        )

    if border_touch_count > 0:

        reasons.append(
            "The detected region touches "
            "the image border."
        )

    # ----------------------------------------
    # CLASSIFICATION REVIEW SIGNALS
    # ----------------------------------------

    if confidence < 0.50:

        reasons.append(
            "Classification confidence "
            "is low."
        )

    if confidence_gap < 0.30:

        reasons.append(
            "The top two classes have "
            "similar probabilities."
        )

    if entropy > 1.50:

        reasons.append(
            "The classification probability "
            "distribution is highly uncertain."
        )

    # ----------------------------------------
    # FINAL REVIEW STATUS
    # ----------------------------------------

    if len(reasons) == 0:

        return {
            "status": "accepted",
            "needs_review": False,
            "reasons": []
        }

    return {
        "status": "needs_review",
        "needs_review": True,
        "reasons": reasons
    }