from pydantic import BaseModel

# Schema for the community messages
class Message(BaseModel):
    message: str
    
# Login request model
class LoginRequest(BaseModel):
    username: str
    password: str