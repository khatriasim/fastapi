from fastapi import FastAPI, Request
from app.core.config import settings
from app.api.v1.router import api_router
from app.core.database import Base, engine
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import socket
from contextlib import asynccontextmanager
import redis.asyncio as aioredis

@asynccontextmanager
async def lifespan(app: FastAPI):
    client = aioredis.Redis.from_url(settings.redis_url, decode_responses = True)
    await client.ping()
    print ("redis connected success")
    await client.close()
    yield

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan
)
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1"]
)

app.include_router(api_router)

@app.get("/")
async def root():
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running"
    }


@app.get("/whoami")
def whoami(request: Request):
    return {
        "container": socket.gethostname(),
        "client_ip": request.headers.get("X-Real-IP"),
        "forwarded_for": request.headers.get("X-Forwarded-For"),
        "host": request.headers.get("Host"),
        "proto": request.headers.get("X-Forwarded-Proto"),
        }