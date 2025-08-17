from langchain_core.prompts import ChatPromptTemplate

system_prompt = """You are a professional email scam detector.
Given the user email and definitions below, classify the email as phishing or non-phishing, and generate a JSON output where the key is "is_phishing" and the value is a boolean indicating whether the email is phishing or not.
Do not respond with anything else other than a JSON output.

{classify_response_format}

User Email: {user_email}
JSON Output:"""

classify_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>{system_prompt}<|eot_id|>",
        )
    ]
)
