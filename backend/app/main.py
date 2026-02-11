from fastapi import FastAPI

app = FastAPI(title="E-commerce Admin AI Assistant API")


@app.get("/")
def read_root():
    return {"message": "E-commerce Admin AI Assistant API", "status": "ok"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
