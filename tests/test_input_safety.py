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
# IMPORT SERVICES
# ========================================

from app.services.segmentation_service import (
    SegmentationService
)

from app.utils.input_safety import (
    check_segmentation_quality
)


# ========================================
# IMAGE PATH
# ========================================

image_path = r"C:\Users\vedan\Downloads\bike.jpg"


if not os.path.exists(image_path):
    raise FileNotFoundError(
        f"Image not found: {image_path}"
    )


# ========================================
# LOAD IMAGE
# ========================================

image = Image.open(image_path).convert("RGB")


# ========================================
# LOAD U-NET
# ========================================

service = SegmentationService()


# ========================================
# SEGMENT IMAGE
# ========================================

segmentation_result = service.segment(image)


# ========================================
# SAFETY CHECK
# ========================================

safety_result = check_segmentation_quality(
    segmentation_result
)


# ========================================
# DISPLAY RESULT
# ========================================

print("\n" + "=" * 40)
print("INPUT SAFETY CHECK")
print("=" * 40)

print(
    "Safe:",
    safety_result["safe"]
)

print(
    "Reason:",
    safety_result["reason"]
)

if safety_result["safe"]:

    print(
        "Lesion Area:",
        f"{safety_result['lesion_area_percentage']:.2f}%"
    )

    print(
        "Fill Ratio:",
        f"{safety_result['fill_ratio']:.4f}"
    )

    print(
        "Bounding Box:",
        safety_result["bounding_box"]
    )

print("=" * 40)