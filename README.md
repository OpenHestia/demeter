# demeter
![image](https://github.com/user-attachments/assets/02965126-358c-48e6-a55e-4faa7677172e)


Demeter is an LLM Retreival Augmented Generation system using ReACT to provide gardening advice. 

## Design
Demeter is a ChatGPT3.5-Turbo-based assistant focused on providing gardening advice. The core idea behind Demeter is that we use a few pieces of information gathered from the system (geolocation of user, local weather), gathered from the user (plants present in garden, question), and gathered from the internet at large (plant information, gardening advice, etc) to provide up-to-date and contextually intelligent advice on plant care. Modes of input and output such as speech for user input (just nice, not impactful on functionality), use of camera images as input (very helpful, but a bit more prone to hallucination and confusion), and output from demeter like notifications (could be nice) and schematics (also nice, just unclear on usefulness).

## Technology Stack
* Python3 as primary development language.
* Using Azure as web hosting
  - [AzureOpenAI](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/) for OpenAI integration.
  - [AzureContainer](https://azure.microsoft.com/en-us/products/container-apps/) for web server.
  - [AzureML](https://azure.microsoft.com/en-ca/products/machine-learning) services for running other LLMs if necessary.
  - [AzureAISpeech](https://azure.microsoft.com/en-us/products/ai-services/ai-speech/) for speech interaction if viable.
  - [AzureCosmosDB](https://python.langchain.com/v0.2/docs/integrations/vectorstores/azure_cosmos_db_no_sql/) for vector storage.
* [Django](https://docs.djangoproject.com/en/5.0/intro/tutorial01/) for web interface.
  - Notification method:
  - GPS information method:
  - Time information method:
  - Camera/image:
* LangChain for basic LLM prompt engineer.
  - GPT-3.5 for central LLM.
  - Using [RAG](https://python.langchain.com/v0.2/docs/tutorials/rag/) and [ReAcT](https://python.langchain.com/v0.1/docs/modules/agents/agent_types/react/), [tool-calling](https://python.langchain.com/v0.1/docs/modules/agents/agent_types/tool_calling/) techniques for central LLM.
  - Probably use [LLaVA](https://github.com/LLaVA-VL/LLaVA-NeXT/?tab=readme-ov-file) for VLM stuff if I get to it.
* Data sources:
  - Plant information: [Trefle}(http://trefle.io/) or [RapidAPIPlants](https://rapidapi.com/tuvshno/api/plants10)
  - Weather information: [OpenWeather](https://openweathermap.org/api)
  - Geolocation: [GeoIP](https://docs.djangoproject.com/en/1.11/ref/contrib/gis/geoip/)
