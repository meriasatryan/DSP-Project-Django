import base64
from PIL import Image
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def convert_blob(blob):
    """
    Decode a base64 encoded image and save it to the default Django storage.
    Returns a dictionary with the file path, URL, width and height.

    Args:
    - blob (str): a base64 encoded image string

    Returns:
    - dict: a dictionary with the file path, URL, width and height
    """
    base64_str = blob
    base64_str = base64_str + "=" * ((4 - len(base64_str) % 4) % 4)
    decoded_image = base64.b64decode(base64_str)
    file_name = 'my_image.jpg'
    file_path = default_storage.save(file_name, ContentFile(decoded_image))
    file_url = default_storage.url(file_path)
    with Image.open("media/" + file_path) as img:
        width, height = img.size
    return {
        'file': file_path,
        'url': file_url,
        'width': width,
        'height': height
    }
