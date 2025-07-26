from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlmodel import SQLModel
from src.session import engine
from src.api import router
import logging
from pythonjsonlogger import jsonlogger


def init_logger(log_level: str = "INFO", enable_json: bool = True) -> None:
    """Initialize structured logging for the application"""
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, log_level.upper()))

    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    handler = logging.StreamHandler()

    if enable_json:
        formatter = jsonlogger.JsonFormatter(
            fmt="%(asctime)s %(levelname)s %(name)s %(message)s %(pathname)s %(funcName)s %(lineno)d"
        )
    else:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    logger.info(
        "Logging initialized",
        extra={"log_level": log_level, "format": "json" if enable_json else "text"},
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize logging
    init_logger(log_level="INFO", enable_json=True)

    # Create database tables
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(title="Zuma App", lifespan=lifespan)
app.include_router(router)

origins = ["http://localhost:5173"]
app.add_middleware(
    CORSMiddleware, allow_origins=origins, allow_methods=["*"], allow_headers=["*"]
)


@app.get("/health", tags=["Health"])
async def health_check():
    return {"message": "Ok"}
