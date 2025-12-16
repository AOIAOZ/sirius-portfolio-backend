import sys
import time
import asyncio

from google.genai.errors import ClientError, ServerError
from dotenv import load_dotenv
load_dotenv()

from .helpers import create_model_config, init_google_client
from .models import GoogleClientConfig, GoogleRecognizer

from .core import logger
from .core import model_id, model_prompt, model_temperature, model_thinking_budget, proxies


try:
    PROXY_STR = next(proxies)
except StopIteration:
    print('Expected to find at least 1 proxy specified')
    sys.exit(1)

genai_client = init_google_client(proxy=PROXY_STR)
model_config = create_model_config(
    thinking_budget=model_thinking_budget,
    temperature=model_temperature
    )
google_config = GoogleClientConfig(
    proxy=PROXY_STR,
    client=genai_client,
    model_id=model_id,
    config=model_config
)
recognizer = GoogleRecognizer(
    prompt=model_prompt,
    config=google_config,
)


async def recognize(image_bytes:bytes=None):
    try:
        start_time = time.time()
        response = await recognizer(image_bytes)
        logger.debug("Processed input in %s!", time.time()-start_time)
    except ClientError as e:
        logger.error(e)
        try:
            proxy = next(proxies)
        except StopIteration:
            logger.error('All proxies resources exhausted')
            return
        recognizer.config.proxy = proxy
        response = await recognizer(image_bytes)
    except ServerError as e:
        logger.error("An server error occured: \"%s\"", e)
        return

    return str(response.text)





if __name__ == '__main__':
    def read_image(file_path):
        with open(file_path, "rb") as file:
            image_bytes = file.read()
        return image_bytes
    img_b = read_image("sample/1.jpg")
    print(len(img_b))
    res = asyncio.run(recognize(image_bytes=img_b))
    print(res)
