from fastapi import FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from app import rayyantest
from app.llm import LLM
from app.models import AnalyseResponseList, MESSAGE

app = FastAPI()

public_origins = [
    "http://localhost:3000",
    "https://mail.google.com",  # Change according to frontend URL
    "http://localhost:5173",
    "chrome-extension://bhjpopgmefpcchjflgipbonlalkfichp",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
async def classify(req: Request) -> dict:
    print("received classify request!")
    data = await req.json()
    api_key = data.get("api_key")
    email_text = data.get("email_text")

    if api_key != DEV_API_KEY:
        return {"error": "Unauthorized access. Invalid API key."}

    print('received')

    is_phishing = llm.classify_email(email_text)  # TODO: Check if return type matches for frontend

    print("from endpoint: ", is_phishing)

    if hasattr(is_phishing, "model_dump"):  
        return is_phishing.model_dump()
    return is_phishing

# Testing endpoint
@app.post("/post-ping")
async def postping(req: Request) -> dict:
    data = await req.json()
    return data


@app.post("/analyse")
async def analyse(req: Request) -> dict:
    data = await req.json()
    api_key = data.get("api_key")
    email_text = data.get("email_text")
    is_phishing = data.get("is_phishing")

    if api_key != DEV_API_KEY:
        return {"error": "Unauthorized access. Invalid API key."}

    # default analysis and message
    analysis_result = AnalyseResponseList(analysis=[])
    message = MESSAGE[is_phishing]

    if is_phishing:
        analysis_result = llm.analyse_email(email_text)  # TODO: Check if return type matches for frontend

    return {
        "message": message, 
        "analysis": analysis_result.model_dump()["analysis"]
    }

# End user endpoint
@app.post("/assess")
async def assess(req: Request) -> dict:
    data = await req.json()
    email_text = data.get("email_text")
    # print("[FASTAPI]: Received Access Request", email_text.strip().replace("\n", " "))
    # classify
    is_phishing = llm.classify_email(email_text)
    print("is_phishing: ", is_phishing)

    if hasattr(is_phishing, "model_dump"):  
        response = is_phishing.model_dump()["is_phishing"]
    else:
        response = is_phishing["is_phishing"]

    message = MESSAGE[response]

    if response:
        # analyze if phishing
        analysis_result = llm.analyse_email(email_text)
    else:
        analysis_result = AnalyseResponseList(analysis=[])

    print("from endpoint: ", analysis_result)

    return {
        "message": message, 
        "analysis": [anal.model_dump() for anal in analysis_result.model_dump()["analysis"]]
    }


@app.post("/rayyanapi")
async def rayyanapi(req: Request) -> dict:
    print("received rayyanapi request!")
    data = await req.json()
    email_text = data.get("email_text")
    res = await rayyantest.callAgent(email_text.replace("\n", " ").strip())
    return {"message": res}
