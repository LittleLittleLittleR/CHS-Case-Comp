from langchain.prompts import PromptTemplate
from models import parser

prompt_template = PromptTemplate(
    template=(
        "You are an AI email analyzer. Analyze the following email and fill in "
        "all the fields in the given JSON schema based on the email content. "
        "If a field cannot be determined, set it to None.\n\n"
        "JSON schema:\n{format_instructions}\n\n"
        "EMAIL:\n{email_text}"
    ),
    input_variables=["email_text"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

# export parser and template
__all__ = ["prompt_template", "parser"]
