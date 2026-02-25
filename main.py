from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from fastapi.responses import RedirectResponse
from auth import authenticate_user, create_access_token, get_role_from_token
from database import get_db
from rag import rag_pipeline
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles


app = FastAPI()
security = HTTPBearer(auto_error=False)


app.mount("/static", StaticFiles(directory="templates"), name="static")

@app.get("/")
def root():
    return RedirectResponse(url="/static/input.html")


def get_current_role(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials is None:
        return "public" 
    token = credentials.credentials
    return get_role_from_token(token)

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(request: LoginRequest, db=Depends(get_db)):
    user = authenticate_user(db, request.username, request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(user)
    return {"access_token": token}

class QueryRequest(BaseModel):
    query: str
    chat_history: list[dict] = []

@app.post("/")
def ask_question(request: QueryRequest, role: str = Depends(get_current_role)):
    response = rag_pipeline(request.query, role, request.chat_history)
    return {
        "response": response
    }