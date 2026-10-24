import os
import numpy as np
from PIL import Image

from app.services.classification_service import ClassificationService


# ========================================
# ISIC DATASET PATH
# ========================================

ISIC_FOLDER = (
    r"C:\D Drive Folder\Major Project"
    r"\ISIC2018_Task3_Training_Input"
)


# ========================================
# OOD REFERENCE SAVE PATH
# ========================================

REFERENCE_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../../../models/ood_reference.npz"
    )
)


# ========================================
# OOD REFERENCE BUILDER
# ========================================

class OODReferenceBuilder:

    def __init__(self):

        print("\n" + "=" * 40)
        print("OOD REFERENCE FEATURE BUILDER")
        print("=" * 40)

        if not os.path.exists(ISIC_FOLDER):

            raise FileNotFoundError(
                f"ISIC folder not found:\n{ISIC_FOLDER}"
            )

        self.classification_service = (
            ClassificationService()
        )

    # ========================================
    # COLLECT ISIC IMAGES
    # ========================================

    def collect_images(self, max_images=100):

        image_files = []

        for filename in os.listdir(ISIC_FOLDER):

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

        image_files = image_files[:max_images]

        print("\n" + "=" * 40)
        print("ISIC IMAGES FOUND")
        print("=" * 40)

        print(
            "Images selected:",
            len(image_files)
        )

        return image_files

    # ========================================
    # BUILD REFERENCE
    # ========================================

    def build_reference(self, max_images=100):

        image_files = self.collect_images(
            max_images=max_images
        )

        if len(image_files) == 0:

            raise ValueError(
                "No ISIC images were found."
            )

        features = []

        print("\n" + "=" * 40)
        print("EXTRACTING HYBRID FEATURES")
        print("=" * 40)

        for index, image_path in enumerate(
            image_files
        ):

            try:

                image = Image.open(
                    image_path
                ).convert("RGB")

                feature_tensor = (
                    self.classification_service
                    .extract_features(image)
                )

                feature_vector = (
                    feature_tensor
                    .squeeze(0)
                    .cpu()
                    .numpy()
                )

                features.append(
                    feature_vector
                )

                print(
                    f"[{index + 1}/{len(image_files)}] "
                    f"{os.path.basename(image_path)}"
                )

            except Exception as error:

                print(
                    "Skipped:",
                    os.path.basename(image_path)
                )

                print(
                    "Reason:",
                    error
                )

        if len(features) == 0:

            raise RuntimeError(
                "No features could be extracted."
            )

        # ========================================
        # CREATE FEATURE MATRIX
        # ========================================

        features = np.stack(
            features
        )

        # ========================================
        # CALCULATE REFERENCE STATISTICS
        # ========================================

        mean_vector = np.mean(
            features,
            axis=0
        )

        std_vector = np.std(
            features,
            axis=0
        )

        # Prevent division by zero later
        std_vector = np.maximum(
            std_vector,
            1e-6
        )

        # ========================================
        # SAVE REFERENCE
        # ========================================

        np.savez(
            REFERENCE_PATH,
            features=features,
            mean=mean_vector,
            std=std_vector
        )

        # ========================================
        # DISPLAY RESULTS
        # ========================================

        print("\n" + "=" * 40)
        print("REFERENCE FEATURES CREATED")
        print("=" * 40)

        print(
            "Feature matrix:",
            features.shape
        )

        print(
            "Feature dimension:",
            features.shape[1]
        )

        print(
            "Reference samples:",
            features.shape[0]
        )

        print("\nReference saved to:")

        print(
            REFERENCE_PATH
        )

        print("\n" + "=" * 40)
        print("OOD REFERENCE SAVED SUCCESSFULLY")
        print("=" * 40)

        return {
            "features": features,
            "mean": mean_vector,
            "std": std_vector
        }


# ========================================
# TEST
# ========================================

if __name__ == "__main__":

    builder = OODReferenceBuilder()

    reference = builder.build_reference(
        max_images=100
    )

    print("\n" + "=" * 40)
    print("OOD REFERENCE TEST COMPLETE")
    print("=" * 40)

    print(
        "Reference shape:",
        reference["features"].shape
    )

    print(
        "Mean shape:",
        reference["mean"].shape
    )

    print(
        "Std shape:",
        reference["std"].shape
    )