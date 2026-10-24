import os
import numpy as np
from PIL import Image

from app.services.classification_service import ClassificationService


ISIC_FOLDER = (
    r"C:\D Drive Folder\Major Project"
    r"\ISIC2018_Task3_Training_Input"
)

REFERENCE_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../models/ood_reference.npz"
    )
)

BIKE_IMAGE = (
    r"C:\Users\vedan\Downloads\bike.jpg"
)

WRONG_IMAGE = (
    r"C:\Users\vedan\Pictures\Screenshots"
    r"\Screenshot 2026-04-29 114902.png"
)


def extract_distances(
    classification_service,
    reference_features,
    image_path
):

    image = Image.open(
        image_path
    ).convert("RGB")

    feature_tensor = (
        classification_service.extract_features(
            image
        )
    )

    feature_vector = (
        feature_tensor
        .squeeze(0)
        .cpu()
        .numpy()
    )

    distances = np.linalg.norm(
        reference_features - feature_vector,
        axis=1
    )

    sorted_distances = np.sort(
        distances
    )

    top5 = sorted_distances[:5]

    return {
        "minimum": float(top5[0]),
        "average": float(np.mean(top5)),
        "median": float(np.median(top5))
    }


def main():

    print("\n" + "=" * 40)
    print("UNSEEN ISIC OOD VALIDATION")
    print("=" * 40)

    reference = np.load(
        REFERENCE_PATH
    )

    reference_features = (
        reference["features"]
    )

    print(
        "Reference samples:",
        reference_features.shape[0]
    )

    classification_service = (
        ClassificationService()
    )

    # ----------------------------------------
    # COLLECT ISIC IMAGES
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

    # The reference was created from the
    # first 100 sorted images.
    unseen_images = image_files[100:120]

    print("\n" + "=" * 40)
    print("UNSEEN ISIC IMAGES")
    print("=" * 40)

    print(
        "Images selected:",
        len(unseen_images)
    )

    unseen_results = []

    for index, image_path in enumerate(
        unseen_images,
        start=1
    ):

        result = extract_distances(
            classification_service,
            reference_features,
            image_path
        )

        unseen_results.append(result)

        print(
            f"[{index}/{len(unseen_images)}] "
            f"{os.path.basename(image_path)}"
        )

        print(
            "  Minimum:",
            f"{result['minimum']:.4f}"
        )

        print(
            "  Top-5 average:",
            f"{result['average']:.4f}"
        )

        print(
            "  Top-5 median:",
            f"{result['median']:.4f}"
        )

    # ----------------------------------------
    # UNSEEN ISIC SUMMARY
    # ----------------------------------------

    if unseen_results:

        minimum_values = np.array([
            result["minimum"]
            for result in unseen_results
        ])

        average_values = np.array([
            result["average"]
            for result in unseen_results
        ])

        median_values = np.array([
            result["median"]
            for result in unseen_results
        ])

        print("\n" + "=" * 40)
        print("UNSEEN ISIC SUMMARY")
        print("=" * 40)

        print(
            "Minimum-distance range:",
            f"{minimum_values.min():.4f}",
            "to",
            f"{minimum_values.max():.4f}"
        )

        print(
            "Top-5 average range:",
            f"{average_values.min():.4f}",
            "to",
            f"{average_values.max():.4f}"
        )

        print(
            "Top-5 median range:",
            f"{median_values.min():.4f}",
            "to",
            f"{median_values.max():.4f}"
        )

        print(
            "Top-5 average mean:",
            f"{average_values.mean():.4f}"
        )

    # ----------------------------------------
    # BIKE
    # ----------------------------------------

    print("\n" + "=" * 40)
    print("BIKE IMAGE")
    print("=" * 40)

    if os.path.exists(BIKE_IMAGE):

        result = extract_distances(
            classification_service,
            reference_features,
            BIKE_IMAGE
        )

        print(
            "Minimum:",
            f"{result['minimum']:.4f}"
        )

        print(
            "Top-5 average:",
            f"{result['average']:.4f}"
        )

        print(
            "Top-5 median:",
            f"{result['median']:.4f}"
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
    print("WRONG / BLACK IMAGE")
    print("=" * 40)

    if os.path.exists(WRONG_IMAGE):

        result = extract_distances(
            classification_service,
            reference_features,
            WRONG_IMAGE
        )

        print(
            "Minimum:",
            f"{result['minimum']:.4f}"
        )

        print(
            "Top-5 average:",
            f"{result['average']:.4f}"
        )

        print(
            "Top-5 median:",
            f"{result['median']:.4f}"
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