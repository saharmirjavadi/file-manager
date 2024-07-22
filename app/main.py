from fastapi import FastAPI

# from app.api.v1 import router as api_router
from app.config.settings import settings  # noqa: F401

app = FastAPI()

# app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
