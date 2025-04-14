import fastapi
from api import base_router
from api.v1.authentication.exception import exception_handlers_map
from settings.base import app_settings


class ApplicationFactory:
    def __init__(self):
        self.app: fastapi.FastAPI | None = None

    def init_app(self):
        self.app = fastapi.FastAPI(title=app_settings.app_name)
        return self

    def include_routers(self):
        self.app.include_router(base_router)
        return self

    def include_error_handlers(self):
        for error, api_error in exception_handlers_map:
            self.app.add_exception_handler(error, api_error())
        return self

    def get_app(self):
        return self.app


app = ApplicationFactory().init_app().include_routers().include_error_handlers().get_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app="app:app", reload=True)
