from Strategy.ValidationStrategy import ValidationStrategy

from PIL import Image

import os


class ImageSizeValidator(ValidationStrategy):
    def validate(self, image_path):
        if image_path == "":
            return 0
        # if image size is up to 1200x630px
        image = Image.open(image_path)
        width, height = image.size
        weight = os.path.getsize(image_path)
        format = image.format

        # count original image size ratio
        ratio = width / height
        # resize image by ratio to width 1200px
        image = image.resize((1200, int(1200 / ratio)))
        # crop image to 630px height from center
        image = image.crop((0, (height - 630) / 2, width, (height + 630) / 2))

        if format == "JPEG" or format == "PNG" or format == "JPG":
            # copress to webp
            image.save(image_path, "webp", quality=80)

        if width <= 1200 and height <= 630:
            if weight <= 2 * 1024 * 1024:
                return 1

        return -1
