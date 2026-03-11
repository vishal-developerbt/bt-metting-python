from fastapi import APIRouter, Request
import httpx

router = APIRouter()

USER_SERVICE = "http://127.0.0.1:8001"
ROOM_SERVICE = "http://127.0.0.1:8002"
BOOKING_SERVICE = "http://127.0.0.1:8003"
NOTIFICATION_SERVICE = "http://127.0.0.1:8004"


@router.api_route("/users/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def user_proxy(path: str, request: Request):
    async with httpx.AsyncClient() as client:
        response = await client.request(
            request.method,
            f"{USER_SERVICE}/users/{path}",
            headers=request.headers.raw,
            content=await request.body(),
        )
    return response.json()


@router.api_route("/rooms/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def room_proxy(path: str, request: Request):
    async with httpx.AsyncClient() as client:
        response = await client.request(
            request.method,
            f"{ROOM_SERVICE}/rooms/{path}",
            headers=request.headers.raw,
            content=await request.body(),
        )
    return response.json()

@router.api_route("/bookings/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def booking_proxy(path: str, request: Request):
    async with httpx.AsyncClient() as client:
        response = await client.request(
            request.method,
            f"{BOOKING_SERVICE}/bookings/{path}",
            headers=request.headers.raw,
            content=await request.body(),
        )
    return response.json()

@router.api_route("/notifications/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def notification_proxy(path: str, request: Request):
    async with httpx.AsyncClient() as client:
        response = await client.request(
            request.method,
            f"{NOTIFICATION_SERVICE}/notifications/{path}",
            headers=request.headers.raw,
            content=await request.body(),
        )
    return response.json()

@router.get("/health")
async def health():
    return {"status": "API Gateway Running"}