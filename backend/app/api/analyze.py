from fastapi import APIRouter, File, UploadFile, HTTPException
from PIL import Image
import io
import time
import base64
import numpy as np

from app.utils.image_validation import validate_image
from app.utils.input_safety import check_segmentation_quality
from app.utils.ood_check import OODChecker
from app.utils.input_assessment import assess_input

from app.services.segmentation_service import SegmentationService
from app.services.classification_service import ClassificationService


router = APIRouter(
    prefix="/analyze",
    tags=["Analysis"]
)


# ----------------------------------------
# LOAD SERVICES
# ----------------------------------------

segmentation_service = SegmentationService()

classification_service = ClassificationService()

ood_checker = OODChecker()


# ----------------------------------------
# ENCODE SEGMENTATION MASK
# ----------------------------------------

def encode_mask_to_base64(mask):

    if hasattr(mask, "detach"):
        mask = mask.detach().cpu().numpy()

    elif isinstance(mask, Image.Image):
        mask = np.asarray(mask)

    else:
        mask = np.asarray(mask)

    mask = np.squeeze(mask)

    if mask.ndim != 2:
        raise ValueError(
            "Segmentation mask has an unexpected shape."
        )

    binary_mask = (
        (mask > 0.5).astype(np.uint8) * 255
    )

    mask_image = Image.fromarray(
        binary_mask,
        mode="L"
    )

    buffer = io.BytesIO()

    mask_image.save(
        buffer,
        format="PNG"
    )

    encoded_mask = base64.b64encode(
        buffer.getvalue()
    ).decode("utf-8")

    return encoded_mask


# ----------------------------------------
# ANALYZE IMAGE
# ----------------------------------------

@router.post("/")
async def analyze_image(
    file: UploadFile = File(...)
):

    start_time = time.perf_counter()

    print("\n" + "=" * 40)
    print("ANALYSIS TIMING")
    print("=" * 40)


    # ------------------------------------
    # READ FILE
    # ------------------------------------

    contents = await file.read()


    # ------------------------------------
    # FILE TYPE VALIDATION
    # ------------------------------------

    allowed_content_types = {
        "image/jpeg",
        "image/jpg",
        "image/png",
        "image/webp"
    }

    if file.content_type not in allowed_content_types:

        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported file type. "
                "Please upload a JPG, JPEG, PNG "
                "or WEBP image."
            )
        )


    # ------------------------------------
    # OPEN IMAGE
    # ------------------------------------

    try:

        image = Image.open(
            io.BytesIO(contents)
        )

    except Exception:

        raise HTTPException(
            status_code=400,
            detail=(
                "The uploaded file could not "
                "be read as an image. "
                "Please upload a valid JPG, "
                "JPEG, PNG or WEBP image."
            )
        )


    # ------------------------------------
    # BASIC IMAGE VALIDATION
    # ------------------------------------

    validation_result = validate_image(
        image
    )

    print(
        "Image validation:",
        round(
            time.perf_counter() - start_time,
            3
        ),
        "seconds"
    )

    if not validation_result["valid"]:

        raise HTTPException(
            status_code=400,
            detail=validation_result["message"]
        )


    # ------------------------------------
    # OOD CHECK
    # ------------------------------------

    ood_result = ood_checker.check(
        image
    )

    print(
        "OOD check:",
        round(
            time.perf_counter() - start_time,
            3
        ),
        "seconds"
    )

    if not ood_result["safe"]:

        return {

            "success": False,

            "status": "rejected",

            "message": (
                "The uploaded image could not "
                "be identified as sufficiently "
                "similar to the supported ISIC "
                "image distribution."
            ),

            "ood": ood_result
        }


    # ------------------------------------
    # SEGMENTATION
    # ------------------------------------

    segmentation_result = (
        segmentation_service.segment(
            image
        )
    )

    print(
        "Segmentation:",
        round(
            time.perf_counter() - start_time,
            3
        ),
        "seconds"
    )


    # ------------------------------------
    # SEGMENTATION SAFETY
    # ------------------------------------

    safety_result = (
        check_segmentation_quality(
            segmentation_result
        )
    )

    if not safety_result["safe"]:

        return {

            "success": False,

            "status": "rejected",

            "message": safety_result["reason"],

            "ood": ood_result,

            "segmentation_safety": safety_result
        }


    # ------------------------------------
    # CLASSIFICATION
    # ------------------------------------

    classification_result = (
        classification_service.predict(
            image
        )
    )

    print(
        "Classification:",
        round(
            time.perf_counter() - start_time,
            3
        ),
        "seconds"
    )


    # ------------------------------------
    # INPUT ASSESSMENT
    # ------------------------------------

    assessment_result = assess_input(
        ood_result,
        safety_result,
        classification_result
    )


    if assessment_result["status"] == "rejected":

        return {

            "success": False,

            "status": "input_rejected",

            "message": (
                "The uploaded image is not "
                "suitable for reliable "
                "skin-lesion analysis."
            ),

            "input_assessment": (
                assessment_result
            )
        }


    # ------------------------------------
    # ENCODE SEGMENTATION MASK
    # ------------------------------------

    try:

        mask_base64 = encode_mask_to_base64(
            segmentation_result["mask"]
        )

        print(
            "Segmentation mask encoded."
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=(
                "Segmentation mask encoding failed: "
                + str(e)
            )
        )


    # ------------------------------------
    # TOTAL TIME
    # ------------------------------------

    print(
        "TOTAL:",
        round(
            time.perf_counter() - start_time,
            3
        ),
        "seconds"
    )

    print("=" * 40)


    # ------------------------------------
    # FINAL RESPONSE
    # ------------------------------------

    return {

        "success": True,

        "status": "analysis_complete",


        # --------------------------------
        # CLASSIFICATION
        # --------------------------------

        "classification": {

            "predicted_class": (
                classification_result[
                    "predicted_class"
                ]
            ),

            "confidence": (
                classification_result[
                    "confidence"
                ]
            ),

            "probabilities": (
                classification_result[
                    "probabilities"
                ]
            )
        },


        # --------------------------------
        # SEGMENTATION
        # --------------------------------

        "segmentation": {

            "lesion_area_percentage": (
                segmentation_result[
                    "lesion_area_percentage"
                ]
            ),

            "mask_base64": mask_base64
        },


        # --------------------------------
        # SEGMENTATION SAFETY
        # --------------------------------

        "segmentation_safety": (
            safety_result
        ),


        # --------------------------------
        # OOD INFORMATION
        # --------------------------------

        "ood": (
            ood_result
        ),


        # --------------------------------
        # INPUT ASSESSMENT
        # --------------------------------

        "input_assessment": (
            assessment_result
        )
    }