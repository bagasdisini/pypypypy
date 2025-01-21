import logging
import uvicorn
import version.version as version

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from api.message import message_router
from api.provinces import provinces_router
from api.security import security_router
from api.transaction import transaction_router
from api.transaction_log import transaction_log_router
from api.users import users_router
from core.config import config
from db.postgresql import init_db
from util.jwt import jwt

AppName = "Pypypypy"

app = FastAPI(
    title=AppName,
    description="A FastAPI project template",
    version=version.VERSION,
)

logging.basicConfig(level=logging.INFO)
init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ALLOW_ORIGINS.split(','),
    allow_headers=["*"],
)


@app.middleware("http")
async def secure_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def root():
    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <title>{AppName}</title>
        </head>
        <body>
            <h1>Welcome to {AppName}</h1>
            <p><a href="/api/version">version: {version.VERSION}</a></p>
            <p><a href="/docs">docs</a></p>
            <h4>Atmatech</h4>
        </body>
    </html>
    """
    return HTMLResponse(content=html_template)


@app.get("/api/version", include_in_schema=False)
def get_version():
    return JSONResponse(content={"name": AppName, "version": version.VERSION})


token = jwt.create_jwt_token("123456", "user@example.com", "user", "session123")
print(token)


app.include_router(users_router, prefix="/api", tags=["User"])
app.include_router(provinces_router, prefix="/api", tags=["Province"])
app.include_router(security_router, prefix="/api", tags=["Security"])
app.include_router(transaction_router, prefix="/api", tags=["Transaction"])
app.include_router(transaction_log_router, prefix="/api", tags=["Transaction Log"])
app.include_router(message_router, prefix="/api", tags=["Message"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=config.APP_HOST,
        port=config.APP_PORT,
        reload=True
    )