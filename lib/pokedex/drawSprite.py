from PIL import Image

def resize_image(img, height):
    desired_height = int(height / 2)
    # with Image.open(image_path) as img:
    original_width, original_height = img.size
    aspect_ratio = original_width / original_height
    new_width = int(desired_height * aspect_ratio)
    img = img.resize((new_width, desired_height), Image.NEAREST)
    return img
