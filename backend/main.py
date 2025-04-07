from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.middleware.cors import CORSMiddleware
from secret_api.router import router as secret


headers = {
    "Cache-Control": "no-cache, no-store, must-revalidate",
    "Pragma": "no-cache",
    "Expires": "0",
}

class HeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        for header_name, header_value in headers.items():
            response.headers[header_name] = header_value
        return response

app = FastAPI()


origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(secret)
# app.include_router(pages)
app.add_middleware(HeadersMiddleware)



# app.mount("/static", StaticFiles(directory="./frontend/static/"), name="static")

