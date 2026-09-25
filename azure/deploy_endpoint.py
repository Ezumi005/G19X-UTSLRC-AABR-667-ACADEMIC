"""Despliegue del endpoint de inferencia mediante el SDK de Azure ML.

Idempotente: registra el modelo y el entorno en el workspace si no existen,
crea el endpoint, el deployment 'blue' y le asigna el 100% del trafico.

Variables de entorno opcionales:
    AZ_RG (default: rg-motor-segmentacion)
    AZ_WS (default: ml-motor-segmentacion)
    AZ_EP (default: motor-seg-ep2)

Uso (desde la raiz del proyecto):
    .venv/Scripts/python.exe azure/deploy_endpoint.py
"""

import os
from pathlib import Path

from azure.ai.ml import MLClient
from azure.ai.ml.entities import (
    CodeConfiguration,
    Environment,
    ManagedOnlineDeployment,
    ManagedOnlineEndpoint,
    Model,
)
from azure.core.exceptions import ResourceNotFoundError
from azure.identity import AzureCliCredential

SUBSCRIPTION = "5144ab2b-f2ca-40f7-be86-ea6423133a5e"
RESOURCE_GROUP = os.environ.get("AZ_RG", "rg-motor-segmentacion")
WORKSPACE = os.environ.get("AZ_WS", "ml-motor-segmentacion")
ENDPOINT_NAME = os.environ.get("AZ_EP", "motor-seg-ep2")

AZURE_DIR = Path(__file__).resolve().parent
ROOT = AZURE_DIR.parent

ml_client = MLClient(AzureCliCredential(), SUBSCRIPTION, RESOURCE_GROUP, WORKSPACE)


def _set_traffic_via_arm(ml_client: MLClient, endpoint_name: str) -> None:
    """Asigna trafico consultando primero el endpoint real (conserva su identidad)."""
    ep = ml_client.online_endpoints.get(endpoint_name)
    ep.traffic = {"blue": 100}
    ml_client.online_endpoints.begin_create_or_update(ep).result()
print(f"workspace: {WORKSPACE} [{RESOURCE_GROUP}] | endpoint: {ENDPOINT_NAME}")

try:
    ml_client.models.get(name="kmeans-local", version="1")
    print("modelo kmeans-local:1 ya registrado")
except ResourceNotFoundError:
    ml_client.models.create_or_update(
        Model(name="kmeans-local", version="1", path=str(ROOT / "models" / "kmeans_local.pkl"))
    )
    print("modelo kmeans-local:1 registrado")

try:
    ml_client.environments.get(name="motor-segmentacion-env", version="1")
    print("entorno motor-segmentacion-env:1 ya registrado")
except ResourceNotFoundError:
    ml_client.environments.create_or_update(
        Environment(
            name="motor-segmentacion-env",
            version="1",
            image="mcr.microsoft.com/azureml/openmpi4.1.0-ubuntu22.04",
            conda_file=str(AZURE_DIR / "conda_env.yml"),
        )
    )
    print("entorno motor-segmentacion-env:1 registrado")

if not os.environ.get("AZ_SKIP_ENDPOINT"):
    endpoint = ManagedOnlineEndpoint(
        name=ENDPOINT_NAME,
        auth_mode="key",
        description="Motor de segmentacion de clientes: K-Means k=6 (MVP)",
        identity={"type": "SystemAssigned"},
    )
    result = ml_client.online_endpoints.begin_create_or_update(endpoint).result()
    print(f"endpoint: {result.name} [{result.provisioning_state}]")
else:
    print("endpoint: se asume ya creado (AZ_SKIP_ENDPOINT=1)")

deployment = ManagedOnlineDeployment(
    name="blue",
    endpoint_name=ENDPOINT_NAME,
    model="kmeans-local:1",
    environment="motor-segmentacion-env:1",
    code_configuration=CodeConfiguration(code=str(AZURE_DIR), scoring_script="score.py"),
    instance_type="Standard_DS2_v2",
    instance_count=1,
)
result = ml_client.online_deployments.begin_create_or_update(deployment).result()
print(f"deployment: {result.name} [{result.provisioning_state}]")

endpoint.traffic = {"blue": 100}
ml_client.online_endpoints.begin_create_or_update(endpoint).result() if not os.environ.get(
    "AZ_SKIP_ENDPOINT"
) else _set_traffic_via_arm(ml_client, ENDPOINT_NAME)
print("trafico asignado: blue 100%")
