from google.genai import Client
from google.genai.types import GenerateContentConfig


class GoogleClientConfig:
    def __init__(self, proxy:str=None, client:Client=None, model_id:str=None, config:GenerateContentConfig=None):
        self._proxy = proxy
        self._client = client
        self._model_id = model_id
        self._gen_config = config

    @property
    def proxy(self):
        return self._proxy

    @proxy.setter
    def proxy(self, new_proxy:str=None) -> None:
        self._proxy = new_proxy
    
    @property
    def client(self):
        return self._client
    
    @client.setter
    def client(self, new_client:Client):
        self._client = new_client

    @property
    def model_id(self):
        return self._model_id
    
    @model_id.setter
    def model_id(self, new_model_id:str):
        self._model_id = new_model_id

    @property
    def gen_config(self):
        return self._gen_config
    
    @gen_config.setter
    def gen_config(self, new_gen_config:GenerateContentConfig):
        self._gen_config = new_gen_config
