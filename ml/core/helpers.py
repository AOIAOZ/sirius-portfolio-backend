import os

from contextlib import contextmanager


@contextmanager
def env_proxy(proxy_str):
    api_key, proxy = proxy_str.split('|')
    old_http = os.environ.get('http_proxy')
    old_https = os.environ.get('https_proxy')
    old_api = os.environ.get('GEMINI_API_KEY')
    os.environ['http_proxy'] = proxy
    os.environ['https_proxy'] = proxy
    os.environ['GEMINI_API_KEY'] = api_key
    try:
        yield
    finally:
        if old_http is None:
            os.environ.pop('http_proxy', None)
        else:
            os.environ['http_proxy'] = old_http
        if old_https is None:
            os.environ.pop('https_proxy', None)
        else:
            os.environ['https_proxy'] = old_https
        if old_api is None:
            os.environ.pop('GEMINI_API_KEY', None)
        else:
            os.environ['GEMINI_API_KEY'] = old_api
