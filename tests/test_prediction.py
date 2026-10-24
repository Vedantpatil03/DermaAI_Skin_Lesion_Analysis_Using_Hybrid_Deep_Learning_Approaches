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
# IMPORT CLASSIFICATION SERVICE
# ========================================

from app.services.classification_service import (
    ClassificationService
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
# LOAD MODEL
# ========================================

service = ClassificationService()


# ========================================
# PREDICT
# ========================================

result = service.predict(
    image
)


# ========================================
# DISPLAY RESULT
# ========================================

print("PREDICTION RESULT")

print(
    "Predicted Class:",
    result["predicted_class"]
)

print(
    "Confidence:",
    f"{result['confidence'] * 100:.2f}%"
)

print("\nClass Probabilities:")

for class_name, probability in result[
    "probabilities"
].items():

    print(
        f"{class_name}: "
        f"{probability * 100:.2f}%"
    )

print("=" * 40)