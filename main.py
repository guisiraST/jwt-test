from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from database.connection import conn
from routes.user_routes import user_router
from routes.model_routes import model_router


app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(user_router, prefix="/user")
app.include_router(model_router, prefix="/model")


@app.on_event("startup")
def on_startup():
    conn()

