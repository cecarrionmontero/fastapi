from fastapi import APIRouter, Body, Depends
from pydantic import BaseModel, create_model
from exec.call_sp import call_stored_procedure, get_all_procedures_and_params
from logger.logging_config import logger
from auth.dependencies import verify_token  # 🔐 Protección JWT

router = APIRouter(
    prefix="/api",
    dependencies=[Depends(verify_token)]
)

logger.info("🟡 Generando endpoints dinámicos desde stored procedures...")

def build_endpoint(sp_name, param_list):
    # Crear campos del modelo
    fields = {
        param: (str, ...) for param in param_list
    }

    # Crear modelo dinámico
    PayloadModel = create_model(f"{sp_name}_Payload", **fields)

    # Agregar ejemplo (solo para docs, no rompe en tiempo de ejecución)
    PayloadModel.model_config = {
        "json_schema_extra": {
            "example": {param: f"valor_{i+1}" for i, param in enumerate(param_list)}
        }
    }

    async def endpoint(payload: PayloadModel = Body(...)):
        result = call_stored_procedure(sp_name, payload.model_dump(), param_list)
        return {"data": result}

    return endpoint

# Crear endpoints dinámicos
for sp_name, param_list in get_all_procedures_and_params().items():
    logger.info(f"✅ Endpoint creado: POST /{sp_name}  |  Parámetros: {param_list}")
    router.add_api_route(
        path=f"/{sp_name}",
        endpoint=build_endpoint(sp_name, param_list),
        methods=["POST"],
        name=sp_name
    )

