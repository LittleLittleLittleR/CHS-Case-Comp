from typing import Optional
from pydantic import BaseModel, Field


class ClassifyResponse(BaseModel):
    is_phishing: bool = Field(
        description="True if the email is phishing, False if it is not."
    )


class AnalyseResponse(BaseModel):
    High_Risk: list[str] = Field(
        description="List of high-risk reasons for classifying the email as phishing."
    )
    Low_Risk: list[str] = Field(
        description="List of low-risk reasons for classifying the email as phishing."
    )

MESSAGE = {
    False: "The email seems safe. But double-check before taking any action.",
    True: "The email is likely a phishing attempt. Please review the analysis below for details.",
}
