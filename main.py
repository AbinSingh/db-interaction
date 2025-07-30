from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import threading
from routers import router, request_queue
from background_worker import process_requests  # Assuming you modularize the background worker
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: launch background worker
    worker_thread = threading.Thread(target=process_requests, daemon=True)
    worker_thread.start()

    yield  # App is running

    # Shutdown: no special cleanup needed here unless you're managing resources
    print("App is shutting down...")

app = FastAPI(
    title="Question Processing API",
    version="1.0",
    lifespan=lifespan
)

# ✅ Middleware (CORS as example)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or restrict to frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Register router with common prefix
app.include_router(router, prefix="/api")




