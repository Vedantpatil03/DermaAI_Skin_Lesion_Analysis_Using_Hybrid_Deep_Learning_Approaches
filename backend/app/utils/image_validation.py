from PIL import Image
import numpy as np


MIN_WIDTH = 100
MIN_HEIGHT = 100


def validate_image(image: Image.Image):

    # ----------------------------------------
    # IMAGE SIZE
    # ----------------------------------------

    width, height = image.size

    if (
        width < MIN_WIDTH
        or height < MIN_HEIGHT
    ):

        return {
            "valid": False,
            "message": (
                "Image resolution is too low. "
                "Please upload a clearer image."
            )
        }

    # ----------------------------------------
    # IMAGE CONTENT
    # ----------------------------------------

    try:

        rgb_image = image.convert(
            "RGB"
        )

        image_array = np.asarray(
            rgb_image,
            dtype=np.float32
        )

    except Exception:

        return {
            "valid": False,
            "message": (
                "The uploaded file could not "
                "be processed as an image."
            )
        }

    # ----------------------------------------
    # VISUAL INFORMATION CHECK
    # ----------------------------------------

    std_value = image_array.std()

    if std_value < 5:

        return {
            "valid": False,
            "message": (
                "Image does not contain enough "
                "visual information. Please upload "
                "a clear skin-lesion image."
            )
        }

    # ----------------------------------------
    # VALID IMAGE
    # ----------------------------------------

    return {
        "valid": True,
        "message": (
            "Image passed basic validation."
        )
    }