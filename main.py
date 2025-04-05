from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

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
app.include_router(secret)
app.add_middleware(HeadersMiddleware)
