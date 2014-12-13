from imagekit.registry import register
from imagekit.processors import Thumbnail as ThumbnailProcessor
from imagekit.specs import ImageSpec
from imagekit.processors import Adjust, Reflection, Transpose
from photologue.utils.watermark import apply_watermark

try:
    import Image
except ImportError:
    try:
        from PIL import Image
    except ImportError:
        raise ImportError('Photologue was unable to import the Python Imaging Library. Please confirm it`s installed and available on your current Python path.')


CROP_ANCHOR_OPTIONS = {
    'top': 't',
    'right': 'r',
    'bottom': 'b',
    'left': 'l',
    'center': 'c',
    'auto': 'auto'
}


class Watermark(object):
    def __init__(self, watermark):
        self.watermark = watermark

    def process(self, img):
        self.watermark.image.seek(0)
        mark = Image.open(self.watermark.image.file)
        img = apply_watermark(im=img, mark=mark, position=self.watermark.style, opacity=self.watermark.opacity)
        return img


class PhotologueSpec(ImageSpec):
    def __init__(self, photo, photosize, **kwargs):

        effect = None
        if photo.effect is not None:
            effect = photo.effect
        elif photosize.effect is not None:
            effect = photosize.effect

        self.processors = []
        self.set_size(photosize=photosize, crop_from=photo.crop_from)
        self.set_effect(effect)
        self.set_watermark(photosize.watermark)

        super(PhotologueSpec, self).__init__(source=photo.image, **kwargs)


    def set_effect(self, effect):
        if not effect:
            return None
        self.processors.append(
            Adjust(
                color=effect.color,
                brightness=effect.brightness,
                contrast=effect.contrast,
                sharpness=effect.sharpness
            )
        )
        if effect.transpose_method:
            method = getattr(Image, effect.transpose_method)
            self.processors.append(
                Transpose(method)
            )

        if effect.reflection_size > 0:
            self.processors.append(
                Reflection(
                    background_color=effect.background_color,
                    size=effect.reflection_size,
                    opacity=effect.reflection_strength
                )
            )

    def set_size(self, photosize, crop_from):
        if not photosize and crop_from:
            return None
        imagekit_anchor = None
        if photosize.crop and crop_from:
            imagekit_anchor = CROP_ANCHOR_OPTIONS[crop_from]

        if photosize.width == 0:
            photosize.width = None
        if photosize.height == 0:
            photosize.height = None
        self.processors.append(
            ThumbnailProcessor(
                width=photosize.width,
                height=photosize.height,
                anchor=imagekit_anchor,
                crop=photosize.crop,
                upscale=photosize.upscale
            )
        )

    def set_watermark(self, watermark):
        if watermark is None:
            return None
        self.processors.append(
            Watermark(watermark)
        )


register.generator('photologue:thumbnail', PhotologueSpec)
