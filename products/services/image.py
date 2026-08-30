from io import BytesIO

from PIL import Image, ImageOps
from django.core.files.base import ContentFile


def process_product_image(image_file):
    image = Image.open(image_file)
    image = ImageOps.exif_transpose(image)

    target_size = (1200, 675)

    image = ImageOps.contain(image, target_size)

    canvas = Image.new("RGB", target_size, "white")

    x = (target_size[0] - image.width) // 2
    y = (target_size[1] - image.height) // 2

    canvas.paste(image, (x, y))

    buffer = BytesIO()
    canvas.save(
        buffer,
        format="JPEG",
        quality=85,
        optimize=True,
    )

    return ContentFile(buffer.getvalue())