import logging
import threading

import uvicorn
from fastapi import FastAPI

from controller.model import model_router
from controller.bioobject import bioobject_router
from settings import settings

logging.basicConfig(filename="ml.log", format='%(asctime)s:%(levelname)s:%(message)s', encoding='utf-8', level=logging.DEBUG)

app = FastAPI(docs_url='/api/', redoc_url=None, title=settings.APP_TITLE, version=settings.APP_VERSION,
              swagger_ui_oauth2_redirect_url='/api/oauth2-redirect/')

app.include_router(router=model_router)
app.include_router(router=bioobject_router)


def server():
    logging.debug("Starting server")
    # noinspection PyTypeChecker
    uvicorn.run(app=app, app_dir=settings.APP_PATH, host=settings.APP_HOST, port=settings.APP_PORT)


if __name__ == '__main__':
    server_thread = threading.Thread(target=server, daemon=True)
    server_thread.start()
    server_thread.join()
