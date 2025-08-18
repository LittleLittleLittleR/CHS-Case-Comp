from typing import Optional
from pydantic import BaseModel, Field


class ClassifyResponse(BaseModel):
    is_phishing: bool = Field(
        description="True if the email is phishing, False if it is not."
    )


class AnalyseResponse(BaseModel):
    html: str = Field(
        description="A word for word quote with the HTML tags from the email that supports the phishing classification."
    )
    reason: str = Field(
        description="A brief reason explaining why the HTML quote supports the phishing classification."
    )
    risk: str = Field(
        description="The overall risk level of the email (e.g., 'High', 'Low')."
    )

class AnalyseResponseList(BaseModel):
    analysis: list[AnalyseResponse]

MESSAGE = {
    False: "The email seems safe. But double-check before taking any action.",
    True: "The email is likely a phishing attempt. Please review the analysis below for details.",
}
