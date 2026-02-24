from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.interface.product_routes import router as product_router
from src.interface.shared_lists_routes import router as shared_lists_router
from src.interface.websocket_routes import router as websocket_router

app = FastAPI(
    title="Backend Lista de productos",
    description="Backend de una lista de productos compartida",
    version="0.0.1"
)

origins = [
    "http://localhost:8000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

app.include_router(product_router)
app.include_router(shared_lists_router)
app.include_router(websocket_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}