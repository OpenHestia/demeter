# demeter
Demeter is an LLM Retreival Augmented Generation system using ReACT to provide gardening advice.

## Technology Stack
* Python3 as primary development language.
* Using Azure as web hosting
  - [AzureOpenAI](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/) for OpenAI integration.
  - [AzureContainer](https://azure.microsoft.com/en-us/products/container-apps/) for web server.
  - [AzureML](https://azure.microsoft.com/en-ca/products/machine-learning) services for running other LLMs if necessary.
  - [AzureAISpeech](https://azure.microsoft.com/en-us/products/ai-services/ai-speech/) for speech interaction if viable.
  - [AzureCosmosDB](https://python.langchain.com/v0.2/docs/integrations/vectorstores/azure_cosmos_db_no_sql/) for vector storage.
* [Django](https://docs.djangoproject.com/en/5.0/intro/tutorial01/) for web interface (most widely-used Python3 web library, never used, but I've used Flask and done webdev with JS).
  - Notification method:
  - GPS information method:
  - Time information method:
  - Camera/image:
* LangChain for basic LLM prompt engineer.
  - GPT-3.5 for central LLM.
  - Using [RAG](https://python.langchain.com/v0.2/docs/tutorials/rag/) and [ReAcT](https://python.langchain.com/v0.1/docs/modules/agents/agent_types/react/), [tool-calling](https://python.langchain.com/v0.1/docs/modules/agents/agent_types/tool_calling/) techniques for central LLM.
  - Probably use [LLaVA](https://github.com/LLaVA-VL/LLaVA-NeXT/?tab=readme-ov-file) for VLM stuff if I get to it.
* Data sources:
  - Plant information:
  - Weather information:
  - 
