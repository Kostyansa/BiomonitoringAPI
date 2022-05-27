import logging
import threading

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from controller.model import model_router
from controller.bioobject import bioobject_router
from config.settings import settings


app = FastAPI(docs_url='/api/', redoc_url=None, title=settings.APP_TITLE, version=settings.APP_VERSION,
              swagger_ui_oauth2_redirect_url='/api/oauth2-redirect/')

app.include_router(router=model_router)
app.include_router(router=bioobject_router)

app.add_middleware(CORSMiddleware, allow_origins=['*'])

app.mount("/picture", StaticFiles(directory="picture"), name="picture")
app.mount("/", StaticFiles(directory="front", html=True), name="front")

def server():
    logging.debug("Starting server")
    # noinspection PyTypeChecker
    uvicorn.run(app=app, app_dir=settings.APP_PATH, host=settings.APP_HOST, port=settings.APP_PORT)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.DEBUG)
    server_thread = threading.Thread(target=server, daemon=True)
    server_thread.start()
    server_thread.join()
