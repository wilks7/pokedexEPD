from PIL import Image
import requests


def resize_image(img, height):
    desired_height = int(height / 2)
    # with Image.open(image_path) as img:
    original_width, original_height = img.size
    aspect_ratio = original_width / original_height
    new_width = int(desired_height * aspect_ratio)
    img = img.resize((new_width, desired_height), Image.NEAREST)
    return img

def fetchSprite(url, height):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        path = "poke_image.png"
        with open(path, 'wb') as f:
            f.write(response.content)
        img = Image.open(path)
        img = resize_image(img, height)

        return img
    else:
        print(f"Error fetching image: {response.status_code}")
        return None