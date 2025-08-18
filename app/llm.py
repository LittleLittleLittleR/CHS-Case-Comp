from transformers import pipeline
from langchain_openai import ChatOpenAI
from openai import OpenAI
from dotenv import load_dotenv
import os

from .models import ClassifyResponse, AnalyseResponseList
from .prompt_templates.classify_template import classify_template
from .prompt_templates.analyse_template import analyse_template
from .chain_helper import classify_chain, analyse_chain


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
        self.model = ChatOpenAI(
            openai_api_key=os.getenv("OPEN_AI_API_KEY"),
            model=os.getenv("OPEN_AI_MODEL"),
        )

    def _run_prompt(self, template, email_text):
        prompt = template.format(email_text=email_text)

        response = self.CLIENT.responses.create(
            model=self.MODEL,
            input=prompt,
        )

        return response.output_text

    def classify_email(self, email_text: str) -> ClassifyResponse:
        print("email received in classify: ", email_text)

        chain = classify_chain(self.model)

        model_output = chain.invoke({"user_email": email_text})

        try:
            return ClassifyResponse(**model_output)
        except Exception as e:
            print("Parsing failed:", e)
            print("Raw model output:", model_output)
            raise e

    def analyse_email(self, email_text: str) -> AnalyseResponseList:
        print("email received in analyse: ", email_text)

        chain = analyse_chain(self.model)

        print("chain created")

        model_output = chain.invoke({"phishing_email": email_text})

        try:
            return AnalyseResponseList(**model_output)
        except Exception as e:
            print("Parsing failed:", e)
            print("Raw model output:", model_output)
            raise e
