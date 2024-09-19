from fastapi import APIRouter, HTTPException, Request, Depends
from auth.authenticate import authenticate

model_router = APIRouter(tags=["model"], dependencies=[Depends(authenticate)])

@model_router.post("/chat_qa")
async def chatbot_qa(user_query):
    return user_query