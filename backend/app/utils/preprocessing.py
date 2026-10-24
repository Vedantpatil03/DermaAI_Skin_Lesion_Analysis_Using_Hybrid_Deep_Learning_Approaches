from PIL import Image
from torchvision import transforms


# Image preprocessing used by the Hybrid CNN + ViT model
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])


def preprocess_image(image: Image.Image):
    """
    Preprocess an uploaded skin lesion image
    for the Hybrid CNN + ViT model.
    """

    # Ensure image has 3 RGB channels
    image = image.convert("RGB")

    # Apply preprocessing
    image_tensor = transform(image)

    # Add batch dimension
    image_tensor = image_tensor.unsqueeze(0)

    return image_tensor