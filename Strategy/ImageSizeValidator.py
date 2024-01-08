from Strategy.ValidationStrategy import ValidationStrategy

from io import BytesIO
from PIL import Image

import os

IDEAL_RATIO = 1.7772277227722772277227722772277
IDEAL_WIDTH = 1436
IDEAL_HEIGHT = 808


class ImageSizeValidator(ValidationStrategy):
    def validate(self, image_path: str) -> int:
        if image_path == "":
            return 0

        image = Image.open(image_path)
        width, height = image.size

        # if image is vertical return -1
        if height > width:
            return -1

        ratio = width / height
        if ratio > IDEAL_RATIO:
            image = image.resize(
                (int(IDEAL_HEIGHT * ratio), IDEAL_HEIGHT), Image.ANTIALIAS
            )
        else:
            image = image.resize(
                (IDEAL_WIDTH, int(IDEAL_WIDTH / ratio)), Image.ANTIALIAS
            )

        width, height = image.size

        if not (width <= IDEAL_WIDTH and height <= IDEAL_HEIGHT):
            image.crop((0, 0, IDEAL_WIDTH, IDEAL_HEIGHT))

        return self.compress_image(image)

    def compress_image(self, image: Image) -> int or BytesIO:
        original_quality = 100
        flag = True

        while flag:
            # Save image to temp file
            buffer = BytesIO()

            image.save(buffer, "webp", quality=original_quality)
            
            weight = len(buffer.getvalue())

            if weight <= 2 * 1024 * 1024:
                buffer.seek(0)  # Przejdź na początek bufora
                return buffer  # Zwróć obiekt BytesIO zawierający skompresowany obraz


            original_quality -= 5  # Adjust how much you want to reduce the quality

            if original_quality <= 0:
                buffer.close()

                return -1  # Couldn't reduce the size below 2 MB
