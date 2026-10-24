import sys
import os

from PIL import Image


# ========================================
# ADD BACKEND TO PYTHON PATH
# ========================================

project_root = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

backend_path = os.path.join(
    project_root,
    "backend"
)

sys.path.insert(
    0,
    backend_path
)


# ========================================
# IMPORT SEGMENTATION SERVICE
# ========================================

from app.services.segmentation_service import (
    SegmentationService
)


# ========================================
# IMAGE PATH
# ========================================

image_path = r"C:\Users\vedan\Downloads\Dermatofibroma.jpg"


# ========================================
# CHECK IMAGE
# ========================================

if not os.path.exists(image_path):

    raise FileNotFoundError(
        f"Image not found: {image_path}"
    )


# ========================================
# LOAD IMAGE
# ========================================

image = Image.open(
    image_path
)


# ========================================
# LOAD U-NET
# ========================================

service = SegmentationService()


# ========================================
# SEGMENT IMAGE
# ========================================

result = service.segment(
    image
)


# ========================================
# DISPLAY RESULT
# ========================================

print("\n" + "=" * 40)
print("U-NET SEGMENTATION RESULT")
print("=" * 40)

print(
    "Original Image Size:",
    result["original_size"]
)

print(
    "Mask Shape:",
    result["mask"].shape
)

print(
    "Lesion Area:",
    f"{result['lesion_area_percentage']:.2f}%"
)

print(
    "Mask Data Type:",
    result["mask"].dtype
)

print(
    "Mask Values:",
    set(result["mask"].flatten())
)

