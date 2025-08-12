from langchain.prompts import PromptTemplate
from transformers import pipeline
from openai import OpenAI
import dotenv
import os

from models import EmailAnalysis, parser
from prompt_template import prompt_template


# example email input
email_text = """
From: attacker@example.com
To: victim@example.com
Subject: Urgent account verification required!
Hello, your account will be suspended unless you verify it now: http://fake-link.com
"""

os.load_dotenv()

prompt = prompt_template.format(email_text=email_text)

# load model
client = OpenAI(
    api_key=os.getenv("OPEN_AI_API_KEY"),
)

response = client.responses.create(
  model="gpt-4o-mini",
  input=prompt,
)
model_output = response.output_text

# parse JSON output
try:
    parsed = parser.parse(response)
    print(parsed.model_dump())
except Exception as e:
    print("Parsing failed:", e)
    print("Raw model output:", response)
