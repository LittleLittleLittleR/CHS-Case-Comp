from langchain.prompts import PromptTemplate
from transformers import pipeline
from openai import OpenAI
from dotenv import load_dotenv
import os

from .models import CLASSIFY_PARSER, ANALYSE_PARSER
from .prompts import classify_template, analyse_template


# example email input
email_text = """
From: attacker@example.com
To: victim@example.com
Subject: Urgent account verification required!
Hello, your account will be suspended unless you verify it now: http://fake-link.com
"""

load_dotenv()


class LLM:

    def __init__(self):
        self.CLIENT = OpenAI(api_key=os.getenv("OPEN_AI_API_KEY"))
        self.MODEL = os.getenv("OPEN_AI_MODEL")


    def _run_prompt(self, template, email_text):
        prompt = template.format(email_text=email_text)

        response = self.CLIENT.responses.create(
            model=self.MODEL,
            input=prompt,
        )

        return response.output_text


    def classify_email(self, email_text: str) -> dict:
        print("email received: ", email_text)
        
        model_output = self._run_prompt(classify_template, email_text)

        try:
            parsed = CLASSIFY_PARSER.parse(model_output)
            return parsed.model_dump()
        except Exception as e:
            print("Parsing failed:", e)
            print("Raw model output:", model_output)
            raise e


    def analyse_email(self, email_text: str) -> dict:
        model_output = self._run_prompt(analyse_template, email_text)

        try:
            parsed = ANALYSE_PARSER.parse(model_output)
            return parsed.model_dump()
        except Exception as e:
            print("Parsing failed:", e)
            print("Raw model output:", model_output)
            raise e
