# This file is the logic of an Azure Function for asking the Demeter oracle,
# which is a ChatGPT3.5-Turbo based RAG for gardening information.

# References:
# https://learn.microsoft.com/en-ca/azure/azure-functions/create-first-function-cli-python?tabs=linux%2Cbash%2Cazure-cli%2Cbrowser

import azure.functions as func
import datetime
import json
import logging

app = func.FunctionApp()

@app.route(route="ask", auth_level='anonymous', methods=['POST'])
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
        return func.HttpResponse(f"{question}")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
    

def send_prompt(question):
    response = ""
    
    return response