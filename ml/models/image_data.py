from google.genai import types


class ImageData:
    def __init__(self, image_bytes:bytes=None):
        self._image = None
        if image_bytes is not None:
            self.image = image_bytes

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, new_image:bytes=None):
        if new_image is None:
            return
        if not isinstance(new_image, bytes):
            raise TypeError("Image must be bytes")
        self._image = types.Part.from_bytes(data=new_image, mime_type="image/jpeg")
