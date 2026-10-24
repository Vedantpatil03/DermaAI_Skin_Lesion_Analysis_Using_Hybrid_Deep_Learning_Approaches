import os
import torch

from app.models.hybrid_model import HybridCNNViT
from app.utils.preprocessing import preprocess_image


class ClassificationService:

    def __init__(self):

        # ========================================
        # Device
        # ========================================

        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )

        print("\n" + "=" * 40)
        print("HYBRID CNN + ViT MODEL")
        print("Device:", self.device)
        print("=" * 40)

        # ========================================
        # Model
        # ========================================

        self.model = HybridCNNViT(
            num_classes=7
        )

        # ========================================
        # Model Path
        # ========================================

        model_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "../../../models/hybrid_cnn_vit.pth"
            )
        )

        print("Model path:")
        print(model_path)

        # ========================================
        # Check File
        # ========================================

        if not os.path.exists(model_path):

            raise FileNotFoundError(
                f"Model file not found: {model_path}"
            )

        # ========================================
        # Load Checkpoint
        # ========================================

        checkpoint = torch.load(
            model_path,
            map_location=self.device
        )

        print("\nCheckpoint loaded.")

        # ========================================
        # Extract Model State
        # ========================================

        if "model_state_dict" not in checkpoint:

            raise KeyError(
                "model_state_dict not found in checkpoint."
            )

        state_dict = checkpoint[
            "model_state_dict"
        ]

        # ========================================
        # Load Trained Weights
        # ========================================

        self.model.load_state_dict(
            state_dict,
            strict=True
        )

        # ========================================
        # Prepare Model
        # ========================================

        self.model = self.model.to(
            self.device
        )

        self.model.eval()

        # ========================================
        # Class Names
        # ========================================

        self.class_names = checkpoint.get(
            "class_names",
            [
                "Melanoma",
                "Melanocytic Nevus",
                "Basal Cell Carcinoma",
                "Actinic Keratosis",
                "Benign Keratosis",
                "Dermatofibroma",
                "Vascular Lesion"
            ]
        )

        print("\n" + "=" * 40)
        print("MODEL LOADED SUCCESSFULLY")
        print("=" * 40)

        print("Classes:", self.class_names)

    # ========================================
    # PREDICTION
    # ========================================

    def predict(self, image):

        # ========================================
        # Preprocess Image
        # ========================================

        image_tensor = preprocess_image(
            image
        )

        image_tensor = image_tensor.to(
            self.device
        )

        # ========================================
        # Model Prediction
        # ========================================

        with torch.no_grad():

            outputs = self.model(
                image_tensor
            )

            probabilities = torch.softmax(
                outputs,
                dim=1
            )

        # ========================================
        # Get Prediction
        # ========================================

        predicted_index = torch.argmax(
            probabilities,
            dim=1
        ).item()

        confidence = probabilities[
            0, predicted_index
        ].item()

        predicted_class = self.class_names[
            predicted_index
        ]

        # ========================================
        # All Class Probabilities
        # ========================================

        all_probabilities = {}

        for index, class_name in enumerate(
            self.class_names
        ):

            all_probabilities[class_name] = (
                probabilities[0, index].item()
            )

        # ========================================
        # Result
        # ========================================

        return {
            "predicted_class": predicted_class,
            "confidence": confidence,
            "probabilities": all_probabilities
        }

    # ========================================
    # EXTRACT HYBRID FEATURES
    # ========================================

    def extract_features(self, image):

        # ========================================
        # Preprocess Image
        # ========================================

        image_tensor = preprocess_image(
            image
        )

        image_tensor = image_tensor.to(
            self.device
        )

        # ========================================
        # Extract Features
        # ========================================

        with torch.no_grad():

            # ------------------------------------
            # ResNet18 Features
            # ------------------------------------

            cnn_features = self.model.cnn(
                image_tensor
            )

            # ------------------------------------
            # ViT Features
            # ------------------------------------

            vit_features = self.model.vit(
                image_tensor
            )

            # ------------------------------------
            # Combine Features
            # ------------------------------------

            combined_features = torch.cat(
                [
                    cnn_features,
                    vit_features
                ],
                dim=1
            )

        return combined_features


# ============================================
# TEST MODEL
# ============================================

if __name__ == "__main__":

    ClassificationService()