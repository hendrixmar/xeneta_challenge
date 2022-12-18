from fastapi import FastAPI
import uvicorn
from app.rates.router import router as rate_router
from app.ports.router import router as port_router

app = FastAPI()
app.include_router(rate_router)
app.include_router(port_router)
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
