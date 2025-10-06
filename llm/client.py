"""Módulo para interagir com a API do modelo de linguagem (LLM)."""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

load_dotenv()


def generate_report_from_llm(template: str, route_data: str) -> str:
    """
    Configura e executa um prompt no modelo Gemini para gerar um relatório.
    """
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)
        prompt = PromptTemplate(input_variables=["route_data_text"], template=template)
        llm_chain = LLMChain(llm=llm, prompt=prompt)
        result = llm_chain.invoke({"route_data_text": route_data})
        return result["text"]
    except Exception as e:
        print(f"Erro ao contatar a API do LLM: {e}")
        return f"<html><body><h1>Erro</h1><p>Não foi possível gerar o relatório: {e}</p></body></html>"
