# tests/conftest.py
import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from uuid import uuid4
import os
import sys

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from src.database.connection import get_db
from src.api.routes.employee_routes import router as employee_router
from src.api.routes.order_routes import router as order_router

# Test database setup
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def app() -> FastAPI:
    app = FastAPI()
    app.include_router(employee_router, prefix="/api/v1")
    app.include_router(order_router, prefix="/api/v1")
    return app

@pytest.fixture(scope="module")
async def async_client(app: FastAPI) -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client