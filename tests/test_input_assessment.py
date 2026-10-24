from app.utils.input_assessment import assess_input


def test_wrong_screenshot():

    print("\n" + "=" * 40)
    print("TEST 1: WRONG SCREENSHOT")
    print("=" * 40)

    ood_result = {
        "distance": 29.8496
    }

    segmentation_result = {
        "lesion_area_percentage": 2.8076,
        "fill_ratio": 0.2319,
        "border_touch_count": 0
    }

    classification_result = {
        "probabilities": {
            "Melanoma": 0.0304,
            "Melanocytic Nevus": 0.4503,
            "Basal Cell Carcinoma": 0.0712,
            "Actinic Keratosis": 0.1882,
            "Benign Keratosis": 0.0409,
            "Dermatofibroma": 0.1165,
            "Vascular Lesion": 0.1025
        }
    }

    result = assess_input(
        ood_result,
        segmentation_result,
        classification_result
    )

    print("Status:", result["status"])
    print(
        "Needs review:",
        result["needs_review"]
    )

    print("\nReasons:")

    for reason in result["reasons"]:
        print("-", reason)


def test_genuine_isic():

    print("\n" + "=" * 40)
    print("TEST 2: GENUINE ISIC")
    print("=" * 40)

    ood_result = {
        "distance": 16.6062
    }

    segmentation_result = {
        "lesion_area_percentage": 5.0,
        "fill_ratio": 0.29,
        "border_touch_count": 0
    }

    classification_result = {
        "probabilities": {
            "Melanoma": 0.0157,
            "Melanocytic Nevus": 0.7776,
            "Basal Cell Carcinoma": 0.0279,
            "Actinic Keratosis": 0.0311,
            "Benign Keratosis": 0.0129,
            "Dermatofibroma": 0.0693,
            "Vascular Lesion": 0.0656
        }
    }

    result = assess_input(
        ood_result,
        segmentation_result,
        classification_result
    )

    print("Status:", result["status"])
    print(
        "Needs review:",
        result["needs_review"]
    )

    print("\nReasons:")

    for reason in result["reasons"]:
        print("-", reason)


def main():

    print("\n" + "=" * 40)
    print("INPUT ASSESSMENT TEST")
    print("=" * 40)

    test_wrong_screenshot()
    test_genuine_isic()

    print("\n" + "=" * 40)
    print("INPUT ASSESSMENT TEST COMPLETE")
    print("=" * 40)


if __name__ == "__main__":
    main()