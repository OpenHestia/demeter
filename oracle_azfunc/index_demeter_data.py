# This file's purpose is to use LangChain to index data for the Demeter RAG.
# We want to collect a set of data, then store it in Azure Cognitive Search as
# a vector store.

# References:
# https://python.langchain.com/v0.2/docs/tutorials/rag/#indexing
# https://api.python.langchain.com/en/latest/vectorstores/langchain_community.vectorstores.azuresearch.AzureSearch.html