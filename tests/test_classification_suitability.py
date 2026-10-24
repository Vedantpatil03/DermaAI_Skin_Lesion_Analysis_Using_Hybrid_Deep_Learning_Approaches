import os
import numpy as np
from PIL import Image

from app.services.classification_service import ClassificationService


ISIC_FOLDER = (
    r"C:\D Drive Folder\Major Project"
    r"\ISIC2018_Task3_Training_Input"
)

BIKE_IMAGE = (
    r"C:\Users\vedan\Downloads\bike.jpg"
)

WRONG_IMAGE = (
    r"C:\Users\vedan\Pictures\Screenshots"
    r"\Screenshot 2026-04-29 114902.png"
)


def analyze_image(
    classification_service,
    image_path
):

    image = Image.open(
        image_path
    ).convert("RGB")

    result = classification_service.predict(
        image
    )

    probabilities = np.array(
        list(
            result["probabilities"].values()
        )
    )

    sorted_probabilities = np.sort(
        probabilities
    )[::-1]

    confidence = sorted_probabilities[0]

    second_probability = (
        sorted_probabilities[1]
    )

    confidence_gap = (
        confidence - second_probability
    )

    entropy = -np.sum(
        probabilities
        * np.log(probabilities + 1e-10)
    )

    return {
        "confidence": float(confidence),
        "gap": float(confidence_gap),
        "entropy": float(entropy),
        "predicted_class": result[
            "predicted_class"
        ]
    }


def print_result(
    name,
    result
):

    print(
        f"{name:<20}"
        f" Confidence: {result['confidence']:.4f}"
        f" | Gap: {result['gap']:.4f}"
        f" | Entropy: {result['entropy']:.4f}"
        f" | Class: {result['predicted_class']}"
    )


def main():

    print("\n" + "=" * 40)
    print("CLASSIFICATION SUITABILITY VALIDATION")
    print("=" * 40)

    service = ClassificationService()

    # ----------------------------------------
    # FIND ISIC IMAGES
    # ----------------------------------------

    image_files = []

    for filename in os.listdir(
        ISIC_FOLDER
    ):

        if filename.lower().endswith(
            (".jpg", ".jpeg", ".png", ".webp")
        ):

            image_files.append(
                os.path.join(
                    ISIC_FOLDER,
                    filename
                )
            )

    image_files.sort()

    # First 100 images were used to build
    # the OOD reference.
    #
    # Use the next 20 as unseen images.

    unseen_images = image_files[100:120]

    print("\n" + "=" * 40)
    print("20 UNSEEN ISIC IMAGES")
    print("=" * 40)

    results = []

    for index, image_path in enumerate(
        unseen_images,
        start=1
    ):

        result = analyze_image(
            service,
            image_path
        )

        results.append(result)

        print_result(
            f"ISIC {index:02d}",
            result
        )

    # ----------------------------------------
    # CALCULATE ISIC RANGES
    # ----------------------------------------

    confidence_values = np.array([
        result["confidence"]
        for result in results
    ])

    gap_values = np.array([
        result["gap"]
        for result in results
    ])

    entropy_values = np.array([
        result["entropy"]
        for result in results
    ])

    print("\n" + "=" * 40)
    print("UNSEEN ISIC SUMMARY")
    print("=" * 40)

    print(
        "Confidence range:",
        f"{confidence_values.min():.4f}",
        "to",
        f"{confidence_values.max():.4f}"
    )

    print(
        "Confidence mean:",
        f"{confidence_values.mean():.4f}"
    )

    print(
        "Confidence gap range:",
        f"{gap_values.min():.4f}",
        "to",
        f"{gap_values.max():.4f}"
    )

    print(
        "Confidence gap mean:",
        f"{gap_values.mean():.4f}"
    )

    print(
        "Entropy range:",
        f"{entropy_values.min():.4f}",
        "to",
        f"{entropy_values.max():.4f}"
    )

    print(
        "Entropy mean:",
        f"{entropy_values.mean():.4f}"
    )

    # ----------------------------------------
    # BIKE
    # ----------------------------------------

    print("\n" + "=" * 40)
    print("BIKE IMAGE")
    print("=" * 40)

    if os.path.exists(BIKE_IMAGE):

        bike_result = analyze_image(
            service,
            BIKE_IMAGE
        )

        print_result(
            "Bike",
            bike_result
        )

    else:

        print(
            "Bike image not found:"
        )

        print(BIKE_IMAGE)

    # ----------------------------------------
    # WRONG IMAGE
    # ----------------------------------------

    print("\n" + "=" * 40)
    print("WRONG / SCREENSHOT IMAGE")
    print("=" * 40)

    if os.path.exists(WRONG_IMAGE):

        wrong_result = analyze_image(
            service,
            WRONG_IMAGE
        )

        print_result(
            "Wrong image",
            wrong_result
        )

    else:

        print(
            "Wrong image not found:"
        )

        print(WRONG_IMAGE)

    print("\n" + "=" * 40)
    print("VALIDATION COMPLETE")
    print("=" * 40)


if __name__ == "__main__":
    main()