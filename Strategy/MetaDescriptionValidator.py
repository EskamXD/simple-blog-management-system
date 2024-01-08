from Strategy.ValidationStrategy import ValidationStrategy

from PIL import Image, ImageDraw, ImageFont

META_OK = ("meta_ok", "#28a745")
META_LONG = ("meta_long", "#dc3545")
META_DEFAULT = ("meta_default", "#007bff")

class MetaDescriptionValidator(ValidationStrategy):
    def validate(self, meta_description):
        if not meta_description:
            return META_DEFAULT[0]
        # if meta_description up to 158 characters and length in pixels for arial 22 is up to 920px
        title_length = len(meta_description)

        font = ImageFont.truetype("Arial.ttf", 14)
        image = ImageDraw.Draw(Image.new("RGB", (1, 1)))
        title_length_in_pixels = image.textlength(meta_description, font)

        if title_length_in_pixels <= 920:
            if title_length <= 158:
                return META_OK[0]

        return META_LONG[0]
