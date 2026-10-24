
from datetime import datetime, timezone
import uuid

from pymongo.errors import PyMongoError

from app.auth import db


history_collection = db["analysis_history"]


def save_analysis_history(
    current_user: dict,
    analysis_data: dict,
) -> str:

    case_information = analysis_data.get(
        "case_information", {}
    )

    case_id = analysis_data.get("case_id")

    if not case_id:
        case_id = (
            "CASE-"
            + datetime.now(timezone.utc).strftime("%Y%m%d")
            + "-"
            + uuid.uuid4().hex[:8].upper()
        )

    record = {
        "owner_id": current_user["id"],
        "case_id": case_id,
        "patient_name": case_information.get("patient_name"),
        "age": case_information.get("age"),
        "sex": case_information.get("sex"),
        "lesion_site": case_information.get("lesion_site"),
        "created_at": datetime.now(timezone.utc),
        "status": analysis_data.get("status", "analysis_complete"),
        "classification": analysis_data.get("classification", {}),
        "original_image": analysis_data.get("original_image"),
        "segmentation": analysis_data.get("segmentation", {}),
        "segmentation_safety": analysis_data.get(
            "segmentation_safety", {}
        ),
        "ood": analysis_data.get("ood", {}),
        "input_assessment": analysis_data.get(
            "input_assessment", {}
        ),
    }

    try:
        existing_record = history_collection.find_one(
            {
                "owner_id": current_user["id"],
                "case_id": case_id,
            },
            {"_id": 1},
        )

        if existing_record:
            history_collection.update_one(
                {"_id": existing_record["_id"]},
                {"$set": record},
            )
            return str(existing_record["_id"])

        result = history_collection.insert_one(record)
        return str(result.inserted_id)

    except PyMongoError:
        raise
