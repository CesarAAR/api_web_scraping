from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import courses as courses_router
from api.routers import health as health_router
import uvicorn

app = FastAPI(
    title="API Courses Scrapping",
    description="API Prueba",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)

app.include_router(courses_router.router, prefix="/api/v1")
app.include_router(health_router.router, prefix="/api/v1")


if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=8000)