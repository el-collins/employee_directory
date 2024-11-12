from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from src.api.routes import employee_routes, order_routes
from src.database.connection import init_db

app = FastAPI(title="Employee Directory API")

@app.on_event("startup")
async def startup():
    await init_db()

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")




app.include_router(employee_routes.router, prefix="/api/v1", tags=["employees"])
app.include_router(order_routes.router, prefix="/api/v1", tags=["orders"])