from typing import Optional
from pydantic import BaseModel
from langchain.output_parsers import PydanticOutputParser

class AnalyseModel(BaseModel):
    High_Risk: list[str]
    Low_Risk: list[str]

PARSER = PydanticOutputParser(pydantic_object=AnalyseModel)

MESSAGE = {
    True: "The email seems safe. But double-check before taking any action.",
    False: "The email is likely a phishing attempt. Please review the analysis below for details."
}
