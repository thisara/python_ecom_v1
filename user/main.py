from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import service

app = FastAPI()

class User(BaseModel):
    user_name: str
    email: str

@app.post("/signup")
def signup_user(user: User): 
    eml = service.validate_user(user.email)
    if user.email == eml:
        raise HTTPException(status_code = 400, detail = "User already exists")
    else:
        service.create_user(user.email,user.user_name)
    
    return {"message" : "Signup successful!"}

@app.get("/validate/{email}")
def validate_user(email: str):
    is_valid_user = False
    eml = service.validate_user(email)
    if eml != None and len(eml) > 0:
        is_valid_user = True

    return is_valid_user

@app.get("/user/{email}")
def validate_user(email: str):
    user = service.get_user(email)
    if user != None:
        return user
    else:
        return "No User Found!"
