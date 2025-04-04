from fastapi import FastAPI

from secret_api.router import router as secret

app = FastAPI()
app.include_router(secret)