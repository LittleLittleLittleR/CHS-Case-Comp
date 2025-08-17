from langchain_core.prompts import ChatPromptTemplate

system_prompt = """"You are an intelligent and meticulous AI phishing email analyzer. 
Given the following phishing email and description, analyze the phishing email and provide a detailed analysis as to why is it a phishing email.
You should provide the reasons under the correct risk levels.

{analyse_response_format}


Here is are 2 examples of the output:

{{
    "High_Risk": [
        "The email contains a suspicious link that leads to a phishing site.",
        "The sender's email address is not recognized and appears to be from a free email service.",
    ],
    "Low_Risk": [
        "The email contains grammatical errors and awkward phrasing."
    ]
}}

{{
    "High_Risk": [
        "The sender claims to be from a legitimate organization but the email address does not match the official domain.",

    ],
    "Low_Risk": [
        "The email has a generic greeting and does not address the recipient by name.",
        "The email contains a sense of urgency, pressuring the recipient to act quickly.",
    ]
}}

Phishing Email: {phishing_email}

"""

analyse_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>{system_prompt}<|eot_id|>",
        )
    ]
)
