from langchain.prompts import PromptTemplate
from models import parser

prompt_template = PromptTemplate(
    template=(
        """
You are an intellegent and meticulous AI email analyzer. 
Your task is to 
1. analyze the following email to determine if it is a phishing or benign. 
2. List out the reasons for your decision and assign a risk level to each reason.

The output should be a JSON object that matches the following schema:
```json
{{
    "Sender": string,
    "Receiver": string,
    "Subject": string,
    "Content": string,
    "Phishing": bool,
    "Reason_1": string | None,
    "Risk_level_1": string | None,
    "Reason_2": string | None,
    "Risk_level_2": string | None,
    "Reason_3": string | None,
    "Risk_level_3": string | None,
}}
```
JSON schema:\n{format_instructions}\n\n
EMAIL:\n{email_text}
"""
        
    ),
    input_variables=["email_text"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

# export parser and template
__all__ = ["prompt_template", "parser"]
