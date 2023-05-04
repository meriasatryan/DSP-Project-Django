from PIL import Image, ImageOps
import os
import shutil
from django.conf import settings


def resize(creative, height, width):
    """
    Resize an image and return its new height, width, and URL.

    Parameters:
    - creative (Creative): The Creative instance to resize.
    - height (int): The desired height in pixels.
    - width (int): The desired width in pixels.

    Returns:
    - tuple: A tuple containing the new height (int), new width (int), and the new URL (str).
    """
    image_path = creative.file.path
    file_name, extension = os.path.splitext(image_path)
    new_file_name = f"{file_name}_copy{extension}"
    new_file_path = os.path.join(settings.MEDIA_ROOT, new_file_name)
    shutil.copy2(image_path, new_file_path)

    img = Image.open(new_file_path)
    img = img.convert('RGB')
    output_size = (width, height)
    img = ImageOps.pad(img, output_size, color='white')
    img.save(new_file_path, 'JPEG')

    height_fin = img.height
    width_fin = img.width
    split_name = new_file_name.split('/')[-1]
    url = f"/media/{split_name}"

    return width_fin, height_fin, url
