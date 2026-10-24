import sys
import os
from PIL import Image


# ========================================
# PROJECT PATH
# ========================================

project_root = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

backend_path = os.path.join(
    project_root,
    "backend"
)

sys.path.insert(0, backend_path)


# ========================================
# IMPORT CLASSIFICATION SERVICE
# ========================================

from app.services.classification_service import (
    ClassificationService
)


# ========================================
# IMAGE PATH
# ========================================

image_path = r"C:\Users\vedan\Downloads\Dermatofibroma.jpg"


if not os.path.exists(image_path):
    raise FileNotFoundError(
        f"Image not found: {image_path}"
    )


# ========================================
# LOAD IMAGE
# ========================================

image = Image.open(image_path).convert("RGB")


# ========================================
# LOAD MODEL
# ========================================

service = ClassificationService()


# ========================================
# EXTRACT FEATURES
# ========================================

features = service.extract_features(image)


# ========================================
# DISPLAY RESULT
# ========================================

print("\n" + "=" * 40)
print("HYBRID FEATURE EXTRACTION")
print("=" * 40)

print("Feature Shape:", features.shape)
print("Feature Type:", features.dtype)

print(
    "Feature Dimension:",
    features.shape[1]
)

print("=" * 40)