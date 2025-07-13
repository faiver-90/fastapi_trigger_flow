# # dependencies/auth.py
# from fastapi import Depends, HTTPException, status, Request
#
#
# async def validate_token(request: Request):
#     auth_header = request.headers.get("Authorization")
#     if not auth_header or not auth_header.startswith("Bearer "):
#         raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
#
#     token = auth_header.split(" ")[1]
#
#     if not await redis_auth.token_exists(token):
#         raise HTTPException(status_code=401, detail="Invalid or expired token")
#
#     return token  # можно вернуть token или user_id, если он есть в Redis
