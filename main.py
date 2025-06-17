from fastapi import FastAPI, Request, Response, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from api.endpoints import router  # Tus endpoints dinámicos
from logger.logging_config import logger  # ✅ Logger personalizado

# 🔐 Módulos de autenticación
from auth.jwt_handler import create_access_token, verify_password
from auth.db import SessionLocal
from auth.models import User

app = FastAPI(
    title="SktCod-API",
    description="API-VDial-Custom",
    version="1.0.0",
    docs_url=None,
    redoc_url=None,
    openapi_url="/openapi.json"
)

# ✅ Middleware para registrar logs de cada petición
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"📥 {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"📤 {response.status_code} {request.url}")
    return response

# ✅ Middleware para limpiar y reforzar headers HTTP
@app.middleware("http")
async def clean_response_headers(request: Request, call_next):
    response: Response = await call_next(request)
    response.headers["server"] = "SktCod-API"
    for header in ["x-powered-by", "date"]:
        if header in response.headers:
            del response.headers[header]
    return response

# ✅ Endpoint de autenticación (login) para obtener JWT
@app.post("/token", include_in_schema=False)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db = SessionLocal()
    user = db.query(User).filter_by(username=form_data.username).first()
    db.close()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Credenciales inválidas")

    access_token = create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=timedelta(minutes=60)
    )
    return {"access_token": access_token, "token_type": "bearer"}

# ✅ Incluir router dinámico protegido
app.include_router(router)

# ✅ Servir archivos estáticos del Swagger personalizado
app.mount("/static", StaticFiles(directory="static"), name="static")

# ✅ Ruta personalizada para Swagger UI
@app.get("/sktcod.custom.api", include_in_schema=False)
async def custom_swagger_ui():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>SktCod-API</title>
        <link rel="stylesheet" type="text/css" href="/static/swagger/swagger-ui.css" />
        <link rel="icon" type="image/png" href="/static/swagger/favicon-32x32.png" />
    </head>
    <body>
        <div id="swagger-ui"></div>
        <script src="/static/swagger/swagger-ui-bundle.js"></script>
        <script>
        const ui = SwaggerUIBundle({
            url: '/openapi.json',
            dom_id: '#swagger-ui',
            presets: [SwaggerUIBundle.presets.apis],
            layout: "BaseLayout"
        });
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

