from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from app.core.config import SECRET_KEY, ALGORITHM
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id = payload.get("sub")
        role = payload.get("role")
        email = payload.get("email")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return {
            "user_id": user_id,
            "role": role,
            "email": email
        }

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# def get_current_user(token: str = Depends(oauth2_scheme)):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

#         user_id = payload.get("sub")
#         role = payload.get("role")
#         email = payload.get("email")

#         if user_id is None:
#             raise HTTPException(status_code=401, detail="Invalid token")

#         return {
#             "user_id": user_id,
#             "role": role,
#             "email": email
#         }

#     except JWTError:
#         raise HTTPException(status_code=401, detail="Invalid token")


def admin_required(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only admin can create rooms"
        )
    return current_user