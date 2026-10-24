from fastapi import APIRouter, File, UploadFile, HTTPException
from PIL import Image
import io

from app.services.classification_service import (
    ClassificationService
)


router = APIRouter(
    prefix="/predict",
    tags=["Prediction"]
)


# ----------------------------------------
# LOAD CLASSIFICATION SERVICE
# ----------------------------------------

classification_service = (
    ClassificationService()
)


# ----------------------------------------
# PREDICT IMAGE
# ----------------------------------------

@router.post("/")
async def predict_image(
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
    # READ IMAGE
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
    # CLASSIFICATION
    # ------------------------------------

    try:

        result = classification_service.predict(
            image
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=(
                "Classification failed: "
                + str(e)
            )
        )


    # ------------------------------------
    # RESPONSE
    # ------------------------------------

    return {

        "success": True,

        "status": "prediction_complete",

        "prediction": {

            "predicted_class": (
                result[
                    "predicted_class"
                ]
            ),

            "confidence": (
                result[
                    "confidence"
                ]
            ),

            "probabilities": (
                result[
                    "probabilities"
                ]
            )
        }
    }