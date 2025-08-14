from langchain.prompts import PromptTemplate

from .models import PARSER

classify_template = PromptTemplate(
    template=(
        """
You are an intellegent and meticulous AI phishing detector. 
Your task is to analyze the following email to determine if it is a phishing email or not.
The output should be a JSON object that matches the following schema:

{
    "is_phishing": True/False  # capitalized boolean
}

JSON schema:\n{format_instructions}\n\n
EMAIL:\n{email_text}
"""
    ),
    input_variables=["email_text"]
)

analyse_template = PromptTemplate(
    template=(
        """
You are an intelligent and meticulous AI phishing email analyzer. 
Your task is to analyze the following phishing email and provide a detailed analysis as to why is it a phishing email.
You should provide the reasons and risk levels for each reason.
The output should be a JSON object that matches the following schema:

{
    "High_Risk": [
        "Reason_1",
        "Reason_2",
        "Reason_3"
    ],
    "Low_Risk": [
        "Reason_1",
        "Reason_2",
        "Reason_3"
    ],
}


Here is are 2 examples of the output:

{
    "High_Risk": [
        "The email contains a suspicious link that leads to a phishing site.",
        "The sender's email address is not recognized and appears to be from a free email service.",
    ],
    "Low_Risk": [
        "The email contains grammatical errors and awkward phrasing."
    ]
}

{
    "High_Risk": [
        "The sender claims to be from a legitimate organization but the email address does not match the official domain.",

    ],
    "Low_Risk": [
        "The email has a generic greeting and does not address the recipient by name.",
        "The email contains a sense of urgency, pressuring the recipient to act quickly.",
    ]
}

"""),
    input_variables=["email_text"],
    partial_variables={"format_instructions": PARSER.get_format_instructions()}
)

__all__ = ["classify_template", "analyse_template"]
