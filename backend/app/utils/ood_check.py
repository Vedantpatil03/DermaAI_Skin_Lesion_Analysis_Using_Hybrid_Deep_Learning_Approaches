import os
import numpy as np

from app.services.classification_service import ClassificationService


# ========================================
# OOD REFERENCE PATH
# ========================================

REFERENCE_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../../../models/ood_reference.npz"
    )
)


# ========================================
# OOD CHECKER
# ========================================

class OODChecker:

    def __init__(self):

        print("\n" + "=" * 40)
        print("OOD INPUT CHECKER")
        print("=" * 40)

        # ========================================
        # CHECK REFERENCE FILE
        # ========================================

        if not os.path.exists(
            REFERENCE_PATH
        ):

            raise FileNotFoundError(
                "OOD reference file not found:\n"
                f"{REFERENCE_PATH}"
            )

        # ========================================
        # LOAD REFERENCE
        # ========================================

        reference = np.load(
            REFERENCE_PATH
        )

        self.reference_features = (
            reference["features"]
        )

        # ========================================
        # LOAD CLASSIFICATION SERVICE
        # ========================================

        self.classification_service = (
            ClassificationService()
        )

        print(
            "Reference loaded."
        )

        print(
            "Reference samples:",
            self.reference_features.shape[0]
        )

        print(
            "Feature dimension:",
            self.reference_features.shape[1]
        )

        print("=" * 40)

    # ========================================
    # CHECK IMAGE
    # ========================================

    def check(self, image):

        # ========================================
        # EXTRACT HYBRID FEATURES
        # ========================================

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

        # ========================================
        # CALCULATE DISTANCES
        # ========================================

        distances = np.linalg.norm(
            self.reference_features
            - feature_vector,
            axis=1
        )

        # ========================================
        # FIND NEAREST ISIC IMAGE
        # ========================================

        nearest_distance = np.min(
            distances
        )

        nearest_index = np.argmin(
            distances
        )

        # ========================================
        # OOD THRESHOLD
        # ========================================

        threshold = 32.0

        is_in_distribution = (
            nearest_distance <= threshold
        )

        # ========================================
        # REASON
        # ========================================

        if is_in_distribution:

            reason = (
                "Image features are sufficiently "
                "close to the ISIC reference "
                "feature distribution."
            )

        else:

            reason = (
                "Image features are too far from "
                "the ISIC reference feature "
                "distribution."
            )

        # ========================================
        # RESULT
        # ========================================

        return {
            "safe": bool(
                is_in_distribution
            ),

            "distance": float(
                nearest_distance
            ),

            "threshold": float(
                threshold
            ),

            "nearest_reference_index": int(
                nearest_index
            ),

            "reason": reason
        }


# ========================================
# TEST INITIALIZATION
# ========================================

if __name__ == "__main__":

    checker = OODChecker()

    print("\n" + "=" * 40)
    print("OOD CHECKER READY")
    print("=" * 40)

    print(
        "Reference:",
        REFERENCE_PATH
    )

    print(
        "Reference samples:",
        checker.reference_features.shape[0]
    )

    print(
        "Feature dimension:",
        checker.reference_features.shape[1]
    )

    print(
        "Threshold:",
        32.0
    )