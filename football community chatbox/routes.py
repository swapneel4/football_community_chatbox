from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie, Body
from user_schema import Message, LoginRequest
from community import message_analysis, display_messages, update_DB
from pymongo import MongoClient
import json
from datetime import datetime, timedelta
import os

router = APIRouter()

# connecting Mongo
client = MongoClient(os.getenv('mongo'))
db = client["football_community_chatbox"]
community_coll = db["community_chat"]
users_collection = db["login"]

# Community Chat 
@router.post("/community")
async def community(response:Response, message_data: Message ):
    
    # Validate the message
    if not message_data.message.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message cannot be empty.",
        )
    sentiment = message_analysis(message_data.message)
    # print(sentiment)
    if sentiment == "negative":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Follow the community guidelines. Negative messages are not allowed."
        )
    # Store Message in MongoDB
    message_entry = {
        "message": message_data.message,
        "timestamp": datetime.utcnow()
    }
    community_coll.insert_one(message_entry)
    return  {"message": message_data.message, "sentiment": sentiment, "success": True}


# Display Community Chat
@router.get("/display_community")
async def  community_load (response:Response):
   
    # Update the Community DB
    update_DB()
    
    # Display messages
    community_dislpay_messages = display_messages()
    return community_dislpay_messages

@router.post("/login")
def login_user(data: LoginRequest):
    user = users_collection.find_one({
        "username": data.username,
        "password": data.password  # 👈 Raw password match (no hashing)
    })
    if user:
        return {"message": "Login successful", "username": data.username}
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")

