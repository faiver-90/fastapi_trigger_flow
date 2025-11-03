from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="FastAPI on Kind 8080", version="0.1.0",
              root_path="/service-2"
              )

class Echo(BaseModel):
    message: str

@app.get("/")
def root():
    return {"status": "ok", "app": "fastapi-kind", "version": "0.1.0"}

@app.get("/health")
def health():
    return {"healthy": True}

@app.post("/echo")
def echo(payload: Echo):
    return {"echo": f"{payload.message}"}
#
# from sqlalchemy.ext.asyncio import create_async_engine
#
# DATABASE_URL = "postgresql+asyncpg://appuser:apppass@postgres:5432/appdb"
# engine = create_async_engine(DATABASE_URL, echo=True)
