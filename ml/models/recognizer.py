from .prompt import Prompt
from .image_data import ImageData
from .client import GoogleClientConfig
from ..core.helpers import env_proxy


class GoogleRecognizer:
    def __init__(self, prompt:Prompt=None, image_data:ImageData=None, config:GoogleClientConfig=None):
        self._prompt = prompt
        self._image_data = image_data
        self._config = config
    
    @property
    def prompt(self):
        return self._prompt

    @prompt.setter
    def prompt(self, new_prompt:Prompt):
        self._prompt = new_prompt
    
    @property
    def image_data(self):
        return self._image_data

    @image_data.setter
    def image_data(self, new_image_data:ImageData):
        self._image_data = new_image_data

    @property
    def config(self):
        return self._image_data

    @config.setter
    def config(self, new_config:GoogleClientConfig):
        self._config = new_config

    async def __call__(self, *args, **kwargs):
        image = None
        if args:
            image = args[0]

        kw_image = kwargs.get("image")
        image = kw_image if kw_image else image

        if isinstance(image, bytes):
            self._image_data = ImageData(image_bytes=image)
        elif isinstance(image, ImageData):
            self._image_data = image
        else:
            raise TypeError(f"Provided an invalid image: {type(image)}")

        with env_proxy(self._config.proxy):
            return await self._config.client.aio.models.generate_content(
                model = self._config.model_id,
                config = self._config.gen_config,
                contents = [self._image_data.image, self._prompt.prompt]
            )
