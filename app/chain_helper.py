from langchain_core.output_parsers import JsonOutputParser
from .models import ClassifyResponse, AnalyseResponseList

from .prompt_templates import (
    classify_template,
    analyse_template,
)

def classify_chain(llm):   
    json_parser = JsonOutputParser(pydantic_object=ClassifyResponse)

    prompt = classify_template.classify_template.partial(
        classify_response_format=json_parser.get_format_instructions()
    )

    chain = prompt | llm | json_parser

    return chain

def analyse_chain(llm):
    json_parser = JsonOutputParser(pydantic_object=AnalyseResponseList)

    prompt = analyse_template.analyse_template.partial(
        analyse_response_format=json_parser.get_format_instructions()
    )

    chain = prompt | llm | json_parser

    return chain