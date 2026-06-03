from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from app.config.database import connect_to_mongodb, close_mongodb_connection
from app.config.logger import get_logger, setup_logging
from app.routes import user_route, product_route, order_route

setup_logging()
logger = get_logger("app")

uploads_dir = Path(__file__).resolve().parent.parent / "uploads"
uploads_dir.mkdir(parents=True, exist_ok=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events for MongoDB connection"""
    await connect_to_mongodb()
    yield
    await close_mongodb_connection()


app = FastAPI(
    title="Mango Sales API",
    description="API for managing mango sales, products, users, and orders",
    version="1.0.0",
    lifespan=lifespan
)

app.mount("/uploads", StaticFiles(directory=str(uploads_dir)), name="uploads")

# Include routers
app.include_router(user_route.router)
app.include_router(product_route.router)
app.include_router(order_route.router)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(
        f"{request.client.host if request.client else 'unknown'} "
        f"{request.method} {request.url.path} "
        f"query={request.url.query or '-'}"
    )
    try:
        response = await call_next(request)
    except Exception:
        logger.exception("Request processing failed")
        raise
    logger.info(
        f"{request.client.host if request.client else 'unknown'} "
        f"{request.method} {request.url.path} "
        f"status={response.status_code}"
    )
    return response


@app.get("/")
def root():
    return {"message": "Welcome to Mango Sales API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}