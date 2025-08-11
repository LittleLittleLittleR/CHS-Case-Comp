from langchain.prompts import PromptTemplate
from transformers import pipeline

from models import EmailAnalysis, parser
from prompt_template import prompt_template


# example email input
email_text = """
From: attacker@example.com
To: victim@example.com
Subject: Urgent account verification required!
Hello, your account will be suspended unless you verify it now: http://fake-link.com
"""


prompt = prompt_template.format(email_text=email_text)

# load model
pipe = pipeline(
    model="microsoft/Phi-4-mini-instruct", 
    task="text-generation",
)

# run model
raw_output = pipe(prompt, max_new_tokens=500, temperature=0)[0]["generated_text"]

# parse JSON output
try:
    parsed = parser.parse(raw_output)
    print(parsed.model_dump())  # Benchmark-ready structured output
except Exception as e:
    print("Parsing failed:", e)
    print("Raw model output:", raw_output)
