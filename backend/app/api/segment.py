from fastapi import APIRouter, File, UploadFile, HTTPException
from PIL import Image
import io

from app.services.segmentation_service import (
    SegmentationService
)


router = APIRouter(
    prefix="/segment",
    tags=["Segmentation"]
)


# ----------------------------------------
# LOAD SEGMENTATION SERVICE
# ----------------------------------------

segmentation_service = (
    SegmentationService()
)


# ----------------------------------------
# SEGMENT IMAGE
# ----------------------------------------

@router.post("/")
async def segment_image(
    file: UploadFile = File(...)
):

    # ------------------------------------
    # FILE TYPE VALIDATION
    # ------------------------------------

    allowed_content_types = {
        "image/jpeg",
        "image/png",
        "image/webp"
    }

    if file.content_type not in allowed_content_types:

        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported file type. "
                "Please upload a JPG, JPEG, "
                "PNG or WEBP image."
            )
        )


    # ------------------------------------
    # READ FILE
    # ------------------------------------

    contents = await file.read()


    # ------------------------------------
    # OPEN IMAGE
    # ------------------------------------

    try:

        image = Image.open(
            io.BytesIO(contents)
        ).convert("RGB")

    except Exception:

        raise HTTPException(
            status_code=400,
            detail=(
                "The uploaded file could not "
                "be read as an image."
            )
        )


    # ------------------------------------
    # RUN SEGMENTATION
    # ------------------------------------

    try:

        result = (
            segmentation_service.segment(
                image
            )
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=(
                "Segmentation failed: "
                + str(e)
            )
        )


    # ------------------------------------
    # RESPONSE
    # ------------------------------------

    return {

        "success": True,

        "status": "segmentation_complete",

        "segmentation": {

            "lesion_area_percentage": (
                result[
                    "lesion_area_percentage"
                ]
            ),

            "probability": (
                result[
                    "probability"
                ]
            ),

            "original_width": (
                result[
                    "original_width"
                ]
            ),

            "original_height": (
                result[
                    "original_height"
                ]
            )
        }
    }