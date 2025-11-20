from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

# User model
class User(BaseModel):
    name: str
    pin_number: str
    bank_balance: float = 0.0

# Request models
class AuthRequest(BaseModel):
    name: str
    pin_number: str

class DepositRequest(BaseModel):
    name: str
    amount: float

class TransferRequest(BaseModel):
    sender_name: str
    sender_pin: str
    recipient_name: str
    amount: float

# In-memory user storage
# For simplicity, using a dictionary where key is the name
users: Dict[str, User] = {
    "mohsin": User(name="mohsin", pin_number="1234", bank_balance=3000.0),
    "rubina": User(name="rubina", pin_number="1111", bank_balance=5000.0),
    "rashida": User(name="rashida", pin_number="3333", bank_balance=7000.0)
}

@app.get("/")
async def read_root():
    return {"message": "Bank Api running"}

@app.post("/authenticate")
async def authenticate_user(request: AuthRequest):
    user = users.get(request.name)
    if not user or user.pin_number != request.pin_number:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"error": "invalid credentials"})
    return {"user_name": user.name, "bank_balance": user.bank_balance}

@app.post("/deposit")
async def deposit_funds(request: DepositRequest):
    user = users.get(request.name)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if request.amount <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Deposit amount must be positive")
    
    user.bank_balance += request.amount
    return {"bank_balance": user.bank_balance}

@app.post("/bank-transfer")
async def bank_transfer(request: TransferRequest):
    sender = users.get(request.sender_name)
    recipient = users.get(request.recipient_name)

    if not sender:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Sender '{request.sender_name}' not found")
    if not recipient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Recipient '{request.recipient_name}' not found")
    if sender.pin_number != request.sender_pin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid PIN for sender")
    if request.amount <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Transfer amount must be positive")
    if sender.bank_balance < request.amount:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient balance")
    
    sender.bank_balance -= request.amount
    recipient.bank_balance += request.amount

    return {
        "message": "Transfer successful",
        "sender_updated_balance": sender.bank_balance,
        "recipient_updated_balance": recipient.bank_balance
    }
