from typing import Optional
from pydantic import BaseModel
from langchain.output_parsers import PydanticOutputParser


class ClassifyModel(BaseModel):
    is_phishing: bool


class AnalyseModel(BaseModel):
    High_Risk: list[str]
    Low_Risk: list[str]


CLASSIFY_PARSER = PydanticOutputParser(pydantic_object=ClassifyModel)
ANALYSE_PARSER = PydanticOutputParser(pydantic_object=AnalyseModel)

MESSAGE = {
    False: "The email seems safe. But double-check before taking any action.",
    True: "The email is likely a phishing attempt. Please review the analysis below for details.",
}
