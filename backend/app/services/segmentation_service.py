import os
import torch
import numpy as np

from PIL import Image
from torchvision import transforms

from app.models.unet_model import UNet


class SegmentationService:

    def __init__(self):

        # ========================================
        # Device
        # ========================================

        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )

        print("\n" + "=" * 40)
        print("U-NET SEGMENTATION MODEL")
        print("Device:", self.device)
        print("=" * 40)

        # ========================================
        # Model
        # ========================================

        self.model = UNet()

        # ========================================
        # Model Path
        # ========================================

        model_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "../../../models/unet_model.pth"
            )
        )

        print("Model path:")
        print(model_path)

        # ========================================
        # Check File
        # ========================================

        if not os.path.exists(model_path):

            raise FileNotFoundError(
                f"U-Net model file not found: {model_path}"
            )

        # ========================================
        # Load Model
        # ========================================

        state_dict = torch.load(
            model_path,
            map_location=self.device
        )

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
        # Preprocessing
        # ========================================

        self.transform = transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.ToTensor()
        ])

        print("\n" + "=" * 40)
        print("U-NET MODEL LOADED SUCCESSFULLY")
        print("=" * 40)

    # ============================================
    # SEGMENT IMAGE
    # ============================================

    def segment(self, image):

        # ========================================
        # Convert to RGB
        # ========================================

        image = image.convert("RGB")

        # ========================================
        # Original Size
        # ========================================

        original_width, original_height = image.size

        # ========================================
        # Preprocess
        # ========================================

        image_tensor = self.transform(
            image
        )

        image_tensor = image_tensor.unsqueeze(
            0
        )

        image_tensor = image_tensor.to(
            self.device
        )

        # ========================================
        # Prediction
        # ========================================

        with torch.no_grad():

            prediction = self.model(
                image_tensor
            )

        # ========================================
        # Remove Batch / Channel Dimensions
        # ========================================

        mask_probability = prediction[
            0, 0
        ].cpu().numpy()

        # ========================================
        # Convert Probability to Binary Mask
        # ========================================

        binary_mask = (
            mask_probability >= 0.5
        ).astype(np.uint8)

        # ========================================
        # Calculate Lesion Area
        # ========================================

        lesion_pixels = np.sum(
            binary_mask
        )

        total_pixels = binary_mask.size

        lesion_area_percentage = (
            lesion_pixels /
            total_pixels
        ) * 100

        # ========================================
        # Return Result
        # ========================================

        return {
            "mask": binary_mask,
            "mask_probability": mask_probability,
            "lesion_area_percentage": (
                float(lesion_area_percentage)
            ),
            "original_size": (
                original_width,
                original_height
            )
        }


# ============================================
# TEST MODEL LOADING
# ============================================

if __name__ == "__main__":

    SegmentationService()