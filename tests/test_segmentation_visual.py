import os

from PIL import Image

from app.services.segmentation_service import SegmentationService


IMAGE_PATH = (
    r"C:\Users\vedan\Pictures\Screenshots"
    r"\Screenshot 2026-04-29 114902.png"
)


def main():

    print("\n" + "=" * 40)
    print("WRONG IMAGE SEGMENTATION TEST")
    print("=" * 40)

    if not os.path.exists(IMAGE_PATH):

        print("Image not found:")
        print(IMAGE_PATH)
        return

    image = Image.open(
        IMAGE_PATH
    ).convert("RGB")

    print("Image:", IMAGE_PATH)
    print("Original size:", image.size)

    service = SegmentationService()

    result = service.segment(image)

    mask = result["mask"]

    print("\n" + "=" * 40)
    print("SEGMENTATION RESULT")
    print("=" * 40)

    print(
        "Mask shape:",
        mask.shape
    )

    print(
        "Mask dtype:",
        mask.dtype
    )

    print(
        "Mask values:",
        set(mask.flatten())
    )

    print(
        "Lesion area:",
        f"{result['lesion_area_percentage']:.4f}%"
    )

    # ----------------------------------------
    # CREATE VISUAL OVERLAY
    # ----------------------------------------

    resized_image = image.resize(
        (256, 256)
    )

    overlay = resized_image.copy()

    overlay_pixels = overlay.load()

    for y in range(256):

        for x in range(256):

            if mask[y, x] == 1:

                r, g, b = overlay_pixels[x, y]

                overlay_pixels[x, y] = (
                    min(255, int(r * 0.5 + 255 * 0.5)),
                    int(g * 0.5),
                    int(b * 0.5)
                )

    output_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "../segmentation_wrong_image_overlay.png"
        )
    )

    overlay.save(
        output_path
    )

    print("\n" + "=" * 40)
    print("OVERLAY CREATED")
    print("=" * 40)

    print(
        "Saved to:"
    )

    print(output_path)

    print("\n" + "=" * 40)
    print("SEGMENTATION TEST COMPLETE")
    print("=" * 40)


if __name__ == "__main__":
    main()