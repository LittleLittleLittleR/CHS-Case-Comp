from typing import Optional
from pydantic import BaseModel
from langchain.output_parsers import PydanticOutputParser

class EmailAnalysis(BaseModel):
    Sender: Optional[str]
    Receiver: Optional[str]
    Subject: Optional[str]
    Content: str
    Phishing: bool
    Reason_1: Optional[str] = None
    Risk_level_1: Optional[str] = None
    Reason_2: Optional[str] = None
    Risk_level_2: Optional[str] = None
    Reason_3: Optional[str] = None
    Risk_level_3: Optional[str] = None
    

parser = PydanticOutputParser(pydantic_object=EmailAnalysis)