from fastapi import FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from app.llm import LLM
from app.models import AnalyseModel, MESSAGE

app = FastAPI()

public_origins = [
    "http://localhost:3000", # Change according to frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=public_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

llm = LLM()

load_dotenv()
DEV_API_KEY = os.getenv("DEV_API_KEY")

@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI backend!"}


# Developer endpoints
@app.get("/ping")
async def ping() -> dict:
    return {"message": "pong"}

@app.post("/classify")
async def classify(api_key: str, email_text: str) -> dict:
    if api_key != DEV_API_KEY:
        return {"error": "Unauthorized access. Invalid API key."}

    is_phishing = llm.classify_email(email_text)
    return is_phishing


@app.post("/analyse")
async def analyse(api_key: str, email_text: str, is_phishing: bool = True) -> dict:
    if api_key != DEV_API_KEY:
        return {"error": "Unauthorized access. Invalid API key."}
    
    # default analysis and message
    analysis_result = {
        "High_Risk": [],
        "Low_Risk": []
    }
    message = MESSAGE[is_phishing]
    
    if is_phishing:
        analysis_result = llm.analyse_email(email_text)
    
    return {
        "message": message,
        "analysis": analysis_result
    }


# End user endpoint
@app.post("/assess")
async def assess(email_text: str) -> dict:
    # classify
    is_phishing = llm.classify_email(email_text)

    message = MESSAGE[is_phishing['is_phishing']]

    if is_phishing:
        # analyze if phishing
        analysis_result = llm.analyse_email(email_text)
    else:
        analysis_result = {
            "High_Risk": [],
            "Low_Risk": []
        }
    
    return {
        "message": message,
        "analysis": analysis_result
    }