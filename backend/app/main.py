"""FastAPI application entrypoint."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers import analise, auth, catalogo, execucao, health, obras, orcamentos, rateio, vendas

app = FastAPI(
    title="Construtor Total API",
    version="0.1.0",
    description="Gestão de obra e custos para construção civil no Brasil.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(obras.router)
app.include_router(catalogo.router)
app.include_router(orcamentos.router)
app.include_router(execucao.router)
app.include_router(rateio.router)
app.include_router(analise.router)
app.include_router(vendas.router)


@app.get("/")
def root() -> dict[str, str]:
    return {"app": "Construtor Total", "version": app.version}
