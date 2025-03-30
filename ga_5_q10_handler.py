import base64
import io
import os
from pathlib import Path
from fastapi import UploadFile
from PIL import Image

# Define mapping based on provided positions
MAPPING = [
    (2, 1, 0, 0), (1, 1, 0, 1), (4, 1, 0, 2), (0, 3, 0, 3), (0, 1, 0, 4),
    (1, 4, 1, 0), (2, 0, 1, 1), (2, 4, 1, 2), (4, 2, 1, 3), (2, 2, 1, 4),
    (0, 0, 2, 0), (3, 2, 2, 1), (4, 3, 2, 2), (3, 0, 2, 3), (3, 4, 2, 4),
    (1, 0, 3, 0), (2, 3, 3, 1), (3, 3, 3, 2), (4, 4, 3, 3), (0, 2, 3, 4),
    (3, 1, 4, 0), (1, 2, 4, 1), (1, 3, 4, 2), (0, 4, 4, 3), (4, 0, 4, 4)
]

GRID_SIZE = 5  # 5x5 grid
PIECE_SIZE = 100  # Each piece is 100x100 pixels in a 500x500 image

def reconstruct_image(file: UploadFile):
    """Reconstructs the original image, saves it as PNG, and returns Base64."""
    image = Image.open(file.file)
    
    # Create a blank image for reconstruction
    reconstructed = Image.new("RGB", (500, 500))

    for orig_row, orig_col, scr_row, scr_col in MAPPING:
        # Extract each piece from the scrambled image
        left = scr_col * PIECE_SIZE
        upper = scr_row * PIECE_SIZE
        right = left + PIECE_SIZE
        lower = upper + PIECE_SIZE
        piece = image.crop((left, upper, right, lower))
        
        # Paste the piece into the correct original position
        new_left = orig_col * PIECE_SIZE
        new_upper = orig_row * PIECE_SIZE
        reconstructed.paste(piece, (new_left, new_upper))
    
    # Get the directory where main.py is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Save the reconstructed image as PNG
    output_path = os.path.join(script_dir, "cbimage.png")
    reconstructed.save(output_path, format="PNG")  # Saving in PNG format
    print(f"Image saved at: {output_path}")

    # Save image to buffer
    img_buffer = io.BytesIO()
    reconstructed.save(img_buffer, format="PNG")
    img_buffer.seek(0)
    
    # Convert image to Base64
    encoded_string = base64.b64encode(img_buffer.read()).decode("utf-8")

    # ✅ Return only the Base64 answer as per exam portal guideline
    return {"answer": encoded_string}
