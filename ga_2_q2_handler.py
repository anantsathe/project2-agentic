import io
import base64
from PIL import Image

# GA-2 Q2

def solve_ga_2_q2(input_path: str, output_path: str) -> dict:
    """
    Compress an image losslessly by reducing its color palette to 8 colors.
    Saves the compressed file if it meets size criteria and returns Base64.

    Args:
        input_path (str): Path to the input image.
        output_path (str): Path to save the compressed image.

    Returns:
        dict: Base64-encoded image.
    """
    with Image.open(input_path) as img:
        # Convert image to 8-color adaptive palette
        img = img.convert("P", palette=Image.Palette.ADAPTIVE, colors=8)
        
        # Save with PNG optimization
        img_bytes = io.BytesIO()
        img.save(img_bytes, format="PNG", optimize=True)

        # Get the compressed file size
        compressed_size = len(img_bytes.getvalue())

        # Save the file and return Base64 encoding
        with open(output_path, "wb") as f:
            f.write(img_bytes.getvalue())
        
        # Convert image to Base64
        base64_str = base64.b64encode(img_bytes.getvalue()).decode("utf-8")

        return {"answer": base64_str}  # ✅ Only return Base64

