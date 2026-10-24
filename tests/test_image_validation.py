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
# IMPORT VALIDATION
# ========================================

from app.utils.image_validation import (
    validate_image
)


# ========================================
# TEST VALID IMAGE
# ========================================

valid_image = Image.new(
    "RGB",
    (500, 500),
    (120, 80, 100)
)

# Add some variation so it is not uniform
pixels = valid_image.load()

for x in range(0, 500, 20):
    for y in range(0, 500, 20):
        pixels[x, y] = (200, 150, 100)


result = validate_image(
    valid_image
)

print("\n" + "=" * 40)
print("VALID IMAGE TEST")
print("=" * 40)

print("Valid:", result["valid"])
print("Message:", result["message"])


# ========================================
# TEST LOW RESOLUTION IMAGE
# ========================================

small_image = Image.new(
    "RGB",
    (50, 50),
    (120, 80, 100)
)

result = validate_image(
    small_image
)

print("\n" + "=" * 40)
print("LOW RESOLUTION TEST")
print("=" * 40)

print("Valid:", result["valid"])
print("Message:", result["message"])


# ========================================
# TEST BLANK IMAGE
# ========================================

blank_image = Image.new(
    "RGB",
    (500, 500),
    (100, 100, 100)
)

result = validate_image(
    blank_image
)

print("\n" + "=" * 40)
print("BLANK IMAGE TEST")
print("=" * 40)

print("Valid:", result["valid"])
print("Message:", result["message"])

print("=" * 40)