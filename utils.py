import os
import math
from PIL import Image


def estimate_image_tokens(image_path: str, detail: str = "high") -> int:
    """
    Estimate the number of tokens an image will consume based on its dimensions and detail level.
    """
    with Image.open(image_path) as img:
        width, height = img.size

    if detail == "low":
        return 85  # Fixed token count for low detail
    elif detail == "high":
        # Resize logic as per OpenAI's image processing steps
        # Step 1: Scale image to fit within 2048x2048 while maintaining aspect ratio
        max_dim = 2048
        scale = min(max_dim / width, max_dim / height, 1)
        width = int(width * scale)
        height = int(height * scale)

        # Step 2: Scale so that the shortest side is 768px
        min_dim = 768
        scale = max(min_dim / width, min_dim / height, 1)
        width = int(width * scale)
        height = int(height * scale)

        # Step 3: Calculate the number of 512x512 tiles
        tiles_w = math.ceil(width / 512)
        tiles_h = math.ceil(height / 512)
        num_tiles = tiles_w * tiles_h

        # Total tokens = 85 (base) + 170 * number of tiles
        return 85 + 170 * num_tiles
    else:
        raise ValueError("Detail must be 'low' or 'high'.")
    
    
def save_caption_output(image_path, result):
    # Extract final folder name and file name without extension
    final_folder = os.path.basename(os.path.dirname(image_path))
    file_name = os.path.splitext(os.path.basename(image_path))[0]

    # Compose text file path
    text_file_path = os.path.join(os.path.dirname(image_path), f"{file_name}.txt")

    # Save to text file
    with open(text_file_path, "w", encoding="utf-8") as f:
        f.write(result)

    print(f"Saved to: {text_file_path}")
