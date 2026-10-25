from fastapi import FastAPI

app = FastAPI(title="Docker Delivery Lab", version="0.1.0")


@app.get("/")
def root() -> dict[str, str]:
    return {"project": "Docker Delivery Lab", "message": "API is running"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
