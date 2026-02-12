from fastapi import FastAPI

from app.config import APP_NAME, settings

app = FastAPI(title=APP_NAME)


@app.get("/")
def read_root():
    return {"message": APP_NAME, "status": "ok"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/config-test")
def config_test():
    return {
        "app_name": APP_NAME,
        "debug": settings.debug,
        "config_loaded": True,
    }
