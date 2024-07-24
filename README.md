# demeter
![image](https://github.com/user-attachments/assets/02965126-358c-48e6-a55e-4faa7677172e)


Demeter is an LLM Retreival Augmented Generation system using ReACT to provide gardening advice. 

## Design
Demeter is a ChatGPT3.5-Turbo-based assistant focused on providing gardening advice. The core idea behind Demeter is that we use a few pieces of information gathered from the system (geolocation of user, local weather), gathered from the user (plants present in garden, question), and gathered from the internet at large (plant information, gardening advice, etc) to provide up-to-date and contextually intelligent advice on plant care. Modes of input and output such as speech for user input (just nice, not impactful on functionality), use of camera images as input (very helpful, but a bit more prone to hallucination and confusion), and output from demeter like notifications (could be nice) and schematics (also nice, just unclear on usefulness).

## Architecture
- Using Azure Functions, I'm going to build a HTTP API for a ChatGPT 3.5 based RAG app, the core demeter oracle. 
- We'll need a vector store for the indexed data.
- We also need some storage for user-specific context, history, and data.
- We'll need a web app wrapping the application.
- If I want to use LLava or another VLM to do image-based generation, we'll need some hosting for that as well. 

## Organization
- oracle_dev: This folder contains on-device prototyping files for the Demeter Oracle (the RAG)
- oracle_azfunc: Azure function servince the Demeter Oracle.