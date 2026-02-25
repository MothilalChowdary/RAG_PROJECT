from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from fastapi.responses import RedirectResponse
from auth import authenticate_user, create_access_token, get_role_from_token
from database import get_db
from rag import rag_pipeline
from fastapi.staticfiles import StaticFiles


app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login", auto_error=False)


app.mount("/static", StaticFiles(directory="templates"), name="static")

@app.get("/")
def root():
    return RedirectResponse(url="/static/input.html")


def get_current_role(token: str = Depends(oauth2_scheme)):
    if not token:
        return "public" 
    return get_role_from_token(token)


@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(user)
    return {"access_token": token, "token_type": "bearer"}

class QueryRequest(BaseModel):
    query: str
    chat_history: list[dict] = []

@app.post("/")
def ask_question(request: QueryRequest, role: str = Depends(get_current_role)):
    response = rag_pipeline(request.query, role, request.chat_history)
    return {
        "response": response
    }