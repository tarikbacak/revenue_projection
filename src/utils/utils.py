import base64

def get_image_base64(image_path):
    """Convert image to base64 string"""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8') 