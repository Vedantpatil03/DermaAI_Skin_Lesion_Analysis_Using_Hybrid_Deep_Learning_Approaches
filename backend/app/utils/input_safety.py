import numpy as np


# ========================================
# INPUT SAFETY CHECK
# ========================================

def check_segmentation_quality(segmentation_result):

    mask = segmentation_result["mask"]

    # ------------------------------------
    # Basic mask information
    # ------------------------------------

    total_pixels = mask.size

    lesion_pixels = np.sum(mask == 1)

    lesion_area_percentage = (
        lesion_pixels / total_pixels
    ) * 100

    # ------------------------------------
    # No detected region
    # ------------------------------------

    if lesion_pixels == 0:

        return {
            "safe": False,
            "reason": (
                "No meaningful lesion region "
                "was detected."
            )
        }

    # ------------------------------------
    # Find lesion coordinates
    # ------------------------------------

    y_coords, x_coords = np.where(mask == 1)

    min_x = x_coords.min()
    max_x = x_coords.max()

    min_y = y_coords.min()
    max_y = y_coords.max()

    # ------------------------------------
    # Image dimensions
    # ------------------------------------

    image_height, image_width = mask.shape

    # ------------------------------------
    # Bounding-box dimensions
    # ------------------------------------

    width = max_x - min_x + 1
    height = max_y - min_y + 1

    # ------------------------------------
    # Bounding-box area
    # ------------------------------------

    bounding_box_area = width * height

    # ------------------------------------
    # Fill ratio
    #
    # Percentage of the bounding box
    # occupied by the predicted region
    # ------------------------------------

    fill_ratio = (
        lesion_pixels / bounding_box_area
    )

    # ------------------------------------
    # Border detection
    # ------------------------------------

    touches_left = min_x == 0
    touches_right = max_x == image_width - 1
    touches_top = min_y == 0
    touches_bottom = max_y == image_height - 1

    border_touch_count = sum([
        touches_left,
        touches_right,
        touches_top,
        touches_bottom
    ])

    # ------------------------------------
    # Reject extremely fragmented /
    # sparse segmentation
    # ------------------------------------

    if fill_ratio < 0.10:

        return {
            "safe": False,
            "reason": (
                "The detected region is too "
                "fragmented for reliable analysis."
            )
        }

    # ------------------------------------
    # Reject if almost the entire image
    # is segmented
    # ------------------------------------

    if lesion_area_percentage > 80:

        return {
            "safe": False,
            "reason": (
                "The segmentation covers an "
                "unusually large portion of the image."
            )
        }

    # ------------------------------------
    # Reject suspicious border-spanning
    # segmentation
    # ------------------------------------
    #
    # This checks a combination of:
    #
    # 1. Region touches an image border
    # 2. Region covers a large area
    # 3. Bounding box has high fill ratio
    #
    # This is NOT based on border contact
    # alone.
    # ------------------------------------

    if (
        border_touch_count > 0
        and lesion_area_percentage > 30
        and fill_ratio > 0.60
    ):

        return {
            "safe": False,
            "reason": (
                "The detected region has an "
                "unusual image-spanning shape "
                "and could not be reliably "
                "localized as a skin lesion."
            )
        }

    # ------------------------------------
    # Passed safety checks
    # ------------------------------------

    return {
        "safe": True,
        "reason": (
            "The detected region passed "
            "the initial segmentation checks."
        ),
        "lesion_area_percentage": float(
            lesion_area_percentage
        ),
        "fill_ratio": float(
            fill_ratio
        ),
        "border_touch_count": int(
            border_touch_count
        ),
        "bounding_box": {
            "x_min": int(min_x),
            "y_min": int(min_y),
            "x_max": int(max_x),
            "y_max": int(max_y)
        }
    }