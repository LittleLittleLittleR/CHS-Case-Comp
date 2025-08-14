from fastapi import FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from app.llm import LLM

app = FastAPI()
llm = LLM()
load_dotenv()
DEV_API_KEY = os.getenv("DEV_API_KEY")

public_origins = [
    "http://localhost:3000", # Change according to frontend URL
]

# Apply CORS for the whole app
app.add_middleware(
    CORSMiddleware,
    allow_origins=public_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI backend!"}


# Developer endpoints
@app.get("/ping")
async def ping():
    return {"message": "pong"}

@app.post("/classify")
async def classify(api_key: str, email_text: str):
    if api_key != DEV_API_KEY:
        return {"error": "Unauthorized access. Invalid API key."}

    # Call the LLM to classify the email
    class_result = llm.classify_email(email_text)
    return class_result

@app.post("/analyse")
async def analyse(api_key: str, email_text: str, class_result: bool = True):
    if api_key != DEV_API_KEY:
        return {"error": "Unauthorized access. Invalid API key."}

    # Call the LLM to analyze the email
    analysis_result = llm.analyse_email(email_text, class_result)
    return analysis_result


# End user endpoint
@app.post("/assess")
async def assess(api_key: str, email_text: str):

    class_result = llm.classify_email(email_text)
    analysis_result = llm.analyse_email(email_text, class_result.Phishing)

    return {
        "classification": class_result,
        "analysis": analysis_result
    }