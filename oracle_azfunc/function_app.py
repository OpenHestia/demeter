# This file is the logic of an Azure Function for asking the Demeter oracle,
# which is a ChatGPT3.5-Turbo based RAG for gardening information.

# References:
# https://learn.microsoft.com/en-ca/azure/azure-functions/create-first-function-cli-python?tabs=linux%2Cbash%2Cazure-cli%2Cbrowser
from decouple import config
import os
VS_ADDRESS = "https://rag-vector-store.search.windows.net"

import azure.functions as func
import datetime
import json
import logging

# Vector store
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_openai import OpenAIEmbeddings

# LLM
from langchain_openai import ChatOpenAI
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import WikipediaRetriever
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

app = func.FunctionApp()

@app.function_name(name="demeter-oracle")
@app.route(route="ask", auth_level='anonymous', methods=['GET'])
def ask_wrapper(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    question = req.params.get('question')
    if not question:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            question = req_body.get('question')

    if question:
        # Here's where the actual work happens, so of course we're going to pass that off.
        response = send_prompt(question)
        return func.HttpResponse(f"{response}")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a question in the query string or in the request body for a personalized response.",
             status_code=200
        )
    
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def send_prompt(question):
    openai_api_version: str = "2023-05-15"
    model: str = "text-embedding-ada-002"
    embeddings = OpenAIEmbeddings(openai_api_version=openai_api_version, model=model)

    index_name = "rag-vector-store"
    vector_store = AzureSearch(
        azure_search_endpoint=VS_ADDRESS,
        azure_search_key=VS_KEY,
        index_name=index_name,
        embedding_function=embeddings.embed_query,
    )

    gardening_retriever = vector_store.as_retriever(search_type="similarity")
    wikipedia_retreiver = WikipediaRetriever()
    retriever = EnsembleRetriever(retrievers=[gardening_retriever, wikipedia_retreiver], weights=[0.5,0.5])


    llm = ChatOpenAI(model="gpt-3.5-turbo-0125")

    prompt = ChatPromptTemplate([
                ("system", "You are an helpful assistant named Demeter, designed answer questions about gardening. \
                    Use the following pieces of retrieved context to answer the question. \
                    If you don't know the answer, just say that you don't know. \
                    Use three sentences maximum and keep the answer concise. \n"),
                ("human", "Question: {question} \n Context: {context} \n Answer:"),
            ])
    
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser())

    response = rag_chain.invoke(question)
    return response