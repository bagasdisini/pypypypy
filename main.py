from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse

import version.version as version
from api.provinces import provinces_router
from api.users import users_router
from core.config import config
from db.postgresql import init_db

AppName = "Pypypypy"

app = FastAPI(
    title=AppName,
    description="A FastAPI project template",
    version=version.VERSION,
)

init_db()


@app.middleware("http")
async def secure_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def root():
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


app.include_router(users_router, prefix="/api", tags=["User"])
app.include_router(provinces_router, prefix="/api", tags=["Province"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=config.APP_HOST, port=config.APP_PORT)
