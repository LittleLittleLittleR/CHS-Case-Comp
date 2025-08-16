from dotenv import load_dotenv
from openai import OpenAI
import json
import os
import openai
from pydantic import BaseModel

load_dotenv()


class ClassifyResponse(BaseModel):
    is_phishing: bool
    reasoning: str


class AnalysisResponse(BaseModel):
    high_risk: list[str]
    low_risk: list[str]


client = OpenAI(api_key=os.getenv("OPEN_AI_API_KEY"))

tools = [
    {
        "type": "function",
        "name": "identify_phishing",
        "description": "Check if email is a phishing email",
        "parameters": {
            "type": "object",
            "properties": {
                "is_phishing": {
                    "type": "boolean",
                    "description": "True if phishing, False if not phishing",
                    "enum": [True, False],
                },
                "reasoning": {
                    "type": "string",
                    "description": "Detailed reasoning of why you think it is phishing or a scam or why it is not **if false**",
                },
            },
            "required": ["is_phishing", "reasoning"],
            "additionalProperties": False,
        },
    },
    {
        "type": "function",
        "name": "phishing_analysis",
        "description": "Provide detailed analysis of phishing email with high and low risk reasons",
        "parameters": {
            "type": "object",
            "properties": {
                "high_risk": {"type": "array", "items": {"type": "string"}},
                "low_risk": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["high_risk", "low_risk"],
        },
    },
]


async def callAgent(emailText):
    print("received function call!")
    prompt = f"""You are an intellegent and meticulous AI scam analyst that can detect Phishing or imitation scams from text messages. 
    You are to always determine if the given text is phishing or scam first before any other calls
 Determine if the following email is phishing. Return JSON: {{"is_phishing": true/false}}. If you are unsure, mark as false.
EMAIL: 
{emailText}
"""

    prompt2 = f"""You are an intellegent and meticulous AI scam analyst that can detect Phishing or imitation scams from text messages and the email has been identified as phishing! You are to provide detailed analysis with High_Risk and Low_Risk reasons in JSON:
{{
  "High_Risk": ["Reason 1", "Reason 2"],
  "Low_Risk": ["Reason 1", "Reason 2"]
}}
EMAIL:
{emailText}
"""

    input_list = [
        {"role": "system", "content": prompt},
    ]
    response = client.responses.parse(
        model="gpt-4o-mini", tools=tools, input=input_list, tool_choice="auto", text_format=ClassifyResponse  # type: ignore
    )
    # for item in response.output:
    #     if item.type == "function_call":
    #         print("Tool call: ", item)
    #         print(item.arguments)
    #
    print("response from first: ", response.output_parsed)
    print("Full Response from First: ", response.output)
    first_response = response.output_parsed

    if first_response and first_response.is_phishing:  # need to do analysis
        print("\n\nStarting Analysis on Email...\n\n")
        analysis_input_list = [{"role": "system", "content": prompt2}]
        analysis_response = client.responses.parse(
            model="gpt-4o-mini",
            tools=tools,  # type: ignore
            input=analysis_input_list,  # type: ignore
            text_format=AnalysisResponse,  # type: ignore
            tool_choice="auto",
        )

        print("\n\nAnalysis Full Response: ", analysis_response, "\n\n")

        print("Analysis Response: ", analysis_response.output_parsed)

    return {"status": 200}  # type: ignore
