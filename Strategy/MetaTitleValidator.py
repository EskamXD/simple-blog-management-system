from Strategy.ValidationStrategy import ValidationStrategy

from PIL import Image, ImageDraw, ImageFont


class MetaTitleValidator(ValidationStrategy):
    def validate(self, meta_title):
        if not meta_title:
            return 0
        # if meta_title beetwen 50 and 60 characters and length in pixels for arial 22 is up to 580px
        title_length = len(meta_title)

        font = ImageFont.truetype("Arial.ttf", 20)
        image = ImageDraw.Draw(Image.new("RGB", (1, 1)))
        title_length_in_pixels = image.textlength(meta_title, font)

        if title_length_in_pixels <= 580:
            if title_length <= 60:
                return 1

        return -1
