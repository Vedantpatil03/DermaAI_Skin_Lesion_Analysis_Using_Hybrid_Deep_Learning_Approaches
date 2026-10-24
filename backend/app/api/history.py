
from datetime import datetime, timezone

from bson import ObjectId
from fastapi import (
    APIRouter,
    Body,
    Depends,
    HTTPException,
)
from pymongo.errors import PyMongoError

from app.auth import db, get_current_user
from app.services.history_service import save_analysis_history


router = APIRouter(
    prefix="/history",
    tags=["Analysis History"],
)

history_collection = db["analysis_history"]


# ----------------------------------------
# SAVE A SUCCESSFUL ANALYSIS
# ----------------------------------------

@router.post("/")
def save_analysis(
    analysis_data: dict = Body(...),
    current_user: dict = Depends(get_current_user),
):
    if analysis_data.get("success") is not True:
        raise HTTPException(
            status_code=400,
            detail="Only successful analyses can be saved.",
        )

    try:
        history_id = save_analysis_history(
            current_user=current_user,
            analysis_data=analysis_data,
        )

        return {
            "success": True,
            "message": "Analysis history saved successfully.",
            "history_id": history_id,
        }

    except PyMongoError:
        raise HTTPException(
            status_code=503,
            detail="Could not save analysis history.",
        )


# ----------------------------------------
# GET THE LOGGED-IN DOCTOR'S HISTORY
# ----------------------------------------

@router.get("/")
def get_analysis_history(
    current_user: dict = Depends(get_current_user),
):
    try:
        records = history_collection.find(
            {
                "owner_id": current_user["id"],
            },
            {
                "segmentation.mask_base64": 0,
            },
        ).sort("created_at", -1)

        history = []

        for record in records:
            history.append(
                {
                    "history_id": str(record["_id"]),
                    "case_id": record.get("case_id"),
                    "patient_name": record.get("patient_name"),
                    "age": record.get("age"),
                    "sex": record.get("sex"),
                    "lesion_site": record.get("lesion_site"),
                    "created_at": record.get("created_at"),
                    "status": record.get("status"),
                    "classification": record.get("classification"),
                    "segmentation": record.get("segmentation"),
                }
            )

        return {
            "success": True,
            "count": len(history),
            "history": history,
        }

    except PyMongoError:
        raise HTTPException(
            status_code=503,
            detail="Could not retrieve analysis history.",
        )


# ----------------------------------------
# GET ONE ANALYSIS RECORD
# ----------------------------------------

@router.get("/{history_id}")
def get_analysis_detail(
    history_id: str,
    current_user: dict = Depends(get_current_user),
):
    if not ObjectId.is_valid(history_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid history ID.",
        )

    try:
        record = history_collection.find_one(
            {
                "_id": ObjectId(history_id),
                "owner_id": current_user["id"],
            }
        )

    except PyMongoError:
        raise HTTPException(
            status_code=503,
            detail="Could not retrieve the analysis record.",
        )

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Analysis record not found.",
        )

    record["history_id"] = str(record.pop("_id"))
    record.pop("owner_id", None)

    return {
        "success": True,
        "analysis": record,
    }


# ----------------------------------------
# DELETE ALL ANALYSIS RECORDS
# ----------------------------------------

@router.delete("/")
def clear_analysis_history(
    current_user: dict = Depends(get_current_user),
):
    try:
        result = history_collection.delete_many(
            {
                "owner_id": current_user["id"],
            }
        )
    except PyMongoError:
        raise HTTPException(
            status_code=503,
            detail="Could not clear analysis history.",
        )

    return {
        "success": True,
        "deleted_count": result.deleted_count,
        "message": "Analysis history cleared successfully.",
    }


# ----------------------------------------
# DELETE ONE ANALYSIS RECORD
# ----------------------------------------

@router.delete("/{history_id}")
def delete_analysis(
    history_id: str,
    current_user: dict = Depends(get_current_user),
):
    if not ObjectId.is_valid(history_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid history ID.",
        )

    try:
        result = history_collection.delete_one(
            {
                "_id": ObjectId(history_id),
                "owner_id": current_user["id"],
            }
        )
    except PyMongoError:
        raise HTTPException(
            status_code=503,
            detail="Could not delete the analysis record.",
        )

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Analysis record not found.",
        )

    return {
        "success": True,
        "message": "Analysis record deleted successfully.",
    }
